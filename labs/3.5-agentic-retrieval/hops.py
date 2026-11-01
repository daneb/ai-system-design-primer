"""Lab 3.5: single-shot retrieval, query fan-out, or an agent loop?

Three question types:
  lookup     - one fact
  multi-part - three independent facts ("compare A, B and C")
  multi-hop  - three facts in a chain: the query for fact 2 needs fact 1's answer
Three strategies:
  single     - one search with the user's question, top-k passages, then answer
  fan-out    - a model writes sub-queries up front; they run in parallel (one planning call)
  agent      - search, read, decide, search again, up to MAX_ROUNDS; notices a miss with
               probability NOTICE and retries; stops too early with probability EARLY per fact
A question is answered correctly only if every fact it needs was retrieved.
All probabilities are assumptions chosen to be plausible; read the shape. numpy only, seeded.
"""
import numpy as np

rng = np.random.default_rng(11)
N = 20_000
FOCUSED = 0.85     # chance a focused query retrieves its fact
DILUTED = 0.60     # chance a mixed query retrieves each of several facts
BLIND = 0.20       # chance a query finds a chained fact it could not name yet
NOTICE, EARLY, MAX_ROUNDS = 0.8, 0.07, 6
FACTS = {"lookup": 1, "multi-part": 3, "multi-hop": 3}


def single(kind):
    n = FACTS[kind]
    if kind == "lookup":
        p = [FOCUSED]
    elif kind == "multi-part":
        p = [DILUTED] * n
    else:
        p = [FOCUSED] + [BLIND] * (n - 1)
    ok = all(rng.random() < x for x in p)
    return ok, 1, 1, 1          # correct, model calls, searches, sequential rounds


def fan_out(kind):
    n = FACTS[kind]
    p = [FOCUSED] * n if kind != "multi-hop" else [FOCUSED] + [BLIND] * (n - 1)
    ok = all(rng.random() < x for x in p)
    return ok, 2, n, 2          # planning call + answer call; searches in parallel


def agent(kind):
    n, calls, searches, rounds = FACTS[kind], 1, 0, 0
    for _ in range(n):
        found = False
        while rounds < MAX_ROUNDS:
            rounds += 1; calls += 1; searches += 1
            if rng.random() < FOCUSED:
                found = True
                break
            if rng.random() > NOTICE:        # didn't notice the miss: moves on with a gap
                break
        if not found or rng.random() < EARLY:
            return False, calls, searches, rounds
    return True, calls, searches, rounds


print(f"{'question':<12}{'strategy':<10}{'correct':>9}{'model calls':>13}{'searches':>10}{'rounds':>8}")
for kind in FACTS:
    for name, fn in [("single", single), ("fan-out", fan_out), ("agent", agent)]:
        r = np.array([fn(kind) for _ in range(N)], dtype=float)
        print(f"{kind:<12}{name:<10}{r[:, 0].mean():>9.0%}{r[:, 1].mean():>13.1f}{r[:, 2].mean():>10.1f}{r[:, 3].mean():>8.1f}")
