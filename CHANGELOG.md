# Changelog

Each release lists what changed and why, newest first.

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
