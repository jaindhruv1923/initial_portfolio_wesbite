@echo off
title Archon Copilot & AI Agent IDE - Windows Launcher
cls
echo ============================================================================
echo   ARCHON COPILOT - Enterprise AI Pair Programmer & Hybrid RAG IDE
echo   Developer: Dhruv Jain ^| BML Munjal University
echo ============================================================================
echo.

cd /d "%~dp0"
set PYTHONPATH=%~dp0
set PATH=C:\Program Files\nodejs;%PATH%

echo [1/4] Starting Ingestion Service on Port 8002...
start "Archon Ingestion (:8002)" cmd /k "title Archon Ingestion (:8002) & cd /d %~dp0 & set PYTHONPATH=%~dp0 & python -m uvicorn services.ingestion_service.app.main:app --host 127.0.0.1 --port 8002 --reload"

echo [2/4] Starting Hybrid RAG Service on Port 8001...
start "Archon RAG Service (:8001)" cmd /k "title Archon RAG Service (:8001) & cd /d %~dp0 & set PYTHONPATH=%~dp0 & python -m uvicorn services.rag_service.app.main:app --host 127.0.0.1 --port 8001 --reload"

echo [3/4] Starting Orchestrator Gateway on Port 8000...
start "Archon Orchestrator (:8000)" cmd /k "title Archon Orchestrator (:8000) & cd /d %~dp0 & set PYTHONPATH=%~dp0 & python -m uvicorn services.orchestrator_service.app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [4/4] Starting Next.js Web Studio Frontend on Port 3000...
start "Archon Frontend (:3000)" cmd /k "title Archon Web IDE (:3000) & cd /d %~dp0frontend & set PATH=C:\Program Files\nodejs;%%PATH%% & cmd.exe /c npm run dev"

echo.
echo Waiting 6 seconds for services to initialize...
timeout /t 6 /nobreak >nul
echo.
echo Opening browser to http://localhost:3000 ...
start http://localhost:3000

echo ============================================================================
echo All Archon Copilot services launched in separate windows!
echo Keep the service windows open while using the application.
echo ============================================================================
pause
