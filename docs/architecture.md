# Proposed architecture

## Objective

Produce one intelligent, sourced market wrap per U.S. trading day using a local scheduled Codex task under the user's ChatGPT plan. Save the result locally, deliver it in ChatGPT, and publish it through GitHub Pages without an OpenAI API key.

## Responsibilities

### Scheduled Codex task

The scheduled task performs the work requiring judgment:

1. Check whether a complete report already exists for the current trading date.
2. Research current markets and upcoming catalysts using web access.
3. Evaluate source quality and corroborate causal claims.
4. Write the narrative, risk-regime assessment, technical interpretation, and risks.
5. Obtain reliable no-key time-series data when charts are possible.
6. Save the report, evidence manifest, and charts.
7. Run deterministic validation.
8. Commit and push only when validation passes.
9. Return the report and publication status in ChatGPT.

The task must not publish approximate values, invented causal explanations, or charts built from unsourced observations.

### Local deterministic tooling

Small Python programs will handle only reproducible operations:

- calculations such as returns and moving averages;
- chart rendering from recorded observations;
- report-schema and timestamp validation;
- citation and asset-table consistency checks;
- static-site generation; and
- archive-index generation.

No LLM API is called by these programs.

### GitHub Actions

GitHub Actions runs only after a push. It validates the committed publication bundle, builds the static site, and deploys GitHub Pages. It does not research markets or write narrative.

## Daily sequence

1. macOS and ChatGPT are available.
2. A recurring catch-up task checks for today's completion marker.
3. If a valid report exists, the task exits without further work.
4. If no report exists, Codex researches and creates a draft bundle.
5. Local tools validate calculations, sources, dates, and files.
6. A successful bundle is moved into the dated publication paths.
7. Codex commits and pushes without force.
8. GitHub Actions deploys the website.
9. Codex reports success or a precise failure inside ChatGPT.

## Failure policy

- Never replace the latest valid report with a partial report.
- Never mark a skipped check as a completed publication.
- Never publish when material claims lack sources.
- Never force-push or overwrite unrelated local changes.
- If the Mac is unavailable, create a late report after wake only within the configured catch-up window.
- Label reports created after the U.S. open as `Intraday update`, not `Pre-market`.
- Preserve the prior public report and show its actual generation timestamp after a failed run.

## Security and privacy

The repository and website are public. Only public market information and publication artifacts may be committed. Secrets, cookies, credentials, browser state, private messages, and local system information are prohibited.

