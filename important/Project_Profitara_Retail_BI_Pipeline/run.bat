@echo off
echo ========================================================
echo   PROFITARA -- Launching 13-Page Streamlit Dashboard
echo ========================================================
echo.
python -m streamlit run dashboard\app.py --server.port 8501
pause
