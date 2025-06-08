from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserSettingsBase(BaseModel):
    theme: str = "light"
    default_timeframe: str = "1d"
    favorite_stocks: List[str] = []
    notification_settings: Dict = {}

class UserSettingsCreate(UserSettingsBase):
    user_id: int

class UserSettingsUpdate(BaseModel):
    theme: Optional[str] = None
    default_timeframe: Optional[str] = None
    favorite_stocks: Optional[List[str]] = None
    notification_settings: Optional[Dict] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class User(UserInDB):
    settings: Optional[UserSettingsBase] = None 