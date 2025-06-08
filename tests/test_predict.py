from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.crud.market import create_stock
from app.schemas.market import StockCreate

client = TestClient(app)

def test_predict_price(db: Session):
    # Создаем тестовую акцию
    stock = create_stock(db, StockCreate(
        symbol="AAPL",
        name="Apple Inc.",
        market_cap=2000000000000,
        sector="Technology"
    ))
    
    request_data = {
        "symbol": "AAPL",
        "days": 7
    }
    
    response = client.post("/api/v1/predict/predict", json=request_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["symbol"] == request_data["symbol"]
    assert len(data["predictions"]) == request_data["days"]
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1
    
    for prediction in data["predictions"]:
        assert "date" in prediction
        assert "price" in prediction
        assert prediction["price"] > 0

def test_predict_price_invalid_symbol():
    request_data = {
        "symbol": "INVALID",
        "days": 7
    }
    
    response = client.post("/api/v1/predict/predict", json=request_data)
    assert response.status_code == 200  # Все равно возвращаем прогноз, даже для несуществующего тикера
    data = response.json()
    assert data["symbol"] == request_data["symbol"]

def test_predict_price_invalid_days():
    request_data = {
        "symbol": "AAPL",
        "days": 31  # Превышаем максимальное количество дней
    }
    
    response = client.post("/api/v1/predict/predict", json=request_data)
    assert response.status_code == 422  # Ошибка валидации 