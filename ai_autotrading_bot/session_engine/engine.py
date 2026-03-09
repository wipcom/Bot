from __future__ import annotations

import pandas as pd


class SessionEngine:
    def tag_sessions(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        hour = out["timestamp"].dt.hour
        out["session"] = "Asia"
        out.loc[(hour >= 7) & (hour < 13), "session"] = "London"
        out.loc[(hour >= 13) & (hour < 22), "session"] = "New York"
        out["killzone"] = out["session"].isin(["London", "New York"])
        return out
