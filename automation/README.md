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
