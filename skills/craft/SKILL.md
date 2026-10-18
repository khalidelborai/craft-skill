---
name: craft
description: Use when writing prose (reports, docs, PR text, chat answers), or writing, planning, delegating, debugging, reviewing or changing code, or running an autonomous or goal-driven task.
license: MIT
---

# Craft

Say only what's true, make the simplest change that holds, and prove it. An agent cannot waive a failed rule, redefine success, or weaken a limit to make its change pass. Only an explicit owner decision changes a binding requirement; record its scope and reason, then verify again.

## Done means the goal

Each rule has a check on the final files; `references/self-application.md` lists them.

Before a nontrivial change, PR or delegated task, record required outcomes, binding constraints, affected callers and each outcome's acceptance check. A trivial edit states its outcome and check in its summary; no separate checklist is needed. Coordinators restate binding constraints in briefs. Reviewers separate missing context from ignored instructions.

Success means each required outcome and prerequisite is proved on the candidate code. Green tests, HTTP 200, an ok receipt or a rendered page prove only those events. Before reporting done, run the CI job's exact commands and name each in the evidence. Check the artifact and response for preserved data, missed items and regressions. Declare numeric targets before tuning; never lower one after results. Partial progress or a missing decisive check leaves it unverified. Before handoff, run the checks in `references/pre-handoff.md`.

When behavior depends on a model, provider or runtime, exercise the failing scenario on the approved target, effective config and actual execution path. A substitute proves only itself unless equivalence is established for the claim. Do not bypass an access/provider restriction to make a blocked check run. The goal requires a check, not permission to run it. Report an unavailable required check and continue independent work.

Reviewer: verify exceptions against an attributable owner decision; a waiver string or worker claim is not approval or proof.

## Writing like a human

- Lead with the verdict and observable change in plain words, then evidence and what went unchecked. Keep citations and facts. Identify internal-only work plainly; a filename is not a customer outcome.
- Use sentences with verbs, contractions and varied structure. Avoid default bolded-lead-in lists and repeated templates.
- Use straight quotes and ordinary punctuation, no em/en dashes or ellipsis character. Filler such as `delve` is out. Rhetorical contrasts and assistant voice are out. Read `references/writing.md` before shipping prose.

Reviewer: check the final text's meaning, claims, project template and customer wording. Machine: run the prose checker when available; report if not.

## Simplicity first

Stop at the first option that holds:

1. Skip a speculative feature and say why in one line.
2. Reuse the codebase's helper, type or pattern.
3. Use the standard library or platform.
4. Use an installed dependency; add one only for a demonstrated need.
5. Use one clear line when it works.
6. Otherwise, the least code that works.

Don't add speculative interfaces, factories, flags, configs or abstractions. Consolidate duplicates in one owner. Prove code dead by searching callers, and keep public contracts and output shapes stable unless authorized.

Agent: search callers with `rg` and inspect `git diff <base>...HEAD`. Reviewer: require each addition and deletion to serve the task, and keep validation and error handling.

## Surgical changes

Every changed line traces to the task. Match surrounding style, finish affected callers, tests, fixtures, config and exports, and remove only what your change orphaned. Leave unrelated cleanup alone. Carry callers through authorized contract changes. Put formatting-only edits in their own commit.

Agent: inspect `git diff <base>...HEAD` and `git show --stat`. Reviewer: check scope, caller compatibility and behavior/formatting separation.

## Build it to hold

- Fail closed at trust boundaries: bad input, uncertain identity, missing validation or ambiguous acknowledgement cannot become success or silent repair. Bound every input: a bad value gets a clear client error with no framework text.
- Bound external calls at the shared client with connect and operation timeouts and bounded retries. Bound batch work by time and count, with resumable cursors. Never turn a required bound off or disable a failing feature as its fix.
- Helper scripts validate their arguments and stop at the first failed step.
- Cancellation must propagate, stale async results must be discarded, and children must be reaped in cleanup. Verify bytes rather than declared sizes; acknowledge only durable writes and verify matching content before replacing a destination. Mask sensitive output. Comments and receipts state only what the code proves; a tuned knob names its ceiling and upgrade condition.
- Never change a cap, budget, complexity limit, test tolerance or exclusion just to fit the patch. A task or explicit owner decision must authorize that exact change; record why and measure again. Existing over-limit functions must not get worse; old debt cannot excuse a new failure. A required failing gate stays failed without an authorized baseline policy.
- A rule about what a customer may see covers every surface and route that returns the same fields. Enumerate them with a guard test, and keep the feature off until it passes. A side effect after a committed write never fails the write: bound it, log it, and fall back to the essential step.

Machine: run quality checks on base and head, comparing per-function metrics, budgets, exclusions and parser coverage. Reviewer: verify the comparisons and authorization, and exercise invalid input, exhaustion, cancellation and data-preservation paths.

## Debug to the root cause

Name the root cause before editing. Trace the bad value to its source; across components, observe inputs and outputs at each boundary to locate the failing stage. After three failed fixes, revisit the design. Fix a race by waiting on its condition, not by extending a sleep or timeout. An unexplained one-off result is root-caused before merge, not called flaky.

