from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.crud.market import create_stock, create_news
from app.schemas.market import StockCreate, NewsCreate
from datetime import datetime, timedelta

client = TestClient(app)

def test_analyze_sentiment(db: Session):
    # Создаем тестовую акцию
    stock = create_stock(db, StockCreate(
        symbol="AAPL",
        name="Apple Inc.",
        market_cap=2000000000000,
        sector="Technology"
    ))
    
    # Создаем тестовые новости
    for i in range(3):
        create_news(db, NewsCreate(
            stock_id=stock.id,
            title=f"Test News {i}",
            content=f"Test content {i}",
            source="Test Source",
            url=f"https://example.com/news/{i}",
            published_at=datetime.utcnow() - timedelta(days=i)
        ))
    
    request_data = {
        "symbol": "AAPL",
        "days": 7
    }
    
    response = client.post("/api/v1/sentiment/sentiment", json=request_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["symbol"] == request_data["symbol"]
    assert "overall_sentiment" in data
    assert data["overall_sentiment"] in ["positive", "negative", "neutral"]
    assert "sentiment_score" in data
    assert -1 <= data["sentiment_score"] <= 1
    assert "articles" in data
    assert len(data["articles"]) > 0
    
    for article in data["articles"]:
        assert "title" in article
        assert "sentiment" in article
        assert article["sentiment"] in ["positive", "negative", "neutral"]
        assert "score" in article
        assert -1 <= article["score"] <= 1
        assert "published_at" in article

def test_analyze_sentiment_no_news(db: Session):
    request_data = {
        "symbol": "NONEWS",
        "days": 7
    }
    
    response = client.post("/api/v1/sentiment/sentiment", json=request_data)
    assert response.status_code == 404
    assert "No news found" in response.json()["detail"]

def test_analyze_sentiment_invalid_days():
    request_data = {
        "symbol": "AAPL",
        "days": 31  # Превышаем максимальное количество дней
    }
    
    response = client.post("/api/v1/sentiment/sentiment", json=request_data)
    assert response.status_code == 422  # Ошибка валидации 