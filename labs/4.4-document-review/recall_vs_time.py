"""Lab 4.4: what 98% recall on risky clauses costs in lawyer time, and whether a second pass helps.

Each contract has 60 playbook positions; 15% are risky (needs a lawyer, red line, or missing clause).
The review model gives each position a risk score; the assistant flags positions above a threshold.
A lawyer reads the summary (10 min) and every flagged position (2.5 min each) and trusts the rest, so
a risky position that isn't flagged is missed. A second pass on red-line topics is a second,
partly independent score (errors correlated 0.5 with the first); a position is flagged if either
pass flags it. Compared at the same number of flags, i.e. the same lawyer time.
numpy only; seeded; scores are synthetic, so read the shape, not the exact numbers.
"""
import numpy as np

rng = np.random.default_rng(4)
CONTRACTS, POSITIONS, RISKY = 4000, 60, 0.15
BASE_MIN, PER_FLAG_MIN, MANUAL_MIN, TARGET = 10.0, 2.5, 90.0, 0.98

risky = rng.random((CONTRACTS, POSITIONS)) < RISKY
shift = np.where(risky, 1.6, -1.0)                       # risky positions score higher on average
e1 = rng.normal(size=risky.shape)
e2 = 0.5 * e1 + np.sqrt(1 - 0.5 ** 2) * rng.normal(size=risky.shape)
one_pass = shift + e1
two_pass = np.maximum(one_pass, shift + e2)              # flag if either pass flags

def at_flag_share(score, share):
    flagged = score > np.quantile(score, 1 - share)
    recall = (flagged & risky).sum() / risky.sum()
    minutes = BASE_MIN + PER_FLAG_MIN * flagged.sum(1).mean()
    return recall, minutes

shares = [i / 100 for i in range(10, 61, 2)]
curves = {"One pass": [at_flag_share(one_pass, s)[0] for s in shares],
          "With a second pass": [at_flag_share(two_pass, s)[0] for s in shares]}

print(f"{RISKY:.0%} of {POSITIONS} positions risky; manual first review {MANUAL_MIN:.0f} min\n")
print("| Positions flagged | Lawyer minutes per contract | Recall, one pass | Recall, with a second pass |")
print("|---|---|---|---|")
for s in (0.15, 0.20, 0.25, 0.30, 0.40, 0.50):
    r1, m = at_flag_share(one_pass, s)
    r2, _ = at_flag_share(two_pass, s)
    print(f"| {s:.0%} | {m:.0f} | {r1:.1%} | {r2:.1%} |")

print(f"\nFlags needed to reach {TARGET:.0%} recall:")
for name, score in (("one pass", one_pass), ("with a second pass", two_pass)):
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if at_flag_share(score, mid)[0] < TARGET else (lo, mid)
    r, m = at_flag_share(score, hi)
    print(f"  {name}: {hi:.0%} of positions, {m:.0f} lawyer minutes per contract "
          f"({1 - m / MANUAL_MIN:.0%} saved vs manual)")

# ---- Chart (optional; needs matplotlib) --------------------------------------------------------
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from chart import line_chart
CHART_PATH = _pl.Path(__file__).with_name("result.svg")
line_chart(CHART_PATH, shares, curves,
           title="98% recall costs far more flags than the risky share suggests",
           xlabel="Share of positions flagged for the lawyer (lawyer time rises with it)",
           ylabel="Recall of risky positions", xpercent=True, ypercent=True, ylim=(0.6, 1.01),
           ref=(TARGET, "98% recall target"))
