"""Lab 0.1: what a token is, why the same meaning costs different amounts, and what temperature does.

Part 1: train a tiny byte-pair encoding (BPE) tokenizer on this primer's own English pages, then count
tokens for the same message in English, in Afrikaans, as JSON, and as numbers. Real tokenizers have
100,000+ entries, not about a thousand, so compare the RATIOS, not the absolute counts.
Part 2: sample a 40-token "answer" from a fixed set of next-token probabilities at several
temperatures and see how often two runs agree.
Standard library only; seeded.
"""
import math, pathlib, random, re
from collections import Counter

random.seed(1)
ROOT = pathlib.Path(__file__).resolve().parents[2]
MERGES = 1000

# ---- Part 1: train BPE on the English pages of Parts 2 and 3 -----------------------------------
text = " ".join(p.read_text(encoding="utf-8") for d in ("2-trade-offs", "3-components")
                for p in sorted((ROOT / "docs" / d).glob("*.md")))
text = re.sub(r"\(https?://[^)]*\)|`[^`]*`|[#*|>\[\]]", " ", text)
WORD = re.compile(r" ?[A-Za-z]+| ?\d| ?[^\sA-Za-z\d]")      # words keep their leading space

def words(s):
    return WORD.findall(s)

vocab = Counter(tuple(w) for w in words(text))
merges = []
for _ in range(MERGES):
    pairs = Counter()
    for w, n in vocab.items():
        for a, b in zip(w, w[1:]):
            pairs[a, b] += n
    if not pairs:
        break
    best = max(pairs, key=pairs.get)
    merges.append(best)
    new = {}
    for w, n in vocab.items():
        out, i = [], 0
        while i < len(w):
            if i + 1 < len(w) and (w[i], w[i + 1]) == best:
                out.append(w[i] + w[i + 1]); i += 2
            else:
                out.append(w[i]); i += 1
        new[tuple(out)] = new.get(tuple(out), 0) + n
    vocab = Counter(new)
rank = {m: i for i, m in enumerate(merges)}

def encode(s):
    toks = []
    for w in words(s):
        w = list(w)
        while True:
            cands = [(rank[(a, b)], i) for i, (a, b) in enumerate(zip(w, w[1:])) if (a, b) in rank]
            if not cands:
                break
            _, i = min(cands)
            w[i:i + 2] = [w[i] + w[i + 1]]
        toks += w
    return toks

samples = {
    "English": "Your payment of two hundred rand to the electricity account was declined because the "
               "daily limit on your cheque account has been reached. Please try again tomorrow or "
               "raise the limit in the banking app.",
    "Afrikaans (same message)": "Jou betaling van tweehonderd rand aan die elektrisiteitsrekening is "
               "geweier omdat die daaglikse limiet op jou tjekrekening bereik is. Probeer asseblief "
               "môre weer of verhoog die limiet in die bankapp.",
    "JSON (same facts)": '{"event":"payment_declined","amount_zar":200.00,"payee":"electricity",'
               '"reason":"daily_limit_reached","account_type":"cheque","retry_after":"2026-11-02"}',
    "Numbers": "Balance 1,284,377.52; limit 5,000.00; ref 4471-0093-2218-6650; 2026-11-01 21:43:07",
}
print(f"Tokenizer: {MERGES} merges learned from {len(text.split()):,} words of this primer\n")
print("| Text | Characters | Tokens | Characters per token | Tokens vs English |")
print("|---|---|---|---|---|")
base = len(encode(samples["English"]))
for name, s in samples.items():
    t = encode(s)
    vs = f"{len(t)/base:.2f}x" if name != "Numbers" else "n/a (different content)"
    print(f"| {name} | {len(s)} | {len(t)} | {len(s)/len(t):.1f} | {vs} |")
print("\nEnglish split:", "|".join(encode(samples["English"])[:24]), "...")

# ---- Part 2: temperature and run-to-run agreement ---------------------------------------------
STEPS, RUNS = 40, 500
# Each step: a model fairly sure of the next token, with a few plausible alternatives.
steps = [[4.0, 2.0 + random.random(), 1.0 + random.random(), 0.5, 0.0] for _ in range(STEPS)]

def probs(logits, t):
    if t == 0:
        p = [0.0] * len(logits); p[max(range(len(logits)), key=logits.__getitem__)] = 1.0
        return p
    m = max(logits)
    e = [math.exp((x - m) / t) for x in logits]
    return [v / sum(e) for v in e]

def top_p(p, cut):
    order = sorted(range(len(p)), key=lambda i: -p[i])
    keep, total = [], 0.0
    for i in order:
        keep.append(i); total += p[i]
        if total >= cut:
            break
    q = [p[i] if i in keep else 0.0 for i in range(len(p))]
    return [v / sum(q) for v in q]

def run(t, cut=1.0):
    return tuple(random.choices(range(5), weights=top_p(probs(lg, t), cut))[0] for lg in steps)

greedy = tuple(0 for _ in steps)
print("\n| Setting | Chance the likeliest token is picked, per step | Distinct answers in 500 runs | Runs identical to the greedy answer |")
print("|---|---|---|---|")
for label, t, cut in (("temperature 0 (greedy)", 0, 1.0), ("temperature 0.3", 0.3, 1.0),
                      ("temperature 0.7", 0.7, 1.0), ("temperature 1.0", 1.0, 1.0),
                      ("temperature 1.0, top-p 0.9", 1.0, 0.9)):
    outs = [run(t, cut) for _ in range(RUNS)]
    p_top = sum(top_p(probs(lg, t), cut)[0] for lg in steps) / STEPS
    print(f"| {label} | {p_top:.0%} | {len(set(outs))} | {sum(o == greedy for o in outs)/RUNS:.0%} |")
