# Git, commits, branches, worktrees and safety gates

Read this before you stage, commit, push, merge, rewrite history, remove a worktree, or run a step that deletes, overwrites or changes shared state. The core rules live in SKILL.md under Commits and the Build it to hold section. This file holds the git gates in full.

## Git state is a gate

- Never stash, reset, clean, switch away from, or check out over another owner's uncommitted work. Preserve every dirty checkout you did not create.
- Stage named paths only. Do not stage with `git add -A` or `git add .`. Review the staged diff with `git diff --cached` before you commit.
- Rewrite history only on a branch you have shown to be private to you. Use `--force-with-lease=<branch>:<oid>` with the OID you reviewed. An unconditional force push is not allowed.
- After a push, the remote OID must equal the HEAD you reviewed. If the remote moved, the push was rejected for a reason: fetch, look at what changed, and decide again. Never force a rejected push.
- Confirm the base before you merge or rebase. A merge into the wrong base is expensive to undo.
- Do not pass `--no-verify`, `--no-gpg-sign` or a force flag to a protected branch unless the owner asks for it in this run.

## Merging the reviewed head

Merge only the head that was reviewed, and pin it: `gh pr merge --match-head-commit <sha>`. After the merge, check whether the branch gained commits after that head. Commits that landed after the review are unreviewed, so they need their own pull request.

Merge automation fails closed. No required check on the head means no merge, and a check marked ignored does not count as passing. One PR nearly merged when its only checks were ignored ones. A conflict shape the automation does not recognise stops the run; it does not guess a resolution.

## Commits

- One logical change per commit. Keep formatting-only edits in their own commit.
- The subject states the behavior that changed, in the imperative mood, with a scope when the repo uses scopes.
- The body records the symptom, the measured root cause, the fix, the limits you chose not to change, and the proof.
- Do not add co-author lines or tool attribution unless the repo's policy or the run's brief asks for them. Before you assume a trailer exists or is absent, check the harness's attribution setting, because harnesses differ: some add a trailer by default and some can be configured to add one. When a harness supplies an attribution line, follow the repo's policy.

Text in this skill cannot remove a trailer that the harness adds by default. In a controlled test, Claude Code added a co-author line to every commit, with and without the skill loaded. Setting `attribution.commit` to an empty string in the harness settings removed it. Where a harness offers such a setting, set it and check the last commit message.
- Commit or push only when the brief asks. An unattended run commits locally and never pushes.
- Stop before committing to a protected branch. Create a feature branch first.
- Never stage secret-like paths: `.env` files, `credentials` files, `*.pem`, `*.key`, and anything the repo's ignore rules were written to hide. If one is staged, unstage it and tell the owner.

## Verifying a push or deploy

A push, a merge, a green workflow or a deployment record proves only itself. A green CI run does not prove that a deployment reached users. Check the live target with the same command or request that users would make, and record the staging proof against the exact commit or image digest that was tested.

A ready deployment or a mutable tag does not prove that traffic moved. Check the serving route.

Record merge, build, rollout and external smoke test as four separate results.

Stop before any step that makes a destructive migration, adds a paid vendor, changes the scope of the release, or passes a production gate without the owner's approval.

## Worktrees

Use one worktree per task and treat it as disposable. The branch holds the work. The checkout is scaffolding.

- Before you create a worktree, confirm that the project-local worktree directory is ignored by git. Creating one that is not ignored leaves untracked state in the repo.
- Prefer the repo's worktree helper if it has one. A raw `git worktree add` is the fallback.
- Build output (`target/`, `node_modules/`, `dist/`) is per worktree and is not shared. Delete it when the branch is merged or abandoned.
- Never `git stash` in a worktree of a shared repo. All worktrees share one stash list. A stash that saved nothing, followed by a pop, applies another worktree's older entry on top of your branch. To test against the base, write the base version of the few files involved to a scratch path, or use a second detached worktree at the base commit.

### Removing a worktree is a data-loss gate

Do not remove a worktree with a bare `git worktree remove` followed by `git worktree prune`. Git refuses to remove a checkout with modified or untracked files, but it does not refuse ignored files. Ignored build output and ignored deliverables disappear with no archive.

The safe sequence:

1. Refuse if the checkout has uncommitted tracked edits. Commit or hand off that work first. Never force a removal past tracked edits.
2. Find untracked and ignored files that matter, such as deliverables, reports and local data. Copy them to an archive outside the repo and verify each copy by size and hash. A failed copy stops the teardown.
3. Stop every process that writes into the worktree.
4. Clean the build output (`cargo clean` or delete the build directory).
5. Remove the checkout with `git worktree remove`, then run `git worktree prune`.
6. Delete the branch only after you confirm it is merged, with `git branch --merged`.

Never remove or nest a worktree that the current task did not create.

## Rule files and checks

- A rule that says "never" needs a check that enforces it, or a named reviewer who checks it. A rule with neither is a wish.
- Pin a dependency you add, and reference the lock file a reviewer will read.
- Before a push, run the checks the repo documents, on the tree you will push. A green run on another tree proves nothing about this one.

## Helper scripts and worktree dependencies

A helper script validates its arguments and stops at the first failed step: `set -euo pipefail`, and check each path before the first write. Never let a pipeline hide a failure. A `cd` that fails inside `cmd | tail` exits 0, and the script runs on in the wrong directory.

Each worktree gets its own copy of its dependencies. On APFS, `cp -cR` clones a directory at almost no disk cost. A symlinked vendor directory loads the sibling worktree's code, so a test in one worktree can exercise another one's code. Before trusting a result, confirm which file a class loads from with a reflection check, for example `(new ReflectionClass(Foo::class))->getFileName()` in PHP or `__file__` in Python.

A shell loop that changes state counts its successes and never hides its output. An unquoted variable in `for q in $L` is not split into words in zsh, so the loop ran one delete with 46 names joined into one argument, and `>/dev/null` hid the failure. Read the list with `while read -r q; do ...; done <<< "$L"`, count the successes, and print the failures.

## One-off scripts and processes

A one-off Laravel script is a standalone PHP file that boots the kernel itself: require the autoloader, build the app from `bootstrap/app.php`, then bootstrap the kernel. `php artisan tinker` waits for terminal input, so it hangs in a non-interactive run.

Never `pkill -f` a pattern from your own command line. The pattern also matches your shell, so the command kills itself. Stop the PID you started, or match an exact process name.

## Secrets

Secret values never appear in output, logs, commits, reports or prompts. Describe where a secret lives (the file, the store, the variable name) and never copy the value. If a secret does appear in output, say so, flag it for the owner, and do not repeat it. Rotation is the owner's call, unless the brief gives you the authority.
