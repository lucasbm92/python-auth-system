@echo off
title Django Setup and Run
color 0A

echo ========================================
echo    Django Backend Setup and Server
echo ========================================
echo.

REM Check if we're in the backend directory
if not exist "manage.py" (
    echo Error: Please run this script from the backend directory
    echo Looking for manage.py in: %CD%
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    py -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Make sure Python is installed and try again
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated.
echo.

REM Check if Django is installed
python -c "import django" 2>nul
if errorlevel 1 (
    echo Django not found. Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install requirements
        pause
        exit /b 1
    )
    echo Requirements installed successfully.
    echo.
) else (
    echo Django is already installed.
    echo.
)

REM Check if database exists
if not exist "db.sqlite3" (
    echo Setting up database...
    echo Making migrations...
    python manage.py makemigrations
    echo.
    echo Applying migrations...
    python manage.py migrate
    echo.
    echo Database setup complete.
    echo.
)

REM Start the server
echo ========================================
echo Starting Django development server...
echo Server URL: http://localhost:8000
echo Admin URL: http://localhost:8000/admin/
echo API Base: http://localhost:8000/api/
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver 8000

echo.
echo Server stopped.
pause
