# Canadian Economy monthly scheduled-task prompt

Use the repository-scoped `$market-wrap` skill. Determine the date and time in `America/Toronto` and consult official Canadian/TMX calendars before broad research. Publish after the final Canadian equity-market close of the calendar month. Stop if another Canadian trading session remains that month or its validated `canadian-economy` marker exists. This is not a day-to-day Canadian stock wrap.

Inspect `docs/report-spec.md`, the source policy, and current schema. Preserve unrelated changes. Write a comprehensive, educational **Canadian Economy** report explaining the month's structural and cyclical trends, key events, policy debate, and outlook.

Cover real growth and demand, labor and wages, inflation, housing and household leverage, population and immigration when material, productivity and investment, trade, energy and key commodities, CAD, financial conditions, the Bank of Canada, federal fiscal policy, and material provincial developments. Include politics only where it affects economic policy, regulation, investment, trade, public finances, or expectations. Represent competing interpretations fairly; distinguish facts, forecasts, policy positions, and synthesis.

Use a small market-context section to connect the economy to the S&P/TSX Composite, Government of Canada two- and ten-year yields, CAD, key commodities, sector trends, and a few economically informative Canadian companies when warranted. Explain each inclusion. Add relevant global context, especially U.S. demand/policy, China and commodities, and global rates/trade.

End with an annotated **Policy and further reading** section linking current substantive pieces from a balanced range: Bank of Canada, Statistics Canada, Finance Canada, Parliamentary Budget Officer, governments, established bank economics teams, business/sector bodies, universities, and reputable Canadian think tanks. Include credible liberal/progressive, centrist/institutional, and conservative/market-oriented analysis. Neutrally label publisher, date, topic, and institutional role or viewpoint. Do not manufacture balance with weak sources or imply endorsement.

For the outlook, identify official releases, Bank of Canada events, fiscal/political milestones, trade/regulatory decisions, and key risks. Use scenarios and signposts. Create charts/tables only from recorded sourced data; label units, frequency, adjustment/revision status, source, and observation period. Never fabricate, silently interpolate, mix nominal and real series, or hide staleness.

Save the bundle under Canadian Economy monthly conventions. Its identity is calendar month plus `canadian-economy`; never overwrite a U.S. report. Record URLs, dates, observations, units, adjustments, transformations, and inputs. All output is public; exclude secrets, credentials, cookies, accounts, private data, and absolute local paths.

Run all tests, validation, and the site build. Inspect the Canadian page, navigation, archive, citations, charts, reading links, caveats, political neutrality, and outlook. Only then mark complete, commit intended artifacts/indexes, reconcile without force, push, and confirm Pages deployment.

On failure, preserve the valid site, leave the marker absent, and report the stage and recovery action. Use only ChatGPT/Codex allowance; never call an OpenAI API, another LLM API, or a service requiring an external API key.
