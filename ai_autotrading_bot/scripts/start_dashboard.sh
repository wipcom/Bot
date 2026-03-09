#!/usr/bin/env bash
set -euo pipefail
uvicorn ai_autotrading_bot.web_dashboard.api:app --host 0.0.0.0 --port 8000 &
streamlit run ai_autotrading_bot/web_dashboard/streamlit_app.py --server.port 8501
