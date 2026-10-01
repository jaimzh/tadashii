@echo off
setlocal

cd /d "%~dp0backend"

if not exist "venv\Scripts\python.exe" (
    echo Backend virtual environment not found.
    echo Create it with:
    echo   py -m venv venv
    echo   venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo Starting Tadashii backend server...
echo API:  http://127.0.0.1:8000
echo Docs: http://127.0.0.1:8000/docs
echo.

"venv\Scripts\python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

pause
