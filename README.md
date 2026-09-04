# Market Wrap

Status: **implemented**. The repository contains the deterministic data, chart,
validation, and site layers used by the scheduled Codex research workflow.

The goal is a researched daily U.S. market wrap that:

- is written by a scheduled Codex task using the user's ChatGPT plan;
- requires no OpenAI API key and no paid data API key;
- is delivered inside ChatGPT;
- is saved as dated files in this repository;
- includes sourced narrative, technical analysis, and trustworthy charts; and
- is published as a public static website through GitHub Pages.

## How it works

1. A scheduled Codex task researches and writes one dated report using the
   user's ChatGPT allowance—there is no LLM API call or API key.
2. No-key public market history is saved alongside explicit source and failure
   metadata. The project calculates technicals and renders charts locally.
3. Validation fails closed if required evidence or files are absent.
4. A push to `main` lets GitHub Actions test and build the public static site.

The public site is [aliboloor.github.io/market-wrap](https://aliboloor.github.io/market-wrap/).

## Local setup

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest
python -m market_wrap validate --root .
python -m market_wrap build --root . --output site
```

Open `site/index.html` to inspect the generated version. See
[operations](docs/operations.md), [architecture](docs/architecture.md), the
[report specification](docs/report-spec.md), and the [decision records](docs/decisions/)
for the operating contract.

## Repository layout

```text
automation/             Scheduled-task prompt and operating instructions
content/reports/        Dated Markdown reports
data/                   Dated, publication-safe source manifests and observations
docs/                   Plans, specifications, and architecture decisions
public/charts/          Dated chart images
scripts/                Deterministic build and validation code
site/                   Generated static website (not hand-edited)
tests/                  Validation tests
```
