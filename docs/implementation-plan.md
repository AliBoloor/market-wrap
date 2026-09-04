# Implementation plan

The first Daily Market Wrap pipeline was implemented on September 3, 2026. The
next release expands it into four publication families while retaining the
validated, no-key, static-site architecture.

## Phase 1 — Existing foundation (complete)

- Deterministic Markdown/front-matter and evidence-manifest validation.
- Reproducible market calculations and chart generation.
- Static-site build, dated archive, and GitHub Pages deployment.
- Repository-scoped Codex skill and source-quality policy.
- Public-repository safety and fail-closed publication behavior.

## Phase 2 — Four-publication information architecture

- Add landing/archive routes for Daily, Weekly, Monthly, and Canadian Economy.
- Add publication type and coverage-period metadata with legacy compatibility.
- Use type-specific completion markers so overlapping reports coexist.
- Make Daily the default landing view and clearly navigate to all sections.

Exit criterion: fixtures for all four types validate and render correctly.

## Phase 3 — Editorial contracts and quantitative coverage

- Enforce the type-specific sections in `docs/report-spec.md`.
- Keep Daily post-close with a tomorrow outlook, technical map, and calendar.
- Add weekly/monthly scorecards and appropriate technical horizons.
- Include global-markets context in Daily, Weekly, and Monthly.
- Add Canadian macro series, neutral political coverage, and balanced annotated
  policy reading.
- Preserve standalone realized-volatility tables and carefully scoped options
  and equity-volume measures when trustworthy data is available.

Exit criterion: a manually reviewed publication of each type satisfies its
editorial, sourcing, chart, and data-quality contract.

## Phase 4 — Scheduled operation

- Replace the former opening-time schedule with bounded post-close Daily checks.
- Schedule Weekly after the actual final session, including Friday holidays.
- Schedule Monthly after the final U.S. session of the month.
- Schedule Canadian Economy after the final Canadian trading session of the month.
- Serialize overlapping tasks and test sleep/wake, holidays, month-end overlap,
  network failure, dirty worktree, and deployment failure.

Exit criterion: each schedule is idempotent, calendar-aware, and independent.

## Phase 5 — Reliability and editorial QA

- Verify citations, timestamps, freshness, tables, and chart reconciliation.
- Confirm the deployed route, not only the workflow job.
- Maintain a public-safe audit trail and actionable failure notice in ChatGPT.
- Test at least five daily sessions, one weekly close, and one month-end cycle.

Exit criterion: failures are visible and recoverable, with the prior site intact.

## Decisions adopted

1. Intelligence runs in Codex under the user's ChatGPT allowance; repository
   code and GitHub Actions do not call an LLM API.
2. Daily means after-close reporting about today and the next session.
3. Weekly publishes after the week's final session; Friday-holiday weeks publish
   Thursday after close.
4. Monthly Market Wrap and Canadian Economy are distinct monthly products.
5. Daily, Weekly, and Monthly include global-markets context.
6. Canadian Economy is macro/educational, politically neutral, and includes
   balanced annotated policy reading.
7. Public no-key endpoints may be used with limitations disclosed.
