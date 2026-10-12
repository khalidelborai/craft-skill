# craft

One agent skill for writing, building and reviewing code and prose. It asks agents to say only what is true, make the smallest change that holds, and prove it on the final revision. It also covers autonomous and goal-driven runs: keep going, decide from the owner's recorded decisions, and stop only at a gate.

The main file is `skills/craft/SKILL.md`, about 1,800 words. Detail sits in `skills/craft/references/`, one file per topic:

- `writing.md`: prose checks, batches of related texts, shortening without losing facts
- `proof-and-debugging.md`: tests, regression proof, root-cause debugging
- `review-and-delegation.md`: dispatch briefs, reviewer rules, plans
- `git-and-safety.md`: git gates, commits, worktree removal, secrets
- `autonomy.md`: goal runs, the decision order, the gates, the final report

## Install

With the [skills CLI](https://github.com/vercel-labs/skills), one command installs the skill into each agent's own skills folder:

    npx skills add khalidelborai/craft-skill -a claude-code codex kimi-code-cli

Add `-g` to install it for every project, and use `-a '*'` for every agent the CLI knows. To check what would change first, add `--dry-run`.

To install by hand, copy `skills/craft` into `~/.agents/skills/craft`, which the skills CLI uses for Codex and Kimi Code, and link it from `~/.claude/skills/craft` for Claude Code.

## Scope

The skill is general. It names no project, company or machine. Where a rule depends on a project, the skill says to read that project's own rules and checks.

## Licence

MIT. See `LICENSE`.
