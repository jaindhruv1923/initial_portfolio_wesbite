@echo off
title KAVACH Model Context Protocol (MCP) Server
cls
echo Starting KAVACH Model Context Protocol (MCP) Server...
echo.
python "%~dp0..\core_engine\mcp_server.py"
pause
