# Backend
FROM python:3.12-slim as backend

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY app/ app/
COPY alembic.ini .
COPY migrations/ migrations/

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend
FROM node:18-alpine as frontend

WORKDIR /app

# Установка зависимостей
COPY frontend/package*.json ./
RUN npm install

# Копирование кода
COPY frontend/ ./

# Сборка приложения
RUN npm run build

# Запуск приложения
CMD ["npm", "start"]

# Nginx
FROM nginx:alpine as nginx

# Копирование конфигурации
COPY nginx.conf /etc/nginx/nginx.conf

# Копирование собранного фронтенда
COPY --from=frontend /app/build /usr/share/nginx/html

# Запуск Nginx
CMD ["nginx", "-g", "daemon off;"] 