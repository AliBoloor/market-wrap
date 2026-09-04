# ADR 0001: Use a scheduled Codex task for intelligence

Status: Proposed

## Decision

Use a local scheduled Codex task, authenticated through the user's ChatGPT plan, for research, reasoning, narrative, and technical interpretation. Do not call an LLM API from repository code or GitHub Actions.

## Consequences

- No OpenAI API key or separate API billing is required.
- Usage counts against the applicable ChatGPT/Codex allowance.
- The Mac, ChatGPT desktop app, local repository, and network must be available.
- GitHub Actions cannot regenerate the intelligent report independently.

