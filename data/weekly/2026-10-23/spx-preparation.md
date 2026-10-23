## SPX next-trading-session preparation

Conditional preparation only; no executable recommendation. SPX cash index (^GSPC), index points.
Observation/bar timestamp: 2026-10-23T13:30:00+00:00; retrieved: 2026-10-23T21:04:27.171000+00:00.
Daily bar timestamps identify the session, not necessarily its close time. Before use, verify the cash session is complete,
including early closes, against the official exchange calendar. [Saved data source](https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?range=2y&interval=1d&events=history).

| Level basis | Index points |
|---|---:|
| Completed-session high | 7660.15 |
| Completed-session low | 7612.07 |
| Completed-session close / gap reference | 7623.68 |
| 20-session high | 7844.52 |
| 20-session low | 7612.07 |
| SMA20 | 7727.48 |
| SMA50 | 7699.64 |
| SMA200 | 7291.31 |

Select support below and resistance above the fresh opening SPX from these observed levels;
cluster overlapping levels rather than treating every line as a separate signal. These are reference levels, not predicted turning points.

**Calendar/catalyst gate:** The next trading session is Monday, October 26, 2026; the [NYSE calendar](https://www.nyse.com/markets/hours-calendars) lists it as a regular session. The scheduled U.S. catalysts are the Dallas Fed Manufacturing Survey at 10:30 a.m. ET ([New York Fed calendar](https://www.newyorkfed.org/research/calendars/nationalecon_cal)) and Verizon results before the open with its call at 8:30 a.m. ET ([Verizon IR](https://www.verizon.com/about/news/verizon-earnings-3q-2026)). The larger week includes Treasury auctions Monday through Thursday ([Treasury schedule](https://treasurydirect.gov/auctions/upcoming/)), the October 27-28 FOMC meeting with Wednesday's statement at 2:00 p.m. and press conference at 2:30 p.m. ET ([Federal Reserve](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)), Microsoft Wednesday after the close ([Microsoft IR](https://www.microsoft.com/en-us/Investor/events/FY-2027/earnings-fy-2027-q1.aspx)), Amazon Thursday after the close ([Amazon IR](https://ir.aboutamazon.com/events/default.aspx)), Thursday GDP and PCE at 8:30 a.m. ET ([BEA](https://www.bea.gov/news/schedule)), and Friday ECI at 8:30 a.m. ET ([BLS](https://www.bls.gov/schedule/news_release/eci.htm)). Reassess after material releases.

| Opening scenario | Conditional behavior and confirmation | Invalidation / possible defined-risk structure |
|---|---|---|
| Gap down below 7623.68 | At 7612.07, wait for a touch, reclaim, five-minute close above, and a holding retest. A break below 7612.07 followed by a failed reclaim instead supports downside continuation. | Bullish case invalid on a five-minute close back below 7612.07; bearish case invalid on a reclaim and hold above it. Use a call or put debit spread only after the matching confirmation. |
| Gap up above 7623.68 | At 7660.15, rejection plus a five-minute close below and failed retest supports a fade. A five-minute breakout close above 7660.15 followed by a holding retest supports continuation toward the 7699.64-7727.48 moving-average cluster. | Fade invalid on reclaim and hold above 7660.15; continuation invalid on a close back below it. Use a directional debit spread only after confirmation. |
| Flat within 0.25% of 7623.68 | Inside Friday's 7612.07-7660.15 range, wait for a range-edge rejection or reclaim, or a five-minute range break and holding retest. Avoid the middle of the range. | Reversal invalid beyond the rejected edge; breakout invalid back inside the range. Staying flat is valid. |

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
