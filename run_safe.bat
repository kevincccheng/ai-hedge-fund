@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

if not exist "crash_logs" mkdir "crash_logs"

set "TIMESTAMP="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"`) do set "TIMESTAMP=%%i"
if "%TIMESTAMP%"=="" set "TIMESTAMP=run"

set "LOGFILE=crash_logs\run_%TIMESTAMP%.log"

echo ================================================
echo  AI Hedge Fund - Safe Launcher (crash protected)
echo ================================================
echo [INFO] Logging output to %LOGFILE%
echo.

call run.bat > "%LOGFILE%" 2>&1
set "EXITCODE=%errorlevel%"

if not "%EXITCODE%"=="0" (
    echo [ERROR] run.bat exited with code %EXITCODE%
    echo [ERROR] Crash log saved to %LOGFILE%
    if exist "outputs" (
        echo [INFO] Preserving any partial report output...
        copy /y "outputs\*.json" "crash_logs\" >nul 2>&1
    )
) else (
    echo [SUCCESS] Run finished. Log saved to %LOGFILE%
)

pause
