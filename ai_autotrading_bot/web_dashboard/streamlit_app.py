from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

API_URL = st.sidebar.text_input("API URL", value="http://localhost:8000")

st.set_page_config(page_title="AI AutoTrading Dashboard", layout="wide")
st.title("AI AutoTrading Bot - Monitor")


def get_json(path: str) -> dict:
    try:
        return requests.get(f"{API_URL}{path}", timeout=3).json()
    except Exception:
        return {}


health = get_json("/health")
metrics = get_json("/metrics")
trades = get_json("/trades")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Bot running", "Sí" if health.get("bot_running") else "No")
c2.metric("Total trades", metrics.get("total_trades", 0))
c3.metric("Winrate", f"{metrics.get('winrate', 0)*100:.2f}%")
c4.metric("PNL", f"{metrics.get('realized_pnl', 0):.2f}")

st.subheader("Control")
col1, col2 = st.columns(2)
if col1.button("Iniciar bot"):
    requests.post(f"{API_URL}/bot/start", timeout=3)
if col2.button("Detener bot"):
    requests.post(f"{API_URL}/bot/stop", timeout=3)

st.subheader("Historial de trades")
st.dataframe(pd.DataFrame(trades.get("items", [])))
