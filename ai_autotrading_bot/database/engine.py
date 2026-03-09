from __future__ import annotations

import sqlite3
from pathlib import Path


class DatabaseEngine:
    def __init__(self, db_path: Path = Path("ai_autotrading.db")):
        self.db_path = db_path
        self._init_schema()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_schema(self):
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY,
                    symbol TEXT,
                    timeframe TEXT,
                    timestamp TEXT,
                    open REAL, high REAL, low REAL, close REAL, volume REAL
                );
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY,
                    order_id TEXT,
                    symbol TEXT,
                    side TEXT,
                    entry REAL,
                    stop_loss REAL,
                    take_profit REAL,
                    pnl REAL,
                    status TEXT,
                    created_at TEXT
                );
                CREATE TABLE IF NOT EXISTS strategy_logs (
                    id INTEGER PRIMARY KEY,
                    message TEXT,
                    level TEXT,
                    created_at TEXT
                );
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY,
                    metric TEXT,
                    value REAL,
                    created_at TEXT
                );
                """
            )

    def insert_trade(self, trade: dict) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO trades (order_id, symbol, side, entry, stop_loss, take_profit, pnl, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                """,
                (
                    trade["order_id"],
                    trade["symbol"],
                    trade["side"],
                    trade["entry"],
                    trade["stop_loss"],
                    trade["take_profit"],
                    trade.get("pnl", 0.0),
                    trade.get("status", "open"),
                ),
            )


    def close_trade(self, order_id: str, pnl: float, status: str = "closed") -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE trades
                SET pnl = ?, status = ?
                WHERE order_id = ?
                """,
                (pnl, status, order_id),
            )

    def fetch_recent_trades(self, limit: int = 50) -> list[dict]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT order_id, symbol, side, entry, stop_loss, take_profit, pnl, status, created_at
                FROM trades ORDER BY id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_summary(self) -> dict:
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM trades").fetchone()[0]
            wins = conn.execute("SELECT COUNT(*) FROM trades WHERE pnl > 0").fetchone()[0]
            pnl = conn.execute("SELECT COALESCE(SUM(pnl), 0) FROM trades").fetchone()[0]
        winrate = (wins / total) if total else 0.0
        return {"total_trades": total, "winrate": winrate, "realized_pnl": float(pnl)}
