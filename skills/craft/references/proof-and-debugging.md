# Proof, tests and debugging

Read this when you write or fix a test, prove a change works, or chase a bug. The core rules live in SKILL.md (Debug to the root cause, Prove what you claim). This file adds the methods behind them.

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
