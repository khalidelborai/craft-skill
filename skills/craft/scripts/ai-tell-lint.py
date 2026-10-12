#!/usr/bin/env python3
"""ai-tell-lint - find AI-writing tells in prose.

Usage:
  ai-tell-lint.py FILE [FILE...]      lint files
  ai-tell-lint.py --text "..."        lint a string
  echo "..." | ai-tell-lint.py -      lint stdin
  ai-tell-lint.py --json FILE         machine-readable

Exit 0 = clean, 1 = tells found, 2 = usage error.
Prose only: code blocks, inline code, URLs and file paths are stripped before checking.
"""
import sys, re, json, os

# ---------- tells ----------
HARD = [
    ('\u2014', 'em dash (use a comma, a period, or parentheses)'),
    ('\u2013', 'en dash'),
    ('[\u201c\u201d]', 'curly double quote (use straight ")'),
    ('[\u2018\u2019]', "curly single quote (use straight ')"),
    ('\u2026', 'ellipsis character (use three periods or rewrite)'),
]

WORDS = [
    # inflated register
    'delve', 'leverage', 'utilize', 'robust', 'seamless', 'seamlessly',
    'comprehensive', 'meticulous', 'meticulously', 'crucial', 'pivotal',
    'vital', 'paramount', 'myriad', 'plethora', 'realm', 'landscape',
    'tapestry', 'testament', 'beacon', 'nuanced', 'holistic', 'multifaceted',
    'underscore', 'underscores', 'showcase', 'showcases', 'elevate', 'elevates',
    'empower', 'empowers', 'unlock', 'unlocks', 'transformative',
    'game-changing', 'cutting-edge', 'state-of-the-art', 'best-in-class',
    # hedge/filler adverbs
    'notably', 'crucially', 'importantly', 'significantly', 'fundamentally',
    'essentially', 'ultimately', 'arguably', 'genuinely', 'thoroughly',
    'effectively', 'efficiently', 'seamlessly',
    # connectives nobody types
    'moreover', 'furthermore', 'additionally', 'consequently', 'nevertheless',
    'nonetheless', 'thereby', 'whilst', 'amongst', 'hence',
]

PHRASES = [
    # "harness" is a real noun in agent/test work; only the verb sense is a tell
    (r'\bharness(?:ing|es)?\s+(?:the\s+|its\s+|their\s+|full\s+)*(?:power|potential|strength|capabilit|might|value)\w*',
     'harness-the-power (verb sense; the noun "test/agent harness" is fine)'),
    (r"\bit'?s (?:not just|not merely|not only) .{1,40}?,? (?:it'?s|but)\b", 'not-just-X-but-Y construction'),
    (r'\bnot (?:just|merely|simply) .{1,30}?,? but\b', 'not-just-X-but-Y construction'),
    (r'\bisn\'?t (?:just|merely) about\b', 'isn\'t-just-about construction'),
    (r'\bat the end of the day\b', 'filler idiom'),
    (r'\bwhen it comes to\b', 'filler idiom'),
    (r'\bin (?:today|this day and age)\b', 'filler opener'),
    (r'\bworth noting\b', 'hedge filler'),
    (r'\bit(?:\'| i)s worth (?:noting|mentioning)\b', 'hedge filler'),
    (r'\bthat said\b', 'pivot filler'),
    (r'\blet\'?s (?:dive|delve) (?:in|into)\b', 'filler opener'),
    (r'\bdive deep(?:er)? into\b', 'filler idiom'),
    (r'\bplays? a (?:key|vital|crucial|significant) role\b', 'empty claim'),
    (r'\ba (?:double-edged sword|silver bullet)\b', 'stock metaphor'),
    (r'\bthe (?:key|secret|trick) (?:is|lies) (?:in|to)\b', 'stock construction'),
    (r'\bnavigat(?:e|ing) the (?:complex|complexities|landscape|world)\b', 'stock construction'),
    (r'\bin conclusion\b', 'essay closer'),
    (r'\bto sum(?: it)? up\b', 'essay closer'),
    (r'\bI hope this helps\b', 'assistant closer'),
    (r'\bfeel free to\b', 'assistant closer'),
    (r'\blet me know if\b', 'assistant closer'),
    (r'\bgreat question\b', 'assistant opener'),
    (r'\byou\'?re absolutely right\b', 'sycophantic opener'),
    (r'\bcertainly[!,.]', 'assistant opener'),
    (r'\b(?:here\'?s|this is) (?:the|a) (?:comprehensive|complete|detailed) (?:guide|overview|breakdown)\b', 'brochure voice'),
    (r'\bensur(?:e|ing) (?:that )?(?:you|we|it) (?:can|are able to)\b', 'padding'),
    (r'\bwhether you\'?re .{1,40}? or\b', 'brochure voice'),
    (r',\s*(?:and\s+)?(?:nothing|no)\s+(?:extra|else|more|frills|fancy|fluff|wasted)\b', 'negation kicker closing a list (crafted beat)'),
    (r'\b(?:no|zero)\s+(?:frills|fluff|fat|ceremony)\b', 'punchy-minimal flourish'),
    # rhetorical triples and antithesis
    (r'\bnot .{1,25}?\. Not .{1,25}?\. (?:But|Just)\b', 'staged antithesis'),
]

