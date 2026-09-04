"""No-key public market-data retrieval.

The Yahoo chart endpoint is used because it provides timestamped OHLC history
without credentials. Retrieval failures are returned explicitly; no prices are
estimated or silently substituted.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable
from urllib.parse import quote
from urllib.request import Request, urlopen

from .models import MarketSeries, Observation


YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


@dataclass(frozen=True)
class DataFailure:
    symbol: str
    source: str
    reason: str


class YahooChartClient:
    def __init__(self, opener: Callable[..., object] = urlopen, timeout: float = 20.0):
        self.opener = opener
        self.timeout = timeout

    def history(
        self,
        symbol: str,
        instrument: str,
        *,
        period: str = "1y",
        interval: str = "1d",
        currency: str = "USD",
    ) -> MarketSeries:
        base_url = YAHOO_CHART_URL.format(symbol=quote(symbol, safe=""))
        url = f"{base_url}?range={quote(period)}&interval={quote(interval)}&events=history"
        request = Request(url, headers={"User-Agent": "market-wrap/1.0"})
        with self.opener(request, timeout=self.timeout) as response:  # type: ignore[attr-defined]
            payload = json.loads(response.read())
        error = payload.get("chart", {}).get("error")
        results = payload.get("chart", {}).get("result")
        if error or not results:
            raise RuntimeError(f"Yahoo returned no data for {symbol}: {error}")
        result = results[0]
        quote_data = result.get("indicators", {}).get("quote", [{}])[0]
        timestamps = result.get("timestamp", [])
        observations: list[Observation] = []
        for index, epoch in enumerate(timestamps):
            values = {key: quote_data.get(key, [None] * len(timestamps))[index] for key in ("open", "high", "low", "close")}
            if any(value is None for value in values.values()):
                continue
            observations.append(
                Observation(
                    timestamp=datetime.fromtimestamp(epoch, tz=timezone.utc).isoformat(),
                    open=float(values["open"]), high=float(values["high"]),
                    low=float(values["low"]), close=float(values["close"]),
                    volume=_optional_number(quote_data.get("volume", []), index),
                )
            )
        if not observations:
            raise RuntimeError(f"Yahoo returned no complete OHLC observations for {symbol}")
        metadata = result.get("meta", {})
        return MarketSeries(
            instrument=instrument, symbol=symbol, interval=interval,
            currency=metadata.get("currency") or currency,
            source_name="Yahoo Finance chart data", source_url=url,
            retrieved_at=datetime.now(timezone.utc).isoformat(),
            observations=tuple(observations),
        )

    def histories(self, instruments: dict[str, str], **kwargs: str) -> tuple[dict[str, MarketSeries], list[DataFailure]]:
        series: dict[str, MarketSeries] = {}
        failures: list[DataFailure] = []
        for symbol, name in instruments.items():
            try:
                series[symbol] = self.history(symbol, name, **kwargs)
            except Exception as exc:  # isolate a failed public endpoint/instrument
                failures.append(DataFailure(symbol, "Yahoo Finance chart data", str(exc)))
        return series, failures


def _optional_number(values: list[float | None], index: int) -> float | None:
    if index >= len(values) or values[index] is None:
        return None
    return float(values[index])
