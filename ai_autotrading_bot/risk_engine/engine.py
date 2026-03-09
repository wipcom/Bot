from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskState:
    daily_pnl: float = 0.0
    equity_peak: float = 0.0


class RiskEngine:
    def __init__(self, max_risk_per_trade: float = 0.01, max_drawdown: float = 0.15, max_daily_loss: float = 0.03):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_drawdown = max_drawdown
        self.max_daily_loss = max_daily_loss

    def calculate_position_size(self, balance: float, entry: float, stop: float) -> float:
        risk_amount = balance * self.max_risk_per_trade
        stop_distance = abs(entry - stop)
        if stop_distance == 0:
            return 0.0
        return risk_amount / stop_distance

    def manage_drawdown(self, equity_peak: float, equity_now: float) -> bool:
        if equity_peak <= 0:
            return True
        drawdown = (equity_peak - equity_now) / equity_peak
        return drawdown <= self.max_drawdown

    def within_daily_loss_limit(self, balance: float, daily_pnl: float) -> bool:
        return abs(min(daily_pnl, 0.0)) <= balance * self.max_daily_loss

    def can_open_trade(self, balance: float, state: RiskState, equity_now: float) -> bool:
        peak = max(state.equity_peak, equity_now)
        return self.manage_drawdown(peak, equity_now) and self.within_daily_loss_limit(balance, state.daily_pnl)
