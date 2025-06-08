<<<<<<< HEAD
# Stock Market Analysis Platform

Платформа для анализа фондового рынка с использованием AI и технического анализа.

## Возможности

- Анализ акций в реальном времени
- AI-прогнозы движения цен
- Анализ тональности новостей
- Технические индикаторы (SMA, RSI, MACD)
- Интерактивные графики
- AI-инсайты и рекомендации

## Технологии

### Backend
- FastAPI
- SQLAlchemy
- Redis
- OpenAI GPT
- FinBERT
- yfinance
- TA-Lib

### Frontend
- React
- Tailwind CSS
- Chart.js
- Axios

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/stock-market-platform.git
cd stock-market-platform
```

2. Создайте файл .env:
```bash
cp .env.example .env
```

3. Заполните необходимые переменные окружения в .env:
```
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
```

4. Запустите с помощью Docker:
```bash
chmod +x deploy.sh
./deploy.sh
```

## Разработка

### Backend

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Перейдите в директорию frontend:
```bash
cd frontend
```

2. Установите зависимости:
```bash
npm install
```

3. Запустите сервер разработки:
```bash
npm start
```

## API Документация

- Swagger UI: http://localhost/docs
- ReDoc: http://localhost/redoc

## Основные эндпоинты

### Рыночные данные
- GET /api/v1/market/stocks/{symbol} - информация об акции
- GET /api/v1/market/stocks/{symbol}/data - исторические данные
- GET /api/v1/market/stocks/{symbol}/news - новости по акции

### AI и прогнозы
- POST /api/v1/predict/predict - прогноз цены
- POST /api/v1/sentiment/sentiment - анализ тональности
- POST /api/v1/predict/insights - AI-инсайты

### Пользователи
- POST /api/v1/auth/login - авторизация
- POST /api/v1/users/ - создание пользователя
- GET /api/v1/users/me - информация о текущем пользователе

## Тестирование

```bash
pytest
```

## Деплой

1. Настройте переменные окружения на сервере
2. Запустите скрипт деплоя:
```bash
./deploy.sh
```

## Лицензия

MIT 
=======
# QuantFinSocietyAI-Int
>>>>>>> 92f529badfdb5077da551f42217c090bf35ba057
