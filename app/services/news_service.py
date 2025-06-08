from newsapi import NewsApiClient
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings
import aiohttp
import asyncio

class NewsService:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)
    
    async def get_news(self, query: str, from_date: Optional[str] = None) -> List[Dict]:
        """
        Get news using NewsAPI
        """
        try:
            if not from_date:
                from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            response = self.newsapi.get_everything(
                q=query,
                from_param=from_date,
                language='en',
                sort_by='relevancy'
            )
            
            return response['articles']
        except Exception as e:
            raise Exception(f"Error fetching news: {str(e)}")
    
    async def get_company_news(self, company_name: str) -> List[Dict]:
        """
        Get news for a specific company
        """
        try:
            return await self.get_news(company_name)
        except Exception as e:
            raise Exception(f"Error fetching company news: {str(e)}")
    
    async def get_market_news(self) -> List[Dict]:
        """
        Get general market news
        """
        try:
            return await self.get_news("stock market OR trading OR finance")
        except Exception as e:
            raise Exception(f"Error fetching market news: {str(e)}")
    
    async def get_economic_calendar(self) -> List[Dict]:
        """
        Get economic calendar
        """
        # Placeholder implementation
        return [
            {
                "date": "2024-01-15",
                "event": "CPI Release",
                "country": "US",
                "importance": "High"
            }
        ] 