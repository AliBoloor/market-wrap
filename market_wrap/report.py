from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape

from .analytics import asset_summary, technical_levels, validate_market_data, volatility_summary
from .charts import create_technical_charts
from .config import AppConfig
from .models import QualityFlag, ReportResult
from .providers import ConfigCalendarProvider, MarketDataProvider, RssNewsProvider


def _html_table(frame: pd.DataFrame, percent_columns: set[str] | None = None) -> str:
    if frame.empty:
        return '<p class="muted">No data available.</p>'
    shown = frame.copy()
    percent_columns = percent_columns or set()
    for column in shown.columns:
        if column in percent_columns:
            shown[column] = shown[column].map(lambda x: "—" if pd.isna(x) else f"{x:.1%}")
        elif pd.api.types.is_numeric_dtype(shown[column]):
            shown[column] = shown[column].map(lambda x: "—" if pd.isna(x) else f"{x:,.2f}")
    return shown.to_html(index=False, border=0, classes="data-table", escape=True)


def generate_report(config: AppConfig, market_provider: MarketDataProvider) -> ReportResult:
    tz = ZoneInfo(config.report.timezone)
    now = datetime.now(tz)
    output_dir = config.report.output_dir / now.strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)

    market = market_provider.history(config.assets, config.report.lookback_days)
    flags: list[QualityFlag] = [*market.flags, *validate_market_data(config.assets, market)]
    news, news_flags = RssNewsProvider().fetch(
        config.news_feeds, now - timedelta(hours=config.report.news_lookback_hours), config.report.max_news_items
    )
    events, calendar_flags = ConfigCalendarProvider().events(config.calendar_events, config.report.timezone, now)
    charts, chart_flags = create_technical_charts(config.assets, market, output_dir)
    flags.extend(news_flags + calendar_flags + chart_flags)

    returns = asset_summary(config.assets, market)
    levels = technical_levels(config.assets, market)
    volatility = volatility_summary(config.assets, market)
    environment = Environment(loader=PackageLoader("market_wrap"), autoescape=select_autoescape())
    template = environment.get_template("report.html.j2")
    html = template.render(
        title=config.report.title,
        as_of=now,
        returns_table=_html_table(returns, {"1D", "5D", "1M", "3M", "YTD", "RV20", "RV60"}),
        levels_table=_html_table(levels),
        volatility_table=_html_table(volatility, {"RV20", "RV60", "IV Proxy", "IV-RV Spread"}),
        news=news,
        events=events,
        charts=charts,
        assets={a.symbol: a for a in config.assets},
        flags=flags,
    )
    path = output_dir / "market-wrap.html"
    path.write_text(html, encoding="utf-8")
    # A redirect keeps chart URLs correct because the full report remains beside its images.
    relative_report = f"{now:%Y-%m-%d}/market-wrap.html"
    redirect = (
        '<!doctype html><html><head><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={relative_report}">'
        f'<link rel="canonical" href="{relative_report}"></head>'
        f'<body><p><a href="{relative_report}">Open the latest Market Wrap</a></p></body></html>'
    )
    index = config.report.output_dir / "index.html"
    latest = config.report.output_dir / "latest.html"
    index.write_text(redirect, encoding="utf-8")
    latest.write_text(redirect, encoding="utf-8")
    return ReportResult(path=path, as_of=now, flags=flags, metadata={"latest": str(index)})
