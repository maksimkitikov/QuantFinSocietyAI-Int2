#!/bin/bash

# Установка зависимостей
echo "Установка зависимостей..."
npm install
cd frontend && npm install && cd ..

# Сборка веб-версии
echo "Сборка веб-версии..."
cd frontend && npm run build && cd ..

# Сборка Electron
echo "Сборка Electron..."
cd frontend && npm run electron-pack && cd ..

# Сборка Android
echo "Сборка Android..."
cd frontend && npm run capacitor:sync && npm run capacitor:build:android && cd ..

# Сборка iOS
echo "Сборка iOS..."
cd frontend && npm run capacitor:sync && npm run capacitor:build:ios && cd ..

# Создание архивов
echo "Создание архивов..."
mkdir -p dist
cp frontend/dist/*.exe dist/stockai-windows.exe
cp frontend/dist/*.dmg dist/stockai-macos.dmg
cp frontend/android/app/build/outputs/apk/release/app-release.apk dist/stockai-android.apk

echo "Сборка завершена!"
echo "Артефакты находятся в директории dist/" 