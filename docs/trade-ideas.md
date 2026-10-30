# Trade Ideas — technical short iron condors

Current policy version 4: fixed universe SPX, QQQ, IWM, TLT, GLD; only short
credit iron condor level sets. Each ticker has one wide horizontal block with
three rows: next trading session, one week and one month. Explain calendar
boundaries and trading-session counts. Use distinct horizon-appropriate support
and resistance, not copied daily bounds. The user selects expiries; remove expiry
selection/verification as a recommendation gate. Technical horizons are not
selected option expirations. Desired technical strikes are not verified contracts.

## Legs and visual contract

One standard 100-multiplier package. Short put at/below technical support, short
call at/above resistance, both bracketing actual spot. BUY put five points below
short put; BUY call five points above short call. Both wings exactly five points
for every ticker and horizon. Display bold SHORT/LONG CALL/PUT actions and all
four strike prices. Adjacent spot-centered schematic has four dashed strike
lines, all labeled axis ticks, and a distinct spot line/marker. Wide on desktop,
stacked legible on mobile. Do not choose naked options, vertical alternatives,
debit or long condors. One concise shared caveat replaces repeated warnings.

The schematic is intrinsic shape before unknown credit/fees; credit shifts it
vertically. It is not next-day, week or month mark-to-market P&L. Remaining time,
IV and actual premiums determine pre-expiry P&L. No invented max profit or exact
breakeven. For one intact five-point package, expiry loss=500-100C+F, with C net
credit in points and F actual all-in USD costs. Meeting the $500 entry requirement
needs 0<C<5 and 100C>=F. Unknown inputs mean conditional eligibility, not a
guaranteed account-loss cap. ETF assignment/pin/after-hours residual-stock risk,
complete-package execution and exact contract/deliverable/settlement checks
remain shared caveats. No broker orders or naked legging.

## Research and timing

The recurring research start/cutoff is 15:00 America/New_York on verified U.S.
trading days, independent of the closing Daily publication. Bind the native
schedule to New York's IANA timezone; don't assume Vancouver or a fixed UTC
offset tracks Eastern DST. Preserve 15:00 on early-close dates and label actual
market state. Actual research/deployment may finish later; never backdate them.

Use month/recent-session and today's up-to-cutoff OHLC, longer averages, confirmed
swings, support/resistance confluence, and transparent secondary methods. Record
all numerical inputs and observation/retrieval meanings. Never mix partial
intraday bars with completed daily averages or use future closing values. Gamma
sign/flip requires a credible provider source, methodology, scope and timestamp;
label assumed dealer sides/model limitations. Otherwise state unavailable; open
interest alone cannot establish dealer inventory or gamma sign.

First authorized policy-4 edition is the completed October 29 close for October
30/day, November 5/week and nominal November 29/month (last exchange session
November 27). Explicitly distinguish the first-run 16:00 close baseline from
recurring 15:00 intraday editions. Earlier noon evidence is retained under
`data/trade-ideas/2026-10-29/revisions/noon/`; other dated editions remain intact.
Legacy policy rendering is for preserved archives only.

## Evidence and implementation

Version 4 bundle: trading_date, next_session, research_cutoff, generated_at,
data_observed_at, publication_mode (close-initial or eastern-1500), calendar_source,
calendar_verified, risk_cap_usd:500, horizons, tickers, research, methods, sources,
limitations. Horizons have id, label, start, end, trading_sessions. Exactly five
ordered ticker blocks carry symbol, actual spot, source/retrieved_at, trend,
gamma_note and three levels. Each level has horizon, short_put, long_put,
short_call, long_call, support, resistance, basis, upside, downside and range.
No expiry, premium, max_profit or breakeven in a level. `condor.py` validates
bounds, widths, universe, cutoff and distinct horizons, then renders the blocks.
Existing CLI, manifests, family/date markers and Pages builder remain in use.

Reuse existing automation ID `trade-ideas-noon-pacific` when reconciling the
15:00 Eastern task; never create another duplicate. Native registration remains
unconfirmed: the automation API requires a local thread, and Codex UI access was
denied. A saved ACTIVE TOML is not evidence of registration/dispatch. Closing
Daily owns only Daily and cannot overwrite Trade Ideas. Independent date/family
markers plus the existing atomic publication lock prevent repeated/racing work.
