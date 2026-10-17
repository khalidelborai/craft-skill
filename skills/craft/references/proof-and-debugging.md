# Proof, tests and debugging

Read this when you write or fix a test, prove a change works, or chase a bug. The core rules live in SKILL.md (Debug to the root cause, Prove what you claim). This file adds the methods behind them.

Contents: the break before the test; regression proof; the whole suite; verification and claims; acceptance on the surface the user sees; skipped tests and the target runtime; local end-to-end listeners; the CI job's own commands and labels that name who acted; side effects after a commit; reproduce before attributing; claims in the interface; what done includes; defect patterns and their checks; the debugging method; waiting on conditions; lean code and its checks; tuned knobs and debt.

## Name the break before the test

Before you write a test, name the production change that would make it fail. If you cannot name one, the test checks nothing.

- Derive the expected value by hand, from the spec or a worked example. Never compute it with the code under test, and do not assert a constant the code just returns.
- After the test passes, mutate the code in scratch: flip a condition, drop a branch, skip a call. At least one test must fail for each realistic mutation. A test that survives every mutation is a mirror of the implementation.
- Mock only the slow or external level (network, clock, disk). Assert on real behavior at every other level.
- Watch the test fail for the expected reason. A test that passes on its first run tests existing behavior; fix the test. A test that errors on a typo is not a red test yet.

## Regression proof for a bug

1. Write the regression test and run it on the unfixed code. It must fail for the reported behavior.
2. Apply the fix and run it again. It must pass.
3. Revert the fix in scratch and run it once more. It must fail again.
4. Restore the fix and record the command, the revision and the result.

The cycle shows the test guards the bug and not something adjacent.

## Run the whole suite

A green run of the test you wrote is not a green suite. Before you call a change done, run the project's full test command (the one the repo documents), and name every failure in your report, including ones you did not cause. The scope of a task limits the deliverable, but it does not limit the verification.

Check the suite on the tree you will integrate. A green run proves only the tree it ran on.

## Verification and claims

- A linter is not a compiler. Lint output does not prove the build passes, and a build does not prove the behavior works.
- Name the command you ran, the revision, the exit status and the relevant output. A status code alone is not proof of the goal.
- For a delegated result, check the diff or the artifact before you repeat the claim. An agent's "done" is a claim.
- If a check could not run, say so and leave the outcome marked unverified.

## Acceptance on the surface the user sees

A requirement about an output covers every surface that shows the output to a user: rendered pages, PDF, DOCX, spreadsheet and CSV exports, email, and UI strings. It also covers every product the requirement names. The owner can cut a surface explicitly. A plan that defers a visible surface is a question for the owner, and it is asked before anything is built. A builder that accepts a language parameter has not met the requirement. Acceptance is what the user sees after choosing the option, checked on the deployed target by rendering the page or walking the screen in a browser.

Translated output gets a page-image pass. Every visible token counts, including enum values, statuses, severities, chart labels, table headers and empty states. Names, URLs and identifiers may stay in their source language. Nothing else may. Walk every state in the second language, error, loading and empty included, with the longest realistic strings. Toggle the language on the page and check that dates and labels update without a reload. Use the product's own term for a module everywhere it appears.

A rule about what a customer may see covers every read path. A dashboard, a scheduled summary and an export are read paths. Enumerate them with a guard test, and keep the feature off for a customer until the guard passes.

A control must change the request it claims to. Before and after changing a filter, toggle or picker, record the request and show that the response changed. A control with no matching request parameter is hidden on that route rather than shipped.

An export covers every record that matches the active filters, not the first page. Run it on the largest tenant, compare the row count to the on-screen total, and open the file in the tool its user will use. Each column comes from a curated schema with a human label. No internal identifier, raw JSON or HTML appears in it.

Every number on the screen, in the export and in the file's digest comes from one source. Open each number in every surface that shows it, and check that the values agree.

A file format with no test in the suite is untested. Say so in the report instead of implying coverage.

## Skipped tests and the target runtime

Green CI is not proof when the decisive tests were skipped. Read the skip count in the test output. If the tests that matter need a database or a broker, run them against a real instance with its connection string set. Lint and smoke-test on the runtime version the target runs, not the version on the developer's machine.

## Local end-to-end listeners

A local end-to-end run proves the server under test only when that server owns the port it calls. Another process on the same port can answer for it, and a real server that fails to bind and exits leaves the impostor serving.

- Before starting the server, check the port (`lsof -nP -iTCP:<port> -sTCP:LISTEN`). If anything listens there, fail fast with the PID and command line, and pick another port.
- After the server starts, confirm the listener's PID is the process you launched and that its command line is the expected binary and arguments (`ps -p <pid> -o pid,command`).
- Make the launcher exit non-zero when the bind fails. The harness waits for readiness and fails when the process exits; it does not wait on a timer.
- Give each parallel worker its own port range, written in its brief, so two workers cannot share a port.

An unexplained one-off result is a defect until its cause is found. Reproduce it, identify which process answered and the first stage whose output is wrong, and fix or document the cause before the merge. A label such as "flaky" needs the same proof as any other claim. A first request that returns 200 with an empty result can be a stranger's server, and the listener check is the first thing to rule out.

## The CI job's own commands and labels that name who acted

A worker reports done only after it runs the commands its CI job runs. Take them from the workflow file, not from memory, and keep the flags and file lists exactly. A syntax check is not a style check. One project ran its style tool on a fixed file list inside a job, and a worker that checked syntax on every file reported "lint clean" while that job still failed.

