# Autonomous runs and goals

Use this file for any run where nobody reads each turn: a goal run with a completion condition, an unattended worker, a scheduled job, or a brief that says to keep going. The owner wants these runs to finish without interruptions, except for decisions that can't be inferred from the owner's recorded decisions and taste.

## Goal runs

`/goal <condition>` (up to 4,000 characters) sets a goal, and a model evaluator decides when it is met. A new goal replaces the active one. `/goal` with no argument shows the status, and `/goal clear` (or `stop`, `off`, `reset`, `none`, `cancel`) removes it. The evaluator also ends the loop when it judges the goal impossible, when a turn fails on an error that needs a fix, or when it sees no progress for several turns in a row. A turn or time limit written into the condition is judged by the evaluator, not enforced. `claude -p "/goal ..."` runs the loop in one invocation.

A goal does not change the permission mode, and it does not lift per-tool prompts. For an unattended run, use the harness's auto mode or a permission setting that allows the run's routine tools, or a prompt will stop the run at a permission check.

A rule that must hold at a hard checkpoint, such as "confirm before a push", is enforced by the harness only when the harness has an ask rule for it. Where the harness supports one, add that rule. Where it does not, the rule still binds the agent by judgment, and the run reports that it was not enforced.

1. Restate the goal and its completion condition in the first step. Write both to the run log. Use the log path from the brief. If the brief names none, create `RUN.md` at the repo root (or in the run's worktree) and keep it out of commits.
2. Treat the condition as the stop test. Split it into required outcomes, and give each one an acceptance check before you start (see the Prove section of SKILL.md).
3. Work until every outcome has evidence on the final candidate. A long step, a slow test or a noisy log is not a reason to stop.
4. Keep the run log current at each checkpoint: what is done, what is verified, the decisions made, what is parked, and the next step. A fresh session must be able to resume from this file alone.

## Decision order

Before you ask anyone, work down this list. Stop at the first one that answers the question.

1. An explicit instruction in the brief or the owner's words in this run.
2. The owner's decision record. Search for it even when the brief names none: the project's memory directory, the CLAUDE.md or AGENTS.md files, the rules directory, and any decisions log in the repo. Apply the matching entry as written and cite it.
3. The codebase's established pattern. Find it by reading the neighbouring code and the recent history (`git log -- <path>`).
4. Your own call, using the simplest option that holds (see Simplicity first in SKILL.md).

Record every decision in the run log with four fields: the decision, the basis (which step above, with a citation), the cost if it is wrong, and how to overrule it. Repeat the list in the final report.

## Acting on an answer

When an answer unblocks work, start that work in the same turn. A gap of hours between an owner's answer and the first dispatch is a failure of the run, even if nothing else was idle.

## Writing answers back

When the owner answers a question or overrules a decision, record the answer in the decision record the same session: the decision, the date, the context and the scope it covers. A later run then finds the answer in step 2 and does not ask again. If the project has no record, create `DECISIONS.md` at the repo root and name it in the final report.

An answer that covers one case is recorded for that case only. Record a rule as a rule only when the owner states it as one.

## Gates: the only reasons to stop

Stop and look for a safe path, or ask, when a step:

- could lose data: a delete, an overwrite, a truncation, a destructive migration, or an acknowledgement sent before the bytes are durable;
- could cause downtime: a restart others depend on, a read-only window, or a blocked write path. A short checkpointed pause is fine when the report states the window;
- could expose secrets or personal data in output, logs, reports, tickets or commits;
- cannot be undone, reaches outside the owner's systems, or spends money the owner has not approved.

Remove the risk first when you can: copy the object aside and verify it by size and hash, use a canary, or prepare a rollback. Then proceed. A guard that prompts is a gate too. Work inside the guard and do not route around it.

Everything else is not a gate. Naming, formatting, tool choice, order of work, scope inside the brief and the choice between two reversible designs are all yours to decide.

## When a question is unavoidable

- No precedent, and the choice matters, but no gate applies: choose the most reversible option, record it, and continue. The owner can overrule it later.
- The rest of the work depends on the answer: park only the dependent items, finish everything else first, and then ask one question. Put the recommended option first and state exactly what is parked and what it blocks.
- Never ask a question you can answer from the decision order above.
- Ask only through the question tool (AskUserQuestion when it is available), with the recommended option first. A question written inside a reply is not an ask: nobody answers it, and the run stalls on it.
- Some harnesses have no question tool in headless or non-interactive mode, and some workers cannot call it at all. In those runs, park the item, finish everything else, and put the question with its recommended option in the final report. The report is then the ask.

## Keep the run visible

- A short status line at each checkpoint, in the run log and wherever the run reports. A silent stretch costs more trust than an early report of trouble.
- A blocker gets three things: what is blocked, what is still moving, and the next action. Then keep working.
- A worker's "done" is a claim. Check its artifact before you repeat it upward.

## Finish

The final report has five parts, in this order:

1. The outcome, with the evidence for each required outcome.
2. The decisions made, each with its basis and how to overrule it.
3. The gates hit, and the safe path taken for each.
4. What was not checked, stated outright.
5. Anything parked, with its owner and next action.

No loose ends. Every gap you noticed gets a fix, a named owner, or a question with its blocking cost. "Noted" and "worth a ticket" are not actions.

Commit or push only when the brief asks. Unattended runs commit locally and never push.
