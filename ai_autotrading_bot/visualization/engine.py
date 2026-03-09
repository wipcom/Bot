from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


class VisualizationEngine:
    def plot_equity_curve(self, trades: pd.DataFrame):
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(trades["equity_curve"])
        ax.set_title("Equity Curve")
        ax.grid(True)
        return fig
