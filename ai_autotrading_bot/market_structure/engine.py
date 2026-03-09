from __future__ import annotations

import pandas as pd


class MarketStructureEngine:
    def detect_swings(self, df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
        out = df.copy()
        out["swing_high"] = out["high"] == out["high"].rolling(window, center=True).max()
        out["swing_low"] = out["low"] == out["low"].rolling(window, center=True).min()
        return out

    def detect_bos(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["bos_bull"] = out["high"] > out["high"].shift(1)
        out["bos_bear"] = out["low"] < out["low"].shift(1)
        return out

    def detect_choch(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["choch"] = (out["bos_bull"] & out["bos_bear"].shift(1)) | (out["bos_bear"] & out["bos_bull"].shift(1))
        return out
