# Pre-handoff checks

Read this before you hand work to a reviewer, a QA tester or a customer. Each check names what it proves. A handoff that skips a check says so in its report.

## Numbers and scopes

1. Prove each number against an independent oracle: the list page, a sibling endpoint or an export. Recount it. Don't read it back from the query that produced it.
2. Sweep the parameters a user can change: date ranges, domain picks, languages, themes, viewports and roles. The default view proves only the default view.
3. Every scope or filter gets three controls on real data. A positive control: the owner sees its own rows with the expected counts. A negative control: another tenant is refused or sees nothing. A no-token control: an anonymous caller is refused.
4. Complements add up. Matching plus not matching equals the unfiltered total. Before a date plus on-or-after that date equals the total. A shortfall exposes nulls and mistyped dates.
5. A clicked number lands on a list with an exact match and the same total. Compare the two totals under the same filters.
6. Normalize keys before comparing: lowercase emails and trim whitespace. Break ties in ranked lists so equal scores keep a stable order.

## Interface and API

7. No raw backend key appears in any language, including the fallback text.
8. Measure the UI for contrast, text fit and console errors, in every combination of English and Arabic, dark and light, desktop and phone.
9. Test how the API handles booleans, numeric strings, duplicates and broken JSON. Check the status codes: 401 for a bad token, 403 for a refused caller, a 4xx for a user error, and never a 500 for an expected failure.

## Delivery

10. Prove that prerequisites ran on the target environment: backfills, flags and seed data. Query the target. Don't infer it from the deploy log.
11. The dry run and the real run agree. Compare the counts and the rows each one touches.
12. A cold load and a refresh keep the filters. Check the URL after each.
13. Report as a table with one row per check and the columns Check, Expected and Result. Include a positive-control row, and it must show a match.

A pass no row proves isn't a pass. Each row names the request and window, the oracle, and the automated test id, where one exists.
