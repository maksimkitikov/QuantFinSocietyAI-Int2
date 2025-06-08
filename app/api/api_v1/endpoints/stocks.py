from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from app.services.stock_service import StockService
from pydantic import BaseModel

router = APIRouter()
stock_service = StockService()

class StockScreenerCriteria(BaseModel):
    min_pe: Optional[float] = None
    max_pe: Optional[float] = None
    min_volume: Optional[int] = None
    max_beta: Optional[float] = None

@router.get("/{symbol}")
async def get_stock_data(
    symbol: str,
    period: str = "1y",
    interval: str = "1d"
) -> Dict:
    """
    Get stock data
    """
    try:
        return await stock_service.get_stock_data(symbol, period, interval)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/compare")
async def compare_stocks(symbols: List[str], period: str = "1y") -> Dict:
    """
    Compare multiple stocks
    """
    try:
        return await stock_service.get_multiple_stocks(symbols, period)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/screener")
async def screen_stocks(criteria: StockScreenerCriteria) -> List[Dict]:
    """
    Screen stocks based on criteria
    """
    try:
        return await stock_service.get_stock_screener(criteria.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 