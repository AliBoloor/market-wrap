from pathlib import Path

import pytest

from market_wrap.site import SiteBuildError, build_site, discover_reports


def _report(path: Path, day: str, title: str, family: str = "daily") -> None:
    report_types = {
        "daily": "Daily Market Wrap",
        "weekly": "Weekly Market Wrap",
        "monthly": "Monthly Market Wrap",
        "canadian-economy": "Canadian Economy",
    }
    path.write_text(
        f"""---
trading_date: {day}
report_family: {family}
title: {title}
report_type: {report_types[family]}
generated_at: {day}T08:15:00-04:00
data_observed_at: {day}T08:10:00-04:00
freshness: Fresh
completeness: Complete
---
# Executive narrative

Markets are **mixed** before the open.

## Cross-asset snapshot

| Instrument | Move |
| --- | ---: |
| S&P 500 futures | +0.2% |
""",
        encoding="utf-8",
    )


def test_builds_latest_dated_pages_and_archive(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    daily = reports / "daily"
    daily.mkdir(parents=True)
    _report(daily / "2026-09-03.md", "2026-09-03", "Earlier report")
    _report(daily / "2026-09-04.md", "2026-09-04", "Latest report")

    output = tmp_path / "site"
    latest = build_site(reports, output)

    assert latest.slug == "2026-09-04"
    assert "Latest report" in (output / "index.html").read_text()
    assert "Latest report" in (output / "daily/index.html").read_text()
    assert "Earlier report" in (output / "daily/reports/2026-09-03/index.html").read_text()
    archive = (output / "daily/archive/index.html").read_text()
    assert archive.index("September 04, 2026") < archive.index("September 03, 2026")
    assert (output / "static/style.css").is_file()
    assert (output / ".nojekyll").is_file()
    for family in ("weekly", "monthly", "canadian-economy"):
        assert "not been published yet" in (output / family / "index.html").read_text()
        assert "No editions" in (output / family / "archive/index.html").read_text()


def test_builds_family_scoped_reports_on_same_date(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    for family, title in (("daily", "Daily edition"), ("weekly", "Weekly edition")):
        folder = reports / family
        folder.mkdir(parents=True)
        _report(folder / "2026-09-04.md", "2026-09-04", title, family)

    output = tmp_path / "site"
    build_site(reports, output)

    assert "Daily edition" in (output / "daily/reports/2026-09-04/index.html").read_text()
    assert "Weekly edition" in (output / "weekly/reports/2026-09-04/index.html").read_text()


def test_rejects_report_filename_that_disagrees_with_metadata(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    daily = reports / "daily"
    daily.mkdir(parents=True)
    _report(daily / "wrong-name.md", "2026-09-04", "Report")

    with pytest.raises(SiteBuildError, match="filename must match"):
        discover_reports(reports)


def test_failed_build_preserves_existing_site(tmp_path: Path) -> None:
    reports = tmp_path / "reports"
    daily = reports / "daily"
    daily.mkdir(parents=True)
    (daily / "2026-09-04.md").write_text("incomplete", encoding="utf-8")
    output = tmp_path / "site"
    output.mkdir()
    (output / "index.html").write_text("known-good", encoding="utf-8")

    with pytest.raises(SiteBuildError, match="missing YAML front matter"):
        build_site(reports, output)

    assert (output / "index.html").read_text() == "known-good"
