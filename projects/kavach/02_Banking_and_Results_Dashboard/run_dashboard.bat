@echo off
title Unified Results Cockpit Telemetry Hub
color 0E
echo ==============================================================================
echo   UNIFIED RESULTS COCKPIT TELEMETRY HUB (Port 8090)
echo ==============================================================================
echo.
cd /d "%~dp0"
python -m uvicorn results_hub:app --app-dir results_dashboard --host 127.0.0.1 --port 8090 --reload
pause
