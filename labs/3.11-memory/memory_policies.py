"""Lab 3.11: what should an agent remember, and how?

One user, 50 sessions. The user has 20 facts (preferences, account details). In each session
they state 2 facts (new or changed: 30% of statements change an existing fact). Each session
also reads one tool result (a web page or email); 1 in 10 contains a planted "fact" (memory
poisoning). At the start of each later session the agent must recall 3 random current facts.

Policies:
  none          - no long-term memory; agent must ask again
  transcript    - replay every past session (~3,000 tokens each); with two versions of a fact,
                  picks the newer with probability PICK_NEWER
  append        - extract facts (EXTRACT accuracy) and append them; never update; retrieves the
                  top 10 by similarity, which may return the stale version
  consolidate   - extract, then update or replace the old version (CONSOLIDATE accuracy)
  consolidate+  - as consolidate, but only writes facts that came from the user, not from tool
                  output (provenance check)
All probabilities are assumptions. numpy only, seeded.
"""
import numpy as np

rng = np.random.default_rng(3)
SESSIONS, FACTS, PER_SESSION, CHANGE, POISON_RATE, ASK = 50, 20, 2, 0.3, 0.1, 3
EXTRACT, CONSOLIDATE, PICK_NEWER, POISON_FOLLOW = 0.9, 0.9, 0.7, 0.8
SESSION_TOKENS, FACT_TOKENS, TOP_K = 3_000, 30, 10


def simulate(policy, runs=300):
    correct = asked = stale = poisoned_hits = tokens = 0
    for _ in range(runs):
        truth = {}                       # fact id -> current version
        store = {}                       # fact id -> list of versions remembered (oldest first)
        poison = set()                   # fact ids with a planted value in memory
        for s in range(SESSIONS):
            # recall check at the start of the session
            if truth:
                for f in rng.choice(list(truth), size=min(ASK, len(truth)), replace=False):
                    asked += 1
                    if policy == "none":
                        continue
                    versions = store.get(f, [])
                    if f in poison and rng.random() < POISON_FOLLOW:
                        poisoned_hits += 1
                        continue
                    if not versions:
                        continue
                    if versions[-1] == truth[f] and (len(versions) == 1 or policy in ("consolidate", "consolidate+")):
                        correct += 1
                    elif versions[-1] == truth[f]:
                        newer_wins = PICK_NEWER if policy == "transcript" else 0.5
                        if rng.random() < newer_wins:
                            correct += 1
                        else:
                            stale += 1
                    else:
                        stale += 1
            # memory tokens loaded this session
            if policy == "transcript":
                tokens += s * SESSION_TOKENS
            elif policy == "append":
                tokens += min(sum(len(v) for v in store.values()), TOP_K) * FACT_TOKENS
            elif policy.startswith("consolidate"):
                tokens += min(len(store), TOP_K) * FACT_TOKENS
            # user states facts this session
            for _ in range(PER_SESSION):
                if truth and rng.random() < CHANGE:
                    f = rng.choice(list(truth)); truth[f] += 1
                else:
                    f = int(rng.integers(FACTS)); truth[f] = truth.get(f, 0) + 1
                if policy == "transcript":
                    store.setdefault(f, []).append(truth[f]); poison.discard(f)
                elif policy == "append" and rng.random() < EXTRACT:
                    store.setdefault(f, []).append(truth[f]); poison.discard(f)
                elif policy.startswith("consolidate") and rng.random() < EXTRACT:
                    if f in store and rng.random() > CONSOLIDATE:
                        store[f].append(truth[f])          # failed to merge: two versions
                    else:
                        store[f] = [truth[f]]
                    poison.discard(f)
            # a tool result may plant a fact
            if rng.random() < POISON_RATE and policy not in ("none", "consolidate+"):
                poison.add(int(rng.integers(FACTS)))
    n = asked
    return correct / n, stale / n, poisoned_hits / n, 1 - (correct + stale + poisoned_hits) / n, tokens / runs / SESSIONS


print(f"{'policy':<14}{'recalled':>9}{'stale':>7}{'poisoned':>10}{'missing':>9}{'memory tokens/session':>23}")
for p in ["none", "transcript", "append", "consolidate", "consolidate+"]:
    c, st, po, miss, tok = simulate(p)
    print(f"{p:<14}{c:>9.0%}{st:>7.0%}{po:>10.0%}{miss:>9.0%}{tok:>23,.0f}")
