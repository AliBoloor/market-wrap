# Weekly Market Wrap scheduled-task prompt

Use the repository-scoped `$market-wrap` skill. Determine the date and time in `America/New_York`, then check the official U.S. exchange calendar before broad research. Publish only after the final U.S. cash close of the week: normally Friday, or Thursday only when Friday is a confirmed full-day U.S. market holiday. Stop if the week is not complete or its validated `weekly` completion marker exists.

Inspect `docs/report-spec.md`, the source policy, and current schema. Preserve unrelated worktree changes. Write one evidence-backed **Weekly Market Wrap** covering the completed week and next-week outlook. It must be more macro-oriented than the daily report.

Explain U.S. equity, rates, credit, currency, commodity, volatility, factor, sector, and breadth trends where reliable data exists. Include a meaningful global-markets section. Identify supported drivers, changes in growth/inflation/policy expectations, sentiment signals, and what the cross-asset mix implies about risk appetite. Separate observation from interpretation and say when attribution is inconclusive.

For next week, provide a calendar of official releases, central-bank decisions and speakers, major earnings, material Treasury supply, policy deadlines, and credible geopolitical catalysts. Use scenarios rather than unsupported point forecasts. Discuss weekly and daily support/resistance, swing points, trend structure, and 20-, 50-, and 200-day simple moving averages for central instruments. Present weekly returns and realized volatility in tables and include VIX and two- and ten-year yields with units and timestamps.

Use charts only from saved, sourced observations. Reconcile each figure to its table and label instrument, interval, units, source, and latest observation. Never fabricate observations or blur cash indexes, futures, and ETFs. Flag stale, partial, revised, or non-comparable data.

Save the report and evidence bundle using the schema's weekly conventions. Use its canonical week-ending identity plus `weekly`; never overwrite another family. Record URLs, access times, observations, units, transformations, and chart inputs. All output is public; exclude secrets, credentials, cookies, accounts, private data, and absolute local paths.

Run all tests, validation, and the site build. Inspect the Weekly page, navigation, archive, tables, charts, citations, week-ending label, freshness, and next-week section. Only then create the marker, commit intended artifacts and required indexes, reconcile without force, push, and confirm Pages deployment.

On failure, preserve the last valid site, leave the marker absent, and report the failed stage and recovery action. Use only ChatGPT/Codex allowance; never call an OpenAI API, another LLM API, or a service requiring an external API key.
