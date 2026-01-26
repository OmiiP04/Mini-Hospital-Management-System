#!/bin/bash
# Quick Start Script for HMS

echo "🏥 Hospital Management System - Setup Guide"
echo "============================================"
echo ""

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.9+"
    exit 1
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL"
    echo "   Windows: https://www.postgresql.org/download/windows/"
    echo "   macOS: brew install postgresql"
    echo "   Linux: sudo apt-get install postgresql"
fi

echo "✅ Prerequisites check complete"
echo ""

# Setup Backend
echo "📦 Setting up Django Backend..."
cd hms_backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your database credentials"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser account..."
python manage.py createsuperuser

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "To start the backend:"
echo "  cd hms_backend"
echo "  source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "  python manage.py runserver"
echo ""

# Setup Serverless
echo "📧 Setting up Serverless Email Service..."
cd ../serverless_email

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found. Skipping serverless setup"
    echo "   Install from: https://nodejs.org/"
else
    if [ ! -d "node_modules" ]; then
        echo "Installing Node dependencies..."
        npm install
    fi
    
    if [ ! -f ".env" ]; then
        echo "Creating .env file..."
        cp .env.example .env
        echo "⚠️  Please edit .env with your Gmail credentials"
    fi
    
    echo ""
    echo "✅ Serverless setup complete!"
    echo ""
    echo "To start the email service:"
    echo "  cd serverless_email"
    echo "  npm run offline"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env files with your credentials"
echo "2. Start PostgreSQL service"
echo "3. Run: python manage.py runserver (in hms_backend)"
echo "4. Run: npm run offline (in serverless_email)"
echo "5. Visit: http://localhost:8000"
