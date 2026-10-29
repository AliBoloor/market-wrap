# Trade Ideas: next-session defined-risk research

The existing Daily research run also publishes Trade Ideas after the completed
U.S. cash session, targeting the next verified exchange session. Reuse its
scheduler, evidence bundle, independent companion marker and static Pages
pipeline. GitHub Actions performs no research. A sleeping Mac, inaccessible
sources or failed research can delay publication; do not promise fresh content.

## Policy version 2

Only three families: call vertical, put vertical, iron condor. Both debit/credit
variations are permitted. All positions, including SPX, have a USD 500 maximum
loss including actual all-in fees. Never naked options; no broker orders.
Core coverage is SPX, QQQ and IWM. Add GLD/TLT or selected sector ETFs only when
current evidence improves the thesis. No single-name expansion or count quota.
At most six alternatives; fewer or no setups is acceptable.

Technical context leads: completed-session OHLC, recent 3–5 sessions and weekly
range, swing levels and supported 20/50/200-session averages. State observations,
source/retrieval times and vendor conflicts; five-minute bars are not daily SMA
inputs. Research next-session official macro times, issuer earnings, news,
public X commentary and cross-asset confirmation. Record inaccessible sources;
never invent posts, positioning, option premiums or implied-volatility views.
Distinguish closing baseline from timestamped post-close developments.

Direction and conditional volatility view select the family. Expansion favors
debit directionals or a long iron condor after a two-sided move thesis;
contraction/range favors credit directionals or a short iron condor after
rejection/range confirmation. Give entry confirmation, invalidation and a
no-trade/alternative case. A stop is not a guaranteed maximum loss.

## Evidence and deterministic rendering

Save `data/trade-ideas/YYYY-MM-DD/ideas.json` with `policy_version: 2`,
`trading_date`, `next_session`, timezone-aware `generated_at` and
`data_observed_at`, `calendar_source`, `risk_caps` (USD, spx:500, other:500),
`research`, `social_coverage`, `sources` and `candidates`.
Each candidate has id, permitted symbol, direction, volatility_view, level_basis,
trigger, invalidation, alternative, expiry, listing_source, listing_status,
listing_note and model. Model has family, kind, strictly increasing strikes,
positive integer quantity and standard multiplier 100. Two strikes describe a
vertical; four describe equal condor wings. All legs use the stated expiry.

A short iron condor buys outer put/call wings and sells inner put/call for a
credit. A long iron condor reverses all four legs for a debit. Put wing must
lie below call wing. Distinguish desired strike/expiry from actually verified
listed contracts. Actual verification requires current source, observation time
and exact contract identifiers. 0DTE is permitted only for an actual listed
same-session expiry; unavailable or inaccessible ETF 0DTE is explicitly labeled.
A generic product schedule alone does not verify exact strikes.

Unknown premiums/fees remain UNKNOWN. Charts show signed intrinsic payoff only;
net P&L and breakevens are parametric. D/C are debit/credit in points/share,
q positive integer quantity, m=100 and F actual all-position USD costs.
Debit loss=q*m*D+F; credit loss=q*m*(wing width-C)+F. Require loss<=500,
0<premium<width and F<500; no trade until listing, fill, fees and liquidity are
checked. Equal-wing condors use the same bounds. Debit gain=q*m*(width-D)-F;
credit gain=q*m*C-F. Large fees can eliminate breakevens. Do not present
hypothetical values as quotes or certify risk from absent premium evidence.
ETF American/physical assignment and pin risk can create exposure outside the
paired-leg expiry model. SPXW European/cash settlement requires explicit PM
series/last-trading verification; standard AM SPX differs.

Run `python -m market_wrap trade-ideas --input <ideas.json> --root .`, then
pytest, publication validation and build. Preserve existing wrap and other
editions. Legacy policy rendering remains solely for unchanged archived bundles;
new generation must read version 2 config. This policy supersedes prior
SPX $1,000, ten-candidate, 1–7DTE and vertical-only companion requirements.
