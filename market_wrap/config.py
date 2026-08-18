from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .models import Asset


@dataclass(frozen=True)
class ReportConfig:
    title: str = "Daily Pre-Market Wrap"
    output_dir: Path = Path("output")
    timezone: str = "America/New_York"
    lookback_days: int = 260
    news_lookback_hours: int = 24
    max_news_items: int = 12


@dataclass(frozen=True)
class ScheduleConfig:
    enabled: bool = True
    hour: int = 7
    minute: int = 0
    weekdays: str = "mon-fri"


@dataclass(frozen=True)
class AppConfig:
    report: ReportConfig
    schedule: ScheduleConfig
    assets: tuple[Asset, ...]
    news_feeds: tuple[dict[str, str], ...] = field(default_factory=tuple)
    calendar_events: tuple[dict[str, Any], ...] = field(default_factory=tuple)


def load_config(path: str | Path) -> AppConfig:
    path = Path(path).resolve()
    raw = yaml.safe_load(path.read_text()) or {}
    report_raw = raw.get("report", {})
    output = Path(report_raw.get("output_dir", "output"))
    if not output.is_absolute():
        output = path.parent / output
    report = ReportConfig(
        title=report_raw.get("title", "Daily Pre-Market Wrap"),
        output_dir=output,
        timezone=report_raw.get("timezone", "America/New_York"),
        lookback_days=int(report_raw.get("lookback_days", 260)),
        news_lookback_hours=int(report_raw.get("news_lookback_hours", 24)),
        max_news_items=int(report_raw.get("max_news_items", 12)),
    )
    schedule = ScheduleConfig(**raw.get("schedule", {}))
    assets = tuple(Asset(**item) for item in raw.get("assets", []))
    if not assets:
        raise ValueError("Configuration must contain at least one tracked asset")
    return AppConfig(
        report=report,
        schedule=schedule,
        assets=assets,
        news_feeds=tuple(raw.get("news_feeds", [])),
        calendar_events=tuple(raw.get("calendar_events", [])),
    )
