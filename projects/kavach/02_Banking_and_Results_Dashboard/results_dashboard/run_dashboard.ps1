# KAVACH x BHARAT BANK - Unified Operations and Results Cockpit Launcher
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  KAVACH x BHARAT BANK - UNIFIED RESULTS COCKPIT" -ForegroundColor White
Write-Host "  Live Operations Telemetry - NIST SHA3-512 DPDP Merkle Ledger" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1/2] Opening Unified Results Dashboard at http://127.0.0.1:8090 ..." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:8090"

Write-Host "[2/2] Launching FastAPI Telemetry and Persistence Hub on Port 8090..." -ForegroundColor Green
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python -m uvicorn results_hub:app --app-dir "$ScriptDir" --host 127.0.0.1 --port 8090 --reload
