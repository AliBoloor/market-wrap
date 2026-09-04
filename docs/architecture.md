# Architecture

## Objective

Publish four intelligent, sourced products—Daily Market Wrap, Weekly Market
Wrap, Monthly Market Wrap, and Canadian Economy—through a public static site.
Scheduled Codex tasks perform research and writing under the user's ChatGPT
plan. Repository code and GitHub Actions use no LLM API and require no OpenAI
API key.

## Responsibilities

### Scheduled Codex tasks

Separate scheduled tasks may serve each cadence. Each task resolves the relevant
trading calendar and coverage period; exits when that type/period already has a
validated completion marker; researches and writes to its editorial contract;
saves its evidence, observations, and charts; validates; commits; pushes; and
confirms the deployed route.

Tasks use distinct publication keys so daily, weekly, and month-end publications
can coexist on one date. When schedules overlap, they must serialize Git
operations, pull safely, and never overwrite another task's artifacts.

### Local deterministic tooling

Python handles calculations, chart rendering, schema/timestamp validation,
citation checks, site generation, and archive indexes. It does not write market
narratives and never calls an LLM.

### GitHub Actions

GitHub Actions starts only after a push. It tests, validates, builds the four
site sections and archives, and deploys GitHub Pages. It performs no research
and creates no editorial content.

## Publication calendar

- **Daily:** after each completed regular U.S. session; always a closing review
  with a next-session outlook.
- **Weekly:** after the week's final U.S. session, normally Friday, or Thursday
  when Friday is a U.S. market holiday.
- **Monthly:** after the final U.S. session of the calendar month.
- **Canadian Economy:** after the final Canadian trading session of each month;
  economic series may have different reference periods, which must be labeled explicitly.

Use bounded post-close catch-up checks rather than one wake-up. A sleeping Mac
cannot execute the task; the next eligible check runs after the Mac and ChatGPT
desktop app resume. A missed period is not silently backfilled outside the
documented recovery policy.

## Failure and concurrency policy

- Never replace a valid publication with a partial report.
- Never mark a skipped check as completed.
- Never publish material claims without adequate sources.
- Never force-push or overwrite unrelated local changes.
- Preserve the prior public site after research, validation, Git, or deployment
  failure.
- Use a publication lock or equivalent serialization when tasks can collide.
- Show actual generation and observation times after delayed execution.

## Security and privacy

The repository and website are public. Commit only public-source research,
publication-safe observations, generated charts, and validation metadata.
Secrets, cookies, credentials, browser state, private messages, account data,
positions, and local system information are prohibited.
