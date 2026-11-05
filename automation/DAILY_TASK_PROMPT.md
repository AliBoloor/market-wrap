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
contracts. The closing guard is Daily-only; Trade Ideas has its separate 15:00 Eastern owner.

## Delivery recovery before research/completion guards

A validated Daily completion marker proves content validation, NOT Pages delivery.
On EVERY wake, after safe checkout refresh and before calendar/duplicate exits,
run `python -m market_wrap publication-status --root . --family daily`.
This is delivery verification, not new market research. Exit code 0/state published
means BOTH latest and dated routes expose the exact validated source SHA-256.
Exit code 2/state deployment_pending means recovery is still needed; HTTP 200,
a validated marker, a pushed commit or a successful build alone is insufficient.
A missing identity on an older deployed page is unconfirmed delivery, not success.

For deployment_pending: preserve and reuse the existing validated bundle. Do NOT
research, rewrite the report, delete its content marker or change Trade Ideas.
Inspect the Pages workflow for the current safely synchronized origin/main SHA.
If queued/in progress, follow that run instead of launching a duplicate. If its
build passed and deploy failed, retry ONLY its failed jobs using
`gh run rerun <run-id> --repo AliBoloor/market-wrap --failed`, at most once per
invocation. If no current-SHA workflow exists, dispatch the existing pages.yml
workflow once for main. Never re-run an old report SHA over a newer main commit.
If build failed, report the actual failed stage; do not blindly redeploy.

Wait for the selected run and verify publication-status again. If deployment is
still pending/failed, notify with exact run URL/stage, preserve the bundle and
leave delivery unconfirmed so the next wake retries recovery. A validated marker
must NEVER turn a failed deployment into a DONT_NOTIFY duplicate skip. Do not
add a committed deployment receipt that would create another push/deploy cycle.
Recovery may run before today's close or on a later date for the latest validated
Daily; it never creates a pre-close report or silently backfills research.

Use the repository-scoped `$market-wrap` skill. This is an **after-close** publication only. Determine the current time and U.S. trading date in `America/New_York`. Stop before broad web research if the U.S. cash session has not closed, today is not a U.S. trading day, or (after delivery verification/recovery) the validated Daily completion marker already exists for today. Never publish a pre-market, intraday, or holiday placeholder as the Daily Market Wrap.

If today needs a report, inspect the public repository and read `docs/report-spec.md`, the source policy, and the relevant schema before editing. Do not disturb unrelated worktree changes. Research and write one evidence-backed **Daily Market Wrap** that answers two questions: what happened in today’s completed U.S. session and what matters for the next trading day.

Cover closing U.S. index and sector performance, breadth where trustworthy data exists, VIX, two- and ten-year Treasury yields, the dollar, material commodities, credit or volatility signals when relevant, and a concise global-markets passage. Explain the risk regime and distinguish observed facts from interpretation. Do not assert a causal driver without evidence; say when attribution is inconclusive.

For the next trading day, identify scheduled economic releases, central-bank appearances, earnings, policy developments, geopolitical risks, and other credible catalysts. Discuss technically relevant support, resistance, prior-session levels, gaps, swing points, and the 20-, 50-, and 200-day simple moving averages for the S&P 500, Nasdaq 100, and other instruments central to the session. Explain how levels were selected and avoid false precision. Keep the realized-volatility table to two columns—instrument and value—with the shared method in prose. For options, research reputable web commentary about what implied moves, skew, term structure, hedging demand, and event pricing suggest. Public X or other social posts are optional and must have verifiable authorship, date, data basis, and methodology. Do not derive a directional story from raw put/call or volume totals or present assumed dealer positioning as fact.

Create only useful charts from saved numerical inputs. Every chart must identify instrument, interval, units, source, and observation time and reconcile with its table. Distinguish cash indexes, futures, and ETFs. Omit unsupported material rather than estimate or fabricate it. State material staleness or coverage limitations prominently.

Save the report and evidence bundle using the repository's current paths and schema. The completion key is the New York trading date plus `daily`; never overwrite another report type. Record source URLs, publication/access times, observation times, instruments, units, transformations, and chart inputs. Treat every committed file and page as public: exclude secrets, credentials, cookies, accounts, private data, and absolute local paths.

Run the full tests, publication validation, and static-site build. Inspect the Daily page, navigation, archive, citations, tables, charts, report date, freshness labels, and tomorrow section. Create the completion marker only after all checks pass. Commit only intended artifacts and required generated indexes, reconcile remote work without force, push, and confirm GitHub Pages deployment.

On research/validation failure, preserve the last valid public site and leave the content marker absent. On push/deployment failure after validation, retain the validated bundle/marker but treat delivery as pending and run the recovery branch on later wakes. Return the actual failed stage and run URL. This task uses the user's ChatGPT/Codex allowance and must not call an OpenAI API, another LLM API, or any service requiring an external API key.

Apply the SPX preparation and sector coverage contract in docs/report-spec.md.
Use actual ^GSPC data; lead next-session technical preparation with SPX while
retaining SPY/QQQ/IWM and XLV/XLK/XLF/XLE/XLI. Integrate and research-complete
spx-preparation.md, including official next-session calendar, macro catalyst
times/sources, three opening scenarios, confirmation, invalidation and no-trade
gates. Do not invent chains, strikes, premiums or probabilities.

## Separate Trade Ideas owner

Trade Ideas is owned exclusively by `automation/TRADE_IDEAS_1500_TASK_PROMPT.md`
and its 15:00 New York task. This closing task must never create, regenerate or
overwrite a Trade Ideas edition or its completion marker. Its completion guard
is Daily-only. Preserve Trade Ideas and all unrelated changes.
