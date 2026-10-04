@echo off
title KAVACH Enterprise AI DevOps Governance Platform
cls
cd /d "%~dp0"
echo ============================================================================
echo   SHIELD / KAVACH - Agentic AI DevOps Security & Governance Platform
echo   Developer: Dhruv Jain ^| BML Munjal University
echo ============================================================================
echo.
echo [1/2] Launching Unified FastAPI Backend + Static Frontend on http://127.0.0.1:8000 ...
echo [2/2] Opening Web Browser to http://localhost:8000 ...
echo.
start http://localhost:8000
echo Server is running. Press CTRL+C in this terminal to stop.
echo ============================================================================
python -m uvicorn app.main:app --app-dir kavach/backend --host 127.0.0.1 --port 8000 --reload
pause
