@echo off
echo Starting Network Anomaly Monitor and Detection System...

echo Creating Python virtual environment...
cd backend
if not exist venv (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo Installing backend dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo Starting backend...
start cmd /k "cd backend && call venv\Scripts\activate && python run.py"
cd ..

echo Installing frontend dependencies...
npm install

echo Starting frontend...
start cmd /k "npm run dev"

echo System started!
echo Backend API: http://localhost:8000
echo Frontend Dashboard: http://localhost:5173
echo API Documentation: http://localhost:8000/docs
