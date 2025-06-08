from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.market import Stock, StockPrice, News
from app.schemas.market import StockCreate, StockUpdate, StockPriceCreate, StockPriceUpdate, NewsCreate, NewsUpdate

class CRUDMarket(CRUDBase[Stock, StockCreate, StockUpdate]):
    def get_multi_stocks(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Stock]:
        return db.query(Stock).offset(skip).limit(limit).all()

    def create_stock(self, db: Session, *, obj_in: StockCreate) -> Stock:
        db_obj = Stock(
            symbol=obj_in.symbol,
            name=obj_in.name,
            market_cap=obj_in.market_cap,
            sector=obj_in.sector,
            industry=obj_in.industry,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_stock(
        self, db: Session, *, db_obj: Stock, obj_in: Union[StockUpdate, Dict[str, Any]]
    ) -> Stock:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_stock(self, db: Session, id: int) -> Optional[Stock]:
        return db.query(Stock).filter(Stock.id == id).first()

    def get_stock_prices(
        self, db: Session, *, stock_id: int, skip: int = 0, limit: int = 100
    ) -> List[StockPrice]:
        return (
            db.query(StockPrice)
            .filter(StockPrice.stock_id == stock_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_stock_price(self, db: Session, *, obj_in: StockPriceCreate) -> StockPrice:
        db_obj = StockPrice(
            stock_id=obj_in.stock_id,
            date=obj_in.date,
            open=obj_in.open,
            high=obj_in.high,
            low=obj_in.low,
            close=obj_in.close,
            volume=obj_in.volume,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_stock_price(
        self, db: Session, *, db_obj: StockPrice, obj_in: Union[StockPriceUpdate, Dict[str, Any]]
    ) -> StockPrice:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_news(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[News]:
        return db.query(News).offset(skip).limit(limit).all()

    def create_news(self, db: Session, *, obj_in: NewsCreate) -> News:
        db_obj = News(
            title=obj_in.title,
            content=obj_in.content,
            source=obj_in.source,
            url=obj_in.url,
            published_at=obj_in.published_at,
            sentiment_score=obj_in.sentiment_score,
            stock_id=obj_in.stock_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_news(
        self, db: Session, *, db_obj: News, obj_in: Union[NewsUpdate, Dict[str, Any]]
    ) -> News:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_news(self, db: Session, id: int) -> Optional[News]:
        return db.query(News).filter(News.id == id).first()

market = CRUDMarket(Stock) 