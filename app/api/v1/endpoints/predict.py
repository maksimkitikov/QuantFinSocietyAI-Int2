from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.schemas.predict import PricePrediction, PredictionRequest
import numpy as np
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/predict", response_model=PricePrediction)
def predict_price(
    request: PredictionRequest,
    db: Session = Depends(deps.get_db)
) -> PricePrediction:
    """
    Прогнозирование цены акции на основе исторических данных.
    
    - **symbol**: Тикер акции
    - **days**: Количество дней для прогноза
    - **confidence**: Уровень уверенности в прогнозе (0-1)
    """
    # Имитация прогноза с использованием случайных данных
    current_price = 100.0  # Базовая цена
    volatility = 0.02  # Волатильность
    
    predictions = []
    for i in range(request.days):
        # Генерируем случайное изменение цены
        change = np.random.normal(0, volatility)
        predicted_price = current_price * (1 + change)
        predictions.append({
            "date": (datetime.utcnow() + timedelta(days=i)).isoformat(),
            "price": round(predicted_price, 2)
        })
        current_price = predicted_price
    
    return PricePrediction(
        symbol=request.symbol,
        predictions=predictions,
        confidence=round(np.random.uniform(0.7, 0.95), 2)
    ) 