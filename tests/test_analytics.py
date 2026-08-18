import numpy as np
import pandas as pd

from market_wrap.analytics import asset_summary, moving_average, technical_levels, volatility_summary
from market_wrap.models import Asset, MarketData


def sample_data() -> MarketData:
    index = pd.bdate_range("2025-01-02", periods=260)
    prices = pd.DataFrame({"close": 100 * np.exp(np.arange(260) * 0.001)}, index=index)
    vix = pd.DataFrame({"close": np.full(260, 20.0)}, index=index)
    return MarketData(prices={"TEST": prices, "^VIX": vix})


def test_summary_returns_and_volatility() -> None:
    assets = (Asset("TEST", "Test Asset", "Test", "^VIX"),)
    summary = asset_summary(assets, sample_data()).iloc[0]
    assert summary["1D"] > 0
    assert summary["YTD"] > 0
    vol = volatility_summary(assets, sample_data()).iloc[0]
    assert vol["IV Proxy"] == 0.2


def test_technical_levels() -> None:
    assets = (Asset("TEST", "Test Asset", "Test"),)
    levels = technical_levels(assets, sample_data()).iloc[0]
    assert levels["20D Low"] <= levels["Last"] <= levels["20D High"]
    assert levels["20D MA"] > levels["50D MA"]
    close = sample_data().prices["TEST"]["close"]
    assert levels["200D MA"] == moving_average(close, 200).iloc[-1]
