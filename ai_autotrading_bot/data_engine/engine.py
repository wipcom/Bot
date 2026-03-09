from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass
class DataEngine:
    """Carga y normalización de OHLCV multi-timeframe (base para CCXT)."""

    data_dir: Path = Path("data")

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:
        # TODO: integrar CCXT real (Bitunix/Bitget/Bingx)
        idx = pd.date_range(end=pd.Timestamp.utcnow(), periods=limit, freq="min")
        df = pd.DataFrame(
            {
                "timestamp": idx,
                "open": 100.0,
                "high": 101.0,
                "low": 99.0,
                "close": 100.5,
                "volume": 10.0,
            }
        )
        return self.normalize(df)

    @staticmethod
    def normalize(df: pd.DataFrame) -> pd.DataFrame:
        cols = ["timestamp", "open", "high", "low", "close", "volume"]
        clean = df[cols].copy()
        clean["timestamp"] = pd.to_datetime(clean["timestamp"], utc=True)
        clean = clean.dropna().sort_values("timestamp").reset_index(drop=True)
        return clean

    def get_multi_timeframe_data(self, symbol: str, timeframes: list[str]) -> Dict[str, pd.DataFrame]:
        return {tf: self.fetch_ohlcv(symbol, tf) for tf in timeframes}

    def store_parquet(self, df: pd.DataFrame, name: str) -> Path:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        path = self.data_dir / f"{name}.parquet"
        df.to_parquet(path, index=False)
        return path
