# Changelog

Each release lists what changed and why, newest first.

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
