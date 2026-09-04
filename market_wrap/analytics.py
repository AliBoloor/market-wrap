"""Transparent technical calculations over recorded observations."""

from __future__ import annotations

from dataclasses import dataclass
from math import log, sqrt
from statistics import stdev

from .models import MarketSeries


@dataclass(frozen=True)
class TechnicalSnapshot:
    symbol: str
    latest_close: float
    prior_high: float | None
    prior_low: float | None
    prior_close: float | None
    recent_high_20d: float | None
    recent_low_20d: float | None
    return_1d_pct: float | None
    sma20: float | None
    sma50: float | None
    sma200: float | None
    distance_sma50_pct: float | None
    distance_sma200_pct: float | None
    sma50_direction: str
    sma200_direction: str
    trend_structure: str
    realized_vol_20d_pct: float | None


def simple_moving_average(values: list[float], window: int) -> list[float | None]:
    if window <= 0:
        raise ValueError("window must be positive")
    output: list[float | None] = [None] * len(values)
    rolling_sum = 0.0
    for index, value in enumerate(values):
        rolling_sum += value
        if index >= window:
            rolling_sum -= values[index - window]
        if index >= window - 1:
            output[index] = rolling_sum / window
    return output


def percent_change(current: float, prior: float) -> float:
    if prior == 0:
        raise ValueError("prior value cannot be zero")
    return (current / prior - 1.0) * 100.0


def realized_volatility(closes: list[float], window: int = 20, annualization: int = 252) -> float | None:
    if len(closes) < window + 1:
        return None
    if any(value <= 0 for value in closes[-(window + 1):]):
        return None
    returns = [log(closes[i] / closes[i - 1]) for i in range(len(closes) - window, len(closes))]
    return stdev(returns) * sqrt(annualization) * 100.0 if len(returns) >= 2 else None


def technical_snapshot(series: MarketSeries) -> TechnicalSnapshot:
    closes = [item.close for item in series.observations]
    if not closes:
        raise ValueError("cannot calculate technicals without observations")
    averages = {window: simple_moving_average(closes, window) for window in (20, 50, 200)}
    latest = closes[-1]
    prior = series.observations[-2] if len(closes) > 1 else None
    recent = series.observations[-20:]
    sma50, sma200 = averages[50][-1], averages[200][-1]

    def direction(window: int) -> str:
        values = averages[window]
        if len(values) < 6 or values[-1] is None or values[-6] is None:
            return "unavailable"
        if values[-1] > values[-6]:
            return "rising"
        if values[-1] < values[-6]:
            return "falling"
        return "flat"

    structure = "unavailable"
    if sma50 is not None and sma200 is not None:
        structure = "bullish" if latest > sma50 > sma200 else "bearish" if latest < sma50 < sma200 else "mixed"
    return TechnicalSnapshot(
        symbol=series.symbol, latest_close=latest,
        prior_high=prior.high if prior else None, prior_low=prior.low if prior else None,
        prior_close=prior.close if prior else None,
        recent_high_20d=max((item.high for item in recent), default=None),
        recent_low_20d=min((item.low for item in recent), default=None),
        return_1d_pct=percent_change(latest, prior.close) if prior else None,
        sma20=averages[20][-1], sma50=sma50, sma200=sma200,
        distance_sma50_pct=percent_change(latest, sma50) if sma50 else None,
        distance_sma200_pct=percent_change(latest, sma200) if sma200 else None,
        sma50_direction=direction(50), sma200_direction=direction(200),
        trend_structure=structure, realized_vol_20d_pct=realized_volatility(closes),
    )
