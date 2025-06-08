from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.crud.market import create_stock, create_stock_price, create_news
from app.schemas.market import StockCreate, StockPriceCreate, NewsCreate
from datetime import datetime, timedelta

client = TestClient(app)

def test_create_stock(db: Session):
    stock_data = {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "market_cap": 2000000000000,
        "sector": "Technology"
    }
    response = client.post("/api/v1/market/stocks/", json=stock_data)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == stock_data["symbol"]
    assert data["name"] == stock_data["name"]

def test_read_stocks(db: Session):
    response = client.get("/api/v1/market/stocks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_stock(db: Session):
    # Создаем тестовую акцию
    stock_data = {
        "symbol": "GOOGL",
        "name": "Alphabet Inc.",
        "market_cap": 1500000000000,
        "sector": "Technology"
    }
    stock = create_stock(db, StockCreate(**stock_data))
    
    response = client.get(f"/api/v1/market/stocks/{stock.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == stock_data["symbol"]
    assert data["name"] == stock_data["name"]

def test_create_stock_price(db: Session):
    # Создаем тестовую акцию
    stock = create_stock(db, StockCreate(
        symbol="MSFT",
        name="Microsoft Corporation",
        market_cap=1800000000000,
        sector="Technology"
    ))
    
    price_data = {
        "stock_id": stock.id,
        "price": 300.50,
        "volume": 1000000,
        "timestamp": datetime.utcnow().isoformat()
    }
    response = client.post("/api/v1/market/prices/", json=price_data)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == price_data["price"]
    assert data["volume"] == price_data["volume"]

def test_read_stock_prices(db: Session):
    response = client.get("/api/v1/market/prices/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_news(db: Session):
    # Создаем тестовую акцию
    stock = create_stock(db, StockCreate(
        symbol="AMZN",
        name="Amazon.com Inc.",
        market_cap=1600000000000,
        sector="Technology"
    ))
    
    news_data = {
        "stock_id": stock.id,
        "title": "Test News",
        "content": "This is a test news article",
        "source": "Test Source",
        "url": "https://example.com/news/1",
        "published_at": datetime.utcnow().isoformat()
    }
    response = client.post("/api/v1/market/news/", json=news_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == news_data["title"]
    assert data["content"] == news_data["content"]

def test_read_news(db: Session):
    response = client.get("/api/v1/market/news/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_stock_news(db: Session):
    # Создаем тестовую акцию и новость
    stock = create_stock(db, StockCreate(
        symbol="TSLA",
        name="Tesla Inc.",
        market_cap=800000000000,
        sector="Automotive"
    ))
    
    news = create_news(db, NewsCreate(
        stock_id=stock.id,
        title="Tesla News",
        content="Tesla announces new factory",
        source="Test Source",
        url="https://example.com/news/2",
        published_at=datetime.utcnow().isoformat()
    ))
    
    response = client.get(f"/api/v1/market/stocks/{stock.id}/news")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == news.title 