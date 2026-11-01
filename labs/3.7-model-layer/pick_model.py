"""Lab 3.7: 'accuracy first, then the cheapest model that meets the bar' -- with noisy evals.

Five candidate models, cheapest last. True accuracies are fixed; we only see eval scores on n cases.
Rule A: pick the cheapest model whose measured score >= target.
Rule B: pick the cheapest model whose 95% lower confidence bound >= target.
How often does each rule pick a model that is truly below target? numpy only; seeded.
"""
import numpy as np
rng = np.random.default_rng(11)
models = [("large", 0.92, 10.0), ("medium-a", 0.90, 4.0), ("medium-b", 0.88, 2.0),
          ("small-a", 0.86, 1.0), ("small-b", 0.83, 0.5)]   # name, true accuracy, relative cost
TARGET, TRIALS = 0.88, 20_000

def choose(scores, n, rule):
    for (name, acc, cost), s in sorted(zip(models, scores), key=lambda x: x[0][2]):   # cheapest first
        if rule == "A" and s >= TARGET: return name, acc, cost
        lb = s - 1.96 * np.sqrt(s * (1 - s) / n)
        if rule == "B" and lb >= TARGET: return name, acc, cost
    return models[0]                                   # fall back to the largest

print(f"Target {TARGET:.0%}. True accuracies: " + ", ".join(f"{m[0]} {m[1]:.0%} (cost {m[2]})" for m in models) + "\n")
print("| Eval cases | Rule | Picked a model truly below target | Average relative cost | Most common pick |")
print("|---|---|---|---|---|")
for n in (50, 100, 300, 1000, 3000):
    for rule in ("A", "B"):
        below, cost, picks = 0, 0.0, {}
        for _ in range(TRIALS):
            scores = rng.binomial(n, [m[1] for m in models]) / n
            name, acc, c = choose(scores, n, rule)
            below += acc < TARGET; cost += c; picks[name] = picks.get(name, 0) + 1
        top = max(picks, key=picks.get)
        label = "measured ≥ target" if rule == "A" else "lower bound ≥ target"
        print(f"| {n} | {label} | {below/TRIALS:.0%} | {cost/TRIALS:.1f} | {top} ({picks[top]/TRIALS:.0%}) |")
