from __future__ import annotations

import argparse
import logging
import os
import shutil
from pathlib import Path

from .config import load_config
from .email_delivery import send_report_email
from .providers import YahooMarketDataProvider
from .report import generate_report
from .scheduler import run_scheduler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="market-wrap")
    parser.add_argument("--config", default="config.yaml", help="Path to YAML configuration")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run", help="Generate one report now")
    deliver_parser = subparsers.add_parser("deliver", help="Generate and email a report link")
    deliver_parser.add_argument("--url", required=True, help="Public URL of the report")
    subparsers.add_parser("schedule", help="Run the weekday scheduler in the foreground")
    init_parser = subparsers.add_parser("init", help="Create config.yaml from the example")
    init_parser.add_argument("--force", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    config_path = Path(args.config)
    if args.command == "init":
        if config_path.exists() and not args.force:
            raise SystemExit(f"{config_path} exists; use --force to replace it")
        source = Path(__file__).resolve().parent.parent / "config.example.yaml"
        shutil.copyfile(source, config_path)
        print(f"Created {config_path}")
        return
    config = load_config(config_path)
    provider = YahooMarketDataProvider()
    if args.command in {"run", "deliver"}:
        result = generate_report(config, provider)
        print(f"Report: {result.path}")
        print(f"Quality flags: {len(result.flags)}")
        if args.command == "deliver":
            send_report_email(result.path, args.url)
            print(f"Email sent to {os.environ['REPORT_EMAIL_TO']}")
    else:
        run_scheduler(config, provider)


if __name__ == "__main__":
    main()
