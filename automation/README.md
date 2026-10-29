# Codex automation prompts

These prompts separate intelligent research from deterministic GitHub Pages publishing. Each scheduled Codex task uses the repository-scoped `$market-wrap` skill and the user's ChatGPT allowance. GitHub Actions only validate, build, and deploy committed content.

| Automation | Prompt | Eligibility gate | Recommended Vancouver-time recurrence |
|---|---|---|---|
| Daily Market Wrap | `DAILY_TASK_PROMPT.md` | Weekday, after the completed U.S. cash close | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=13,14,15,16,17,18;BYMINUTE=30` |
| Weekly Market Wrap | `WEEKLY_TASK_PROMPT.md` | Friday close, or Thursday close when Friday is a confirmed full-day U.S. holiday | `FREQ=WEEKLY;BYDAY=TH,FR;BYHOUR=14,15,16,17,18,19;BYMINUTE=5` |
| Monthly Market Wrap | `MONTHLY_TASK_PROMPT.md` | Final U.S. trading-day close of the month | `FREQ=MONTHLY;BYMONTHDAY=25,26,27,28,29,30,31;BYDAY=MO,TU,WE,TH,FR;BYHOUR=14,15,16,17,18,19;BYMINUTE=40` |
| Canadian Economy | `CANADIAN_ECONOMY_TASK_PROMPT.md` | Final Canadian trading-day close of the month | `FREQ=MONTHLY;BYMONTHDAY=25,26,27,28,29,30,31;BYDAY=MO,TU,WE,TH,FR;BYHOUR=15,16,17,18,19,20;BYMINUTE=15` |

Configure each recurrence with timezone `America/Vancouver`. The repeated evening attempts provide catch-up after sleep or a temporary outage. Eligibility checks and type-specific completion markers make later attempts no-ops. The monthly tasks run a cheap official-calendar gate on ordinary weekdays because an RRULE cannot reliably encode the last exchange trading day or ad hoc holidays.

Staggering the four schedules reduces concurrent edits to the shared repository. Monthly checks are limited to the final seven calendar days. If two eligible tasks still overlap, each must stop when the worktree contains overlapping publication changes; a later recurrence can retry after the first push completes. Never force-push.

Trade Ideas is a companion branch of the existing Daily task, not a fifth
automation. Check the daily/trade-ideas completion markers independently. Proposed
prompt changes do not activate themselves; preserve the recurrences above.

The active Daily automation retains its existing after-close catch-up recurrence and owner. Its prompt was updated for policy version 2 on 2026-10-29; no duplicate automation was created. Every wake must first refresh the checkout safely and reread the current companion contract. The local Mac/app must be awake and sources accessible. GitHub Actions does not supply fresh research.

## Trade Ideas — noon Pacific

`trade-ideas-noon-pacific` / Trade Ideas — Noon Pacific owns the separate weekday
12:00 America/Vancouver refresh, with official exchange holiday gates. The
closing Daily schedule remains 13:30–18:30 Vancouver and owns Daily only. Both
use independent family/date markers. Noon stays noon on early closes. The
Mac/app must be awake; scheduler dispatch/research/deployment can delay delivery.
