# ADR 0002: Use idempotent bounded catch-up schedules

Status: Superseded by ADR 0005

## Decision

Run lightweight checks during bounded publication windows. Generate only when
no validated marker exists for the applicable publication type and period.

## Consequences

- A Mac that wakes late can create a report at the next eligible check.
- Repeated checks must stop before web research when a report already exists.
- Daily reports are always closing reports and run only after the session ends.
- Weekly and monthly checks resolve the actual final trading session.
- Sleep catch-up depends on the ChatGPT app resuming and is not guaranteed by a single missed scheduled run.
