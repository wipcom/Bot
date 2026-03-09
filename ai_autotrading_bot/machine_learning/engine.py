from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MLPredictions:
    sweep_probability: float
    trend_continuation_probability: float
    volatility_score: float


class MachineLearningEngine:
    def predict_market_state(self, features: dict) -> MLPredictions:
        # TODO: reemplazar por sklearn/xgboost entrenado
        return MLPredictions(0.55, 0.60, 0.45)
