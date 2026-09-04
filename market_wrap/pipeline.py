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

CANADIAN_INSTRUMENTS = {
    "^GSPTSE": "S&P/TSX Composite Index",
    "CAD=X": "USD/CAD exchange rate (CAD per USD)",
    "CL=F": "WTI crude futures",
    "GC=F": "Gold futures",
    "RY": "Royal Bank of Canada",
    "TD": "Toronto-Dominion Bank",
    "ENB": "Enbridge",
    "CNI": "Canadian National Railway",
}


def safe_symbol(symbol: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", symbol).strip("_")


def clip_series_on_or_before(item: MarketSeries, cutoff: date) -> MarketSeries | None:
    """Return a series bounded to a publication date, or None when empty."""
    observations = tuple(
        observation
        for observation in item.observations
        if observation.timestamp[:10] <= cutoff.isoformat()
    )
    if not observations:
        return None
    return MarketSeries(
        instrument=item.instrument,
        symbol=item.symbol,
        interval=item.interval,
        currency=item.currency,
        source_name=item.source_name,
        source_url=item.source_url,
        retrieved_at=item.retrieved_at,
        observations=observations,
    )


def collect_bundle(
    root: Path,
    trading_date: date,
    *,
    report_family: str = "daily",
) -> tuple[dict[str, MarketSeries], list[DataFailure]]:
    """Collect history, calculations, and charts; preserve explicit failures."""
    if report_family not in {"daily", "weekly", "monthly", "canadian-economy"}:
        raise ValueError(f"unsupported report family: {report_family}")
    instruments = CANADIAN_INSTRUMENTS if report_family == "canadian-economy" else DEFAULT_INSTRUMENTS
    fetched, failures = YahooChartClient().histories(instruments, period="2y", interval="1d")
    series: dict[str, MarketSeries] = {}
    for symbol, item in fetched.items():
        clipped = clip_series_on_or_before(item, trading_date)
        if clipped is None:
            failures.append(
                DataFailure(
                    symbol=symbol,
                    source=item.source_name,
                    reason=f"no observations on or before {trading_date.isoformat()}",
                )
            )
            continue
        series[symbol] = clipped
    data_dir = root / "data" / report_family / trading_date.isoformat()
    series_dir = data_dir / "series"
    chart_dir = root / "public" / "charts" / report_family / trading_date.isoformat()
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
    if report_family == "canadian-economy":
        for symbol in ("^GSPTSE", "CAD=X"):
            if symbol in series:
                render_price_chart(series[symbol], chart_dir / f"{safe_symbol(symbol)}.png")
    return series, failures
