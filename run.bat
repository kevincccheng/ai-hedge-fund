@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo  AI Hedge Fund - Kevin's Launcher (Windows)
echo ================================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"
set PYTHONIOENCODING=utf-8

echo [INFO] Starting backend (FastAPI) on http://127.0.0.1:8000 ...
start "AI Hedge Fund - Backend" /min cmd /k "cd /d %~dp0 && call .venv\Scripts\activate.bat && set PYTHONIOENCODING=utf-8 && poetry run uvicorn app.backend.main:app --host 127.0.0.1 --port 8000"

echo [INFO] Starting frontend (React) on http://localhost:5173 ...
start "AI Hedge Fund - Frontend" /min cmd /k "cd /d %~dp0app\frontend && npm run dev"

echo [INFO] Waiting for services to start...
timeout /t 3 /nobreak >nul

echo [INFO] Opening browser...
start "" "http://localhost:5173"

echo.
echo ================================================
echo  AI Hedge Fund is running
echo  Frontend: http://localhost:5173
echo  Backend:  http://127.0.0.1:8000
echo  Docs:     http://127.0.0.1:8000/docs
echo.
echo  Close the Backend / Frontend windows to stop the app.
echo ================================================
echo.

REM Convert the latest saved analysis report (outputs\*.json) to a PDF, if any
python convert_report.py

pause
