from __future__ import annotations

import pandas as pd


class SMCPatternsEngine:
    def detect_fvg(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["bullish_fvg"] = out["high"].shift(2) < out["low"]
        out["bearish_fvg"] = out["low"].shift(2) > out["high"]
        return out

    def detect_order_blocks(self, df: pd.DataFrame) -> pd.Series:
        return (df["close"].shift(1) < df["open"].shift(1)) & (df["close"] > df["high"].shift(1))

    def detect_premium_discount(self, df: pd.DataFrame, lookback: int = 50) -> pd.DataFrame:
        out = df.copy()
        rng_high = out["high"].rolling(lookback).max()
        rng_low = out["low"].rolling(lookback).min()
        mid = (rng_high + rng_low) / 2
        out["premium_zone"] = out["close"] > mid
        out["discount_zone"] = out["close"] <= mid
        return out
