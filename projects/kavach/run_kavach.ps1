Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  SHIELD / KAVACH - Agentic AI DevOps Security & Governance Platform" -ForegroundColor Green
Write-Host "  Developer: Dhruv Jain | BML Munjal University" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1/2] Starting Unified Server on http://127.0.0.1:8000 ..." -ForegroundColor White
Write-Host "[2/2] Opening Dashboard in your browser: http://localhost:8000" -ForegroundColor White
Write-Host ""

Start-Process "http://localhost:8000"

if (Test-Path "01_KAVACH_Platform\backend") {
    python -m uvicorn app.main:app --app-dir 01_KAVACH_Platform/backend --host 127.0.0.1 --port 8000 --reload
} elseif (Test-Path "important\kavach\backend") {
    python -m uvicorn app.main:app --app-dir important/kavach/backend --host 127.0.0.1 --port 8000 --reload
} else {
    python -m uvicorn app.main:app --app-dir kavach/backend --host 127.0.0.1 --port 8000 --reload
}
