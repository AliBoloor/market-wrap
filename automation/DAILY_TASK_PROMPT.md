# Scheduled-task prompt

Run this task every 15 minutes on weekdays during the approved morning catch-up window. Use the repository-scoped `$market-wrap` skill.

First determine the current date and time in `America/New_York` and perform the repository’s deterministic completion check. If a validated completion marker already exists for the current trading date, stop immediately without web research, file changes, Git operations, or publication. Stop outside the approved catch-up window.

If today needs a report, research and produce at most one evidence-backed U.S. Market Wrap. Before 9:30 a.m. New York time label it `Pre-market`. At or after the open label it `Intraday update` and use current intraday observations. On a U.S. market holiday create a short `Market holiday` report focused on the next session.

Cover the overnight or current cross-asset setup, the strongest supported market drivers, consequences of material recent events, today’s and the next two trading days’ catalysts, the risk regime, technical setup, and invalidation risks. Prefer official primary sources for scheduled events and released data. Use reputable reporting for breaking context. Separate observation from interpretation, corroborate causal claims, and state when attribution is inconclusive.

When trustworthy time series are available, calculate the 20-, 50-, and 200-day simple moving averages, distance from the 50- and 200-day averages, trend direction, prior-session levels, gaps, recent swing points, and nearby support and resistance for the S&P 500, Nasdaq 100, and instruments central to the day. Distinguish futures, cash indexes, and ETFs. Explain how important levels were selected and avoid false precision.

Create two to four charts only from recorded, sourced numerical observations. Each chart must identify the instrument, interval, units, source, and latest observation time, and must agree with the corresponding table. Omit a chart or use a table when trustworthy data is unavailable; never fabricate or visually interpolate values.

Save the dated report, evidence manifest, numerical chart inputs, and chart images in the repository’s required paths. Run all tests, validation, and the static-site build. Inspect the rendered site. Do not create the completion marker or commit unless every required check passes. Commit only the new publication artifacts and generated indexes, reconcile remote work safely, push without force, and confirm GitHub Pages deployment.

Return the finished report and public link in ChatGPT. If any stage fails, leave the last valid public report unchanged and return a concise explanation naming the failed stage and recovery action. Never publish secrets, private data, absolute local paths, or unsupported claims. This task uses the user’s ChatGPT/Codex allowance and must not call an OpenAI or other LLM API.
