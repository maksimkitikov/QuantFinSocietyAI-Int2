from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Stock(BaseModel):
    __tablename__ = "stocks"
    
    symbol = Column(String, unique=True, index=True)
    name = Column(String)
    market_cap = Column(Float, nullable=True)
    sector = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    pe_ratio = Column(Float)
    beta = Column(Float)
    dividend_yield = Column(Float)

    prices = relationship("StockPrice", back_populates="stock")
    news = relationship("News", back_populates="stock")

class StockPrice(BaseModel):
    __tablename__ = "stock_prices"
    
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    indicators = Column(JSON, nullable=True)

    stock = relationship("Stock", back_populates="prices")

class News(BaseModel):
    __tablename__ = "news"
    
    title = Column(String)
    content = Column(String)
    source = Column(String)
    url = Column(String)
    published_at = Column(DateTime)
    sentiment_score = Column(Float, nullable=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=True)
    related_stocks = Column(JSON, nullable=True)

    stock = relationship("Stock", back_populates="news") 