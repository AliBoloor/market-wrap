"""Stable command-line interface used locally and by GitHub Pages."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .site import build_site
from .validation import load_manifest, validate_manifest, validate_markdown_citations


def _build(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    latest = build_site(
        root / "content" / "reports",
        root / args.output,
        charts_dir=root / "public" / "charts",
    )
    print(f"Built {args.output} with latest report {latest.slug}")
    return 0


def _validate(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    reports = sorted((root / "content" / "reports").glob("*.md"))
    if not reports:
        raise ValueError("no reports found")
    errors: list[str] = []
    warnings: list[str] = []
    today = datetime.now(timezone.utc).date().isoformat()
    for report_path in reports:
        trading_date = report_path.stem
        manifest_path = root / "data" / trading_date / "manifest.json"
        completion_path = root / "data" / trading_date / "complete.json"
        if not manifest_path.is_file():
            errors.append(f"{trading_date}: missing evidence manifest")
            continue
        if not completion_path.is_file():
            errors.append(f"{trading_date}: missing completion marker")
        else:
            marker = json.loads(completion_path.read_text(encoding="utf-8"))
            if marker.get("trading_date") != trading_date or marker.get("status") != "validated":
                errors.append(f"{trading_date}: invalid completion marker")
        manifest = load_manifest(manifest_path)
        # Historical archive entries remain valid; only today's publication has
        # an operational freshness deadline.
        maximum_age = timedelta(hours=24) if trading_date == today else timedelta(days=36500)
        result = validate_manifest(
            manifest, root, expected_date=trading_date, maximum_age=maximum_age
        )
        citations = validate_markdown_citations(
            report_path.read_text(encoding="utf-8"), manifest
        )
        errors.extend(f"{trading_date}: {item}" for item in result.errors + citations.errors)
        warnings.extend(f"{trading_date}: {item}" for item in result.warnings + citations.warnings)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        raise ValueError("\n".join(errors))
    print(f"Validated {len(reports)} report(s)")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Market Wrap publication tooling")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build", help="build the static site")
    build.add_argument("--root", type=Path, default=Path("."))
    build.add_argument("--output", type=Path, default=Path("site"))
    build.set_defaults(handler=_build)
    validate = subparsers.add_parser("validate", help="validate publication bundles")
    validate.add_argument("--root", type=Path, default=Path("."))
    validate.set_defaults(handler=_validate)
    return parser


def main() -> int:
    args = _parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
