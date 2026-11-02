@echo off
title Smart Campus Food Pre-Order System
cd /d "%~dp0"
echo ========================================================
echo       SMART CAMPUS FOOD PRE-ORDER SYSTEM
echo ========================================================
echo.

:: 1. Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python aapke computer me install nahi hai ya PATH me add nahi hai!
    echo.
    echo Kripya Python download karein: https://www.python.org/downloads/
    echo (Note: Install karte waqt "Add python.exe to PATH" box par tick zaroor karein)
    echo.
    pause
    exit /b
)

:: 2. Check and install Flask automatically
echo [1/3] Checking dependencies (Flask)...
python -m pip install -r requirements.txt --quiet

:: 3. Inform user and launch browser
echo [2/3] Starting Web Server on http://127.0.0.1:5000 ...
echo [3/3] Opening browser automatically...
echo.
echo ========================================================
echo  * Web App is now running!
echo  * Browser me nahi khula toh manually open karein:
echo    http://127.0.0.1:5000
echo  * Is window ko band mat karna jab tak project chalana ho!
echo ========================================================
echo.

:: Automatically open browser after 2 seconds
start "" http://127.0.0.1:5000

:: Start Flask app
python app.py

pause
