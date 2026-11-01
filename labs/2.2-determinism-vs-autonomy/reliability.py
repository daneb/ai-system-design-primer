"""Lab 2.2: what autonomy costs in reliability and predictability.

Part 1: end-to-end success when every step must succeed.
Part 2: pass@1 vs pass^k when tasks differ in difficulty.
Part 3: spread of model calls per request, fixed workflow vs agent loop.
numpy only; seeded.
"""
import numpy as np

rng = np.random.default_rng(7)

print("Part 1: end-to-end success = p^n\n")
print("| Per-step success | 3 steps | 5 steps | 10 steps | 20 steps |")
print("|---|---|---|---|---|")
for p in (0.99, 0.95, 0.90):
    print(f"| {p:.0%} | " + " | ".join(f"{p**n:.0%}" for n in (3, 5, 10, 20)) + " |")

print("\nPart 2: same average, different consistency (1,000 tasks)\n")
print("| Population | pass@1 | pass^2 | pass^4 | pass^8 |")
print("|---|---|---|---|---|")
pops = {
    "every task 60% (pure noise)": np.full(1000, 0.6),
    "60% of tasks always, 40% never": np.r_[np.ones(600), np.zeros(400)],
    "mixed difficulty (Beta 1.5,1)": rng.beta(1.5, 1.0, 1000),
}
for name, q in pops.items():
    print(f"| {name} | " + " | ".join(f"{np.mean(q**k):.0%}" for k in (1, 2, 4, 8)) + " |")

print("\nPart 3: model calls per request (100,000 requests)\n")
n = 100_000
workflow = np.full(n, 4)                      # classify, retrieve+answer, check, format
agent = 2 + rng.geometric(0.25, n)            # plan + answer + a variable tool loop
agent = np.minimum(agent, 25)                 # step cap
print("| Design | Mean | p50 | p95 | p99 | Max |")
print("|---|---|---|---|---|---|")
for name, x in (("Workflow (4 fixed calls)", workflow), ("Agent loop (cap 25)", agent)):
    print(f"| {name} | {x.mean():.1f} | {np.percentile(x,50):.0f} | {np.percentile(x,95):.0f} | "
          f"{np.percentile(x,99):.0f} | {x.max()} |")
print(f"\nAgent requests hitting the cap: {np.mean(agent == 25):.2%}")
