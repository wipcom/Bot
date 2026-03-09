from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExecutionResult:
    status: str
    order_id: str


class ExecutionEngine:
    def __init__(self, mode: str = "paper"):
        self.mode = mode

    def open_trade(self, symbol: str, side: str, size: float, entry: float, stop_loss: float, take_profit: float) -> ExecutionResult:
        # TODO: integrar CCXT real
        return ExecutionResult("filled", f"paper_{symbol}_{side}_{size:.4f}")

    def close_trade(self, order_id: str) -> ExecutionResult:
        return ExecutionResult("closed", order_id)

    def modify_stop_loss(self, order_id: str, stop_loss: float) -> None:
        return None

    def move_take_profit(self, order_id: str, take_profit: float) -> None:
        return None
