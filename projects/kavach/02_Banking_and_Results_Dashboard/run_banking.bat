@echo off
title Bharat Core Banking & KAVACH Shield
color 0B
echo ==============================================================================
echo   BHARAT COMMERCIAL CORE BANKING & KAVACH HIGHWAY (Port 8050)
echo ==============================================================================
echo.
cd /d "%~dp0"
python -m uvicorn implementation_banks.server:app --host 127.0.0.1 --port 8050 --reload
pause
