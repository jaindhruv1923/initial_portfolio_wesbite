# Bharat Core Bank x KAVACH AI Shield Launcher
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "  BHARAT CORE BANK x KAVACH AI GOVERNANCE SYSTEM" -ForegroundColor White
Write-Host "  Enterprise 5-Gate Defense & NIST SHA3-512 Merkle Ledger" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1/2] Opening Web Cockpit on http://127.0.0.1:8050 ..." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:8050"
Write-Host "[2/2] Launching FastApi Core Server on Port 8050..." -ForegroundColor Green
python -m uvicorn implementation_banks.server:app --host 127.0.0.1 --port 8050 --reload
