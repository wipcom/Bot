from __future__ import annotations

from pathlib import Path


class AIOptimizer:
    def __init__(self, model: str = "llama3"):
        self.model = model

    def suggest_parameters(self, trade_log_path: Path) -> dict:
        # TODO: integrar Ollama local para analizar logs
        return {
            "avoid_asia_session": False,
            "target_rr": 3.0,
            "volatility_filter_min": 0.3,
        }
