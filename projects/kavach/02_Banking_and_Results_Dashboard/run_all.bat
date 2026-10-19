@echo off
title Bharat Banking & Results Dashboard Launcher
color 0A
echo ==============================================================================
echo   BHARAT BANKING & RESULTS DASHBOARD DUAL LAUNCHER
echo   1. Bharat Core Banking Highway: http://localhost:8050
echo   2. Unified Results Cockpit:    http://localhost:8090
echo ==============================================================================
echo.
cd /d "%~dp0"
start "Bharat-Banking-8050" cmd /k "python -m uvicorn implementation_banks.server:app --host 127.0.0.1 --port 8050 --reload"
start "Results-Cockpit-8090" cmd /k "python -m uvicorn results_hub:app --app-dir results_dashboard --host 127.0.0.1 --port 8090 --reload"
timeout /t 3 >nul
start http://localhost:8050
start http://localhost:8090
echo Both services launched successfully.
pause
