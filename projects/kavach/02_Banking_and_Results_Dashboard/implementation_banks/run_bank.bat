@echo off
title Bharat Core Bank x KAVACH AI Shield (Port 8050)
color 0B
echo =====================================================================
echo   BHARAT CORE BANK x KAVACH AI GOVERNANCE SYSTEM
echo   Enterprise 5-Gate Defense & NIST SHA3-512 Merkle Ledger
echo =====================================================================
echo.
echo [1/2] Launching Banking FastApi Engine on http://127.0.0.1:8050 ...
start "" http://127.0.0.1:8050
python -m uvicorn implementation_banks.server:app --host 127.0.0.1 --port 8050 --reload
pause
