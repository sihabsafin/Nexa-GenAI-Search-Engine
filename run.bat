@echo off
REM Nexa Search - Easy Run Script for Windows
REM This script handles virtual environment and launches the app

echo 🔍 Starting Nexa Search...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ⚠️  Virtual environment not found. Creating one...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ⚠️  Dependencies not found. Installing...
    pip install -r requirements.txt
    echo ✓ Dependencies installed
)

REM Check for API key
if not exist ".env" (
    echo ❌ Error: .env file not found
    echo Please copy .env.example to .env and add your Groq API key
    echo.
    echo Run: copy .env.example .env
    echo Then edit .env and add your GROQ_API_KEY
    pause
    exit /b 1
)

REM Check if API key is set
findstr /C:"your_groq_api_key_here" .env >nul
if not errorlevel 1 (
    echo ❌ Error: Please set your GROQ_API_KEY in .env file
    echo Edit .env and replace 'your_groq_api_key_here' with your actual key
    pause
    exit /b 1
)

REM Launch the app
echo ✓ Starting Nexa Search...
echo.
streamlit run app.py

pause
