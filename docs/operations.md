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
- **Deploy fails:** verify Pages permissions and rerun after correction.
- **Publication is late:** use the next eligible post-close check and show the
  real generation time; never reclassify Daily as an opening or mid-session report.
- **Publication exists:** exit without research, changes, or a new commit.

## Safety

The repository is public. Review staged files before publication. Never commit
secrets, cookies, private messages, local paths, account details, positions,
orders, or browser state. Never force-push from a scheduled task.
