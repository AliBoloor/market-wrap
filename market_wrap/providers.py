from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

import feedparser
import pandas as pd
import yfinance as yf

from .models import Asset, CalendarEvent, MarketData, NewsItem, QualityFlag


class MarketDataProvider(ABC):
    """Boundary for future IBKR or Option Research adapters."""

    @abstractmethod
    def history(self, assets: tuple[Asset, ...], lookback_days: int) -> MarketData: ...


class YahooMarketDataProvider(MarketDataProvider):
    def history(self, assets: tuple[Asset, ...], lookback_days: int) -> MarketData:
        result = MarketData()
        symbols = list(dict.fromkeys(
            [a.symbol for a in assets] +
            [a.implied_vol_symbol for a in assets if a.implied_vol_symbol]
        ))
        period_days = max(lookback_days * 2, 60)
        try:
            raw = yf.download(
                symbols, period=f"{period_days}d", interval="1d", auto_adjust=False,
                group_by="ticker", progress=False, threads=True,
            )
        except Exception as exc:
            return MarketData(flags=[QualityFlag("error", "yahoo", f"Download failed: {exc}")])

        for symbol in symbols:
            try:
                frame = raw[symbol].copy() if len(symbols) > 1 else raw.copy()
                frame.columns = [str(c).lower().replace(" ", "_") for c in frame.columns]
                frame = frame.dropna(how="all").tail(lookback_days)
                if frame.empty or "close" not in frame:
                    raise ValueError("no closing-price history")
                result.prices[symbol] = frame
                age = pd.Timestamp.now(tz="UTC") - pd.Timestamp(frame.index[-1]).tz_localize("UTC")
                if age > pd.Timedelta(days=5):
                    result.flags.append(QualityFlag("warning", symbol, f"Last price is {age.days} days old"))
                if len(frame) < min(60, lookback_days // 2):
                    result.flags.append(QualityFlag("warning", symbol, f"Only {len(frame)} observations"))
            except Exception as exc:
                result.flags.append(QualityFlag("error", symbol, str(exc)))
        return result


class RssNewsProvider:
    def fetch(self, feeds: tuple[dict[str, str], ...], since: datetime, limit: int) -> tuple[list[NewsItem], list[QualityFlag]]:
        items: list[NewsItem] = []
        flags: list[QualityFlag] = []
        for feed in feeds:
            try:
                parsed = feedparser.parse(feed["url"])
                if getattr(parsed, "bozo", False) and not parsed.entries:
                    raise ValueError(str(getattr(parsed, "bozo_exception", "invalid feed")))
                for entry in parsed.entries:
                    published = None
                    value = entry.get("published") or entry.get("updated")
                    if value:
                        try:
                            published = parsedate_to_datetime(value)
                            if published.tzinfo is None:
                                published = published.replace(tzinfo=ZoneInfo("UTC"))
                        except (TypeError, ValueError):
                            pass
                    if published is None or published >= since:
                        items.append(NewsItem(published, feed["name"], entry.get("title", "Untitled"), entry.get("link", "")))
            except Exception as exc:
                flags.append(QualityFlag("warning", feed.get("name", "rss"), f"News unavailable: {exc}"))
        items.sort(key=lambda x: x.published or since, reverse=True)
        return items[:limit], flags


class ConfigCalendarProvider:
    def events(self, rows: tuple[dict, ...], timezone: str, now: datetime) -> tuple[list[CalendarEvent], list[QualityFlag]]:
        events: list[CalendarEvent] = []
        flags: list[QualityFlag] = []
        for row in rows:
            try:
                local_tz = ZoneInfo(row.get("timezone", timezone))
                when = datetime.fromisoformat(str(row["time"]))
                when = when.replace(tzinfo=local_tz) if when.tzinfo is None else when
                if now - timedelta(hours=2) <= when <= now + timedelta(days=7):
                    events.append(CalendarEvent(when, row["title"], row.get("importance", "normal")))
            except Exception as exc:
                flags.append(QualityFlag("warning", "calendar", f"Invalid event {row}: {exc}"))
        return sorted(events, key=lambda x: x.when), flags
