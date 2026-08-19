# Market Wrap

Phase 1 is a runnable pre-market report pipeline. It downloads daily cross-asset history, calculates returns and technical levels, estimates realized volatility, adds configured implied-volatility proxies, collects RSS headlines and calendar events, renders charts, records data-quality exceptions, and produces a self-contained HTML report.

The default source is Yahoo Finance. It is convenient for an initial personal workflow, but is not an exchange-grade feed. Provider interfaces isolate ingestion so an IBKR adapter and the Option Research codebase can be added later.

## Quick start

Python 3.11 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
market-wrap --config config.yaml init
market-wrap --config config.yaml run
```

Open `output/latest.html`. A dated copy and its chart images are stored under `output/YYYY-MM-DD/`.

## Public page

The included GitHub Actions workflow generates and publishes the report to GitHub Pages at 07:00 New York time each weekday. The latest report is available at <https://aliboloor.github.io/market-wrap/>. The workflow can also be run manually from the repository's Actions page.

Network or provider failures do not silently disappear: available sections still render and the Data Quality section identifies missing, stale, suspicious, or failed inputs. A complete market-data outage still produces a report shell.

## Configure assets and events

Edit `config.yaml`. Each asset has a Yahoo symbol, display name, and group. `implied_vol_symbol` is optional; for example, SPY uses `^VIX` as a broad proxy. These proxies are shown separately and should not be interpreted as exact option-chain IV.

Economic events can be listed under `calendar_events`. Times without an explicit offset use the event `timezone`, or the report timezone if omitted. RSS feeds are configured under `news_feeds`; feed availability varies, and failures are flagged.

## Daily scheduling

The built-in scheduler runs in the foreground and uses the report timezone:

```bash
market-wrap --config config.yaml schedule
```

By default it generates the report at 07:00 America/New_York on weekdays. Keep this process alive with your normal service manager (launchd on macOS, systemd on Linux, or a container). Alternatively, use cron or a platform scheduler to invoke `market-wrap --config /absolute/path/config.yaml run` daily. The process logs failures and prevents overlapping jobs.

## Architecture and extension points

- `providers.py`: source adapters. Implement `MarketDataProvider` for IBKR or internal data.
- `analytics.py`: returns, technical levels, and volatility calculations.
- `charts.py`: static report charts.
- `report.py` and `templates/`: orchestration and HTML rendering.
- `scheduler.py`: timezone-aware weekday execution.
- `models.py`: shared typed domain objects; useful as the integration contract.

For an Option Research integration, add an adapter that returns option-chain IV/skew/term-structure outputs, then pass those results into the report context. For IBKR, implement `MarketDataProvider.history` using `ib_insync` or the official API and select it in the CLI. Neither dependency is coupled to the Phase 1 pipeline.

## Validation

```bash
python -m pip install -e '.[dev]'
pytest
ruff check market_wrap tests
```

This project is informational and does not provide investment advice.
