import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import requests
from app.core.config import settings
import talib
from datetime import datetime, timedelta
import redis
import ta

# Инициализация Redis для кэширования
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

class MarketDataService:
    def __init__(self):
        self.alpha_vantage_key = settings.ALPHA_VANTAGE_API_KEY
        self.base_url = "https://www.alphavantage.co/query"

    async def get_stock_data(self, symbol: str, interval: str = "1d", period: str = "1mo") -> Dict:
        """Получение данных об акции"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period, interval=interval)
            
            # Получаем дополнительную информацию через Alpha Vantage
            overview = self._get_company_overview(symbol)
            
            return {
                "symbol": symbol,
                "name": overview.get("Name", ""),
                "sector": overview.get("Sector", ""),
                "industry": overview.get("Industry", ""),
                "price": hist["Close"].iloc[-1] if not hist.empty else None,
                "change": hist["Close"].pct_change().iloc[-1] if not hist.empty else None,
                "volume": hist["Volume"].iloc[-1] if not hist.empty else None,
                "market_cap": overview.get("MarketCapitalization", ""),
                "pe_ratio": overview.get("PERatio", ""),
                "eps": overview.get("EPS", ""),
                "dividend_yield": overview.get("DividendYield", ""),
                "beta": overview.get("Beta", ""),
                "technical_indicators": self._calculate_technical_indicators(hist)
            }
        except Exception as e:
            raise Exception(f"Ошибка при получении данных об акции: {str(e)}")

    def _get_company_overview(self, symbol: str) -> Dict:
        """Получение общей информации о компании через Alpha Vantage"""
        params = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": self.alpha_vantage_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    def _calculate_technical_indicators(self, df: pd.DataFrame) -> Dict:
        """Расчет технических индикаторов"""
        if df.empty:
            return {}
            
        close = df["Close"].values
        high = df["High"].values
        low = df["Low"].values
        volume = df["Volume"].values

        return {
            "sma_20": talib.SMA(close, timeperiod=20)[-1],
            "sma_50": talib.SMA(close, timeperiod=50)[-1],
            "rsi": talib.RSI(close, timeperiod=14)[-1],
            "macd": talib.MACD(close)[0][-1],
            "macd_signal": talib.MACD(close)[1][-1],
            "macd_hist": talib.MACD(close)[2][-1],
            "bollinger_upper": talib.BBANDS(close)[0][-1],
            "bollinger_middle": talib.BBANDS(close)[1][-1],
            "bollinger_lower": talib.BBANDS(close)[2][-1],
            "atr": talib.ATR(high, low, close, timeperiod=14)[-1],
            "obv": talib.OBV(close, volume)[-1]
        }

    async def get_historical_data(self, symbol: str, interval: str = "1d", period: str = "1y") -> List[Dict]:
        """Получение исторических данных"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period, interval=interval)
            
            return [{
                "date": index.strftime("%Y-%m-%d"),
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"]
            } for index, row in hist.iterrows()]
        except Exception as e:
            raise Exception(f"Ошибка при получении исторических данных: {str(e)}")

    async def get_market_news(self, symbol: str) -> List[Dict]:
        """Получение новостей по акции"""
        try:
            stock = yf.Ticker(symbol)
            news = stock.news
            
            return [{
                "title": item["title"],
                "link": item["link"],
                "publisher": item["publisher"],
                "published": datetime.fromtimestamp(item["providerPublishTime"]).strftime("%Y-%m-%d %H:%M:%S"),
                "type": item["type"]
            } for item in news]
        except Exception as e:
            raise Exception(f"Ошибка при получении новостей: {str(e)}")

market_data_service = MarketDataService()

def get_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Получение данных акции с кэшированием
    """
    cache_key = f"stock_data:{symbol}:{period}"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return pd.read_json(cached_data)
    
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    
    # Добавление технических индикаторов
    data['SMA20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['SMA50'] = ta.trend.sma_indicator(data['Close'], window=50)
    data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
    data['MACD'] = ta.trend.macd_diff(data['Close'])
    
    # Кэширование на 5 минут
    redis_client.setex(cache_key, 300, data.to_json())
    
    return data

def get_stock_info(symbol: str) -> Dict:
    """
    Получение информации об акции
    """
    cache_key = f"stock_info:{symbol}"
    cached_info = redis_client.get(cache_key)
    
    if cached_info:
        return eval(cached_info)
    
    stock = yf.Ticker(symbol)
    info = stock.info
    
    # Кэширование на 1 час
    redis_client.setex(cache_key, 3600, str(info))
    
    return info

def get_technical_indicators(data: pd.DataFrame) -> Dict:
    """
    Расчет технических индикаторов
    """
    return {
        "sma20": data['SMA20'].iloc[-1],
        "sma50": data['SMA50'].iloc[-1],
        "rsi": data['RSI'].iloc[-1],
        "macd": data['MACD'].iloc[-1],
        "volume": data['Volume'].iloc[-1],
        "price_change": ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
    }

def get_market_summary() -> Dict:
    """
    Получение сводки рынка
    """
    cache_key = "market_summary"
    cached_summary = redis_client.get(cache_key)
    
    if cached_summary:
        return eval(cached_summary)
    
    # Получение данных основных индексов
    indices = {
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones",
        "^IXIC": "NASDAQ",
        "^RUT": "Russell 2000"
    }
    
    summary = {}
    for symbol, name in indices.items():
        data = yf.download(symbol, period="1d")
        summary[name] = {
            "price": data['Close'].iloc[-1],
            "change": ((data['Close'].iloc[-1] - data['Open'].iloc[0]) / data['Open'].iloc[0]) * 100
        }
    
    # Кэширование на 5 минут
    redis_client.setex(cache_key, 300, str(summary))
    
    return summary 