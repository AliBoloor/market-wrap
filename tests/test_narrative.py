from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd

from market_wrap.models import CalendarEvent, NewsItem
from market_wrap.narrative import build_market_narrative


def test_narrative_uses_market_calendar_and_news() -> None:
    now = datetime(2026, 8, 18, 7, tzinfo=ZoneInfo("America/New_York"))
    returns = pd.DataFrame([
        {"Group": "Equities", "Asset": "S&P 500", "1D": 0.01},
        {"Group": "Equities", "Asset": "Nasdaq 100", "1D": -0.005},
    ])
    levels = pd.DataFrame([
        {"Asset": "S&P 500", "Last": 110, "50D MA": 105, "200D MA": 100},
        {"Asset": "Nasdaq 100", "Last": 95, "50D MA": 100, "200D MA": 98},
    ])
    volatility = pd.DataFrame([
        {"Asset": "S&P 500", "RV20": 0.15, "IV Proxy": 0.20, "IV-RV Spread": 0.05}
    ])
    events = [CalendarEvent(now + timedelta(days=2), "FOMC decision", "high")]
    news = [NewsItem(now, "Wire", "Markets await policy decision", "https://example.com")]
    paragraphs = build_market_narrative(returns, levels, volatility, events, news, now)
    joined = " ".join(paragraphs)
    assert "FOMC decision" in joined
    assert "Markets await policy decision" in joined
    assert "50-day" in joined
