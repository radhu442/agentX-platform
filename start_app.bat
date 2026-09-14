@echo off
title AgentX Platform Runner
echo ==========================================
echo ⚡ Starting AgentX Platform on Windows...
echo ==========================================

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3 from https://www.python.org/
    pause
    exit /b
)

REM Set up virtual environment if not present
if not exist ".venv" (
    echo [1/3] Setting up Python virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo [2/3] Installing dependencies...
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo [3/3] Opening browser and starting server...
start http://127.0.0.1:3000

python app.py
pause
