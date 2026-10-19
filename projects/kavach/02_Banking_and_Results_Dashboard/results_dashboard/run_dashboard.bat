@echo off
title KAVACH x BHARAT BANK - Unified Results Cockpit
echo =====================================================================
echo   KAVACH x BHARAT BANK - UNIFIED RESULTS COCKPIT
echo   Live Operations Telemetry - NIST SHA3-512 DPDP Merkle Ledger
echo =====================================================================
echo.
echo [1/2] Opening Dashboard in default browser: http://127.0.0.1:8090
start http://127.0.0.1:8090
echo [2/2] Launching FastApi Telemetry Hub on Port 8090...
cd /d "%~dp0"
python -m uvicorn results_hub:app --host 127.0.0.1 --port 8090 --reload
pause
