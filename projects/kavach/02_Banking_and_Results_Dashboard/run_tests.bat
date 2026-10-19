@echo off
title Bharat Banking & Unified 200-Test Execution
color 0F
echo ==============================================================================
echo   EXECUTING BHARAT BANKING & UNIFIED CROSS-PLATFORM TEST SUITES (200 TESTS)
echo ==============================================================================
echo.
cd /d "%~dp0"
echo [1/2] Running Bharat Banking 100 Suite...
python -m pytest implementation_banks/test_banking_100_suite.py -q
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Banking 100 Suite failed!
    pause
    exit /b %ERRORLEVEL%
)
echo.
echo [2/2] Running Unified Cross-Platform 100 Suite...
python -m pytest tests_unified/test_unified_100_suite.py -q
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Unified 100 Suite failed!
    pause
    exit /b %ERRORLEVEL%
)
echo.
echo ==============================================================================
echo   ALL 200 DETERMINISTIC BANKING & UNIFIED TESTS PASSED (100%% SUCCESS)!
echo ==============================================================================
pause
