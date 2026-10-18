# Changelog

Each release lists what changed and why, newest first.

## 1.11.0 - 2026-10-18

Subject: craft 1.11.0 adds meaning-change, scope, drill-down and retest rules

Overnight retests of one build found four defect shapes that the earlier rules did not name.

- A value that changes meaning is changed in every operator that touches it, and tested with the parameters users set. The list page for the same window is the oracle.
- A scope or filter check needs a positive control on real staging data. A ticket's prerequisites are verified on the target before it counts as shipped.
- A number and its drill-down share one definition, and the click-through total is tested against the number clicked.
- A retest report is a pass/fail table with the exact request, the window, the oracle and the automated test id.

The eval gate runs on the candidate content. The bench does not yet measure these rules, so the gate guards against regression only.

## 1.10.0 - 2026-10-17

Subject: craft 1.10.0 adds probes, helper-script, skip and cross-service rules

A batch of five lessons from one build. Each one came from a defect or a wrong claim that got past the checks.

- Queries that matter run on the production engine first, read-only: a zero-match probe, then a count checked against an independent recount.
- Helper scripts validate their arguments and stop at the first failed step. Each worktree gets its own dependency copy, and a reflection check confirms which file a class loads from.
- A test that skips for missing local data never ran in CI. A defect shape seen in one place gets one fix at the shared owner and a guard test with a positive control.
- A rule copied into a second service is mapped to that service's customer-facing outputs, with one owner for the rule and a cross-repo contract test on the copy.
- One-off Laravel scripts boot the kernel directly, not through tinker. A process is never stopped with `pkill -f` on a pattern from the same command line.

The eval gate runs on the candidate content. The bench does not yet measure these rules, so the gate guards against regression only.

## 1.9.0 - 2026-10-17

Subject: craft 1.9.0 applies visibility rules to every surface returning a field

A build hid who acted on one audit screen, but a second endpoint returned the same fact, and a test asserted that leak. The visibility rule now covers every surface that returns the same fields.

- A visibility rule covers every endpoint, export, search, report and webhook that returns the same fields. Grep them all and list each one in the PR.
- A test that asserts the old exposure is the bug's spec, so it is rewritten to assert the new rule.

The eval gate runs on the candidate content. The bench does not yet measure these rules, so the gate guards against regression only.

## 1.8.0 - 2026-10-17

Subject: craft 1.8.0 runs each CI job's own commands and checks every role

A worker reported a PHP lint pass, but the CI job still failed: its style tool ran on a fixed file list, and the worker had checked syntax only. A label reading "our staff" would also have been wrong for a reseller's action on the same screens.

- Before reporting done, a worker runs each command its CI job runs, copied from the workflow file, and names each one in the evidence.
- A label that names who acted is checked against every role that can reach its code path, not only the roles the ticket names.

The eval gate runs on the candidate content. The bench does not yet measure these rules, so the gate guards against regression only.

## 1.7.0 - 2026-10-17

Subject: craft 1.7.0 proves the e2e listener is the tested process

A local end-to-end run returned an empty 200 that looked flaky. The cause was another worker's mock server on the same port: the real server failed to bind and exited, and the mock answered. The rule now asks for proof of the listener before a local run counts, and for an explanation of any one-off result.

- Before a local end-to-end run counts, the listener on its port must be the process under test. A taken port fails fast.
- Parallel workers get their own port ranges, written in the brief.
- An unexplained one-off result is root-caused before the merge. It is never written off as flaky.

The eval gate runs on the candidate content. The bench does not yet measure this rule, so the gate guards against regression only.

## 1.6.0 - 2026-10-17

Subject: craft 1.6.0 checks every CI job before a merge, not only reruns

A merge reviewed on its suites alone let a red lint job reach the integration branch, and the next two PRs inherited the failure. The rule now covers every job on the PR.

- Before a merge, the owner reads every CI job, including lint, typecheck and build. A red job is fixed, or proven red on the clean base with an owner and an action.
- The review reference gives the procedure, with the reason: a lint rule can fail a change that every test passes.

The eval gate runs on the candidate content. As before, the bench does not yet measure this rule, so the gate guards against regression only.

## 1.5.0 - 2026-10-17

Subject: craft 1.5.0 adds acceptance, input and permission rules from a QA review

A review of 1,668 bugs filed by one QA lead over 21 months showed the same defect shapes returning each sprint. The rules below sharpen existing sections where they overlapped, and add the checks that were missing.

- Acceptance walks every state in each language, with one source for every number shown.
- A control must change the request it claims to, and an export covers the full filtered set and is opened in its target tool.
- Every input is bounded, and a bad value gets a client error with no framework text.
- A caller's test covers each role, another tenant and an anonymous caller.
- Success text comes from the server response. Notifications count as delivered only when the provider reports it.
- A defect-pattern list gives a check for each shape that recurs in review.

The eval gate ran the four existing tasks, three samples each, on the candidate content. As with 1.4.0, the bench does not yet measure these rules, so the gate guards against regression only.

## 1.4.0 - 2026-10-17

Subject: craft 1.4.0 adds delivery, contract and merge rules

