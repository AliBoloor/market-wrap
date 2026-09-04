"""Fail-closed validation for a candidate publication bundle."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .models import EvidenceManifest


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    def require_valid(self) -> None:
        if self.errors:
            raise ValueError("publication validation failed: " + "; ".join(self.errors))


def load_manifest(path: Path) -> EvidenceManifest:
    return EvidenceManifest.from_dict(json.loads(path.read_text(encoding="utf-8")))


def validate_manifest(
    manifest: EvidenceManifest,
    repository: Path,
    *,
    expected_date: str | None = None,
    expected_family: str | None = None,
    now: datetime | None = None,
    maximum_age: timedelta = timedelta(hours=18),
) -> ValidationResult:
    result = ValidationResult()
    if manifest.schema_version != "1.0":
        result.errors.append(f"unsupported evidence schema: {manifest.schema_version}")
    if expected_date and manifest.trading_date != expected_date:
        result.errors.append(f"trading date {manifest.trading_date} does not match {expected_date}")
    if expected_family and manifest.report_family != expected_family:
        result.errors.append(
            f"report family {manifest.report_family} does not match {expected_family}"
        )
    generated = datetime.fromisoformat(manifest.generated_at.replace("Z", "+00:00"))
    reference = now or datetime.now(timezone.utc)
    if generated > reference + timedelta(minutes=5):
        result.errors.append("generation time is in the future")
    if reference - generated > maximum_age:
        result.errors.append("report is stale")
    if manifest.state not in ("validated", "published"):
        result.errors.append(f"publication state is {manifest.state}")
    if not manifest.sources:
        result.errors.append("manifest has no sources")
    source_ids = [source.source_id for source in manifest.sources]
    if len(source_ids) != len(set(source_ids)):
        result.errors.append("source IDs are not unique")
    for relative in manifest.series_files + manifest.chart_files:
        path = (repository / relative).resolve()
        try:
            path.relative_to(repository.resolve())
        except ValueError:
            result.errors.append(f"file escapes repository: {relative}")
            continue
        if not path.is_file() or path.stat().st_size == 0:
            result.errors.append(f"missing or empty file: {relative}")
    unsupported = [warning for warning in manifest.warnings if warning.startswith("CRITICAL:")]
    if unsupported:
        result.errors.extend(unsupported)
    return result


def validate_markdown_citations(markdown: str, manifest: EvidenceManifest) -> ValidationResult:
    result = ValidationResult()
    if not markdown.strip():
        result.errors.append("report markdown is empty")
        return result
    for source in manifest.sources:
        if source.supports and source.url not in markdown:
            result.errors.append(f"cited evidence missing from report: {source.source_id}")
    if "Generated" not in markdown and "generated_at" not in markdown:
        result.warnings.append("report does not visibly label generation time")
    return result
