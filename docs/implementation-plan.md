# Implementation plan

The initial end-to-end version was implemented on September 3, 2026. The phase
descriptions below now serve as an operating roadmap; production hardening and
the five-session reliability trial remain ongoing.

## Phase 1 — Publication foundation

- Define the report Markdown front matter and evidence-manifest schema.
- Build a deterministic static-site generator.
- Build the latest-report page and dated archive.
- Add freshness, citation, file, and schema validation.
- Add GitHub Pages deployment triggered only by pushes to `main`.
- Test publication using a fixed sample report with no market research.

Exit criterion: a sample bundle can be validated and published reproducibly.

## Phase 2 — Research workflow

- Turn the approved prompt into a repository-scoped Market Wrap skill.
- Define source priorities and minimum corroboration rules.
- Define the risk-regime rubric and technical-analysis methodology.
- Establish no-key sources for current values, history, calendars, and news.
- Run several manual research trials before scheduling.

Exit criterion: repeated manual runs produce appropriately sourced, consistent reports.

## Phase 3 — Charts and quantitative checks

- Implement transparent calculations for returns and 20/50/200-day averages.
- Record exact inputs used by each chart.
- Generate accessible, publication-quality chart images.
- Test that final moving-average values match report tables.
- Add stale-data and instrument-mismatch detection.

Exit criterion: charts are reproducible from the committed observation bundle and agree with the narrative.

## Phase 4 — Local scheduled operation

- Configure the task to work directly in this dedicated repository.
- Pre-authorize the narrow filesystem, web, and Git operations it requires.
- Schedule an idempotent check every 15 minutes during the weekday morning window.
- Generate a pre-market report before the open or a clearly labeled intraday update after the open.
- Prevent duplicates with an atomic dated completion marker.
- Test sleep, wake, network-failure, dirty-worktree, and push-failure scenarios.

Exit criterion: five consecutive trading-day runs complete or produce actionable failure notices without corrupting the archive.

## Phase 5 — Operational hardening

- Add link and citation checks.
- Add a visible last-updated and freshness indicator.
- Add deployment confirmation.
- Add an audit log containing no secrets.
- Document recovery and manual-run procedures.

Exit criterion: failures are visible, recoverable, and never silently presented as fresh reports.

## Decisions adopted

1. Weekday catch-up window: 05:30–12:00 America/Vancouver.
2. Before 09:30 America/New_York use `Pre-market`; after the open use `Intraday update`.
3. The report sections and focused two-to-four-chart set are approved.
4. Public no-key endpoints may be used, with failures and timestamps disclosed.
5. GitHub Actions builds generated site files; only source reports, evidence,
   and chart assets are committed.
