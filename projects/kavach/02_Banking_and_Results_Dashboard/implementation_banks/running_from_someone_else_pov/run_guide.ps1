# KAVACH x Core Banking Multi-Perspective Animated Guide Launcher
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "  KAVACH x CORE BANKING SYSTEM: ANIMATED INTERACTIVE GUIDE" -ForegroundColor White
Write-Host "  Multi-Perspective Governance (Customer, DevOps, Hacker, RBI, CISO)" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
$htmlPath = Join-Path $PSScriptRoot "animated_guide.html"
Write-Host "Opening Animated Guide: $htmlPath" -ForegroundColor Yellow
Start-Process $htmlPath
Write-Host "Done!" -ForegroundColor Green
