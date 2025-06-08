from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.schemas.market import Stock, StockCreate, StockUpdate, StockPrice, News, NewsCreate, NewsUpdate, StockData, HistoricalData, NewsItem, PricePrediction, SentimentAnalysis, AIInsights
from app.services.market_data import market_data_service
from app.services.ai import ai_service

router = APIRouter()

@router.get("/stocks/", response_model=List[Stock])
def read_stocks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve stocks.
    """
    stocks = crud.market.get_multi_stocks(db, skip=skip, limit=limit)
    return stocks

@router.post("/stocks/", response_model=Stock)
def create_stock(
    *,
    db: Session = Depends(deps.get_db),
    stock_in: StockCreate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new stock.
    """
    stock = crud.market.create_stock(db, obj_in=stock_in)
    return stock

@router.put("/stocks/{stock_id}", response_model=Stock)
def update_stock(
    *,
    db: Session = Depends(deps.get_db),
    stock_id: int,
    stock_in: StockUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a stock.
    """
    stock = crud.market.get_stock(db, id=stock_id)
    if not stock:
        raise HTTPException(
            status_code=404,
            detail="The stock with this ID does not exist in the system",
        )
    stock = crud.market.update_stock(db, db_obj=stock, obj_in=stock_in)
    return stock

@router.get("/stocks/{stock_id}", response_model=Stock)
def read_stock(
    *,
    db: Session = Depends(deps.get_db),
    stock_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get stock by ID.
    """
    stock = crud.market.get_stock(db, id=stock_id)
    if not stock:
        raise HTTPException(
            status_code=404,
            detail="The stock with this ID does not exist in the system",
        )
    return stock

@router.get("/stocks/{stock_id}/prices", response_model=List[StockPrice])
def read_stock_prices(
    *,
    db: Session = Depends(deps.get_db),
    stock_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get stock prices.
    """
    stock = crud.market.get_stock(db, id=stock_id)
    if not stock:
        raise HTTPException(
            status_code=404,
            detail="The stock with this ID does not exist in the system",
        )
    prices = crud.market.get_stock_prices(db, stock_id=stock_id, skip=skip, limit=limit)
    return prices

@router.get("/news/", response_model=List[News])
def read_news(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve news.
    """
    news = crud.market.get_multi_news(db, skip=skip, limit=limit)
    return news

@router.post("/news/", response_model=News)
def create_news(
    *,
    db: Session = Depends(deps.get_db),
    news_in: NewsCreate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new news.
    """
    news = crud.market.create_news(db, obj_in=news_in)
    return news

@router.put("/news/{news_id}", response_model=News)
def update_news(
    *,
    db: Session = Depends(deps.get_db),
    news_id: int,
    news_in: NewsUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a news.
    """
    news = crud.market.get_news(db, id=news_id)
    if not news:
        raise HTTPException(
            status_code=404,
            detail="The news with this ID does not exist in the system",
        )
    news = crud.market.update_news(db, db_obj=news, obj_in=news_in)
    return news

@router.get("/news/{news_id}", response_model=News)
def read_news_by_id(
    *,
    db: Session = Depends(deps.get_db),
    news_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get news by ID.
    """
    news = crud.market.get_news(db, id=news_id)
    if not news:
        raise HTTPException(
            status_code=404,
            detail="The news with this ID does not exist in the system",
        )
    return news

@router.get("/stocks/{symbol}", response_model=StockData)
async def get_stock_data(
    symbol: str,
    db: Session = Depends(deps.get_db)
):
    """Получение данных об акции"""
    try:
        return await market_data_service.get_stock_data(symbol)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stocks/{symbol}/data", response_model=List[HistoricalData])
async def get_historical_data(
    symbol: str,
    interval: str = "1d",
    period: str = "1y",
    db: Session = Depends(deps.get_db)
):
    """Получение исторических данных"""
    try:
        return await market_data_service.get_historical_data(symbol, interval, period)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stocks/{symbol}/news", response_model=List[NewsItem])
async def get_market_news(
    symbol: str,
    db: Session = Depends(deps.get_db)
):
    """Получение новостей по акции"""
    try:
        return await market_data_service.get_market_news(symbol)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict/{symbol}", response_model=PricePrediction)
async def predict_price(
    symbol: str,
    db: Session = Depends(deps.get_db)
):
    """Прогноз цены акции"""
    try:
        historical_data = await market_data_service.get_historical_data(symbol)
        return await ai_service.predict_price(symbol, historical_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sentiment", response_model=SentimentAnalysis)
async def analyze_sentiment(
    text: str,
    db: Session = Depends(deps.get_db)
):
    """Анализ тональности текста"""
    try:
        return await ai_service.analyze_sentiment(text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/insights/{symbol}", response_model=AIInsights)
async def generate_insights(
    symbol: str,
    db: Session = Depends(deps.get_db)
):
    """Генерация AI-инсайтов"""
    try:
        market_data = await market_data_service.get_stock_data(symbol)
        return await ai_service.generate_insights(symbol, market_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 