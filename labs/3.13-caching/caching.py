"""Lab 3.13: when a prompt cache pays, and what a semantic cache gets wrong.

Part 1: prompt (prefix) caching economics with write 1.25x, read 0.1x of the input price, and a
cache that expires 5 minutes after its last use. Requests for one prefix arrive at random.
Part 2: a toy semantic cache over bank FAQs. Similarity is character-trigram cosine, a crude stand-in
for embeddings. Each incoming question is labelled with the cached question it truly matches (-1: none).
Standard library only; seeded.
"""
import json, math, pathlib, random
from collections import Counter

random.seed(5)
WRITE, READ, TTL = 1.25, 0.10, 300.0

def simulate(rate_per_min, n=20_000):
    t, expires, cost, hits = 0.0, -1.0, 0.0, 0
    for _ in range(n):
        t += random.expovariate(rate_per_min / 60.0)
        if t <= expires:
            cost += READ; hits += 1
        else:
            cost += WRITE
        expires = t + TTL          # every use refreshes the expiry
    return hits / n, cost / n

print("| Requests per minute sharing the prefix | Hit rate | Prefix cost vs no caching |")
print("|---|---|---|")
for r in (0.05, 0.1, 0.2, 0.5, 1, 5, 30):
    h, c = simulate(r)
    print(f"| {r} | {h:.0%} | {c:.2f}x |")

data = json.loads((pathlib.Path(__file__).parent / "pairs.json").read_text())
def grams(s):
    s = " " + "".join(ch.lower() for ch in s if ch.isalnum() or ch == " ") + " "
    return Counter(s[i:i+3] for i in range(len(s) - 2))
def cos(a, b):
    num = sum(a[k] * b[k] for k in a)
    return num / math.sqrt(sum(v*v for v in a.values()) * sum(v*v for v in b.values()))
cached = [grams(q) for q in data["cached"]]

print("\n| Similarity threshold | Served from cache | Correct hits | Wrong answers served | Missed reuse |")
print("|---|---|---|---|---|")
for thr in (0.5, 0.6, 0.7, 0.8, 0.9):
    served = correct = wrong = missed = 0
    for q, truth in data["incoming"]:
        g = grams(q)
        best = max(range(len(cached)), key=lambda i: cos(g, cached[i]))
        if cos(g, cached[best]) >= thr:
            served += 1
            if best == truth: correct += 1
            else: wrong += 1
        elif truth >= 0:
            missed += 1
    print(f"| {thr} | {served} of 12 | {correct} | {wrong} | {missed} |")

# ---- Chart (optional; needs matplotlib) --------------------------------------------------------
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from chart import line_chart
CHART_PATH = _pl.Path(__file__).with_name("result.svg")
rates = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 5, 10, 30]
line_chart(CHART_PATH, rates, {"Prefix cost with caching": [simulate(r)[1] for r in rates]},
           title="A prompt cache pays once its prefix is reused within its lifetime",
           xlabel="Requests per minute sharing the prefix (5-minute cache)", ylabel="Cost vs no caching (x)",
           logx=True, ref=(1, "no caching"), xticks=[0.02, 0.1, 0.5, 2, 10, 30])
