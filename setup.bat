@echo off
REM Quick Start Script for HMS on Windows

echo 🏥 Hospital Management System - Setup Guide
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

REM Check PostgreSQL
psql --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PostgreSQL not found. Please install PostgreSQL
    echo    Download: https://www.postgresql.org/download/windows/
)

echo ✅ Prerequisites check complete
echo.

REM Setup Backend
echo 📦 Setting up Django Backend...
cd hms_backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env with your database credentials
)

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Create superuser
echo Creating superuser account...
python manage.py createsuperuser

echo.
echo ✅ Backend setup complete!
echo.
echo To start the backend:
echo   cd hms_backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.

REM Setup Serverless
echo 📧 Setting up Serverless Email Service...
cd ..\serverless_email

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Node.js not found. Skipping serverless setup
    echo    Install from: https://nodejs.org/
) else (
    if not exist "node_modules" (
        echo Installing Node dependencies...
        call npm install
    )
    
    if not exist ".env" (
        echo Creating .env file...
        copy .env.example .env
        echo ⚠️  Please edit .env with your Gmail credentials
    )
    
    echo.
    echo ✅ Serverless setup complete!
    echo.
    echo To start the email service:
    echo   cd serverless_email
    echo   npm run offline
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Update .env files with your credentials
echo 2. Start PostgreSQL service
echo 3. Run: python manage.py runserver (in hms_backend)
echo 4. Run: npm run offline (in serverless_email)
echo 5. Visit: http://localhost:8000
echo.
pause
