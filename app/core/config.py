from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, EmailStr, validator
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stock Market Analysis Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # API Keys
    NEWS_API_KEY: Optional[str] = os.getenv("NEWS_API_KEY")
    ALPHA_VANTAGE_API_KEY: str = "93W1HE3ISFG6TDKQ"
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./app.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # В продакшене заменить на безопасный ключ
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 дней
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    
    # OpenAI
    OPENAI_API_KEY: str = "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"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 