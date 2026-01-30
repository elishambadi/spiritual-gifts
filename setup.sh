#!/bin/bash

echo "🚀 Setting up Spiritual Gifts Survey Application..."
echo ""

# Backend setup
echo "📦 Setting up Django backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Populate data
echo "Populating database with questions..."
python manage.py populate_data

echo ""
echo "✅ Backend setup complete!"
echo ""

# Frontend setup
echo "📦 Setting up Vue frontend..."
cd ../frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

echo ""
echo "✅ Frontend setup complete!"
echo ""

# Back to root
cd ..

echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. Terminal 1 - Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Terminal 2 - Frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"