1. Open the workflow file and copy each `run:` line of the job, with its file list, filters and flags (a style tool's file list, a test runner's `--filter`).
2. Run each one on the candidate revision. The evidence names every command, the revision and the exit status.
3. If a command needs a service or secret the worker lacks, say so and mark that job unverified. Do not swap in a nearby command.

A label that names who acted (an audit entry, a "changed by" field, a notification, a status tag) is checked against every role that can reach its code path, not only the roles the ticket names. Resellers and managed service providers can reach the screens that staff use. A label that reads "our staff" on a reseller's action is wrong. List the roles from the route guards or the permission matrix, run each one through the path, and read the label each time.

## Side effects after a commit

A side effect that runs after a committed write (a queue dispatch, a cache warmer, a notification) must not turn the write into an error. Bound the side effect with a timeout, log it with a reason code, and fall back to the essential synchronous step, such as invalidating a cache key. Test it with a dependency that throws, and confirm the write still succeeded.

## Reproduce before attributing

Before a failure is blamed on a change, reproduce it on the clean base. A failure that already exists on the base goes on a loose-ends list with an owner and an action. It does not go into the change under review.

## Claims in the interface

A success message comes from the server response, not from the click. Diff what was sent against what the server returned, and show that the two match. A destructive action asks for confirmation and names the object. A notification counts as delivered only when the provider reports it: show sent, failed and retrying states, never a success without a message id, and retry with backoff while logging each attempt.

A fix that reached production is checked on production. A fix can pass on staging and fail there.

## What done includes

Done is observed on the deployed target, not in the diff. It covers the unhappy path: oversized, reversed, duplicate and whitespace input, double clicks, slow networks and empty data. It covers every role and language the requirement names, and documented behavior equals live behavior, status codes included. A narrowed scope is stated, because silence about a cut reads as a defect. Done leaves no raw keys, identifiers, stack traces or SQL on screen, and it stays done after neighboring changes.

## Defect patterns and their checks

These patterns recur in review. Each one has a check to run before the change ships.

- A control that looks wired but is not: check that its request changes, as above.
- A list that stops at a silent cap or lacks a true total: cap every page size, return a true total, and reset the page index when a filter changes.
- An input nobody bounded: bound every free-text, list and enum field, and send one bad value per field to confirm a 422 with no internals.
- A fix applied to one module and not its siblings: grep the defect class before closing, fix it at the shared owner, or list each excluded caller and why.
- Two views of one record that disagree: open the record in every surface that shows it.
- Stale state, or loading shown as an empty state: after each change, check the list, the detail and the counters without a reload. Show loading and empty as separate states.
- A success message not taken from the response: see Claims above.
- Permissions that differ by route: run a matrix test per endpoint for owner, analyst, admin, other tenant and anonymous. Keep secrets out of bodies and hidden attributes.
- Contract drift between the docs and the live API: generate the schema from the code, and diff live responses against it in CI.
- Dead ends, and filters lost on reload: click every link, reload, and paste the URL into a new tab. Filters live in the URL.
- A dashboard count that does not match the list it links to: click through and compare totals under the same filters, and state the scope on screen.
- Overlays clipped or mis-anchored: open each at the first and last row, scrolled, on the narrowest viewport and in right-to-left.
- Forms that accept bad input: submit empty, whitespace, duplicate, wrong-type, over-long and unchanged values.

## Debugging method

Find the root cause before you change code. The sequence is:

1. Read the full error, including stack traces and line numbers. Reproduce it on demand. If it does not reproduce, gather more data before you guess.
2. Check recent changes: the diff, recent commits, dependency and config changes, and differences between the failing and working environments.
3. For a bug that crosses components (CI to build to signing, API to service to database), log what enters and leaves each boundary, run once, and find the first stage whose output is wrong. Then investigate only that stage.
4. Trace the bad value backward to where it enters. Fix it at the source, not where it surfaced. A stack-trace log placed before the risky operation helps when the source is deep in the call chain.
5. Form one hypothesis, written as "X causes Y because Z". Make the smallest change that tests it. One variable at a time.
6. Count the fixes you have tried. After three failed fixes, stop and question the design. Each fix that removes the symptom and moves the failure elsewhere is a sign the design is wrong.

### When to stop localizing

Stop once one candidate explains the symptom and a focused read shows a minimal fix. Reopen the search only when the source contradicts the explanation or more than one candidate remains. A data-flow result is not proof of the cause; cross-function bugs still need the compiler or a test that reaches them.

### Waiting on conditions

Fix a race by waiting for the state that must hold, not by lengthening a sleep or a timeout. A fixed wait is allowed only when the timing is measured and documented next to the code, with the condition it stands in for and the ceiling it assumes.

## Lean code and its checks

These rules keep a fix small without skipping its proof.

- Before you change a shared function, grep every caller. Fix the shared owner once, so the callers inherit the fix. Patching one caller leaves its siblings broken.
- Never remove validation at a trust boundary to simplify code. Validate once at the boundary and trust the value inside it.
- Trivial one-line changes need a run of the existing check, not a new test. Non-trivial logic (a branch, a loop, a parser, a money or security path) needs one runnable check: the smallest test that fails if the logic breaks.
- A deliberate shortcut carries a comment that names its ceiling and the condition for upgrading it. An unexplained shortcut reads as a mistake.
- Before you write a new helper, search for an existing one. Re-implementing a helper a few files away is the most common duplication.

## Tuned knobs and debt

A constant that was tuned by measurement stays visible: name the value, the measurement behind it and the trigger for revisiting it. A marker comment with no trigger is debt that nobody will collect. Scan for such markers during review and give each one a trigger or delete it.
