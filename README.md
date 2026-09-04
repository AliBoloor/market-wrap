# Market Wrap

Status: **implemented and being expanded to four publications**. This repository
contains the deterministic data, chart, validation, and static-site layers used
by scheduled Codex research workflows.

The public publication has four sections:

- **Daily Market Wrap** — a closing report for each U.S. trading session: what
  happened, why it mattered, and what to watch in the next session.
- **Weekly Market Wrap** — published after the final U.S. session of the week
  (normally Friday, or Thursday when Friday is a market holiday), with a more
  macro-oriented review and week-ahead outlook.
- **Monthly Market Wrap** — a U.S. and global macro review covering the economy,
  earnings, growth, rates, policy, markets, and the month ahead.
- **Canadian Economy** — a monthly, educational macro and political review of
  Canada, ending with balanced further reading from public institutions and
  policy organizations across viewpoints.

Daily, weekly, and monthly Market Wraps include a concise global-markets section.
All publications distinguish observations from interpretation, carry direct
source links, expose stale or missing data, and use reproducible calculations
for their tables and charts.

## How it works

1. Scheduled Codex tasks research and write the publications using the user's
   ChatGPT allowance. Repository code never calls an LLM API and requires no
   OpenAI API key.
2. No-key public market history is saved with source, timestamp, scope, and
   failure metadata. Local Python tooling calculates technicals and charts.
3. Validation fails closed if required evidence or publication files are absent.
4. A push to `main` lets GitHub Actions build and deploy the public static site.

GitHub Actions performs no research and creates no narrative. The public site is
[aliboloor.github.io/market-wrap](https://aliboloor.github.io/market-wrap/).

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
[report specification](docs/report-spec.md), and the
[decision records](docs/decisions/) for the operating contract.

## Repository layout

```text
automation/             Scheduled-task prompts and operating instructions
content/reports/        Dated publication source files
data/                   Publication-safe source manifests and observations
docs/                   Plans, specifications, and architecture decisions
public/charts/          Dated chart images
market_wrap/            Deterministic calculations, validation, and site build
site/                   Generated static website (not hand-edited)
tests/                  Validation tests
```
