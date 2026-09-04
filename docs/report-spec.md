# Daily report specification

## Required metadata

- Trading date
- Report type: `Pre-market`, `Intraday update`, or `Market holiday`
- Generation time and timezone
- Latest market-data observation time
- Freshness and completeness status
- Source links

## Required sections

### 1. Executive narrative

Three to five concise paragraphs covering the overnight setup, strongest supported market drivers, consequences of recent events, and the current risk regime. Observations and interpretation must be distinguishable.

### 2. Cross-asset snapshot

When reliable values are available, include U.S. equity futures or equivalent liquid proxies, Treasury yields, the dollar, oil, gold, bitcoin, volatility, and meaningful sector leaders and laggards. Every value requires an instrument label, timestamp, and source.

### 3. Catalyst calendar

Include material economic releases, central-bank events, Treasury events, major earnings, and geopolitical or corporate catalysts for the current day and next two trading days. Times must be displayed in New York time.

### 4. Technical setup

For the S&P 500, Nasdaq 100, and other instruments central to that day's setup, include when supported:

- 20-, 50-, and 200-day simple moving averages;
- percentage distance from the 50- and 200-day averages;
- moving-average direction and 50/200-day trend structure;
- prior-session high, low, and close;
- overnight or opening gap;
- recent swing highs and lows;
- nearby support and resistance; and
- the most important levels for the session.

The report must explain how important levels were selected, avoid false precision, and distinguish futures, cash indexes, and ETFs.

### 5. Charts

Include two to four charts only when reliable observations are available:

1. S&P 500 or liquid proxy, six to twelve months, with 20/50/200-day averages.
2. Nasdaq 100 or liquid proxy with the same averages.
3. One or two relationships relevant to the day's market, such as equities versus yields, VIX, dollar, oil, gold, or breadth.

Each chart requires a title, instrument, interval, axes with units, readable legend, source, latest observation time, and agreement with the report's stated figures. Missing data must result in a table or omission, never interpolation disguised as observation.

### 6. Risks and scenarios

List the developments most capable of changing the current interpretation and state what evidence would invalidate the reported risk regime.

### 7. Sources

Provide direct links near claims and a compact source list. Prefer primary sources for scheduled events and official data. Use reputable reporting for breaking context. Do not assert causation from timing alone.

## Publication states

- `draft`: research or validation incomplete; never published.
- `validated`: all required checks pass; eligible for commit.
- `published`: pushed and confirmed on GitHub Pages.
- `failed`: preserve the last valid public report and record the reason locally.

