@echo off
title Mathruseva Foundation - NGO Management System
color 0A
echo ========================================
echo    Mathruseva Foundation
echo    NGO Management System
echo ========================================
echo.
echo Starting application...
echo.

cd /d "C:\Users\nehaj\CascadeProjects\mathruseva_foundation"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ first
    pause
    exit /b
)

echo Python found: 
python --version

REM Check if required packages are installed
echo.
echo Checking dependencies...
python -c "import flask, mysql.connector, flask_cors, reportlab" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install flask flask-cors mysql-connector-python reportlab
    if %errorlevel% neq 0 (
        echo Failed to install packages. Please check your internet connection.
        pause
        exit /b
    )
)

echo Dependencies installed successfully!

REM Start the application
echo.
echo ========================================
echo    Starting Web Server...
echo    Open your browser and go to:
echo    http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python secure_app.py

echo.
echo Application stopped.
pause
