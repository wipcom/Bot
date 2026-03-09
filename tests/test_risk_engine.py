import unittest

from ai_autotrading_bot.risk_engine import RiskEngine, RiskState


class RiskEngineTest(unittest.TestCase):
    def test_position_size_basic(self):
        engine = RiskEngine(max_risk_per_trade=0.01)
        size = engine.calculate_position_size(balance=10000, entry=100, stop=99)
        self.assertEqual(size, 100.0)

    def test_can_open_trade_blocked_by_daily_loss(self):
        engine = RiskEngine(max_daily_loss=0.02)
        state = RiskState(daily_pnl=-300, equity_peak=10000)
        self.assertFalse(engine.can_open_trade(balance=10000, state=state, equity_now=9800))


if __name__ == "__main__":
    unittest.main()
