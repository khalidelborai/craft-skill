# Review, delegation and plans

Read this when you dispatch work to another agent, review a branch, act on review feedback, or write an executable plan. The core rules live in SKILL.md under Plans and decisions and Review. This file gives the mechanics. Where a source skill conflicted with those core rules, the core rule wins and the conflict is recorded in the owner's decision list.

## Subagent rules

These rules hold for any subagent, whatever the harness. The harness details differ, so check them when you dispatch.

1. A subagent gets one task and a brief that holds everything it needs. It does not get the session history.
2. Assume the subagent cannot call the question tool. The brief tells it to park each question in its report and stop only at a gate.
3. Name the model in the brief when the result depends on it. Some harnesses let a child inherit the parent's model, some need an explicit override, and some let the parent choose per dispatch. Find out which one the harness uses before you rely on it.
4. Give each subagent the permissions its job needs. A reviewer gets read-only tools and does not edit or switch branches. An unattended worker needs allow rules for its routine tools, or its first prompt stops the run.
5. Run subagents in parallel only when their file sets and shared state do not overlap. Keep the number of concurrent children within the harness's limit. Do not assume a limit; check it.
6. Do not nest review. A reviewer does not spawn reviewers and does not hand part of the review to another agent.
7. Use a fresh subagent for each task. Resume a subagent only for a fix round on the same task, because it still holds the context of its own change.
8. Treat a subagent's "done" as a claim. Check its diff or artifact before you repeat the claim, and spot-check the result.
9. Wait in bounded intervals and read the report file. Absence of a report is not proof of failure. Stop or retry a subagent only on positive evidence.
10. Commits made by a subagent follow the git rules. An unattended subagent commits locally and never pushes.
11. A subagent deletes nothing outside its own worktree or the temporary paths it created and recorded. A shared temporary directory is not its to clear.
12. The coordinator checks any subagent claim that gates a merge by running the check itself: the golden file unchanged on the base, the page rendered, the tests run with real dependencies. The report is not the check.

## Dispatching work

A dispatch brief is a contract. It carries:

- one line of project context and the path to the task's brief file;
- the interfaces that earlier tasks produced, copied in, so the worker does not need the session history;
- the coordinator's answer to every ambiguity the worker might hit;
- the path where the worker writes its report.

A brief describes one task. It does not paste the session history, the earlier discussion or the reasoning behind the plan, unless the worker needs a specific fact from it.

The brief tells the worker how to stop. Many workers cannot call the question tool, so the brief says to park a question in the report and stop only at a gate. Name the model in the brief when it matters, because some harnesses let a child inherit the parent's model.

Set the model explicitly on every dispatch. A worker that hit a failure gets a changed brief or a stronger model before a retry. The same model with the same brief fails the same way.

