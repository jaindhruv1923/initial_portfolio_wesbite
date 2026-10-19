@echo off
title KAVACH Agentic AI Platform Runner
color 0A
echo ===============================================================================
echo   KAVACH: Zero-Trust Agentic AI DevOps Platform ^& Professor Review Suite
echo   Instructors: Dr. Soharab Hossain Shaikh ^& Mr. Pranshu Tiwari (CSE3101)
echo ===============================================================================
echo.
echo [1/2] Opening KAVACH Frontend in default browser: http://localhost:8000 ...
start http://localhost:8000
echo.
echo [2/2] Launching FastAPI Backend ^& Frontend Server on Port 8000...
echo Server running at http://127.0.0.1:8000 (Press Ctrl+C to stop)
echo.
if exist "01_KAVACH_Platform\backend" (
    python -m uvicorn app.main:app --app-dir 01_KAVACH_Platform/backend --host 127.0.0.1 --port 8000 --reload
) else (
    python -m uvicorn app.main:app --app-dir important/kavach/backend --host 127.0.0.1 --port 8000 --reload
)
pause
