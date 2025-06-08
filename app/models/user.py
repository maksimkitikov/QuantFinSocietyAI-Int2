from sqlalchemy import Column, String, Boolean, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    settings = relationship("UserSettings", back_populates="user", uselist=False)

class UserSettings(BaseModel):
    __tablename__ = "user_settings"
    
    user_id = Column(Integer, ForeignKey("users.id"))
    theme = Column(String, default="light")
    default_timeframe = Column(String, default="1d")
    favorite_stocks = Column(JSON, default=list)
    notification_settings = Column(JSON, default=dict)
    
    user = relationship("User", back_populates="settings") 