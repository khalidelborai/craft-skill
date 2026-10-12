# Agent capabilities that change these rules

Read this when you run craft in a specific harness, or when you write a brief for an agent you have not used before. The rules in SKILL.md and the other references hold for every agent. This file lists where the harness changes how a rule is applied.

Each entry gives the skill directory the agent reads, whether it has a structured question tool in headless mode, the flag or setting for unattended runs, and whether it adds a commit trailer by default. Where the official docs did not say, the entry says so. Check the harness before you rely on an entry.

## Harnesses

Claude Code reads `~/.claude/skills`. Its question tool, AskUserQuestion, cannot be called from a subagent. Unattended `-p` runs need the permission-prompts setting turned off. `/goal` takes a condition and keeps working toward it. It does not lift per-tool prompts. Commit trailers depend on the `attribution.commit` and `attribution.pr` keys, so check them before you assume a trailer.

Codex reads `~/.agents/skills`. Its `request_user_input` tool does not run under `codex exec`, so an unattended run parks the question and reports it. Codex can add a `Co-authored-by` trailer. Its Stop hook can continue a turn when it returns a block decision. A child agent inherits the parent's model unless the spawn request sets one.

Kimi Code reads `~/.agents/skills`. Its question tool is denied in Never Ask mode and in headless mode. `kimi -p` rejects `--auto`, so the auto preference applies only to interactive runs. A subagent can keep the caller's model with `model: primary`, but that option needs a configured secondary model.

Command Code reads `~/.commandcode/skills`. Its `ask_user_question` tool is withheld under `-p`, and enabling it picks the first option, so an unattended run must not enable it. Its `--yolo` flag removes every check. Its commit trailer is on by default. Its goal pauses after three rejected checks and reports a pause, not a finish. Once about 42 skills are installed, it stops sending skill descriptions to the model and sends only names. The trigger for craft therefore has to appear in the instruction file as well as in the skill.

Qwen Code reads `~/.qwen/skills`. In headless mode its question tool returns an error, so the question goes in the report. A headless run needs `--approval-mode yolo` or an allow list, or each confirmation-gated tool fails. It adds a commit trailer by default, and `gitCoAuthor.commit` turns that off. It also adds a "Generated with Qwen Code" line to pull request bodies made by `gh pr create`, and a git note on commits. Auto-compaction starts at 85% of the window.

Gemini CLI reads `~/.gemini/skills` and `~/.agents/skills`. Its ask tool is `ask_user`, and headless behavior is not documented. Google announced that individual subscribers lose Gemini CLI access on June 18, 2026, so check which Gemini product is in use before writing Gemini rules.

Cursor reads `.agents/skills` and `.cursor/skills`. Its subagents take a `readonly` flag. No ask tool is documented. Cloud agents do not load user-level skills, so a brief must carry the rules. Project rules must be `.mdc` files. Forum reports describe a `Co-authored-by` trailer with an opt-out, and the docs do not confirm it.

GitHub Copilot CLI reads `.github/skills`, `.agents/skills` and `~/.copilot/skills`. No ask tool is documented. Its autopilot mode stops when the agent judges the task done, when a problem blocks progress, or at the continuation limit. Its `--allow-all` flag grants every tool. Its instruction file is `.github/copilot-instructions.md`.

OpenCode reads `~/.config/opencode/skills` and `.agents/skills`. Its question tool is documented for interactive use only. Its `--auto` flag approves permissions that are not explicitly denied. Subagents run through the `task` tool and take a model setting.

Devin Desktop, the renamed Windsurf, reads `.devin/rules` and falls back to `.windsurf/rules`. Its Turbo mode runs every command except those on the deny list. Its hooks can block a command. Its question tool is not documented.

Droid reads skills and its hooks can block a tool call. Subagents cannot ask the user. `droid exec` starts read-only, and an unattended run needs `--auto medium` or higher.

Kiro CLI reads `.kiro/skills` and `~/.kiro/skills`. Headless runs need `--trust-tools` with exact tool IDs, because no user can approve a call.

Zed reads `.agents/skills` only from trusted worktrees. Its instruction loader takes the first matching file from a fixed list, so a project with a `.rules` file never reads its `AGENTS.md`. An unattended run needs `agent.tool_permissions.default` set to `allow`.

Hermes Agent reads `~/.hermes/skills` and loads reference files on demand. Approval denies by default in unattended and cron runs. Its subagents cannot use the clarify tool. The docs give two different default numbers for concurrent subagents, so check the number in the installed version.

Goose reads `.agents/skills`. Its autonomous mode is the default, but its docs conflict on the default permission mode.

Junie reads `.junie/skills` and `.agents/skills`. Unattended approval depends on Brave mode, which is set per run.

Warp reads `.agents/skills`. Its denylist takes precedence over its allowlist. Unattended runs need a profile that allows the routine tools.

Cline reads skills from `.cline/skills` and `~/.cline/skills`, not from `.agents/skills`. Its subagents run in parallel in the CLI and desktop apps.

Amp, Roo Code, Augment, Continue, Replit, Trae, Pi and Devin (the terminal agent) read `SKILL.md` folders. Their question tools, hook behavior and commit trailers are not documented well enough to write rules for them. Pi needs no change.

## Harnesses that cannot read skills

Some agents in the skills CLI list have no documented skill directory. Reasonix reads flat `.reasonix/skills/<name>.md` files, OpenClaw reads `<workspace>/skills`, and Deep Agents takes its path from the host app. For these, paste the rules into the brief or the instruction file the agent reads.

## What holds everywhere

No harness here gives a subagent a reliable question tool, so every brief says how to park a question. Every harness that can auto-approve needs an explicit setting for unattended runs. Every harness that adds a trailer by default needs the attribution setting checked before a commit. A stop by a goal, a pause or a turn limit is a stop, and the run log records it as one.
