from __future__ import annotations

import argparse
import time
from pathlib import Path

from ai_autotrading_bot.ai_optimizer import AIOptimizer
from ai_autotrading_bot.config import BotConfig
from ai_autotrading_bot.data_engine import DataEngine
from ai_autotrading_bot.database import DatabaseEngine
from ai_autotrading_bot.execution_engine import ExecutionEngine
from ai_autotrading_bot.liquidity_engine import LiquidityEngine
from ai_autotrading_bot.machine_learning import MachineLearningEngine
from ai_autotrading_bot.market_structure import MarketStructureEngine
from ai_autotrading_bot.risk_engine import RiskEngine, RiskState
from ai_autotrading_bot.session_engine import SessionEngine
from ai_autotrading_bot.smc_patterns import SMCPatternsEngine
from ai_autotrading_bot.strategy_engine import StrategyEngine
from ai_autotrading_bot.trade_manager import TradeManager


def run_bot(config: BotConfig, iterations: int | None = None):
    data_engine = DataEngine()
    db = DatabaseEngine()
    ms = MarketStructureEngine()
    liq = LiquidityEngine()
    smc = SMCPatternsEngine()
    sess = SessionEngine()
    strategy = StrategyEngine()
    trade_manager = TradeManager()
    risk = RiskEngine(
        max_risk_per_trade=config.risk.max_risk_per_trade,
        max_drawdown=config.risk.max_drawdown,
        max_daily_loss=config.risk.max_daily_loss,
    )
    execution = ExecutionEngine(mode=config.mode)
    ml = MachineLearningEngine()
    ai = AIOptimizer()

    balance = 100_000.0
    loop_count = 0
    risk_state = RiskState(daily_pnl=0.0, equity_peak=balance)
    open_trades: list[dict] = []

    while True:
        mtf_data = data_engine.get_multi_timeframe_data(config.symbol, config.timeframes)
        df = mtf_data["15m"]
        current_price = float(df.iloc[-1]["close"])

        for trade in open_trades[:]:
            trade_manager.apply_break_even(trade, current_price)
            trade_manager.trailing_stop(trade, current_price, trail=0.5)
            should_close, reason = trade_manager.should_close_trade(trade, current_price)
            if should_close:
                pnl = trade_manager.compute_pnl(trade, current_price)
                balance += pnl
                risk_state.daily_pnl += pnl
                db.close_trade(trade["order_id"], pnl=pnl, status=reason)
                open_trades.remove(trade)

        df = ms.detect_swings(df)
        df = ms.detect_bos(df)
        df = ms.detect_choch(df)
        df["equal_highs"] = liq.detect_equal_highs(df)
        df["equal_lows"] = liq.detect_equal_lows(df)
        df["liquidity_sweep"] = liq.detect_liquidity_sweeps(df)
        df = smc.detect_fvg(df)
        df = smc.detect_premium_discount(df)
        df["order_block"] = smc.detect_order_blocks(df)
        df = sess.tag_sessions(df)

        predictions = ml.predict_market_state({"volatility": 0.4})
        signal = strategy.generate_signal(df)

        if signal and predictions.sweep_probability > 0.5 and risk.can_open_trade(balance, risk_state, equity_now=balance):
            size = risk.calculate_position_size(balance, signal.entry, signal.stop_loss)
            result = execution.open_trade(config.symbol, signal.side, size, signal.entry, signal.stop_loss, signal.take_profit)
            trade = {
                "order_id": result.order_id,
                "symbol": config.symbol,
                "side": signal.side,
                "entry": signal.entry,
                "stop_loss": signal.stop_loss,
                "take_profit": signal.take_profit,
                "size": size,
            }
            open_trades.append(trade)
            db.insert_trade({**trade, "pnl": 0.0, "status": "open"})
            print(f"Orden ejecutada: {result}")

        risk_state.equity_peak = max(risk_state.equity_peak, balance)

        if int(time.time()) % 300 == 0:
            print("Sugerencias IA:", ai.suggest_parameters(trade_log_path=Path("trade_log.csv")))

        loop_count += 1
        if iterations is not None and loop_count >= iterations:
            break

        time.sleep(config.loop_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Autotrading Bot")
    parser.add_argument("--iterations", type=int, default=None, help="Cantidad de loops a ejecutar (debug/test)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_bot(BotConfig(), iterations=args.iterations)