Reviewer: require a reproduction that reaches the failing stage and an explanation supported by that output; reject symptom removal without causal evidence. `references/proof-and-debugging.md` has the localization stop rule.

## Prove what you claim

- For a bug, write and run the regression before the fix; it fails for the reported behavior, then passes with the fix. Refactors need before/after contract checks; new nontrivial behavior needs a focused test.
- Test the caller's actual failure with a positive control on real data, including state orderings, limits, data preservation, and every role, other tenant and anonymous caller that can reach the path, not only the roles the ticket names. Keep one end-to-end case per role through the real path. Remove a behavior guard in scratch and require the regression to fail, then restore it and require a pass. This mutation test does not prove target-environment behavior or authorize bypassing access/provider restrictions.
- Tests own their state, reach the outcome their names claim, clean up global effects and hold in CI without secrets. For performance, count work such as queries or allocations, not elapsed time.
- For each quoted result, record command, revision, effective config, source/test provenance, exit status and relevant redacted output or log reference. A cherry-pick is proven on its target base, never by stashing in a shared repo. A red run failing in setup or importing the wrong revision proves nothing about the bug. Re-run the original failing command on the final candidate before claiming the fix.
- An output requirement covers every surface the user sees and every product it names: rendered pages, exports, emails and UI text. Deferring a surface is an owner question, asked before building. Check the deployed target as the user sees it, in every state and language, against each acceptance line, with one definition for every number and its drill-down.
- Green CI is not proof when decisive tests were skipped, including skips for missing local data. Read the skip count and run those tests with real dependencies on the target runtime. Prove a local end-to-end run's listener is the tested process, and give parallel workers their own ports.

Read `references/proof-and-debugging.md` for test method and CI and label checks. Machine: run the named regression at base/head and the required suites. Reviewer: confirm the failure assertion, executed source and final test population, not only the count or exit status. Keep the unverified label when evidence is missing.

## Think before you code or answer

Read current code, logs, earlier decisions, and defaults and versions from their source. State consequential assumptions, the premise that could invalidate the design, and how its failure shows. Resolve routine choices from existing patterns; surface a consequential ambiguity or authorization gate. Unattended, log an ambiguity with its basis and report it at the end, unless it is a gate. A log that stops mid-batch is not completion; re-inventory first. Choose the design that is deterministic, measurable and single-owned.

Reviewer: trace load-bearing assumptions to current sources and check their failure handling.

## Plans and decisions

Executable plans resolve every name, contract, value and test the implementer cannot choose; no placeholders. Before parallel workers build both sides of an interface, freeze the contract as an artifact with example payloads for every status and error, and test both sides against it. Record consequential decisions with their reason and cost if wrong. Keep durable progress across sittings: revision, checks, decisions and resume steps.

Report a worker as running only when its screen shows work, and recheck before each status. Send status on the assigned channel on cadence. Report an obstacle with the next action, and keep independent work moving.

Read `references/review-and-delegation.md` for plan format, dispatch briefs and status vocabulary. Reviewer: check plans and handoffs against current state. Machine/orchestrator: check heartbeat age during dispatch, honoring documented waits; unfinished transcripts prove no stall.

## Review

A fresh reader reviews every branch, one-line changes included, with task, diff, constraints and evidence. Access-control changes get an independent stale-state review. Verify delegated claims against code before repeating them. Refresh checks and review after edits; the verdict names the final revision. Before a merge, the owner checks the verdict, required gates and every CI job, (lint, typecheck, build), not only suites rerun by hand. A red job is fixed, or proven red on the clean base with an owner and an action. A missing required PR body fails its gate. Merge gates fail closed: no required check on the head, no merge. Check gating claims by running the check yourself; a merge takes only the reviewed head.

Reviewer: confirm each required outcome and counterexample against the final revision, and check approvals and every gate result. Unresolved required failures block SHIP; unchecked paths stay unverified. Read `references/review-and-delegation.md` to dispatch or review.

## Commits

One logical change per commit. The scoped subject states behavior; the body records symptom, measured root cause, fix, deliberate limits and proof. Use locked dependencies; pin additions.

Agent: inspect `git show --format=fuller --stat`. Reviewer: compare the commit's claims with the diff and recorded evidence. Read `references/git-and-safety.md` before staging, pushing, stashing, rewriting history or removing worktrees.

## Autonomous and goal runs

When nobody reads each turn, keep going to the completion condition without asking, and stop only for a gate. Restate the goal and its condition, keep a run log, and decide what the owner's decisions and taste settle, recording each basis and how to overrule it. Stop only when a step could lose data, cause downtime, expose secrets or personal data, or reach outside the owner's systems or spend money the owner has not approved, with no safe path to remove the risk. A prompting guard is a gate too. Procedure: `references/autonomy.md`. Harness differences: `references/agent-capabilities.md`.

## Red flags that mean stop

- "I'll just bump the timeout" or "a third fix should do it": reproduce the cause and revisit the design.
- "Tests pass", "the worker said done" or "the gate was already failing": verify the goal and do not add failures.
- "The check was optional": an unproved required outcome stays unverified.
- "Probably still 8080", "a flag for later" or "nearby cleanup": read the source and keep the change in scope.

Reviewer: reject these; stop the claim and report the obstacle.
