from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from market_wrap.config import AppConfig, ReportConfig, ScheduleConfig
from market_wrap.models import Asset, MarketData
from market_wrap.providers import MarketDataProvider
from market_wrap.report import generate_report


class FakeProvider(MarketDataProvider):
    def history(self, assets: tuple[Asset, ...], lookback_days: int) -> MarketData:
        index = pd.bdate_range(end=datetime.now(ZoneInfo("UTC")).date(), periods=260)
        frame = pd.DataFrame({"close": 100 + np.arange(260, dtype=float)}, index=index)
        return MarketData(prices={assets[0].symbol: frame})


def test_report_and_latest_redirect(tmp_path: Path) -> None:
    config = AppConfig(
        report=ReportConfig(output_dir=tmp_path, timezone="UTC"),
        schedule=ScheduleConfig(),
        assets=(Asset("TEST", "Test", "Test"),),
    )
    result = generate_report(config, FakeProvider())
    assert result.path.exists()
    index = tmp_path / "index.html"
    assert index.exists()
    assert f"{result.as_of:%Y-%m-%d}/market-wrap.html" in index.read_text()
