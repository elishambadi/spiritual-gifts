#!/bin/bash

echo "🚀 Starting Spiritual Gifts Survey Application..."
echo ""
echo "Starting backend server on http://localhost:8000"
echo "Starting frontend server on http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to kill both processes on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup INT TERM

# Start backend
cd backend
source venv/bin/activate
python manage.py runserver > ../backend.log 2>&1 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Go back to root
cd ..

echo "✅ Servers started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Logs:"
echo "  Backend: tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo ""

# Wait for both processes
wait
