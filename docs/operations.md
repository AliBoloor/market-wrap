# Operations

## Intelligent generation

Scheduled Codex tasks are the only intelligent generators. They run under the
user's ChatGPT allowance and write into this dedicated repository. Repository
code, builds, and GitHub Actions contain no LLM call and require no OpenAI key.

Each task uses the calendar and distinct completion key in
`docs/architecture.md`. Daily runs use a bounded post-close catch-up window.
Weekly, Monthly, and Canadian Economy tasks run only when their calendar
condition is met. If more than one is due, run serially and pull/revalidate
between commits.

The Mac must be awake, logged in, online, and running ChatGPT desktop. A missed
run cannot execute while it sleeps; bounded checks provide catch-up after wake.
Every delayed publication shows its true generation and observation times.

The editorial procedure lives in `.agents/skills/market-wrap/SKILL.md`; detailed
requirements live in `docs/report-spec.md`.

## Local verification

```bash
python -m pytest
python -m market_wrap validate --root .
python -m market_wrap build --root . --output site
```

Inspect the new route and archive entry. Verify publication name and coverage
period, timestamps, citations, chart/table agreement, freshness, outlook
horizon, and navigation among all four sections.

## Publication

A push to `main` starts `.github/workflows/pages.yml`. GitHub Actions installs,
tests, validates, builds `site/`, and deploys GitHub Pages. It does not research
or write. It needs only the standard `GITHUB_TOKEN`, not a repository secret.

## Failure recovery

- **Research/validation fails:** do not commit; preserve the previous site.
- **Tasks overlap:** serialize, update the next checkout, and revalidate.
- **Push fails:** reconcile remote changes without force-pushing.
- **Build fails:** repair locally and push a new commit.
- **Deploy fails:** keep the validated content bundle; inspect the exact Pages
  run and retry failed deploy jobs only after identifying the failed stage. A
  marker is not publication proof. See the Daily delivery recovery preflight.
- **Publication is late:** use the next eligible post-close check and show the
  real generation time; never reclassify Daily as an opening or mid-session report.
- **Daily content exists:** skip research, then run `python -m market_wrap
  publication-status --root . --family daily`. Exit as already published only
  when BOTH latest and dated pages match the source hash. Otherwise recover
  delivery without rewriting content. Never commit a delivery receipt/push loop.

## Safety

The repository is public. Review staged files before publication. Never commit
secrets, cookies, private messages, local paths, account details, positions,
orders, or browser state. Never force-push from a scheduled task.

## November 4 deployment recovery

The report commit c5f77e439929eb6ba1cf962a23591d6260dd926d passed build, tests
and validation, but Pages stayed updating_pages until its 600-second timeout.
A failed-job-only retry succeeded. Later scheduled checks had incorrectly
suppressed recovery because complete.json was validated. Report article identity
now carries family/date/source SHA-256, and publication-status verifies BOTH
latest and dated routes. Network errors, old HTML, wrong dates or changed source
content are pending delivery, never successful completion. Retry existing runs,
not new research. See automation/DAILY_TASK_PROMPT.md for bounded/no-duplicate
recovery. Native scheduler controls remain separate; no control denial is bypassed.
