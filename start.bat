@echo off
REM E-Commerce Recommendation System - Quick Start Script (Windows)
REM This script automates the setup and launch process

echo ==========================================
echo E-Commerce Recommendation System
echo Quick Start Script
echo ==========================================
echo.

REM Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo + Python found
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo + Virtual environment created
) else (
    echo + Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo + Virtual environment activated
echo.

REM Install dependencies
echo [4/6] Installing dependencies...
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo + Dependencies installed
echo.

REM Run setup
echo [5/6] Setting up the system...
if not exist "models\recommender_model.pkl" (
    python setup.py
) else (
    echo + System already set up (models exist)
    set /p retrain="Do you want to retrain the model? (y/N): "
    if /i "%retrain%"=="y" (
        del /q data\*.csv models\*.pkl 2>nul
        python setup.py
    )
)
echo.

REM Launch application
echo [6/6] Launching application...
echo.
echo ==========================================
echo Application is starting...
echo ==========================================
echo.
echo The app will open in your browser at:
echo   http://localhost:8501
echo.
echo Create an account or login to get started!
echo.
echo Press Ctrl+C to stop the application
echo ==========================================
echo.

streamlit run app.py

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat
