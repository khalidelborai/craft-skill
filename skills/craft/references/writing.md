# Writing that reads as a person wrote it

Read this before you ship text that leaves the machine: docs, reports, commit messages, PR bodies, messages, and chat answers. The short rules live in SKILL.md under Writing like a human. This file adds the checks, the batch rule and the method for shortening.

## The checks

Run the project's prose lint on the text before it ships, when one exists. Point at the script with a variable, not a fixed path:

    python3 "$AI_TELL_LINT" FILE      # exit 0 is clean
    python3 "$AI_TELL_LINT" --text "one string"

If no lint is available, say so in the report and check the rules below by reading. A flagged word that reads naturally in its context stays. The lint finds candidates; you judge them. Do not reword a sentence just to clear a word the lint dislikes when the sentence already says the thing plainly.

Keep the banned vocabulary inside inline code when you quote it, so a lint that skips code spans does not flag your own rule list.

## Shape

- Lead with the verdict and the observable change, in plain words. Then the evidence. Then what you did not check.
- Keep every citation and every observed fact when you shorten. You drop the scaffolding first.
- Give every sentence a finite verb. A list item that is a noun phrase with no verb reads like a crafted beat. Turn it into a sentence.
- Vary sentence length because the content calls for it. Do not aim for a numeric quota of words per sentence, and do not hold a fixed rhythm across a document.
- Use contractions where they fall naturally. Long prose with none reads generated.
- Use ordinary punctuation. Write straight quotes, commas, periods and parentheses. Do not use em or en dashes, the ellipsis character or curly quotes.
- Avoid a bolded label at the start of each bullet as the default answer shape. Plain sentences or a short table usually carry the content better.

## Words and patterns to avoid

Avoid the AI-register vocabulary in the banned list (`delve`, `leverage`, `robust`, `seamless`, `comprehensive`, `crucial`, `notably`, `genuinely` and their kin). Avoid rhetorical contrasts such as `not just X but Y`, rhetorical triples, negation kickers such as `no frills`, assistant voice such as `I hope this helps`, and essay furniture such as `in conclusion` or `worth noting`.

Open point for the owner: "robust" and "comprehensive" are banned in this skill, while the lint's source list allows them inside engineering contexts such as "robust error handling". Until the owner decides, follow the banned list here and rephrase in engineering text with a specific claim (for example "retries three times with a 2 s timeout").

## Batches of related texts

A set of related texts (worker reports, several PR bodies, a series of briefs, a batch of rationales) fails when the texts share a skeleton even though each one reads fine alone. Check the batch as a whole:

- No two texts share an opening sentence pattern.
- No two texts share a scaffold, such as the same headings in the same order.
- No four-word run repeats across texts, unless it is a term of art.
- Lengths vary with the content.

You change the structure first and the wording second. The evidence stays the same in every text.

## Shortening without losing content

Before you edit a passage to make it shorter, list every proposition in it: who acts, under what condition, what is required, what is forbidden, what is guaranteed, and what happens on failure. Then write the shorter version and check that every proposition still appears, with the same condition and the same negative guarantee. A smaller word count alone does not make the text better. A missing failure case makes it worse.

## Skills and rules you write

A rule in a skill or a rules file needs its scope and its check. State what it covers and what it does not. Name how it is checked: by a machine, by a reviewer, or by the agent with a named command. A rule that cannot be checked is a wish, so either add a check or cut the rule.

Keep a rule to a few lines and link to the detail. A reference file holds the detail and the examples.

## Remembered facts in documents

A fact recalled from memory is a lead to re-verify, not evidence. Before a document states a value, a path, a version or a status as current, read it from its source, and cite the source where it helps the reader. Strip names, private paths and one-machine state from any text meant for other people or other machines.
