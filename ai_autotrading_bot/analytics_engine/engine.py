from __future__ import annotations

import pandas as pd


class AnalyticsEngine:
    def stats_by_session(self, trades: pd.DataFrame) -> pd.DataFrame:
        return trades.groupby("session", as_index=False)["pnl"].agg(["count", "mean", "sum"]).reset_index()

    def stats_by_setup(self, trades: pd.DataFrame) -> pd.DataFrame:
        return trades.groupby("setup", as_index=False)["pnl"].agg(["count", "mean", "sum"]).reset_index()