STRUCTURE = [
    (r'^\s*(?:[-*]\s+)?\*\*[^*]{2,40}\*\*\s*[:—-]\s', 'bolded-lead-in bullet (reads as generated list)'),
    (r'(?m)^#{1,6} .*\n+#{1,6} ', 'stacked headings with no prose between'),
]

def strip_code(t):
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    t = re.sub(r'`[^`]*`', ' ', t)
    t = re.sub(r'https?://\S+', ' ', t)
    t = re.sub(r'(?m)^\s{4,}\S.*$', ' ', t)          # indented code
    t = re.sub(r'(?m)^\s*\|.*\|\s*$', ' ', t)        # table rows
    t = re.sub(r'/[\w./-]{6,}', ' ', t)              # file paths
    return t

def lint_text(raw, name='<text>'):
    t = strip_code(raw)
    hits = []
    for pat, why in HARD:
        for m in re.finditer(pat, t):
            hits.append({'sev': 'hard', 'at': m.start(), 'found': m.group(0), 'why': why})
    # Spans inside straight double quotes are almost always evidence quoted from a source.
    # Flagging a banned word there pushes you to paraphrase the quote, which damages the
    # citation to satisfy a style rule. Skip them for the word list only; every other check
    # still sees the whole text.
    quoted = [(m.start(), m.end()) for m in re.finditer(r'"[^"\n]{0,400}"', t)]
    def in_quote(i):
        return any(a < i < b for a, b in quoted)

    wpat = re.compile(r'\b(' + '|'.join(WORDS) + r')\b', re.I)
    for m in wpat.finditer(t):
        if in_quote(m.start()):
            continue
        hits.append({'sev': 'word', 'at': m.start(), 'found': m.group(0), 'why': 'AI-register word'})
    for pat, why in PHRASES:
        for m in re.finditer(pat, t, re.I):
            hits.append({'sev': 'phrase', 'at': m.start(), 'found': m.group(0)[:60], 'why': why})
    for pat, why in STRUCTURE:
        for m in re.finditer(pat, t, re.M):
            hits.append({'sev': 'structure', 'at': m.start(), 'found': m.group(0)[:50].strip(), 'why': why})

    # verbless multi-item fragments ("66 lines, one validation pass, nothing extra.")
    VERBS = re.compile(r"\b(is|are|was|were|be|been|being|am|has|have|had|do|does|did|"
                       r"can|could|will|would|shall|should|may|might|must|"
                       r"get|gets|got|go|goes|went|make|makes|made|run|runs|ran|"
                       r"take|takes|took|give|gives|gave|come|comes|came|use|uses|used|"
                       r"work|works|worked|check|checks|checked|hold|holds|held|"
                       r"read|reads|write|writes|wrote|ship|ships|shipped|pass|passes|passed|"
                       r"fail|fails|failed|need|needs|needed|keep|keeps|kept|"
                       r"looks?|seems?|feels?|stays?|lives?|sits?|does|handles?|carries|carry)\b", re.I)
    for m in re.finditer(r'(?:(?<=[.!?])\s+|^)([^.!?\n]{10,110}?)[.!?]', t):
        s = m.group(1).strip()
        w = s.split()
        if not (3 <= len(w) <= 16):
            continue
        if s.count(',') < 1:
            continue
        # strip leading connectors so "And tight, fast, clean" still counts
        core = re.sub(r'^(?:and|but|so|then|also)\s+', '', s, flags=re.I)
        # a real clause has connectors or a contraction; a crafted beat is bare apposition
        if re.search(r"\b(but|so|because|which|that|when|if|though|while|since|after|"
                     r"before|unless|until|and then|where)\b", core, re.I):
            continue
        if re.search(r"\w'(?:s|re|ve|ll|t|d|m)\b", core):
            continue
        if VERBS.search(core):
            continue
        items = [x.strip() for x in core.split(',') if x.strip()]
        # a segment starting with a subject pronoun is a clause, not bare apposition
        if any(re.match(r"(?:it|they|he|she|we|i|you|there|this|that|these|those)\b", x, re.I)
               for x in items):
            continue
        # a crafted beat is made of SHORT bare phrases; a real clause runs longer
        if any(len(x.split()) > 5 for x in items):
            continue
        if len(items) >= 2:
            hits.append({'sev': 'phrase', 'at': m.start(1), 'found': s[:60],
                         'why': 'verbless list-fragment; reads as a crafted beat, give it a verb'})

    # rhythm: no contractions at all in substantial prose is itself a tell
    words = len(re.findall(r'\b\w+\b', t))
    contractions = len(re.findall(r"\b\w+'(?:t|s|re|ve|ll|d|m)\b", t))
    if words > 180 and contractions == 0:
        hits.append({'sev': 'rhythm', 'at': 0, 'found': f'{words} words, 0 contractions',
                     'why': 'zero contractions in long prose reads as generated'})

    # uniform sentence length is a tell
    sents = [s for s in re.split(r'(?<=[.!?])\s+', t) if len(s.split()) > 2]
    if len(sents) >= 6:
        lens = [len(s.split()) for s in sents]
        mean = sum(lens) / len(lens)
        var = sum((l - mean) ** 2 for l in lens) / len(lens)
        if var < 12 and mean > 12:
            hits.append({'sev': 'rhythm', 'at': 0,
                         'found': f'{len(sents)} sentences, mean {mean:.0f} words, variance {var:.0f}',
                         'why': 'uniform sentence length; vary it, mix in a short one'})
    for h in hits:
        h['file'] = name
        h['line'] = raw.count('\n', 0, h['at']) + 1 if h['at'] else 1
    return hits

