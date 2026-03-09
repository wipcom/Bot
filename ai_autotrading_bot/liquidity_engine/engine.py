from __future__ import annotations

import pandas as pd


class LiquidityEngine:
    def detect_equal_highs(self, df: pd.DataFrame, tolerance: float = 0.001) -> pd.Series:
        return (df["high"].pct_change().abs() <= tolerance).fillna(False)

    def detect_equal_lows(self, df: pd.DataFrame, tolerance: float = 0.001) -> pd.Series:
        return (df["low"].pct_change().abs() <= tolerance).fillna(False)

    def detect_liquidity_sweeps(self, df: pd.DataFrame) -> pd.Series:
        return (df["high"] > df["high"].shift(1)) & (df["close"] < df["high"].shift(1))
