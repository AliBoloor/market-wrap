from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class Asset:
    symbol: str
    name: str
    group: str
    implied_vol_symbol: str | None = None


@dataclass(frozen=True)
class QualityFlag:
    severity: str
    source: str
    message: str


@dataclass
class MarketData:
    prices: dict[str, pd.DataFrame] = field(default_factory=dict)
    flags: list[QualityFlag] = field(default_factory=list)


@dataclass(frozen=True)
class NewsItem:
    published: datetime | None
    source: str
    title: str
    link: str


@dataclass(frozen=True)
class CalendarEvent:
    when: datetime
    title: str
    importance: str = "normal"


@dataclass
class ReportResult:
    path: Path
    as_of: datetime
    flags: list[QualityFlag]
    metadata: dict[str, Any] = field(default_factory=dict)

