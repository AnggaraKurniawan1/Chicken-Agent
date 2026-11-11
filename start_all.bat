@echo off
title Chicken-Agent + DeepSeek Harness Launcher
echo ========================================================
echo     Menjalankan Chicken-Agent & DeepSeek Harness
echo ========================================================
echo.
echo 1. Membuka Chicken-Agent Web UI (Port 5050)...
start "Chicken-Agent Web" cmd /c "python main.py --web"

echo 2. Membuka DeepSeek Harness Web UI (Port 3080)...
start "DeepSeek Harness" cmd /c "npx --yes @deepseek-ai/dsh web"

echo.
echo Kedua agen sedang berjalan!
echo - Chicken-Agent:   http://127.0.0.1:5050
echo - DeepSeek Harness: http://127.0.0.1:3080
echo ========================================================
pause
