"""Deterministic conditional SPX preparation; never selects executable contracts."""
from __future__ import annotations

from datetime import date
from .analytics import technical_snapshot
from .models import MarketSeries


def spx_preparation(series: MarketSeries | None, session: date) -> str:
    heading = '## SPX next-trading-session preparation\n\n'
    if (series is None or series.symbol != '^GSPC' or series.interval != '1d'
            or series.latest.timestamp[:10] != session.isoformat()):
        return heading + 'UNAVAILABLE: fresh daily SPX cash-index history for the completed session is missing. No numeric SPX levels or proxy substitutions.\n'
    t = technical_snapshot(series)
    levels = [('Completed-session high', t.session_high), ('Completed-session low', t.session_low),
              ('Completed-session close / gap reference', t.latest_close),
              ('20-session high', t.recent_high_20d), ('20-session low', t.recent_low_20d),
              ('SMA20', t.sma20), ('SMA50', t.sma50), ('SMA200', t.sma200)]
    table = '\n'.join(f'| {name} | {value:.2f} |' if value is not None else f'| {name} | unavailable |' for name, value in levels)
    return heading + f'''Conditional preparation only; no executable recommendation. SPX cash index (^GSPC), index points.
Observation/bar timestamp: {series.latest.timestamp}; retrieved: {series.retrieved_at}.
Daily bar timestamps identify the session, not necessarily its close time. Before use, verify the cash session is complete,
including early closes, against the official exchange calendar. [Saved data source]({series.source_url}).

| Level basis | Index points |
|---|---:|
{table}

Select support below and resistance above the fresh opening SPX from these observed levels;
cluster overlapping levels rather than treating every line as a separate signal. These are reference levels, not predicted turning points.

**Calendar/catalyst gate:** Next-session date is pending official calendar verification; never assume tomorrow or just skip weekends.
Research must resolve holidays, exceptional closures and early closes, and list scheduled macro releases,
Fed appearances, Treasury events and major earnings with dates, New York times and primary-source links.
Unknown or unverified calendar/catalysts means no trade-ready plan. Reassess after material releases.

| Opening scenario | Conditional behavior and confirmation | Invalidation / possible defined-risk structure |
|---|---|---|
| Gap down below completed close | At mapped support, wait for a touch, reclaim and a five-minute close above it, then a retest that holds. A break below support followed by a failed reclaim instead supports a downside continuation case. | Bullish case invalid on a five-minute close back below reclaimed support; consider a call debit spread only after confirmation. Bearish case invalid on a reclaim/hold above broken support; consider a put debit spread. |
| Gap up above completed close | At mapped resistance, rejection plus a five-minute close below and failed retest supports a fade. A five-minute breakout close above resistance followed by a holding retest supports continuation. | Fade invalid on reclaim/hold above resistance; possible put debit spread. Continuation invalid on close back below breakout level; possible call debit spread. |
| Flat near close / inside completed range | Flat tolerance must be explicitly set using fresh opening conditions; inside refers to the completed high/low and may overlap a small gap. Wait for range-edge rejection/reclaim, or a five-minute range break and holding retest. | Reversal invalid beyond rejected range edge; breakout invalid back inside range. Directional debit spread only after confirmation; staying flat is valid. |

**No trade:** mere touch without confirmation; conflicting signals; chop in the middle of the range;
gap beyond all mapped levels without a new intraday structure; stale/delayed index quotes; unknown catalysts;
imminent major release; absent/illiquid chain or excessive spread; insufficient time before expiration.
SPX has no directly traded volume or native traded VWAP. SPY volume/VWAP or ES futures volume/VWAP,
if separately sourced and timestamped, are labeled participation proxies, never SPX prices or SPX volume.

**SPX risk cap:** USD 1,000 maximum loss per trade including fees when known. Require quantity × multiplier × actual debit + all fees ≤ 1,000 for debit verticals; unknown premium/fees means eligibility is unconfirmed.

**0DTE gate:** Fresh opening SPX, actual same-day option chains, bid/ask, expiration and settlement type
are required before any strikes, premiums, widths or sizing can be evaluated. No probabilities are assigned.
For a same-expiry debit vertical, maximum theoretical loss is debit paid times the contract multiplier plus costs;
maximum theoretical gain is (width minus debit) times multiplier less costs. Confirm positive debit below width.
Credit verticals are an alternative only with confirmed rejection/hold and actual executable quotes;
maximum theoretical loss is (width minus credit) times multiplier plus costs. Stops do not guarantee fills.
Rapid gamma, time decay and slippage can consume the full defined risk. No naked options.
SPX options are cash settled and European exercise; verify AM versus PM settlement and last trading time
for the exact series. The cash close is not the AM special settlement value (SET).
[Cboe contract specifications](https://www.cboe.com/en/tradable-products/sp-500/spx-options/spx-specifications/).
'''
