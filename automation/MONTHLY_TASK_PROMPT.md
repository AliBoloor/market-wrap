# Monthly Market Wrap scheduled-task prompt

Use the repository-scoped `$market-wrap` skill. Determine the date and time in `America/New_York` and consult the official U.S. exchange calendar before broad research. Publish only after the final U.S. cash close of the calendar month. Stop if another U.S. trading session remains that month or its validated `monthly` marker exists.

Inspect `docs/report-spec.md`, the source policy, and current schema. Preserve unrelated worktree changes. Write one comprehensive **Monthly Market Wrap** explaining the completed month and next-month outlook. Synthesize the evidence; do not concatenate daily news.

Assess growth, labor, inflation, earnings expectations and revisions, monetary and fiscal policy, liquidity and financial conditions, rates and the yield curve, credit, currencies, commodities, volatility, equity valuations, sectors, factors, and breadth. Include a substantive global section covering major economies, policy divergence, geopolitical or trade developments, and cross-border consequences. Separate fact, consensus, inference, and scenario.

For next month, provide a dated calendar of high-impact releases, central-bank meetings, earnings themes, fiscal or policy deadlines, supply events, and credible geopolitical risks. Use upside, base, and downside scenarios with observable signposts. Discuss longer trend structure, support/resistance, swing points, and 20-, 50-, and 200-day averages for central instruments. Include returns, useful drawdowns, VIX, two- and ten-year yields, and realized volatility in scoped tables.

Use sourced charts sparingly. Generate each from saved numerical inputs, reconcile it to a table, and label instrument, interval, units, source, and latest observation. Never fabricate, mix incomparable series, or disguise stale/preliminary data.

Save the report and bundle using monthly U.S. conventions. Its identity is calendar month plus `monthly`; never overwrite another family. Record URLs, access times, observations, units, transformations, revisions, and chart inputs. All output is public; exclude secrets, credentials, cookies, accounts, private data, and absolute local paths.

Run all tests, validation, and the site build. Inspect the Monthly page, navigation, archive, citations, period/freshness labels, scenarios, and next-month calendar. Only then mark complete, commit intended artifacts and indexes, reconcile without force, push, and confirm Pages deployment.

On failure, preserve the valid site, leave the marker absent, and report the stage and recovery action. Use only ChatGPT/Codex allowance; never call an OpenAI API, another LLM API, or a service requiring an external API key.
