@echo off
echo ========================================
echo  Django Backend Setup & Run Script
echo ========================================

cd /d "C:\Users\Lucas B Marinho\Documents\Projetos\flask-auth-system\backend"

echo.
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
python --version

echo.
echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo Virtual environment already exists
)

echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated

echo.
echo [4/6] Installing Django dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully

echo.
echo [5/6] Running Django migrations...
python manage.py makemigrations
python manage.py migrate
echo Migrations completed

echo.
echo [6/6] Starting Django development server...
echo.
echo ========================================
echo  Django Backend running at:
echo  http://localhost:8000
echo ========================================
echo  Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver 8000
