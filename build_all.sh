#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting build process for all platforms...${NC}"

# Create build directories
mkdir -p dist/{web,desktop,mobile}

# Build web version
echo -e "${GREEN}Building web version...${NC}"
npm run build
cp -r build/* dist/web/

# Build desktop versions
echo -e "${GREEN}Building desktop versions...${NC}"

# Windows
echo -e "${GREEN}Building Windows version...${NC}"
npm run electron-pack -- --win
cp -r dist/win-unpacked/* dist/desktop/windows/

# macOS
echo -e "${GREEN}Building macOS version...${NC}"
npm run electron-pack -- --mac
cp -r dist/mac/* dist/desktop/macos/

# Linux
echo -e "${GREEN}Building Linux version...${NC}"
npm run electron-pack -- --linux
cp -r dist/linux-unpacked/* dist/desktop/linux/

# Build mobile versions
echo -e "${GREEN}Building mobile versions...${NC}"

# Android
echo -e "${GREEN}Building Android version...${NC}"
npm run capacitor:build:android
cp -r android/app/build/outputs/apk/release/* dist/mobile/android/

# iOS
echo -e "${GREEN}Building iOS version...${NC}"
npm run capacitor:build:ios
cp -r ios/App/build/Release-iphoneos/* dist/mobile/ios/

# Create archives
echo -e "${GREEN}Creating archives...${NC}"

# Web
cd dist/web
zip -r ../web.zip .
cd ../..

# Desktop
cd dist/desktop
zip -r ../desktop-windows.zip windows/
zip -r ../desktop-macos.zip macos/
zip -r ../desktop-linux.zip linux/
cd ../..

# Mobile
cd dist/mobile
zip -r ../mobile-android.zip android/
zip -r ../mobile-ios.zip ios/
cd ../..

echo -e "${GREEN}Build process completed!${NC}"
echo -e "Artifacts are located in the dist/ directory:"
echo -e "- Web: dist/web.zip"
echo -e "- Desktop:"
echo -e "  - Windows: dist/desktop-windows.zip"
echo -e "  - macOS: dist/desktop-macos.zip"
echo -e "  - Linux: dist/desktop-linux.zip"
echo -e "- Mobile:"
echo -e "  - Android: dist/mobile-android.zip"
echo -e "  - iOS: dist/mobile-ios.zip" 