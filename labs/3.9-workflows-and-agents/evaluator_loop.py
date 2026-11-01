"""Lab 3.9: what an evaluator-optimizer loop is worth depends on the evaluator.

A generator produces a correct draft with probability p (revisions improve it a little each round).
An evaluator accepts a correct draft with probability TPR and wrongly accepts a bad one with FPR.
Loop: generate -> evaluate -> if rejected, revise (up to max rounds). Measure final accuracy and calls.
numpy only; seeded.
"""
import numpy as np
rng = np.random.default_rng(9)
N = 100_000

def run(p0, tpr, fpr, max_rounds, gain=0.10):
    correct_final = 0; calls = 0
    for _ in range(N):
        p = p0
        for r in range(max_rounds):
            ok = rng.random() < p
            calls += 2                                  # generate + evaluate
            accept = rng.random() < (tpr if ok else fpr)
            if accept or r == max_rounds - 1:
                correct_final += ok
                break
            p = min(0.99, p + gain)                     # revision with feedback helps a little
    return correct_final / N, calls / N

print("| Evaluator | True-accept rate | False-accept rate | Final accuracy (p=0.6, up to 3 rounds) | Calls per task |")
print("|---|---|---|---|---|")
print(f"| none (single call) | — | — | 60% | 1.0 |")
for name, tpr, fpr in (("code check (exact)", 1.0, 0.0), ("strong judge", 0.95, 0.10),
                       ("weak judge", 0.85, 0.40), ("rubber stamp", 1.0, 1.0)):
    acc, c = run(0.6, tpr, fpr, 3)
    print(f"| {name} | {tpr:.0%} | {fpr:.0%} | {acc:.0%} | {c:.1f} |")

print("\n| Rounds allowed (strong judge) | Final accuracy | Calls per task |")
print("|---|---|---|")
for k in (1, 2, 3, 5, 8):
    acc, c = run(0.6, 0.95, 0.10, k)
    print(f"| {k} | {acc:.0%} | {c:.1f} |")
