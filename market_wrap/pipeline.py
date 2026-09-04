"""Deterministic no-key market-data collection for a report bundle."""

from __future__ import annotations

import json
import re
from dataclasses import asdict
from datetime import date
from pathlib import Path

from .analytics import technical_snapshot
from .charts import render_price_chart, render_relative_chart
from .data import DataFailure, YahooChartClient
from .models import MarketSeries


DEFAULT_INSTRUMENTS = {
    "SPY": "S&P 500 ETF",
    "QQQ": "Nasdaq-100 ETF",
    "IWM": "Russell 2000 ETF",
    "TLT": "20+ Year Treasury Bond ETF",
    "^VIX": "CBOE Volatility Index",
    "^TNX": "10-Year Treasury Yield Index",
    "DX-Y.NYB": "U.S. Dollar Index",
    "GC=F": "Gold futures",
    "CL=F": "WTI crude futures",
    "BTC-USD": "Bitcoin / U.S. dollar",
}


def safe_symbol(symbol: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", symbol).strip("_")


def collect_bundle(root: Path, trading_date: date) -> tuple[dict[str, MarketSeries], list[DataFailure]]:
    """Collect history, calculations, and charts; preserve explicit failures."""
    series, failures = YahooChartClient().histories(DEFAULT_INSTRUMENTS, period="2y", interval="1d")
    data_dir = root / "data" / trading_date.isoformat()
    series_dir = data_dir / "series"
    chart_dir = root / "public" / "charts" / trading_date.isoformat()
    technicals: dict[str, object] = {}
    for symbol, item in series.items():
        item.write_json(series_dir / f"{safe_symbol(symbol)}.json")
        technicals[symbol] = asdict(technical_snapshot(item))
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "technicals.json").write_text(
        json.dumps(technicals, indent=2) + "\n", encoding="utf-8"
    )
    (data_dir / "failures.json").write_text(
        json.dumps([asdict(item) for item in failures], indent=2) + "\n", encoding="utf-8"
    )
    for symbol in ("SPY", "QQQ", "IWM"):
        if symbol in series:
            render_price_chart(series[symbol], chart_dir / f"{symbol}.png")
    if "SPY" in series and "TLT" in series:
        render_relative_chart(series["SPY"], series["TLT"], chart_dir / "SPY-vs-TLT.png")
    return series, failures
