from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class TradeSignal:
    side: str
    entry: float
    stop_loss: float
    take_profit: float
    reason: str


class StrategyEngine:
    def generate_signal(self, df: pd.DataFrame) -> TradeSignal | None:
        if len(df) < 5:
            return None
        row = df.iloc[-1]
        if bool(row.get("liquidity_sweep", False)) and bool(row.get("bos_bull", False)) and bool(row.get("bullish_fvg", False)):
            entry = float(row["close"])
            stop = float(row["low"])
            tp = entry + (entry - stop) * 3
            return TradeSignal("buy", entry, stop, tp, "Sweep + BOS + Bullish FVG")
        return None
