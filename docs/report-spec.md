# Publication specification

## Common editorial and evidence contract

Every publication must include its name and coverage period, generation time and
timezone, latest observation time, freshness/completeness and material failure
flags, an answer-first narrative, outlook, risks, and direct source links.
Separate observed facts, attributed explanations, and Codex's interpretation.

Prefer primary sources for official releases, policy, schedules, filings, and
company announcements. Use reputable financial reporting for timely context.
Never infer causation from timing alone, invent missing observations, or hide a
stale-data limitation. Treat cash indexes, ETFs, futures, yields, contracts,
shares, volume, and open interest as distinct measures. Every chart must state
its title, instrument, interval, axes, units, source, and latest observation time
and must agree with the accompanying table.

## Daily Market Wrap

### Cadence and purpose

Publish after each completed regular U.S. trading session. This is always a
**closing report**, never an opening or mid-session edition. Explain what happened
in the completed session and what investors should watch in the next U.S.
trading session. Do not create a Daily Market Wrap on a U.S. market holiday
unless the editorial task explicitly calls for a dated holiday note.

### Required sections

1. **Closing assessment** — price action, breadth and leadership, supported
   drivers, rates and cross-asset confirmation, consequences of recent news, and
   the closing risk-on/risk-off or mixed regime.
2. **Closing dashboard** — major U.S. equity indexes or liquid proxies, VIX,
   two- and ten-year Treasury yields, dollar, oil, gold, bitcoin, and meaningful
   sector leaders/laggards, with close/change, instrument, units, timestamp, and
   source.
3. **Global markets** — a few lines on material developments in Europe, Asia,
   emerging markets, currencies, commodities, or sovereign rates and their
   relevance to the U.S. session.
4. **Options and volatility** — realized volatility in a standalone two-column
   table containing only instrument and realized-volatility value; state the
   shared lookback and annualization method in adjacent prose. Synthesize what
   reputable derivatives commentary says option prices imply about expected
   movement, skew, term structure, hedging demand, or event risk. Prefer Cboe,
   established brokers and transparent specialist research. Public X or other
   social commentary may add color only when author, date, data basis and
   methodology are verifiable. Do not calculate a directional story from raw
   put/call or venue-volume totals, assume dealer positioning, or compare
   options contracts with equity shares as equivalent units.
5. **What mattered today** — releases, central-bank developments, Treasury
   activity, major earnings, corporate events, and geopolitics that mattered.
6. **Tomorrow's setup** — scheduled economic, central-bank, Treasury, major
   earnings, geopolitical, and corporate catalysts for the next trading day.
   Display times in New York time.
7. **Technical map for tomorrow** — for the S&P 500, Nasdaq 100, and other
   central instruments, discuss support, resistance, prior high/low/close,
   recent swing levels, and 20/50/200-day simple moving averages where supported.
   Include distance from the 50- and 200-day averages, explain level selection,
   avoid false precision, and keep indexes, futures, and ETFs distinct.
8. **Tomorrow scenarios** — concise conditional base, upside, and downside
   cases tied to observable catalysts or technical confirmation.
9. **Charts and sources** — normally two to four decision-useful charts,
   followed by direct source links.

## Weekly Market Wrap

### Cadence and purpose

Publish after the final U.S. regular session of each week: normally Friday
close, or Thursday close when Friday is a U.S. market holiday. Otherwise use the
actual last U.S. session. Cover the completed week and the next week. Do not
publish twice for the same week-ending trading date.

### Required sections

1. **Week in review** — dominant narrative, turning points, market regime,
   breadth, factor/sector leadership, and cross-asset confirmation.
2. **Weekly scorecard** — U.S. equities, VIX, two- and ten-year yields and curve,
   dollar, credit when available, oil, gold, bitcoin, styles, and sectors using
   consistent week-over-week comparisons.
3. **Global week** — material equity, rates, currency, commodity, policy, and
   geopolitical developments across major regions.
4. **Macro and earnings pulse** — what the week's data, policy communication,
   and company results changed about growth, inflation, earnings, and rates.
5. **Technical and positioning map** — weekly trend, 20/50/200-day structures,
   support/resistance, volatility, participation, and well-sourced positioning
   or options measures when available.
6. **Week ahead** — key releases, central-bank and Treasury events, major
   earnings, political/geopolitical risks, and dates in New York time.
7. **Next-week scenarios** — conditional base/upside/downside paths, confirming
   levels or evidence, and invalidation conditions.

## Monthly Market Wrap

### Cadence and purpose

Publish after the final U.S. trading session of each calendar month. Review the
completed month and frame the next month, prioritizing durable trends over daily
noise.

### Required sections

1. **Macro thesis and regime** — the central conclusion and changes in growth,
   inflation, liquidity, financial conditions, and risk appetite.
2. **U.S. economy** — activity, labor, consumer, housing, inflation, financial
   conditions, and expansion/recession evidence, including revisions and gaps.
3. **Rates and policy** — Federal Reserve expectations, Treasury curve, fiscal
   and Treasury developments, credit, and major policy risks.
