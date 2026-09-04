# Operations

## Daily execution

The recurring Codex task is the only intelligent generator. It checks every 15 minutes during the configured weekday morning window and exits before research when a validated report already exists for the current New York date.

The Mac must be awake, logged in, online, and running the ChatGPT desktop app. A task missed while the Mac sleeps is not guaranteed to run on wake; the recurring check supplies catch-up behavior. A catch-up after 9:30 a.m. New York time is labeled `Intraday update`.

The task instructions live in `automation/DAILY_TASK_PROMPT.md`. The repository-scoped procedure lives in `.agents/skills/market-wrap/SKILL.md`.

## Local verification

From the repository root:

```bash
python -m pytest
python -m market_wrap validate --root .
python -m market_wrap build --root . --output site
```

Open `site/index.html` and inspect the newest report, charts, timestamps, source links, freshness state, and archive navigation before pushing.

## Publication

A push to `main` starts `.github/workflows/pages.yml`. GitHub Actions installs the project, runs tests, validates committed content, builds `site/`, and deploys it to GitHub Pages. It does not research or write the report and needs no OpenAI API key.

Enable GitHub Pages with **GitHub Actions** as its source in the repository settings. The workflow requires only the standard `GITHUB_TOKEN`; no repository secret is required.

## Failure recovery

- **Research or local validation fails:** do not commit; keep the previous public report.
- **Push fails:** confirm GitHub authentication and reconcile remote changes without force-pushing.
- **Build job fails:** inspect the first failed test or validation step, repair locally, and push a new commit.
- **Deploy job fails:** verify Pages is enabled and the workflow has Pages permissions; rerun after correcting configuration.
- **Report is late:** let the next catch-up check create an `Intraday update` within the allowed window.
- **Report already exists:** exit successfully without research, file changes, or a new commit.

## Safety

The repository is public. Review staged files before every publication. Never commit secrets, cookies, private messages, local paths, account details, or browser state. Never force-push from the scheduled task.
