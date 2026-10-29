# Trade Ideas — noon Pacific, next-session owner

On EVERY invocation reread this file, the repository skill, docs/trade-ideas.md
and config/trade-ideas.json. This prompt explicitly overrides the skill's
closing-only and combined-companion gates for Trade Ideas only. Daily remains
a separate after-close publication.

Inspect status, fetch origin main, fast-forward only when clean and incoming
paths do not overlap untracked files. Never stash/reset/clean/force/overwrite.
Re-read contracts after refresh. If another publication owns
`.trade-ideas-publication.lock`, stop this attempt and report lock owner; never
race another run. Acquire that directory atomically before writing, release
on completion/failure. Ignore the lock in Git; it is local coordination only.

At exactly 12:00 America/Vancouver each weekday, verify today is a U.S. exchange
trading day using the official calendar, including exceptional closures. Stop
before research on holidays/weekends or before noon. Use the current Pacific
calendar date, verify New York session date, then resolve the NEXT actual U.S.
trading session. Do not shift early-close sessions to 11:00: noon is still the
requested time, even when cash trading has ended. Label session state honestly.
The schedule starts research/refresh at noon; actual publication may be later.
Mac/app sleep or execution/source delays must be disclosed, not backdated.

Check only `data/trade-ideas/<date>/complete.json`: validated matching family/date
means no-op. Daily completion must neither suppress nor trigger this task.
Generate only one noon edition per date; closing Daily must not overwrite it.
Never label unfinished intraday observations as closing data or use a future
close. Save publication_mode `noon`, scheduled_for with Pacific offset,
generated_at, latest actual data_observed_at and explicit source observation
meaning/delays. Research the latest few sessions/week and current intraday
technicals, macro results, next-session official catalysts/times, earnings/news,
accessible attributed public X (or truthful access gap) and cross-asset cases.

Follow version 2 three-family/$500 contract, verify listed expiration/legs or
label desired unverified strikes; unknown premium/fees means parametric risk
and intrinsic-only schematics, not certified maximum account loss. Core symbols
SPX/QQQ/IWM; optional supported ETF context; no naked options/orders or count quota.
Save date-scoped evidence, render using the existing trade-ideas CLI, run targeted
payoff/gate/site tests, publication validation and build; inspect title, target,
intraday labels, timestamps, citations and desired-leg warnings. Write completion
marker only after checks, commit intended files, push and verify Pages. Preserve
Daily and all other publication artifacts. No external LLM APIs or paid keys.
