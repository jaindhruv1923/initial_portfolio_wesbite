@echo off
REM ==============================================================================
REM KAVACH 1-Click Instant Live Public Cloud Edge Tunnel (Double-Click Launcher)
REM ==============================================================================
title KAVACH Instant Live Public Cloud Edge Tunnel
cls
echo ==================================================================
echo   KAVACH LIVE EDGE CLOUD TUNNEL (INSTANT PUBLIC HTTPS LINK)
echo ==================================================================
echo Connecting to secure edge reverse proxy over localhost:8000...
echo Free SSL HTTPS link will be generated below in 3 seconds.
echo Press Ctrl+C to close the tunnel.
echo.

ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:8000 nokey@localhost.run
pause
