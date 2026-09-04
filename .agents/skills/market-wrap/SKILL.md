---
name: market-wrap
description: Research, write, validate, archive, and publish the daily U.S. Market Wrap from this repository. Use when Codex is asked to produce or retry a pre-market, intraday catch-up, or market-holiday report; update the Market Wrap archive; or diagnose a failed daily publication. This workflow uses Codex web research under the user’s ChatGPT plan and never calls an LLM API.
---

# Market Wrap

Produce at most one validated report for each New York trading date. Treat the repository as public.

## Run the daily workflow

1. Read `AGENTS.md`, `docs/report-spec.md`, and `automation/DAILY_TASK_PROMPT.md`.
2. Determine the current date and time in `America/New_York`. Stop before web research when today’s validated completion marker already exists.
3. Stop outside the configured weekday catch-up window. On a U.S. market holiday, produce the short holiday form defined by the report specification.
4. Inspect the worktree. Never overwrite, commit, or publish unrelated local changes.
5. Research the current session. Apply [the source and evidence policy](references/source-policy.md). Prefer primary sources for schedules and official releases; use reputable financial reporting for context.
6. Distinguish observed facts from interpretation. Describe a causal market driver only when evidence supports it; otherwise state that attribution is inconclusive.
7. Create the report bundle in the paths required by the repository schema. Record source URLs, observation timestamps, instruments, units, and chart inputs. Do not put secrets, local paths, account data, cookies, or private information in any artifact.
8. Use deterministic repository tooling for calculations and charts. Never estimate a plotted value by eye or invent missing observations.
9. Run:

   ```bash
   python -m pytest
   python -m market_wrap validate --root .
   python -m market_wrap build --root . --output site
   ```

10. Inspect the built site and verify the report date, latest-update time, citations, charts, archive link, and freshness label.
11. Commit only the validated publication artifacts and related generated indexes. Pull safely if necessary; never force-push. Push to the configured publication branch.
12. Confirm the GitHub Pages deployment. Return the report and public URL in ChatGPT.

## Choose the report type

- Before 9:30 a.m. New York time: `Pre-market`.
- At or after 9:30 a.m. during the approved catch-up window: `Intraday update`; use current observations and say that trading has begun.
- U.S. market holiday: `Market holiday`; focus on the next session and omit unsupported live-market claims.

## Fail safely

- Preserve the last valid public report whenever research, validation, build, Git, or deployment fails.
- Do not write a completion marker until the full bundle validates.
- Do not treat a skipped duplicate run as a new publication.
- Report the failed stage and the smallest useful recovery action in ChatGPT.
- If the worktree contains overlapping user changes, stop before committing and explain the conflict.

## Keep GitHub deterministic

GitHub Actions may test, validate, build, and deploy committed content. It must never perform research, call an LLM, or silently create narrative. The intelligent report content must be created by the scheduled Codex run under the user’s ChatGPT allowance.
