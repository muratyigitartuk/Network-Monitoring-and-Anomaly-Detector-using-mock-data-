#!/bin/bash
echo "Starting Network Anomaly Monitor and Detection System..."

echo "Creating Python virtual environment..."
cd backend
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

echo "Installing backend dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "Starting backend..."
python run.py &
BACKEND_PID=$!
cd ..

echo "Installing frontend dependencies..."
npm install

echo "Starting frontend..."
npm run dev &
FRONTEND_PID=$!

echo "System started!"
echo "Backend API: http://localhost:8000"
echo "Frontend Dashboard: http://localhost:5173"
echo "API Documentation: http://localhost:8000/docs"

# Handle graceful shutdown
function cleanup() {
    echo "Shutting down..."
    kill $FRONTEND_PID
    kill $BACKEND_PID
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