Workers report one of four statuses: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT` or `BLOCKED`. A worker that reports `NEEDS_CONTEXT` or `BLOCKED` gets an answer or a new brief. Nobody ignores an escalation.

Dispatch in parallel only when the tasks touch different files and share no state. Two workers that edit the same file interfere, so run them one after the other.

Batch same-shaped edits into one dispatch instead of many small ones.

## Checking delegated results

After a worker returns, check its claim against the diff and the artifact before you repeat it. Then:

- check for conflicts between the workers' changes;
- run the full project suite on the combined tree;
- spot-check two or three changed lines by reading them, because a worker can make the same systematic mistake in several places.

Wait in bounded intervals, five to ten minutes each, and send one status line between waits. Absence of a report is not proof that the worker failed. Stop, abandon or retry a worker only on positive evidence: an error in its log, an exit status, or a missing heartbeat over an interval the brief set.

## Reviewing a branch

A fresh reader reviews the branch with the task, the diff, the constraints and the evidence. Give the reviewer the context it needs, not your reasoning.

Reviewer rules:

- The reviewer is read-only. It does not switch branches, move HEAD or edit files.
- The reviewer does not hand part of the review to another reviewer.
- The reviewer does not tell the author to ignore a finding. It reports what it saw and leaves the call to the author.
- Record the base commit before dispatch and diff against that recorded commit, not against `HEAD~1`. A base recorded in advance cannot drift.
- Keep a "declined to judge" list. Each behavior the reviewer set aside gets a reason, so the author can rule on it.
- Check the change against the spec, and also check the behavior the spec does not mention. Silence in the spec is not permission.

Report the review with the verdict first, then the findings in order of severity, then what the reviewer did not check.

## Reusing UI components

UI work reuses the product's existing components and patterns before it builds anything new. Search for the component first, and reuse it as it is. A new screen that needs a card, a table, a filter or a dialog uses the one the product already has.

When the right component lives in one product module and another module needs it, move it to the shared library both modules import, and repoint every caller to that copy. One owner holds the component. Copying it, or writing a lookalike with the same look, creates two components that drift apart. Nothing in the move is optional: the old location is removed, so no second copy remains.

Example: a review step was asked to match the new dashboards' cards. The card component lived in one module, so it moved to the shared theme library, and the review step and the dashboards both import it from there.

## Checking every CI job before a merge

The suites you ran by hand are not the whole gate. Before a merge, list every check on the PR with `gh pr checks <number>` and read each job, including lint, typecheck and build. For each red job:

- Run the same job's command on a clean checkout of the base commit. If it passes there, the PR caused it, and the PR is fixed before the merge.
- If the base already fails it, record an owner and an action on the loose-ends list, and name both in the merge note.

A lint rule can catch what every test passes. A static import of a lazy-loaded module, for example, fails lint and runs fine in tests. A red lint job left on an integration branch fails the next PR that merges on top of it.

## Copying a rule into another service

Before a rule goes into a second service, map that service's customer-facing outputs with file and line: every response field, export, notification and page the rule touches. Keep one owner of the rule. Pin the other copy with a cross-repo contract test that fails when either side drifts. One sync-side filter dropped data that an off switch was meant to restore, and a shared test would have caught it.

A claim that nothing reaches customers is checked by reading every caller and every scheduler yourself. A summary is not the check.

## Reviewing access-control changes

An access-control change gets an independent review from a reader who did not write it. A second model is acceptable. The reviewer's first question is where the authority comes from at request time. Authority that comes from a session, a cached selection, a token claim or a permission cache can outlive the membership that granted it.

The stale-state pass checks, for each path that grants access:

- Which state holds the grant: the session, a selected team or tenant, a token, a cache. How long it lives, and what clears it.
- What happens when the membership changes mid-session. A user who has left a team must lose that team's cross-tenant reads on the next request, not at the next login.
- Whether the test that claims to cover the path reaches it, or seeds the state and skips the path.

One review found a selected team that a user had left still authorizing cross-tenant reads. The change had passed its tests, because none removed membership in a live session.

## Acting on review feedback

Treat each finding as a claim to check against the code. Then:

- Grep for the real usage before you add a feature a reviewer suggested. An unused endpoint gets removed, not made "professional".
- You fix blocking findings first, then simple ones, then complex ones. Test each fix on its own.
- For a finding you reject, give the reason with evidence: the test that shows the behavior, the caller that depends on it.

Verdicts on a re-review use two states: `ADDRESSED` or `NOT ADDRESSED`. An attempted fix is not addressed. The re-review checks the fix against the finding, and it re-runs the checks that the fix could have affected.

A minor finding that does not block the change goes on the list for a later change. It does not enter the current fix pass.

## Plans

An executable plan resolves every name, signature, value and test that the implementer could not choose alone. A plan with a "TBD" or "similar to the step above" has deferred a decision, so resolve it before anyone executes the plan.

Write each task so it carries its own test cycle. The smallest unit of work that can be tested on its own is a task. Each task lists:

- what it consumes: the interfaces and files it reads from earlier tasks;
- what it produces: the interfaces and files it hands to later tasks.

A worker sees only its own task, so these two lists are the whole contract between tasks.

Before execution, build a conflict table with one row for each pair of tasks that share a file or an interface. Tasks in a row run in sequence.

Use a code body in a plan only where the signature and the tests leave a real choice open. Otherwise give the signature and the tests and let the implementer write the body. A plan that transcribes the program has stopped being a plan.

Add a review focus list for each feature: the inputs the spec implies but no test covers, each with the test that covers it.

## Freezing a contract before parallel work

Before workers build both sides of an interface in parallel, freeze the contract as an artifact they both code to. Use an OpenAPI fragment or a shared types file, with example requests and responses for every status, every error and every dry run. Nullable and approximate fields belong in the contract, and their shape is written down. Each side gets a contract test against those examples. A change goes to the contract first, then to both sides. Diff live responses against the contract in CI, so drift fails the build.

A prose contract diverged once on dry-run behavior, error shape and whether a figure was exact. That cost a relay and a second frontend pass.

## Progress and recovery

Keep a ledger with one line per completed task, written in the same step as the commit. After a context compaction, trust the ledger and the git log over memory. A remembered fact about progress is a lead to check.

Record each plan change with the reason and the cost if it is wrong. A change made in a message that no file records is gone after compaction.

## Orchestration status

A successful send proves that the message was accepted, not that the recipient read it. Confirm the recipient started work before you rely on it. An input the worker must act on, such as a file path or an answer, goes into a fresh dispatch's brief, or the send is confirmed acknowledged. A message sent while the worker was busy may never have been read. One such message waited 30 minutes. A timeout or an empty wait is a checkpoint and not a failure. Only positive evidence stops, abandons or retries work.

A dispatch receipt proves that the worker was created. It does not prove that the worker runs. Within a minute of dispatch, look at the worker's screen. A spinner, a tool call or new output shows work. A worker waiting at a prompt, such as a per-worktree trust or permission prompt, is not running, however long it has existed. Recheck the screen before every status report, and report a worker as running only on that check. A later done message does not repair an earlier silent interval.

One batch of five workers sat at a per-worktree trust prompt for an hour while the coordinator reported them as running. The user caught it. Clear the prompt, and only then report the worker as running.

The coordinator reads every message that is not a heartbeat, of every type. A filter that drops one message type can hide a worker's contract change for an hour. Filter heartbeats only.
