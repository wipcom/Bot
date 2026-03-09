@echo off
setlocal
cd /d "%~dp0\..\.."
start "autotrading-api" cmd /k uvicorn ai_autotrading_bot.web_dashboard.api:app --host 0.0.0.0 --port 8000
streamlit run ai_autotrading_bot/web_dashboard/streamlit_app.py --server.port 8501
endlocal
