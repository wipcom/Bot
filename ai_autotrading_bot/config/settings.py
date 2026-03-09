from dataclasses import dataclass, field
from typing import List


@dataclass
class RiskConfig:
    max_risk_per_trade: float = 0.01
    max_daily_loss: float = 0.03
    max_drawdown: float = 0.15
    min_rr: float = 3.0


@dataclass
class BotConfig:
    exchange: str = "bitget"
    symbol: str = "BTC/USDT"
    timeframes: List[str] = field(default_factory=lambda: ["1m", "5m", "15m", "1h", "4h", "1d"])
    loop_seconds: int = 30
    mode: str = "paper"
    risk: RiskConfig = field(default_factory=RiskConfig)
