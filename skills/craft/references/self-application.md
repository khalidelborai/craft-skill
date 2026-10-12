# The skill applies its own rules

Read this before you change the skill or cut a release, to see which check covers each rule.

This skill is held to the same standard it sets for other work. Before a change to the skill ships, each rule below has a check, and the check runs on the final files. A rule without a check is a wish, so the table names the check for each one.

## Checks for the skill's own text

| Rule | Check | Who runs it |
| --- | --- | --- |
| Prose has no dashes, curly quotes or ellipsis character | grep for the characters in SKILL.md and references/ | release script |
| Prose passes the lint, including verbless fragments and bolded lead-in bullets | the project's prose lint, exit 0 on each file | release script |
| No owner-specific names, hosts or personal machine paths; generic harness paths such as ~/.claude/skills are allowed | privacy scan with the names listed in the script | release script |
| The description states triggers only, under 500 characters | length and form check on the frontmatter | release script |
| Every reference is linked from SKILL.md and every link resolves | link check in both directions | release script |
| The rubric's rows still map to real case files | count the rows and resolve each case ID | release script (private repo) |
| SKILL.md stays near its size budget | word count against the budget in the release script | release script |
| Each rule states how it is checked | a reviewer reads the table and the rules it covers | fresh reader before release |
| The public copy matches the source on the final revision | compare the synced files byte for byte | release script |

## What a release proves

A release proves the checks above on the candidate files. It does not prove that agents follow the rules. Agent behavior is checked separately with the rubric in `evals/`, on transcripts from real runs, and the release notes say which of those runs were graded.

## When a rule changes

A change that adds text to a file the agent always loads, such as the short form in an instruction file or a section of SKILL.md that every run reads, ships only with a paired run. The paired run uses the same task on the same harness, once with the text and once without it. The change ships when quality holds: no case that passed before fails, and the treatment is not graded lower on any case. Cost, turns and time are recorded and reported, but they do not gate a release. The goal is better work, and a faster or cheaper run that does worse work does not count as an improvement. Context files help agents follow non-standard practices, but a repository overview does not improve results, so add only the rules an agent cannot infer from the code.

A change to a rule comes with its check in the same change. If no machine check can cover it, name the reviewer who checks it, and say so in the release notes. A rule that weakens another rule, or raises a budget, needs an explicit owner decision recorded with its reason.
