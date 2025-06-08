from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.v1.api import api_router
from app.core.config import settings

# Создаем лимитер
limiter = Limiter(key_func=get_remote_address)

# Создаем приложение
app = FastAPI(
    title="Stock Market API",
    description="API для работы с рыночными данными, прогнозами и анализом тональности",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Добавляем лимитер в приложение
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(api_router, prefix="/api/v1")

# Глобальный rate limit
@app.middleware("http")
async def add_rate_limit(request: Request, call_next):
    response = await call_next(request)
    return response

@app.get("/")
@limiter.limit("30/minute")
async def root(request: Request):
    """
    Корневой эндпоинт API.
    
    Returns:
        dict: Информация о версии API
    """
    return {
        "message": "Welcome to Stock Market API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 