# ADR 0003: Make GitHub publishing deterministic

Status: Accepted

## Decision

GitHub Actions will validate, build, and deploy the static site only after Codex commits and pushes a validated report. GitHub Actions will not perform LLM research or narrative generation.

## Consequences

- The public website is reproducible from repository content.
- A local file change alone does not deploy; a successful push is required.
- A failed or incomplete local run leaves the last valid website intact.
