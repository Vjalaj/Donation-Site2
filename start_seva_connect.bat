@echo off
title Seva Connect - Complete Startup
echo.
echo ============================================
echo          SEVA CONNECT STARTUP SCRIPT
echo ============================================
echo.

:: Change to project directory
cd /d "j:\Seva Connect 2.O"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Check if PHP is available
php --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PHP is not installed or not in PATH
    echo Please install XAMPP or add PHP to your PATH
    pause
    exit /b 1
)

echo [INFO] Starting Seva Connect services...
echo.

:: Start Python services in background
echo [1/2] Starting Python backend services...
start "Python Services" cmd /k "cd python && python start_services.py"

:: Wait a moment for Python services to start
timeout /t 5 /nobreak >nul

:: Start PHP server
echo [2/2] Starting PHP server...
echo.
echo ============================================
echo   SEVA CONNECT IS NOW RUNNING!
echo ============================================
echo.
echo Main Website: http://localhost:8000
echo Admin Panel:  http://localhost:8000/admin
echo Setup Check:  http://localhost:8000/setup.html
echo.
echo Python Services:
echo - Certificate API: http://localhost:5002
echo - Payment API:     http://localhost:5000  
echo - OAuth API:       http://localhost:5001
echo.
echo Default Admin Login:
echo Username: admin
echo Password: admin123
echo.
echo TIP: If admin login fails, visit setup page first!
echo Press Ctrl+C to stop all services
echo ============================================
echo.

:: Start PHP server (this will block until stopped)
php -S 0.0.0.0:8000

echo.
echo [INFO] PHP server stopped
pause
