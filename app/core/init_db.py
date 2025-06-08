from app.core.database import engine
from app.models.base import Base
from app.models.user import User, UserSettings
from app.models.market import Stock, StockPrice, News

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!") 