# Trade Ideas daily companion

Trade Ideas is a fifth site section, generated during the existing daily task;
there is no second scheduler. Daily retains SPX opening scenarios and its separate
0DTE feature. Expanded 1–7 DTE candidates belong in Trade Ideas. Weekly/monthly
retain technical context. The target is ten, never a minimum filled by guesses.

The existing architecture delegates research to scheduled Codex, not Python or
GitHub Actions. Python validates structured evidence and renders candidates;
it never invents candidates or calls a broker/database/LLM. New site sections
have a truthful empty state until a validated edition exists. No historical
archive report is rewritten or fabricated to populate the new tab.

Daily generation first resolves the actual completed and next U.S. sessions
using official exchange calendars (including holidays/early closes), researches
current data/catalysts, and collects OHLC for technical context. Candidates use
current-session observations and source links, with quote delay/staleness shown.
A next-open executable decision requires fresh opening prices and chains.
Do not use research PostgreSQL data. Reuse public daily inputs and fetch current
single-name data only when needed. No paid endpoint, credentials or broker.

## Evidence input

Save `data/trade-ideas/YYYY-MM-DD/ideas.json`, then run:

```
python -m market_wrap trade-ideas --input data/trade-ideas/YYYY-MM-DD/ideas.json --root .
```

This writes `content/reports/trade-ideas/YYYY-MM-DD.md`. To validate/publish under
the existing convention, create a standard manifest with family `trade-ideas`,
type `Trade Ideas`, direct evidence URLs, timestamps, series_files including
ideas.json and any quote/chain snapshots, warnings and validated state only
after checks. Create a `trade-ideas` completion marker independently of Daily.
`validate` rejects a report that differs from the rendered evidence. Both marker
checks are independent on retries; preserve valid Daily when its companion fails.

Bundle fields:

- `trading_date`, `next_session`: ISO dates; verified official `calendar_source`
  HTTPS URL and timezone-aware `generated_at`.
- `risk_caps`: read `config/trade-ideas.json`: USD 1,000 per SPX trade and USD 500
  per other ETF/single-name trade. Include fees when known; missing premium/fees
  means eligibility remains unconfirmed. Legacy `max_loss_cap` remains available
  as a display-only configurable field for fixtures, never risk certification.
- `social_coverage`: describe search date/scope, direct versus indexed access,
  search limitations and missing evidence. Ten posts are not mandatory.
- `candidates`: zero to ten unique candidates. If fewer, `shortfall_reason` is
  required. Expiry is 1–7 **calendar** days after next_session; confirm the
  actual listed expiration and product's last trading/settlement conventions.

Each candidate requires `id`, `symbol`, `instrument`, actual positive
`underlying_price`, timezone-aware `observed_at`, HTTPS `market_source`,
`thesis`, `level_basis`, `trigger`, `invalidation`, `no_trade`, `structure`,
ISO `expiry`, and `strike_status` (`illustrative` or `verified listed`).
Structure may explicitly suggest level-based strikes, but illustrative strikes
are hypotheses until listing/expiry is verified. Verified listed status also
requires `chain_source`, `chain_observed_at` and `contract_identifiers`.
The renderer checks metadata, not external truth: the researcher must inspect
and preserve source evidence. Same-session timing alone does not prove a final
close or a fresh option quote; preserve observation meaning, delay and interval.

Optional `outside_commentary` requires original `post_url`, `posted_at`,
`author`, `excerpt`, `quote_or_paraphrase`, `credibility`, `own_assessment`.
Link directly to the original post, distinguish outside opinion from own
analysis and quote faithfully. Independently validate price/level/contract
claims; follower count and self-reported wins are not a track record.
A `performance_claim` requires `independent_performance_source`; otherwise omit
any performance claim and say unverified. Public indexed sources are acceptable
with an explicit coverage limit; never fabricate inaccessible posts.

The schema deliberately rejects casual `premium`, `max_loss`, or
`cap_certified` fields. Exact loss analysis needs a separate sourced calculation
with contemporaneous bid/ask, fees, quantity, multiplier and contract width;
never certify a cap from absent premium or fee evidence. Debit vertical theoretical maximum loss is debit
× multiplier × quantity + costs; credit vertical is (width − credit) × multiplier
× quantity + costs. Verify currency, 0 < premium < width and liquidity. Do not
present indicative quotes as executable fills or a stop as guaranteed risk.

## Verification and activation

Run pytest, repository validation, build, inspect the new tab/archives and actual
candidate evidence, and preserve existing delivery. Proposed prompt changes are
local only; the operator must separately authorize updating the active existing
daily automation's prompt and publishing code. Do not create a new automation.

When the daily history endpoint lags, the daily research task may call
`market_wrap.pipeline.collect_current_quotes(root, session_date, instruments)`
for selected ETFs/single names. It saves current five-minute bars separately in
Trade Ideas evidence, rejects a stale New York observation date and returns
failures. Do not calculate “20-day SMA” from 20 five-minute bars or replace daily
history with intraday bars. Save returned failures in the companion bundle.
