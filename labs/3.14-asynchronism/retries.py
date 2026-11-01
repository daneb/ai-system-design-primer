"""Lab 3.14: retries during an overload, and checkpoints for long runs.

Part 1: 1,000 clients each need one call. The provider serves 100 calls per second, but for the first
10 seconds only 20 per second. Rejected calls retry by one of three policies. Count total attempts
and when the last client succeeds.
Part 2: a 12-step agent run where each step fails transiently 5% of the time. On failure, either
restart from step 1 or resume from the failed step (durable checkpoint). Count model calls paid for.
numpy + stdlib; seeded.
"""
import random
import numpy as np

def overload(policy, seed=1):
    rng = random.Random(seed)
    due = [rng.uniform(0, 1.0) for _ in range(1000)]     # first attempt times (all within 1 s)
    attempts = [0] * 1000
    done_at = [None] * 1000
    t, step = 0.0, 0.05
    pending = set(range(1000))
    while pending and t < 600:
        cap = (20 if t < 10 else 100) * step
        ready = sorted(i for i in pending if due[i] <= t)
        rng.shuffle(ready)
        served = ready[:int(cap)]
        for i in ready:
            attempts[i] += 1
        for i in served:
            done_at[i] = t; pending.discard(i)
        for i in ready[int(cap):]:
            a = attempts[i]
            if policy == "immediate":
                due[i] = t + 0.05
            elif policy == "backoff":
                due[i] = t + min(30, 0.5 * 2 ** a)
            else:                                        # full jitter
                due[i] = t + rng.uniform(0, min(30, 0.5 * 2 ** a))
        t += step
    return sum(attempts), max(d for d in done_at if d is not None)

print("| Retry policy | Total attempts for 1,000 calls | Last call succeeds at (s) |")
print("|---|---|---|")
for p, label in (("immediate", "retry immediately"), ("backoff", "exponential backoff"),
                 ("jitter", "exponential backoff + full jitter")):
    n, last = overload(p)
    print(f"| {label} | {n:,} | {last:.1f} |")

rng = np.random.default_rng(2)
STEPS, P_FAIL, RUNS = 12, 0.05, 20_000
def calls(resume):
    total = 0
    step = 0
    while step < STEPS:
        total += 1
        if rng.random() < P_FAIL:
            step = step if resume else 0
        else:
            step += 1
    return total
restart = np.mean([calls(False) for _ in range(RUNS)])
resume = np.mean([calls(True) for _ in range(RUNS)])
print("\n| On a transient failure | Model calls per completed 12-step run | vs minimum (12) |")
print("|---|---|---|")
print(f"| restart the whole run | {restart:.1f} | +{restart/12-1:.0%} |")
print(f"| resume from the failed step (checkpoint) | {resume:.1f} | +{resume/12-1:.0%} |")
