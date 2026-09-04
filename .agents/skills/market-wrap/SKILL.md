---
name: market-wrap
description: Research, write, validate, archive, and publish the Daily Market Wrap, Weekly Market Wrap, Monthly Market Wrap, or Canadian Economy report from this repository. Use for closing-market reports, week or month reviews and outlooks, Canadian macro/policy reporting, publication retries, archive updates, or failed-publication diagnosis. This workflow uses Codex web research under the user's ChatGPT plan and never calls an LLM API.
---

# Market Wrap

Create validated, public research publications without an external LLM API.
Treat every repository artifact as public.

## Start every publication

1. Read `AGENTS.md`, `docs/report-spec.md`, `docs/architecture.md`, and the
   applicable scheduled-task prompt.
2. Determine the current time in `America/New_York`, resolve the trading
   calendar, and identify publication type and coverage period.
3. Stop before web research if that type/period has a validated marker.
4. Confirm the cadence is due:
   - Daily: after the completed regular U.S. session.
   - Weekly: after the week's final U.S. session, normally Friday, or Thursday
     when Friday is a U.S. market holiday.
   - Monthly: after the final U.S. session of the calendar month.
   - Canadian Economy: after the final Canadian trading session of the month.
5. Inspect the worktree. Never overwrite, commit, or publish unrelated changes.
   Serialize work if another publication task is writing or pushing.

## Research and write

1. Apply [the source and evidence policy](references/source-policy.md). Use
   primary sources for schedules and releases and reputable financial reporting
   for timely context.
2. Match the depth and horizon in `docs/report-spec.md`:
   - Daily explains the completed session and tomorrow's catalysts, technical
     levels, and conditional scenarios.
   - Weekly explains the completed week and next week, with more macro,
     positioning, sentiment, and calendar context.
   - Monthly explains durable U.S./global economic, earnings, growth, rates,
     policy, and market trends and frames the next month.
   - Canadian Economy is a comprehensive educational macro/political review,
     not a daily equity recap, ending with annotated reading from credible
     institutions and varied policy viewpoints.
3. Include global-market context in Daily, Weekly, and Monthly.
4. Separate observed facts, attributed explanations, and interpretation. Assert
   a causal driver only when evidence supports it; otherwise call attribution
   inconclusive.
5. Save source URLs, publication/coverage dates, observation timestamps,
   instruments, units, and failure flags. Never include secrets, local paths,
   account data, cookies, or private information.
6. Use deterministic repository tooling for calculations and charts. Never
   estimate plotted values by eye, invent missing observations, or hide stale
   data. Reconcile chart endpoints with tables.

## Validate and publish

Run:

```bash
python -m pytest
python -m market_wrap validate --root .
python -m market_wrap build --root . --output site
```

Inspect the built site and verify publication name, coverage period, generation
and observation times, citations, charts, archive route, navigation, freshness,
and required outlook. Then:

1. Write the type-and-period completion marker only after validation.
2. Commit only the validated bundle and related generated indexes.
3. Pull safely when needed; never force-push.
4. Push and confirm the exact GitHub Pages route renders successfully.
5. Return the publication and public URL in ChatGPT.

## Fail safely

- Preserve the last valid publication when research, validation, build, Git, or
  deployment fails.
- Never treat a skipped duplicate as a new publication.
- Publish simultaneous due reports serially and revalidate after upstream change.
- Report the failed stage and smallest useful recovery action in ChatGPT.
- Stop before committing when the worktree has overlapping user changes.

## Keep GitHub deterministic

GitHub Actions may test, validate, build, and deploy committed content. It must
never research, call an LLM, or silently create narrative. Intelligent content
is created only by scheduled Codex tasks under the user's ChatGPT allowance.
