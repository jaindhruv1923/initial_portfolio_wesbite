# ==============================================================================
# KAVACH 1-Click Instant Live Public Cloud Edge Tunnel
# Generates a live public HTTPS URL with SSL in 5 seconds with ZERO install!
# Perfect for live Viva demonstrations, mobile phone testing & remote grading.
# ==============================================================================

param(
    [int]$LocalPort = 8000
)

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "   KAVACH LIVE EDGE CLOUD TUNNEL (INSTANT PUBLIC HTTPS LINK)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " Target Local Port: $LocalPort" -ForegroundColor Green
Write-Host " Testing local service availability..." -ForegroundColor Yellow

# Test if port is listening locally
$tcpTest = $false
try {
    $socket = New-Object System.Net.Sockets.TcpClient
    $socket.Connect("127.0.0.1", $LocalPort)
    $tcpTest = $true
    $socket.Close()
} catch {
    $tcpTest = $false
}

if (-not $tcpTest) {
    Write-Host "[WARNING] No service detected on localhost:$LocalPort." -ForegroundColor Red
    Write-Host "Make sure KAVACH is running: python -m uvicorn app.main:app --app-dir 01_KAVACH_Platform/backend --port 8000" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "[SUCCESS] KAVACH is live on localhost:$LocalPort." -ForegroundColor Green
}

Write-Host "Establishing secure SSH reverse-proxy tunnel via localhost.run..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C at any time to terminate the tunnel." -ForegroundColor DarkGray
Write-Host ""

# Run ssh reverse tunnel
ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:$LocalPort nokey@localhost.run
