#!/bin/bash

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "Ошибка: файл .env не найден"
    exit 1
fi

# Остановка и удаление старых контейнеров
echo "Остановка старых контейнеров..."
docker-compose down

# Сборка и запуск новых контейнеров
echo "Сборка и запуск новых контейнеров..."
docker-compose up --build -d

# Проверка статуса контейнеров
echo "Проверка статуса контейнеров..."
docker-compose ps

# Ожидание готовности сервисов
echo "Ожидание готовности сервисов..."
sleep 10

# Проверка доступности API
echo "Проверка доступности API..."
curl -s http://localhost/api/v1/health || {
    echo "Ошибка: API недоступен"
    exit 1
}

echo "Деплой успешно завершен!"
echo "Приложение доступно по адресу: http://localhost" 