A two-day build with several parallel agents exposed gaps the skill did not cover. Each rule below came from a logged failure, with the evidence kept in the source run.

- Acceptance covers every surface the user sees and every product a requirement names. Deferring a surface is an owner question, asked before building.
- Translated output gets a page-image pass, enum values and empty states included.
- A rule about what a customer may see covers every read path, enumerated by a guard test.
- Green CI is not proof when decisive tests were skipped. Read the skip count, and run those tests with real dependencies on the target runtime.
- Side effects after a committed write never turn the write into an error.
- Parallel work on both sides of an interface starts only after the contract is frozen as an artifact.
- The coordinator reads every non-heartbeat message, and merges only the reviewed head.
- Subagents delete nothing outside their own worktree or recorded temporary paths.
- An answer that unblocks work starts in the same turn.

The eval gate ran the four existing tasks, three samples each, on the candidate content (hash 37d9e46b6e343f5b). It measures regression, not the new rules, because those rules need multi-agent runs that the bench does not yet cover.

## 1.3.2 - 2026-10-12

Subject: craft 1.3.2 ships its prose lint and gates releases on quality

The prose lint was not in the public skill, so the skill could not run its own check. It now ships in `scripts/`, and the writing reference points at it from the skill folder.

- `scripts/ai-tell-lint.py` is a portable copy. The owner-specific ledger path and the rule-file message are removed.
- The A/B gate and the release gate judge quality. Cost, turns and tokens are recorded and reported, and they do not block a release. A faster or cheaper run with worse work does not count as an improvement.
- Twelve paired Claude runs on this content pass every task that the previous content passed.

## 1.3.1 - 2026-10-12

Subject: craft 1.3.1 fixes three flag claims and records the commit-trailer test

Three flags in the capability reference did not match the installed CLIs. Codex's unattended run sets the approval policy with a config key, because `codex exec` has no approval flag. Qwen's installed version lists no approval flag, so the earlier one is removed. Claude's attribution setting is confirmed against this machine's settings.

- Text in the skill cannot remove a commit trailer that the harness adds by default. In a test, Claude Code added a co-author line to every commit, with and without the skill. The attribution setting removed it, so the git reference now names the setting.
- Twelve paired runs on the candidate pass every task that the previous content passed, and the commit task passes on all three samples where the old content failed all three. The cost difference across the four tasks is flat.

## 1.3.0 - 2026-10-12

Subject: craft 1.3.0 corrects the Copilot, Gemini and Devin Desktop entries

Checking the Copilot, Gemini, OpenCode, Cursor and Devin Desktop sources showed that the first draft of the capability reference was wrong on three points: Copilot has an ask tool and a per-launch model flag, Gemini subagents take a model setting, and Devin Desktop reads skills from `.devin/skills`.

- Copilot's `--no-ask-user` and `--max-autopilot-continues` flags are now listed for headless runs.
- OpenCode's `--auto` flag is described as skipping only actions that are not denied.
- Devin Desktop's skill folder and the 12,000-character rule limit are now listed, so the full skill installs as a skill.

## 1.2.0 - 2026-10-12

Subject: craft 1.2.0 records how Command Code and Qwen Code differ

Command Code stops sending skill descriptions once a catalog grows past about 42 skills, so the trigger needs to appear in the instruction file too. Qwen Code adds a line to pull request bodies made by `gh pr create`, on top of its commit trailer.

- `references/agent-capabilities.md` covers both differences, with the attribution settings that turn them off.
- The short form for instruction files now names the trigger and no longer points at a Claude-only path.

## 1.1.0 - 2026-10-12

Subject: craft 1.1.0 checks its own rules at release and covers headless runs

The skill now applies its own rules to its own release, and it covers headless runs that have no question tool.

- Adds `references/self-application.md`, which maps each rule to the check that proves it. The release script runs those checks: links, dashes and curly quotes, reference headers, a 2,000-word budget and the rubric row count.
- Headless runs park their questions and put them in the final report, because some harnesses have no question tool outside an interactive session.
- Goal runs state that `/goal` does not lift per-tool prompts, and that a hard checkpoint needs a harness ask rule where the harness has one.
- Commit guidance tells the agent to check the harness's attribution setting before assuming a trailer.
- Briefs tell workers how to stop, because many workers cannot call the question tool.
- Adds ten subagent rules, covering the brief, questions, models, permissions, concurrency, review nesting, fresh versus resumed workers, and claims of success.
- Adds `references/agent-capabilities.md`, which lists for each harness the skill directory, the headless question behavior, the unattended setting and the default commit trailer. Facts the official docs do not give are marked as not documented.
- Releases are published as tagged GitHub releases, and commits carry no attribution trailers.

## 1.0.0 - 2026-10-12

Subject: craft 1.0.0 publishes one skill for writing, building and autonomous runs

The first public version: one skill for prose, simplicity, proof, debugging, review, delegation, plans, git safety and autonomous or goal-driven runs.

- `SKILL.md` holds the core rules, and five references hold the detail: writing, proof and debugging, review and delegation, git and safety, and autonomy.
- Installs with the skills CLI for Claude Code, Codex and Kimi Code.
