@echo off
echo ======================================
echo  Multi-Modal AI Inspector - Startup
echo ======================================
echo.

echo Starting Backend Server...
cd backend

REM Activate virtual environment
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo            .venv\Scripts\activate
    echo            pip install -r requirements.txt
    pause
    exit /b 1
)

REM Start backend in background
start "Multi-Modal AI Inspector - Backend" cmd /k "python -m app.main"

echo.
echo Backend starting at http://localhost:8000
echo.
echo Starting Frontend...
cd ..\frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
)

REM Start frontend
start "Multi-Modal AI Inspector - Frontend" cmd /k "npm run dev"

echo.
echo ======================================
echo  Application is starting!
echo.
echo  Frontend: http://localhost:5173
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo.
echo  Press Ctrl+C in each window to stop
echo ======================================
echo.

pause
