# ADR 0004: Treat all repository content as public

Status: Accepted

## Decision

Allow only public-source research, publication-safe observations, generated charts, validation metadata, and website files in the repository. Prohibit secrets and private machine or account data.

## Consequences

- The repository can remain public.
- Source manifests must contain public URLs and timestamps only.
- Validation must scan for common secret patterns before commit.
