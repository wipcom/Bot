from __future__ import annotations

import pandas as pd


class BacktestingEngine:
    def compute_metrics(self, trades: pd.DataFrame) -> dict:
        if trades.empty:
            return {"winrate": 0, "profit_factor": 0, "max_drawdown": 0, "expectancy": 0, "sharpe_ratio": 0, "total_trades": 0}
        wins = (trades["pnl"] > 0).sum()
        losses = (trades["pnl"] < 0).sum()
        gross_profit = trades.loc[trades["pnl"] > 0, "pnl"].sum()
        gross_loss = abs(trades.loc[trades["pnl"] < 0, "pnl"].sum())
        return {
            "winrate": wins / len(trades),
            "profit_factor": (gross_profit / gross_loss) if gross_loss else float("inf"),
            "max_drawdown": float(trades["equity_curve"].cummax().sub(trades["equity_curve"]).max()),
            "expectancy": float(trades["pnl"].mean()),
            "sharpe_ratio": float(trades["pnl"].mean() / (trades["pnl"].std() + 1e-9)),
            "total_trades": int(len(trades)),
            "loss_trades": int(losses),
        }
