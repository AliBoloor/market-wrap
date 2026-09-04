"""Build the public static site from validated Markdown reports.

The builder deliberately contains no research or LLM integration. It turns the
committed publication bundle into reproducible HTML suitable for GitHub Pages.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from string import Template
from typing import Any, Iterable, Mapping, Sequence

import markdown
import yaml


_FRONT_MATTER = re.compile(r"\A---\s*\n(?P<meta>.*?)\n---\s*\n(?P<body>.*)\Z", re.DOTALL)
_REQUIRED_METADATA = (
    "report_family",
    "trading_date",
    "title",
    "report_type",
    "generated_at",
    "data_observed_at",
    "freshness",
    "completeness",
)

REPORT_FAMILIES = {
    "daily": "Daily Wrap",
    "weekly": "Weekly Wrap",
    "monthly": "Monthly Wrap",
    "canadian-economy": "Canadian Economy",
}
REPORT_TYPES = {
    "daily": "Daily Market Wrap",
    "weekly": "Weekly Market Wrap",
    "monthly": "Monthly Market Wrap",
    "canadian-economy": "Canadian Economy",
}


class SiteBuildError(ValueError):
    """Raised when publication input cannot produce a trustworthy site."""


@dataclass(frozen=True)
class Report:
    source: Path
    metadata: Mapping[str, Any]
    body_markdown: str

    @property
    def trading_date(self) -> date:
        value = self.metadata["trading_date"]
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return date.fromisoformat(str(value))

    @property
    def slug(self) -> str:
        return self.trading_date.isoformat()

    @property
    def family(self) -> str:
        return str(self.metadata["report_family"])


def load_report(path: Path) -> Report:
    """Read one report and validate the metadata needed for navigation."""
    text = path.read_text(encoding="utf-8")
    match = _FRONT_MATTER.match(text)
    if not match:
        raise SiteBuildError(f"{path}: missing YAML front matter")

    raw_metadata = yaml.safe_load(match.group("meta"))
    if not isinstance(raw_metadata, dict):
        raise SiteBuildError(f"{path}: front matter must be a mapping")
    missing = [key for key in _REQUIRED_METADATA if raw_metadata.get(key) in (None, "")]
    if missing:
        raise SiteBuildError(f"{path}: missing metadata: {', '.join(missing)}")

    try:
        trading_date = raw_metadata["trading_date"]
        parsed_date = (
            trading_date.date()
            if isinstance(trading_date, datetime)
            else trading_date
            if isinstance(trading_date, date)
            else date.fromisoformat(str(trading_date))
        )
    except (TypeError, ValueError) as exc:
        raise SiteBuildError(f"{path}: trading_date must be ISO YYYY-MM-DD") from exc
    if path.stem != parsed_date.isoformat():
        raise SiteBuildError(
            f"{path}: filename must match trading_date {parsed_date.isoformat()}"
        )
    family = str(raw_metadata["report_family"])
    if family not in REPORT_FAMILIES:
        raise SiteBuildError(f"{path}: unsupported report_family {family!r}")
    if path.parent.name != family:
        raise SiteBuildError(f"{path}: parent directory must match report_family {family}")
    expected_type = REPORT_TYPES[family]
    if str(raw_metadata["report_type"]) != expected_type:
        raise SiteBuildError(
            f"{path}: report_type must be {expected_type!r} for family {family!r}"
        )
    return Report(path, raw_metadata, match.group("body").strip())


def discover_reports(reports_dir: Path) -> list[Report]:
    reports = [load_report(path) for path in sorted(reports_dir.glob("*/*.md"))]
    slugs = [(report.family, report.slug) for report in reports]
    if len(slugs) != len(set(slugs)):
        raise SiteBuildError("duplicate report family/date pairs")
    return sorted(reports, key=lambda report: report.trading_date, reverse=True)


def _read_template(templates_dir: Path, name: str) -> Template:
    try:
        return Template((templates_dir / name).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SiteBuildError(f"missing template: {templates_dir / name}") from exc


def _render_markdown(value: str) -> str:
    return markdown.markdown(
        value,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )


def _report_article(report: Report, template: Template) -> str:
    metadata = report.metadata
    freshness = str(metadata["freshness"])
    completeness = str(metadata["completeness"])
    return template.substitute(
        title=html.escape(str(metadata["title"])),
        trading_date=html.escape(report.slug),
        report_type=html.escape(str(metadata["report_type"])),
        generated_at=html.escape(str(metadata["generated_at"])),
        data_observed_at=html.escape(str(metadata["data_observed_at"])),
        freshness=html.escape(freshness),
        freshness_class=_css_token(freshness),
        completeness=html.escape(completeness),
        completeness_class=_css_token(completeness),
        family_archive_path=f"/market-wrap/{report.family}/archive/",
        report_body=_render_markdown(report.body_markdown),
    )


def _css_token(value: str) -> str:
    token = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return token or "unknown"


def _page(base: Template, *, title: str, content: str, canonical_path: str) -> str:
    return base.substitute(
        page_title=html.escape(title),
        canonical_path=html.escape(canonical_path, quote=True),
        content=content,
    )


def _archive_list(reports: Iterable[Report], family: str) -> str:
    items = []
    for report in reports:
        metadata = report.metadata
        items.append(
            '<li><a href="../reports/{slug}/">{date}</a>'
            '<span>{kind} · {title}</span></li>'.format(
                slug=report.slug,
                date=html.escape(report.trading_date.strftime("%B %d, %Y")),
                kind=html.escape(str(metadata["report_type"])),
                title=html.escape(str(metadata["title"])),
            )
        )
    return "\n".join(items)


def _empty_family(label: str) -> str:
    slug = next(key for key, value in REPORT_FAMILIES.items() if value == label)
    return (
        '<section class="archive empty-state"><p class="eyebrow">Coming soon</p>'
        f'<h1>{html.escape(label)}</h1>'
        '<p>The first validated edition has not been published yet. '
        'It will appear here automatically after publication.</p>'
        f'<p><a href="/market-wrap/{slug}/archive/">View archive</a></p></section>'
    )


def build_site(
    reports_dir: Path,
    output_dir: Path,
    *,
    templates_dir: Path | None = None,
    static_dir: Path | None = None,
    charts_dir: Path | None = None,
) -> Report:
    """Build latest, dated report, and archive pages; return latest report."""
    package_root = Path(__file__).resolve().parent
    templates_dir = templates_dir or package_root / "templates"
    static_dir = static_dir or package_root / "static"
    reports = discover_reports(reports_dir)
    grouped = {
        family: [report for report in reports if report.family == family]
        for family in REPORT_FAMILIES
    }
    if not grouped["daily"]:
        raise SiteBuildError("at least one daily report is required")
    latest = grouped["daily"][0]

    staging = output_dir.with_name(f".{output_dir.name}.staging")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    base = _read_template(templates_dir, "base.html")
    report_template = _read_template(templates_dir, "report.html")
    archive_template = _read_template(templates_dir, "archive.html")

    for family, label in REPORT_FAMILIES.items():
        family_reports = grouped[family]
        family_root = staging / family
        family_root.mkdir(parents=True)
        for report in family_reports:
            article = _report_article(report, report_template)
            destination = family_root / "reports" / report.slug
            destination.mkdir(parents=True)
            (destination / "index.html").write_text(
                _page(
                    base,
                    title=str(report.metadata["title"]),
                    content=article,
                    canonical_path=f"{family}/reports/{report.slug}/",
                ),
                encoding="utf-8",
            )

        if family_reports:
            newest = family_reports[0]
            family_content = _report_article(newest, report_template)
            family_title = str(newest.metadata["title"])
        else:
            family_content = _empty_family(label)
            family_title = label
        (family_root / "index.html").write_text(
            _page(base, title=family_title, content=family_content, canonical_path=f"{family}/"),
            encoding="utf-8",
        )

        archive_destination = family_root / "archive"
        archive_destination.mkdir()
        archive_content = archive_template.substitute(
            archive_title=f"{label} archive",
            archive_description=f"Every validated {label.lower()} remains available with its original timestamps.",
            report_items=_archive_list(family_reports, family),
            empty_message=("" if family_reports else "<p>No editions have been published yet.</p>"),
        )
        (archive_destination / "index.html").write_text(
            _page(base, title=f"{label} archive", content=archive_content, canonical_path=f"{family}/archive/"),
            encoding="utf-8",
        )

    latest_article = _report_article(latest, report_template)
    (staging / "index.html").write_text(
        _page(base, title=str(latest.metadata["title"]), content=latest_article, canonical_path=""),
        encoding="utf-8",
    )

    if static_dir.exists():
        shutil.copytree(static_dir, staging / "static")
    if charts_dir and charts_dir.exists():
        shutil.copytree(charts_dir, staging / "charts")
    (staging / ".nojekyll").touch()

    if output_dir.exists():
        shutil.rmtree(output_dir)
    staging.replace(output_dir)
    return latest


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the Market Wrap static site")
    parser.add_argument("--reports", type=Path, default=Path("content/reports"))
    parser.add_argument("--output", type=Path, default=Path("site"))
    parser.add_argument("--charts", type=Path, default=Path("public/charts"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    latest = build_site(args.reports, args.output, charts_dir=args.charts)
    print(f"Built {args.output} with latest report {latest.slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