4. **Earnings and valuation** — aggregate earnings, revisions, margins,
   guidance, breadth, and valuation without overstating incomplete evidence.
5. **Markets and technical regime** — monthly asset/sector performance,
   participation, volatility, and long-horizon trend/technical levels.
6. **Global markets and economy** — major developed/emerging economies, central
   banks, currencies, commodities, and global risk transmission.
7. **Month ahead** — releases, central-bank meetings, earnings themes,
   political/geopolitical events, technical levels, and conditional scenarios.

## Canadian Economy

### Cadence and purpose

Publish after the final Canadian trading session of the calendar month as a
comprehensive educational review of Canada's economy and outlook. This is not a daily stock recap. Market
prices and selected companies appear only when they illuminate a macro, sector,
financial-stability, trade, or policy trend.

### Required sections

1. **Executive thesis** — the central Canadian macro story, what changed, and
   the most important implications.
2. **Growth and demand** — GDP/nowcast evidence, consumption, investment,
   productivity, inventories, and regional/sector differences.
3. **Households, housing, and labor** — employment, wages, population where
   relevant, household leverage, mortgage resets, housing, affordability, and
   consumer stress.
4. **Inflation, rates, and financial conditions** — CPI measures, Bank of Canada
   policy, yield curve, credit, currency, and policy transmission.
5. **Fiscal, trade, resources, and industry** — federal/provincial fiscal themes,
   U.S./global trade exposure, energy/resources, industry, and competitiveness.
6. **Politics and policy** — material federal and provincial developments,
   described neutrally with facts separate from analysis and competing views
   represented fairly.
7. **Market signals** — TSX/sub-index trends, CAD, yields, commodities, and a
   small number of economically important companies only when they add insight.
8. **Outlook and scenarios** — next-month and medium-term expectations with
   base/upside/downside conditions and explicit risks.
9. **Policy reading** — annotated direct links to timely work from the Bank of
   Canada, Statistics Canada, Finance Canada or other governments, commercial
   bank economists, business/labour organizations, and reputable think tanks
   spanning market-oriented/conservative, centrist/institutional, and
   progressive/liberal perspectives. Label publisher and institutional role or
   viewpoint; inclusion is educational, not endorsement. Prefer substantive
   original pieces over homepages.

## Publication states

- `draft`: research or validation incomplete; never published.
- `validated`: all required checks pass; eligible for commit.
- `published`: pushed and confirmed on GitHub Pages.
- `failed`: preserve the last valid publication and record the reason locally.

## SPX preparation and sector coverage (U.S. publications)

SPX cash index (`^GSPC` from Yahoo; no SPY scaling) is the primary technical
preparation instrument. Retain SPY, QQQ and IWM as separate ETF contexts.
Include XLV and XLK; add XLF, XLE and XLI for financial/credit sensitivity,
energy/inflation and industrial/cyclical breadth. This compact sector selection
complements technology and defensive health care without an eleven-sector dump.
Use actual observations and explain any missing coverage. Weekly and monthly
retain their macro horizons but include a concise next-session SPX preparation
box alongside their longer-horizon outlook. Canadian Economy is unchanged.

Use `data/<family>/<date>/spx-preparation.md` as a deterministic starting section,
not a finished report. Lead the daily outlook with this section. The level map
uses the just-completed session high/low/close (not the penultimate bar) and
20-session extremes/SMA20/50/200. Explain level clustering and distance from
SMA50/200 using `technicals.json`. The collector omits stale instruments and
records failures; no SPY fallback for SPX. A current date on an intraday Yahoo
bar does not prove a final close: collection remains strictly after confirmed
cash close. Record actual retrieval and observation timestamps and quote delay.

Research must replace the calendar/catalyst gate with the verified next session
and dated primary-source calendar evidence, including intervening holidays,
weekends, early closes and exceptional closures. Include scheduled releases in
New York time, their sources and material uncertainty. Never infer “no events”
from a failed calendar lookup. Keep a no-trade gate when unresolved.
Retain all three opening scenarios, confirmations, invalidations and no-trade
cases. No invented strikes, premia, probabilities or chain data. These are
conditional educational plans; execution requires fresh opening SPX and actual
same-day chains. Identify exact expiration/AM or PM settlement; SPX close is
not SET. SPX has no traded volume; separately label any SPY/ES volume/VWAP proxy.

## Trade Ideas

See [Trade Ideas evidence contract](trade-ideas.md). Daily retains its primary
SPX next-session technical scenarios and separate 0DTE feature. Expanded trade
candidates go into the companion tab, targeting ten supported 1–7 DTE ideas
across indices/ETFs/single names, with fewer shown when current evidence is
insufficient. Illustrative level-based strikes are explicitly labeled and never
represented as verified listed contracts or executable quotes. Maximum-loss cap
amount/currency remain unset until clarified. Do not certify a cap from missing
premiums/fees. Attribute X commentary and distinguish it from own analysis.
