# KAVACH Master Platform Launcher (PowerShell)
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  KAVACH AGENTIC AI PLATFORM & MULTI-SERVICE MESH MASTER LAUNCHER" -ForegroundColor Green
Write-Host "  1. KAVACH Platform & Frontend: http://localhost:8000" -ForegroundColor White
Write-Host "  2. Bharat Core Banking Highway: http://localhost:8050" -ForegroundColor White
Write-Host "  3. Unified Results Cockpit:    http://localhost:8090" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

$root = $PSScriptRoot

Write-Host "[1/3] Starting KAVACH Platform (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root'; python -m uvicorn app.main:app --app-dir 01_KAVACH_Platform/backend --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/3] Starting Bharat Core Banking (Port 8050)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root/02_Banking_and_Results_Dashboard'; python -m uvicorn implementation_banks.server:app --host 127.0.0.1 --port 8050 --reload"

Write-Host "[3/3] Starting Unified Results Cockpit (Port 8090)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root/02_Banking_and_Results_Dashboard'; python -m uvicorn results_hub:app --app-dir results_dashboard --host 127.0.0.1 --port 8090 --reload"

Start-Sleep -Seconds 3

Write-Host "Opening KAVACH Frontend (http://localhost:8000)..." -ForegroundColor Green
Start-Process "http://localhost:8000"

Write-Host "Opening Results Cockpit (http://localhost:8090)..." -ForegroundColor Green
Start-Process "http://localhost:8090"

Write-Host ""
Write-Host "All 3 services are running in background processes." -ForegroundColor Cyan
