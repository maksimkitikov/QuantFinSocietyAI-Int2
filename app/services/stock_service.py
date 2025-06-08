import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class StockService:
    @staticmethod
    async def get_stock_data(symbol: str, period: str = "1y", interval: str = "1d") -> Dict:
        """
        Get stock data using Yahoo Finance API
        """
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=period, interval=interval)
            
            # Calculate technical indicators
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
            
            # RSI
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            hist['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
            exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
            hist['MACD'] = exp1 - exp2
            hist['Signal_Line'] = hist['MACD'].ewm(span=9, adjust=False).mean()
            
            # Bollinger Bands
            hist['BB_middle'] = hist['Close'].rolling(window=20).mean()
            hist['BB_std'] = hist['Close'].rolling(window=20).std()
            hist['BB_upper'] = hist['BB_middle'] + (hist['BB_std'] * 2)
            hist['BB_lower'] = hist['BB_middle'] - (hist['BB_std'] * 2)
            
            return {
                "symbol": symbol,
                "data": hist.reset_index().to_dict(orient='records'),
                "info": stock.info
            }
        except Exception as e:
            raise Exception(f"Error fetching stock data: {str(e)}")
    
    @staticmethod
    async def get_multiple_stocks(symbols: List[str], period: str = "1y") -> Dict:
        """
        Get data for multiple stocks for comparison
        """
        try:
            data = {}
            for symbol in symbols:
                stock_data = await StockService.get_stock_data(symbol, period)
                data[symbol] = stock_data
            return data
        except Exception as e:
            raise Exception(f"Error fetching multiple stocks data: {str(e)}")
    
    @staticmethod
    async def get_stock_screener(criteria: Dict) -> List[Dict]:
        """
        Stock screener based on given criteria
        """
        # Placeholder implementation
        return [
            {
                "symbol": "AAPL",
                "pe_ratio": 25.5,
                "beta": 1.2,
                "volume": 1000000
            }
        ] 