from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class StockData(BaseModel):
    symbol: str
    name: str
    sector: str
    industry: str
    price: float
    change: float
    volume: int
    market_cap: str
    pe_ratio: str
    eps: str
    dividend_yield: str
    beta: str
    technical_indicators: Dict[str, float]

class HistoricalData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class NewsItem(BaseModel):
    title: str
    link: str
    publisher: str
    published: str
    type: str

class PricePrediction(BaseModel):
    symbol: str
    current_price: float
    prediction: str
    timestamp: str

class SentimentAnalysis(BaseModel):
    text: str
    analysis: str
    timestamp: str

class AIInsights(BaseModel):
    symbol: str
    insights: str
    timestamp: str

class StockBase(BaseModel):
    symbol: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None

class StockCreate(StockBase):
    pass

class StockUpdate(StockBase):
    pass

class Stock(StockBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StockPriceBase(BaseModel):
    stock_id: int
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class StockPriceCreate(StockPriceBase):
    pass

class StockPriceUpdate(StockPriceBase):
    pass

class StockPrice(StockPriceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    stock_id: int
    title: str
    content: str
    source: str
    url: str
    published_at: datetime
    sentiment_score: Optional[float] = None

class NewsCreate(NewsBase):
    pass

class NewsUpdate(NewsBase):
    pass

class News(NewsBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 