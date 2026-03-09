import unittest

from ai_autotrading_bot.trade_manager import TradeManager


class TradeManagerTest(unittest.TestCase):
    def test_should_close_take_profit(self):
        tm = TradeManager()
        trade = {"side": "buy", "entry": 100.0, "stop_loss": 99.0, "take_profit": 103.0, "size": 1.0}
        close, reason = tm.should_close_trade(trade, 103.5)
        self.assertTrue(close)
        self.assertEqual(reason, "take_profit")

    def test_compute_pnl_buy(self):
        tm = TradeManager()
        trade = {"side": "buy", "entry": 100.0, "stop_loss": 99.0, "take_profit": 103.0, "size": 2.0}
        self.assertEqual(tm.compute_pnl(trade, 101.5), 3.0)


if __name__ == "__main__":
    unittest.main()
