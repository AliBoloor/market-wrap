# ADR 0002: Use an idempotent morning catch-up schedule

Status: Proposed

## Decision

Run a lightweight check every 15 minutes during an approved weekday morning window. Generate a report only when no validated completion marker exists for the current U.S. trading date.

## Consequences

- A Mac that wakes late can create a report at the next check.
- Repeated checks must stop before web research when a report already exists.
- A report created after the regular-session open must be labeled `Intraday update`.
- Sleep catch-up depends on the ChatGPT app resuming and is not guaranteed by a single missed scheduled run.

