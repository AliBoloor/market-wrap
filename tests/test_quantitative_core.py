from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from market_wrap.analytics import simple_moving_average, technical_snapshot
from market_wrap.charts import render_price_chart
from market_wrap.data import YahooChartClient
from market_wrap.models import EvidenceManifest, MarketSeries, Observation, SourceEvidence
from market_wrap.pipeline import clip_series_on_or_before
from market_wrap.validation import validate_manifest, validate_markdown_citations


def make_series(count: int = 210) -> MarketSeries:
    from datetime import timedelta
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    observations = tuple(
        Observation((start + timedelta(days=i)).isoformat(), i + 99, i + 101, i + 98, i + 100)
        for i in range(count)
    )
    return MarketSeries("S&P 500 ETF", "SPY", "1d", "USD", "Test", "https://example.com/data", start.isoformat(), observations)


def test_moving_average_and_snapshot_use_full_history() -> None:
    assert simple_moving_average([1, 2, 3, 4], 3) == [None, None, 2.0, 3.0]
    snapshot = technical_snapshot(make_series())
    assert snapshot.sma200 == pytest.approx(209.5)
    assert snapshot.sma50_direction == "rising"
    assert snapshot.trend_structure == "bullish"
    assert snapshot.prior_close == 308


def test_series_rejects_unsorted_observations() -> None:
    series = make_series(2)
    with pytest.raises(ValueError, match="sorted"):
        MarketSeries("Test", "T", "1d", "USD", "Test", "https://example.com", series.retrieved_at, tuple(reversed(series.observations)))


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None


def test_yahoo_client_skips_incomplete_rows() -> None:
    payload = {"chart": {"error": None, "result": [{
        "meta": {"currency": "USD"}, "timestamp": [1_700_000_000, 1_700_086_400],
        "indicators": {"quote": [{"open": [10, None], "high": [12, None], "low": [9, None], "close": [11, None], "volume": [100, None]}]},
    }]}}
    client = YahooChartClient(opener=lambda *_args, **_kwargs: FakeResponse(json.dumps(payload).encode()))
    series = client.history("SPY", "S&P 500 ETF")
    assert len(series.observations) == 1
    assert series.latest.close == 11


def test_validation_fails_closed(tmp_path: Path) -> None:
    now = datetime.now(timezone.utc)
    source = SourceEvidence("fed", "Federal Reserve", "https://federalreserve.gov", "Fed", now.isoformat(), ("calendar",))
    manifest = EvidenceManifest("1.0", now.date().isoformat(), "Daily Market Wrap", now.isoformat(), now.isoformat(), "validated", [source], ["data/series.json"], [], [])
    result = validate_manifest(manifest, tmp_path, expected_date=now.date().isoformat(), now=now)
    assert not result.valid
    assert "missing or empty file" in result.errors[0]
    citation_result = validate_markdown_citations("Generated today", manifest)
    assert not citation_result.valid


def test_price_chart_is_nonempty(tmp_path: Path) -> None:
    pytest.importorskip("matplotlib")
    chart = render_price_chart(make_series(), tmp_path / "spy.png")
    assert chart.stat().st_size > 1_000


def test_historical_bundle_series_stops_at_publication_date() -> None:
    from datetime import date

    series = make_series(3)
    clipped = clip_series_on_or_before(series, date(2025, 1, 2))

    assert clipped is not None
    assert len(clipped.observations) == 2
    assert clipped.latest.timestamp.startswith("2025-01-02")
