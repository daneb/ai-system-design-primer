"""Lab 4.5: consistency (pass^k) of a support agent with policy in the prompt vs in a policy engine.

A toy refund policy has four rules (within 30 days; not a final-sale item; under the self-service
limit, else hand over; one refund per order). Each of 300 simulated scenarios needs one to four of
them. Two designs:
  prompt   - the model applies each needed rule itself; most rules it gets right 98% of the time,
             but each scenario has a 25% chance of a "tricky" rule it gets right only 75% of the time
  engine   - a deterministic policy engine applies the rules; the model only has to pick the right
             tool and fill it in (97-99.5% per scenario) and relay the answer
Every scenario is run 8 times. pass^k counts a scenario only if its first k runs all succeed.
Standard library only; seeded; rates are illustrative.
"""
import random

random.seed(45)
SCENARIOS, RUNS = 300, 8

def scenario():
    rules = random.randint(1, 4)
    p_rules = [0.75 if random.random() < 0.25 else 0.98 for _ in range(rules)]
    p_prompt = 1.0
    for p in p_rules:
        p_prompt *= p
    p_prompt *= 0.99                                # relay the outcome correctly
    p_engine = random.uniform(0.97, 0.995)          # pick and fill the tool, relay the answer
    return p_prompt, p_engine

cases = [scenario() for _ in range(SCENARIOS)]
runs = {name: [[random.random() < c[i] for _ in range(RUNS)] for c in cases]
        for i, name in enumerate(("Policy in the prompt", "Policy engine"))}

def pass_k(results, k):
    return sum(all(r[:k]) for r in results) / len(results)

print(f"{SCENARIOS} scenarios x {RUNS} runs\n")
print("| Design | pass@1 (one run) | pass^2 | pass^4 | pass^8 | pass@8 (any of 8) |")
print("|---|---|---|---|---|---|")
for name, res in runs.items():
    any8 = sum(any(r) for r in res) / len(res)
    print(f"| {name} | " + " | ".join(f"{pass_k(res, k):.0%}" for k in (1, 2, 4, 8)) + f" | {any8:.0%} |")

flaky = [sum(r) for r in runs["Policy in the prompt"] if 0 < sum(r) < RUNS]
print(f"\nPolicy in the prompt: {len(flaky)} of {SCENARIOS} scenarios passed some runs and failed others;"
      f" a single run per scenario can't tell those apart from reliable ones.")

# ---- Chart (optional; needs matplotlib) --------------------------------------------------------
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from chart import line_chart
CHART_PATH = _pl.Path(__file__).with_name("result.svg")
ks = list(range(1, RUNS + 1))
line_chart(CHART_PATH, ks, {name: [pass_k(res, k) for k in ks] for name, res in runs.items()},
           title="Moving policy into code keeps the agent consistent across runs",
           xlabel="Runs per scenario that must all succeed (k)", ylabel="pass^k",
           ypercent=True, ylim=(0, 1.02), xticks=ks)
