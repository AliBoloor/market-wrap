# Daily Market Wrap scheduled-task prompt

## Per-wake checkout refresh

On EVERY invocation, including heartbeat retries in a long-lived thread, read
this prompt and `.agents/skills/market-wrap/SKILL.md` from disk before using
cached instructions or completion guards. The scheduler's existing target and
recurrence stay unchanged.

Before publication work or completion checks, inspect Git status and fetch
`origin main`. Fast-forward with `git merge --ff-only origin/main` only when
tracked files are clean and incoming paths do not overlap untracked files.
Preserve unrelated files; do not stash, reset, clean, force, or overwrite them.
If synchronization fails or branches diverge, stop this publication attempt,
report the exact stage, and preserve the last valid publications. After a
successful fast-forward, re-read the updated skill, this prompt and referenced
contracts. A cached Daily-only completion guard must never bypass the companion.

Use the repository-scoped `$market-wrap` skill. This is an **after-close** publication only. Determine the current time and U.S. trading date in `America/New_York`. Stop before broad web research if the U.S. cash session has not closed, today is not a U.S. trading day, or the validated Daily completion marker already exists for today. Never publish a pre-market, intraday, or holiday placeholder as the Daily Market Wrap.

If today needs a report, inspect the public repository and read `docs/report-spec.md`, the source policy, and the relevant schema before editing. Do not disturb unrelated worktree changes. Research and write one evidence-backed **Daily Market Wrap** that answers two questions: what happened in today’s completed U.S. session and what matters for the next trading day.

Cover closing U.S. index and sector performance, breadth where trustworthy data exists, VIX, two- and ten-year Treasury yields, the dollar, material commodities, credit or volatility signals when relevant, and a concise global-markets passage. Explain the risk regime and distinguish observed facts from interpretation. Do not assert a causal driver without evidence; say when attribution is inconclusive.

For the next trading day, identify scheduled economic releases, central-bank appearances, earnings, policy developments, geopolitical risks, and other credible catalysts. Discuss technically relevant support, resistance, prior-session levels, gaps, swing points, and the 20-, 50-, and 200-day simple moving averages for the S&P 500, Nasdaq 100, and other instruments central to the session. Explain how levels were selected and avoid false precision. Keep the realized-volatility table to two columns—instrument and value—with the shared method in prose. For options, research reputable web commentary about what implied moves, skew, term structure, hedging demand, and event pricing suggest. Public X or other social posts are optional and must have verifiable authorship, date, data basis, and methodology. Do not derive a directional story from raw put/call or volume totals or present assumed dealer positioning as fact.

Create only useful charts from saved numerical inputs. Every chart must identify instrument, interval, units, source, and observation time and reconcile with its table. Distinguish cash indexes, futures, and ETFs. Omit unsupported material rather than estimate or fabricate it. State material staleness or coverage limitations prominently.

Save the report and evidence bundle using the repository's current paths and schema. The completion key is the New York trading date plus `daily`; never overwrite another report type. Record source URLs, publication/access times, observation times, instruments, units, transformations, and chart inputs. Treat every committed file and page as public: exclude secrets, credentials, cookies, accounts, private data, and absolute local paths.

Run the full tests, publication validation, and static-site build. Inspect the Daily page, navigation, archive, citations, tables, charts, report date, freshness labels, and tomorrow section. Create the completion marker only after all checks pass. Commit only intended artifacts and required generated indexes, reconcile remote work without force, push, and confirm GitHub Pages deployment.

On failure, preserve the last valid public site, leave the completion marker absent, and return the failed stage and smallest recovery action. This task uses the user's ChatGPT/Codex allowance and must not call an OpenAI API, another LLM API, or any service requiring an external API key.

Apply the SPX preparation and sector coverage contract in docs/report-spec.md.
Use actual ^GSPC data; lead next-session technical preparation with SPX while
retaining SPY/QQQ/IWM and XLV/XLK/XLF/XLE/XLI. Integrate and research-complete
spx-preparation.md, including official next-session calendar, macro catalyst
times/sources, three opening scenarios, confirmation, invalidation and no-trade
gates. Do not invent chains, strikes, premiums or probabilities.

## Separate Trade Ideas owner

Trade Ideas is owned exclusively by `automation/TRADE_IDEAS_NOON_TASK_PROMPT.md`
and its noon Pacific task. This closing task must never create, regenerate or
overwrite a Trade Ideas edition or its completion marker. Its completion guard
is Daily-only. Preserve Trade Ideas and all unrelated changes.
