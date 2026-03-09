from __future__ import annotations


class TradeManager:
    def apply_break_even(self, trade: dict, current_price: float, trigger_rr: float = 1.0) -> dict:
        risk = abs(trade["entry"] - trade["stop_loss"])
        profit = abs(current_price - trade["entry"])
        if risk > 0 and (profit / risk) >= trigger_rr:
            trade["stop_loss"] = trade["entry"]
        return trade

    def trailing_stop(self, trade: dict, current_price: float, trail: float) -> dict:
        if trade["side"] == "buy":
            trade["stop_loss"] = max(trade["stop_loss"], current_price - trail)
        return trade

    def should_close_trade(self, trade: dict, current_price: float) -> tuple[bool, str]:
        if trade["side"] == "buy":
            if current_price <= trade["stop_loss"]:
                return True, "stop_loss"
            if current_price >= trade["take_profit"]:
                return True, "take_profit"
        return False, ""

    def compute_pnl(self, trade: dict, exit_price: float) -> float:
        if trade["side"] == "buy":
            return (exit_price - trade["entry"]) * trade["size"]
        return (trade["entry"] - exit_price) * trade["size"]
