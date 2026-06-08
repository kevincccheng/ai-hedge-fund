@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo  AI Hedge Fund - Kevin's Setup (Windows)
echo ================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Install it from https://python.org/
    pause
    exit /b 1
)

where node >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Install it from https://nodejs.org/
    pause
    exit /b 1
)

echo [INFO] Configuring git line endings for Windows...
git config core.autocrlf true

echo [INFO] Creating Python virtual environment (.venv)...
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create the virtual environment
        pause
        exit /b 1
    )
) else (
    echo [INFO] .venv already exists, skipping creation
)

echo [INFO] Activating virtual environment and installing Python dependencies...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install poetry reportlab
if errorlevel 1 (
    echo [ERROR] Failed to install base Python tooling
    pause
    exit /b 1
)

poetry install
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies via Poetry
    pause
    exit /b 1
)

echo [INFO] Installing frontend (Node.js) dependencies...
pushd "app\frontend"
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install frontend dependencies
    popd
    pause
    exit /b 1
)
popd

echo [INFO] Setting up environment file...
if not exist ".env" (
    if exist ".env.kevin.example" (
        copy /y ".env.kevin.example" ".env" >nul
        echo [INFO] Created .env from .env.kevin.example - edit it to add your API keys
    ) else (
        echo [WARNING] .env.kevin.example not found - create .env manually with your API keys
    )
) else (
    echo [INFO] .env already exists, leaving it untouched
)

echo.
echo ================================================
echo  [SUCCESS] Setup complete!
echo  Next step: edit .env with your API keys, then
echo  double-click run.bat to start the app
echo ================================================
echo.
pause
