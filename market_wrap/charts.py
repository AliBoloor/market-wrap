from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .analytics import close_series
from .models import Asset, MarketData, QualityFlag


def create_technical_charts(assets: tuple[Asset, ...], data: MarketData, output_dir: Path) -> tuple[dict[str, str], list[QualityFlag]]:
    chart_dir = output_dir / "charts"
    chart_dir.mkdir(parents=True, exist_ok=True)
    charts: dict[str, str] = {}
    flags: list[QualityFlag] = []
    for asset in assets:
        frame = data.prices.get(asset.symbol)
        if frame is None or frame.empty:
            continue
        try:
            close = close_series(frame).tail(252)
            fig, ax = plt.subplots(figsize=(8.5, 3.2))
            ax.plot(close.index, close, label="Close", color="#2563eb", linewidth=1.5)
            for window, color in ((20, "#f59e0b"), (50, "#8b5cf6"), (200, "#64748b")):
                if len(close) >= window:
                    ax.plot(close.index, close.rolling(window).mean(), label=f"{window}D MA", color=color, linewidth=1)
            ax.set_title(f"{asset.name} ({asset.symbol})")
            ax.grid(alpha=0.2)
            ax.legend(ncol=4, fontsize=8, frameon=False)
            fig.tight_layout()
            safe_symbol = asset.symbol.replace("^", "idx-").replace("/", "-")
            path = chart_dir / f"{safe_symbol}.png"
            fig.savefig(path, dpi=130)
            plt.close(fig)
            charts[asset.symbol] = str(path.relative_to(output_dir))
        except Exception as exc:
            flags.append(QualityFlag("warning", asset.symbol, f"Chart failed: {exc}"))
    return charts, flags

