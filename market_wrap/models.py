"""Typed publication models and their JSON representation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Literal


ReportFamily = Literal["daily", "weekly", "monthly", "canadian-economy"]
REPORT_FAMILIES = frozenset({"daily", "weekly", "monthly", "canadian-economy"})
ReportType = Literal[
    "Daily Market Wrap",
    "Weekly Market Wrap",
    "Monthly Market Wrap",
    "Canadian Economy",
]
PublicationState = Literal["draft", "validated", "published", "failed"]


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include a timezone: {value}")
    return parsed


@dataclass(frozen=True)
class Observation:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None

    def __post_init__(self) -> None:
        _parse_time(self.timestamp)
        scale = max(abs(self.open), abs(self.high), abs(self.low), abs(self.close), 1.0)
        tolerance = scale * 1e-7
        if self.high + tolerance < max(self.open, self.close, self.low):
            raise ValueError("high is below another OHLC value")
        if self.low - tolerance > min(self.open, self.close, self.high):
            raise ValueError("low is above another OHLC value")


@dataclass(frozen=True)
class MarketSeries:
    instrument: str
    symbol: str
    interval: str
    currency: str
    source_name: str
    source_url: str
    retrieved_at: str
    observations: tuple[Observation, ...]

    def __post_init__(self) -> None:
        _parse_time(self.retrieved_at)
        if not self.instrument or not self.symbol or not self.source_url.startswith("http"):
            raise ValueError("series requires instrument, symbol, and HTTP source URL")
        times = [item.timestamp for item in self.observations]
        if times != sorted(times) or len(times) != len(set(times)):
            raise ValueError("observations must be sorted and unique")

    @property
    def latest(self) -> Observation:
        if not self.observations:
            raise ValueError(f"{self.symbol} has no observations")
        return self.observations[-1]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")
        return path


@dataclass(frozen=True)
class SourceEvidence:
    source_id: str
    title: str
    url: str
    publisher: str
    accessed_at: str
    supports: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _parse_time(self.accessed_at)
        if not self.source_id or not self.url.startswith("http"):
            raise ValueError("evidence requires a source_id and HTTP URL")


@dataclass
class EvidenceManifest:
    schema_version: str
    trading_date: str
    report_type: ReportType
    generated_at: str
    market_data_as_of: str
    state: PublicationState = "draft"
    sources: list[SourceEvidence] = field(default_factory=list)
    series_files: list[str] = field(default_factory=list)
    chart_files: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    report_family: ReportFamily = "daily"

    def __post_init__(self) -> None:
        datetime.fromisoformat(self.trading_date)
        _parse_time(self.generated_at)
        _parse_time(self.market_data_as_of)
        if self.report_family not in REPORT_FAMILIES:
            raise ValueError(f"unsupported report family: {self.report_family}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def write_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")
        return path

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "EvidenceManifest":
        data = dict(value)
        data["sources"] = [SourceEvidence(**item) for item in data.get("sources", [])]
        return cls(**data)