# ---------- batch mode: the template is the tell ----------
def _norm_words(t):
    # Drop quoted spans before looking for repeated phrasing. Two texts that cite the same
    # source share its words by necessity, and one text quoting a source twice is not a
    # template. Keying on quotes would push you to paraphrase a citation differently in each
    # place, which is worse writing and worse evidence. Everything outside the quotes counts.
    t = re.sub(r'"[^"\n]{0,400}"', ' ', strip_code(t))
    # Mark sentence and paragraph ends. Without this the tokeniser welds the tail of one
    # sentence to the head of the next, so "...the heading it wrote. Nothing gets checked..."
    # reports the phrase "it wrote nothing", which nobody wrote.
    t = re.sub(r'[.!?;:]+[\s"\')\]]*|\n{2,}', ' \x00 ', t.lower())
    return [w for w in re.sub(r'[^a-z0-9\x00 ]', ' ', t).split() if w]

def _grams(words, n=4):
    out = set()
    for i in range(max(0, len(words) - n + 1)):
        g = words[i:i+n]
        if '\x00' in g:          # never form a phrase across a sentence boundary
            continue
        out.add(' '.join(g))
    return out

def lint_batch(texts, names=None, n=4):
    """texts: list of related prose (4 rationales, 10 prompts). Finds shared skeleton."""
    names = names or [f'text{i+1}' for i in range(len(texts))]
    hits = []
    W = [_norm_words(t) for t in texts]
    G = [_grams(w, n) for w in W]

    # shared n-grams across any pair
    for a in range(len(G)):
        for b in range(a+1, len(G)):
            common = G[a] & G[b]
            common = {c for c in common if len(c.split()) == n}
            # A gram wrapped around a number is a shared citation, not a shared skeleton.
            # Two texts that both report the same measurement have to say the number, and
            # a number needs a preposition and a noun beside it. Flagging that pushes you
            # to reword evidence, which is the opposite of what this check is for.
            common = {c for c in common if not any(x.isdigit() for x in c.split())}
            for c in sorted(common)[:6]:
                hits.append({'sev': 'batch', 'file': f'{names[a]}~{names[b]}', 'line': 1,
                             'found': c, 'why': f'{n}-word sequence shared between two texts in the set'})

    # shared openers
    openers = [' '.join(w[:4]) for w in W]
    for a in range(len(openers)):
        for b in range(a+1, len(openers)):
            if openers[a] and openers[a] == openers[b]:
                hits.append({'sev': 'batch', 'file': f'{names[a]}~{names[b]}', 'line': 1,
                             'found': openers[a], 'why': 'identical opening words'})
    # near-identical first word
    firsts = [w[0] if w else '' for w in W]
    dupe = {f for f in firsts if f and firsts.count(f) > max(1, len(firsts)//3)}
    for f in dupe:
        hits.append({'sev': 'batch', 'file': 'set', 'line': 1, 'found': f,
                     'why': f'{firsts.count(f)} of {len(firsts)} texts open with the same word'})

    # length uniformity
    lens = [len(w) for w in W]
    if len(lens) >= 3 and min(lens) > 0:
        spread = (max(lens) - min(lens)) / max(lens)
        if spread < 0.15:
            hits.append({'sev': 'batch', 'file': 'set', 'line': 1,
                         'found': f'lengths {lens}',
                         'why': 'all texts within 15% length; vary them deliberately'})
    return hits

# ---------- ledger: do not reuse your own phrasing across units ----------
LEDGER = os.environ.get('STYLE_LEDGER')  # optional: set to a JSON path to keep a phrase ledger across files

def _load_ledger():
    try:
        return json.load(open(LEDGER))
    except Exception:
        return {'openers': {}, 'phrases': {}}

# Function words. A 3-gram built mostly from these is ordinary English, not a phrasing
# fingerprint: after a few units the ledger was flagging "there is no" and "which is why",
# which pushes you to damage the prose to dodge the check. Keep the list wide.
_STOP = {
    'the','a','an','and','or','but','of','to','in','into','it','its','is','was','are','were',
    'be','been','being','that','this','these','those','with','without','for','on','at','as',
    'by','from','not','no','nor','so','than','then','there','here','which','who','what','when',
    'where','why','how','all','any','both','each','every','one','two','some','more','most',
    'other','such','only','own','same','too','very','can','will','would','should','could',
    'do','does','did','done','have','has','had','having','i','me','my','we','us','our','you',
    'your','he','she','they','them','their','him','her','his','hers','ours','yours','theirs',
    'if','because','while','after','before','up','down','out','off','over','under','again',
    'just','also','still','yet','about','against','between','through','during','above','below',
    # apostrophe halves: _norm_words splits "model's" into "model s" and "isn't" into "isn t",
    # so these stray letters must not count as content or every possessive looks like a phrase.
    's','t','re','ve','ll','d','m'
}

def _distinctive(t, n=3):
    """3-grams carrying at least two content words and no bare number.

    A gram containing a number is a citation or a measurement ("at step 89",
    "999 203 characters"). Those are evidence the text is obliged to carry, so the
    ledger must not push you to reword them.
    """
    w = _norm_words(t)
    out = set()
    for i in range(max(0, len(w)-n+1)):
        g = w[i:i+n]
        if '\x00' in g:          # a phrase does not straddle a sentence boundary
            continue
        if any(x.isdigit() for x in g):
            continue
        if sum(1 for x in g if x not in _STOP) >= 2:
            out.add(' '.join(g))
    return out

def lint_ledger(texts, names=None, record=False, window=5):
    names = names or [f'text{i+1}' for i in range(len(texts))]
    led = _load_ledger()
    me = os.environ.get('STYLE_UNIT', '')   # reusing your OWN phrasing in the same unit is fine
    hits = []
    for t, nm in zip(texts, names):
        w = _norm_words(t)
        op = ' '.join(w[:3])
        if op and op in led['openers'] and led['openers'][op] != me:
            hits.append({'sev': 'ledger', 'file': nm, 'line': 1, 'found': op,
                         'why': f"opener already used in unit '{led['openers'][op]}'; open differently"})
        for ph in _distinctive(t):
            if ph in led['phrases'] and led['phrases'][ph] != me:
                hits.append({'sev': 'ledger', 'file': nm, 'line': 1, 'found': ph,
                             'why': f"phrase already used in unit '{led['phrases'][ph]}'"})
    if record:
        tag = os.environ.get('STYLE_UNIT', 'unrecorded')
        for t in texts:
            w = _norm_words(t)
            op = ' '.join(w[:3])
            if op:
                led['openers'][op] = tag
            for ph in _distinctive(t):
                led['phrases'][ph] = tag
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        json.dump(led, open(LEDGER, 'w'))
    return hits

def report(hits, as_json=False):
    if as_json:
        print(json.dumps(hits, indent=1))
        return 1 if hits else 0
    if not hits:
        print('ai-tell-lint: clean')
        return 0
    order = {'hard': 0, 'batch': 1, 'ledger': 2, 'phrase': 3, 'structure': 4, 'word': 5, 'rhythm': 6}
    hits.sort(key=lambda h: (order.get(h['sev'], 9), h['file'], h['line']))
    print(f'ai-tell-lint: {len(hits)} tell(s)\n')
    for h in hits:
        print(f"  {h['file']}:{h['line']} [{h['sev']}] {h['found']!r} -- {h['why']}")
    print('\nRewrite these before shipping. See references/writing.md in the craft skill.')
    return 1

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 2
    as_json = '--json' in args
    args = [a for a in args if a != '--json']
    batch = '--batch' in args
    ledger = '--ledger' in args
    record = '--record' in args
    args = [a for a in args if a not in ('--batch', '--ledger', '--record')]

    if batch or ledger:
        texts, names = [], []
        for f in args:
            if not os.path.exists(f):
                print(f'ai-tell-lint: no such file: {f}', file=sys.stderr); return 2
            texts.append(open(f, encoding='utf-8', errors='replace').read())
            names.append(os.path.basename(f))
        if len(texts) < 2 and batch:
            print('ai-tell-lint: --batch needs 2+ files', file=sys.stderr); return 2
        hits = []
        for t, n_ in zip(texts, names):
            hits += lint_text(t, n_)
        if batch:
            hits += lint_batch(texts, names)
        if ledger:
            hits += lint_ledger(texts, names, record=record)
        return report(hits, as_json)

    hits = []
    if args and args[0] == '--text':
        # ponytail: `--text -` used to lint the literal "-" and always pass; callers pipe text, so read stdin
        hits = lint_text(sys.stdin.read(), '<stdin>') if args[1:] == ['-'] else lint_text(' '.join(args[1:]))
    elif args and args[0] == '-':
        hits = lint_text(sys.stdin.read(), '<stdin>')
    else:
        for f in args:
            if not os.path.exists(f):
                print(f'ai-tell-lint: no such file: {f}', file=sys.stderr); return 2
            try:
                hits += lint_text(open(f, encoding='utf-8', errors='replace').read(), os.path.basename(f))
            except Exception as e:
                print(f'ai-tell-lint: {f}: {e}', file=sys.stderr)
    return report(hits, as_json)

if __name__ == '__main__':
    sys.exit(main())
