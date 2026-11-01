"""Lab 2.5: one agent or several?

Two tasks:
  breadth - 10 independent sub-topics ("find the board members of these ten companies")
  chain   - 6 dependent steps; each needs what earlier steps decided ("design, build, test")
Four designs:
  single            - one agent, one growing context, in order
  single+compaction - one agent that replaces each finished sub-task with a short summary (3.3)
  independent       - parallel sub-agents, results concatenated, nobody checks
  orchestrated      - a lead briefs sub-agents, checks each result, re-runs a failure once
Every sub-task is 5 model calls, each adding 3k tokens of tool results (15k per sub-task).
Input tokens are counted per call (the whole context is re-sent each time).
Assumptions (invented; read the shape, not the numbers):
  P0      = 0.92  chance a sub-task succeeds in a fresh context
  ROT     = 0.20  reliability lost per 100k tokens already in context
  HANDOFF = 0.15  chance a hand-off between agents drops something the next step needed
  CATCH   = 0.6   chance a reviewer with fresh context catches a bad result (0.3 for self-review)
numpy only, seeded.
"""
import numpy as np

rng = np.random.default_rng(5)
N = 20_000
P0, ROT, HANDOFF, CATCH, SELF_CATCH = 0.92, 0.20, 0.15, 0.6, 0.3
SYSTEM, CALLS, PER_CALL, SUMMARY, BRIEF, MINUTES = 2_000, 5, 3_000, 1_500, 2_000, 3.0


def subtask_tokens(start):
    """Input tokens for one sub-task's 5 calls, starting from a context of `start` tokens."""
    return sum(SYSTEM + start + i * PER_CALL for i in range(CALLS))


def run(task, design):
    k = 10 if task == "breadth" else 6
    dependent = task == "chain"
    ok_count, tokens, ctx = 0, 0, 0
    for step in range(k):
        if design.startswith("single"):
            p = P0 - ROT * ctx / 100_000
            good = rng.random() < p
            if not good and rng.random() < SELF_CATCH:
                good = rng.random() < p
            tokens += subtask_tokens(ctx)
            ctx += SUMMARY if design == "single+compaction" else CALLS * PER_CALL
        else:
            lost = dependent and step > 0 and rng.random() < HANDOFF
            good = (not lost) and rng.random() < P0
            tokens += subtask_tokens(BRIEF + (step * SUMMARY if dependent else 0))
            if design == "orchestrated":
                tokens += 2 * (SYSTEM + ctx + BRIEF)          # lead briefs, then reviews
                if not good and rng.random() < CATCH:
                    good = rng.random() < P0 * (1 - HANDOFF if dependent else 1)
                    tokens += subtask_tokens(BRIEF)
            ctx += SUMMARY
        ok_count += good
        if dependent and not good:
            return 0.0, tokens
    return (ok_count / k if not dependent else 1.0), tokens


def minutes(task, design):
    k = 10 if task == "breadth" else 6
    if design.startswith("single") or task == "chain":
        extra = 1.3 if design == "orchestrated" else (1.1 if design == "independent" else 1.0)
        return k * MINUTES * extra
    return MINUTES * (2 if design == "orchestrated" else 1) + 1     # parallel


DESIGNS = ["single", "single+compaction", "independent", "orchestrated"]
for task, label in [("breadth", "Breadth (10 independent sub-topics): share answered correctly"),
                    ("chain", "Chain (6 dependent steps): share of runs with every step right")]:
    print(label)
    print(f"  {'design':<19}{'quality':>8}{'input tokens':>14}{'minutes':>9}")
    for d in DESIGNS:
        r = np.array([run(task, d) for _ in range(N)])
        print(f"  {d:<19}{r[:, 0].mean():>8.0%}{r[:, 1].mean():>14,.0f}{minutes(task, d):>9.0f}")
    print()
