@echo off
title KAVACH Multi-Service Mesh Master Launcher
color 0B
echo ===============================================================================
echo   KAVACH FULL PLATFORM MASTER LAUNCHER (3 ENGINES IN PARALLEL)
echo   1. KAVACH Platform ^& Frontend: http://localhost:8000
echo   2. Bharat Core Banking Highway: http://localhost:8050
echo   3. Unified Results Cockpit:    http://localhost:8090
echo ===============================================================================
echo.

echo Launching Service 1: KAVACH Platform (Port 8000)...
start "KAVACH-Platform-8000" cmd /k "python -m uvicorn app.main:app --app-dir 01_KAVACH_Platform/backend --host 127.0.0.1 --port 8000 --reload"

echo Launching Service 2: Bharat Core Banking (Port 8050)...
start "Bharat-Banking-8050" cmd /k "cd 02_Banking_and_Results_Dashboard && python -m uvicorn implementation_banks.server:app --host 127.0.0.1 --port 8050 --reload"

echo Launching Service 3: Unified Results Cockpit (Port 8090)...
start "Results-Cockpit-8090" cmd /k "cd 02_Banking_and_Results_Dashboard && python -m uvicorn results_hub:app --app-dir results_dashboard --host 127.0.0.1 --port 8090 --reload"

echo.
echo Waiting 3 seconds for servers to initialize...
timeout /t 3 >nul

echo Opening Browser Windows...
start http://localhost:8000
start http://localhost:8090

echo ===============================================================================
echo   ALL 3 ENGINES ARE RUNNING SUCCESSFULLY!
echo   Press any key to exit this launcher window (servers will continue running).
echo ===============================================================================
pause
