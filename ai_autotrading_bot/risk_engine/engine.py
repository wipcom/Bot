from __future__ import annotations


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
            return False
        drawdown = (equity_peak - equity_now) / equity_peak
        return drawdown <= self.max_drawdown
