from __future__ import annotations

import os
import signal
import subprocess
from pathlib import Path

from fastapi import FastAPI, HTTPException

from ai_autotrading_bot.database import DatabaseEngine

app = FastAPI(title="AI AutoTrading Bot API")
DB = DatabaseEngine()
PID_FILE = Path(".bot.pid")


def _is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


@app.get("/health")
def health():
    pid = int(PID_FILE.read_text()) if PID_FILE.exists() else None
    running = bool(pid and _is_running(pid))
    return {"status": "ok", "bot_running": running, "pid": pid}


@app.post("/bot/start")
def start_bot():
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text())
        if _is_running(pid):
            raise HTTPException(status_code=400, detail="Bot ya está corriendo")

    proc = subprocess.Popen(["python", "main.py"], start_new_session=True)
    PID_FILE.write_text(str(proc.pid))
    return {"message": "Bot iniciado", "pid": proc.pid}


@app.post("/bot/stop")
def stop_bot():
    if not PID_FILE.exists():
        return {"message": "Bot ya detenido"}

    pid = int(PID_FILE.read_text())
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    PID_FILE.unlink(missing_ok=True)
    return {"message": "Bot detenido", "pid": pid}


@app.get("/metrics")
def metrics():
    return DB.get_summary()


@app.get("/trades")
def trades(limit: int = 50):
    return {"items": DB.fetch_recent_trades(limit=limit)}
