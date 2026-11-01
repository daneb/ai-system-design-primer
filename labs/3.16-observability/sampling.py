"""Lab 3.16: which agent traces should you keep?

200,000 agent runs a day. Each run produces a trace of SPANS spans. Per run:
  0.5% hard errors (exception, timeout, tool error)  - visible in the trace status
  1.0% slow runs (over the latency target)          - visible in the duration
  3.0% silent failures (wrong or unsafe answer, no error) - invisible unless something scores it
Policies:
  keep-all       - store every trace
  head 1%        - decide at the start, keep 1% at random
  tail           - decide at the end: keep every error and slow run, plus 1% of the rest
  tail+eval      - tail, plus an online evaluator (a cheap judge on a 10% sample) that flags
                   silent failures with recall JUDGE_RECALL and false-positive rate JUDGE_FPR
Trace size with full content (prompts, tool results) vs metadata only. Storage cost illustrative.
numpy only, seeded.
"""
import numpy as np

rng = np.random.default_rng(1)
RUNS, ERR, SLOW, SILENT = 200_000, 0.005, 0.01, 0.03
CONTENT_KB, META_KB = 60, 4                 # per trace
GB_DAY_COST = 0.50                          # $ per GB ingested + 30-day retention, illustrative
EVAL_SAMPLE, JUDGE_RECALL, JUDGE_FPR, JUDGE_COST = 0.10, 0.7, 0.05, 0.002   # $ per judged run

u = rng.random(RUNS)
kind = np.where(u < ERR, "error", np.where(u < ERR + SLOW, "slow", np.where(u < ERR + SLOW + SILENT, "silent", "ok")))
rand = rng.random(RUNS)
judged = rng.random(RUNS) < EVAL_SAMPLE
flag = judged & (((kind == "silent") & (rng.random(RUNS) < JUDGE_RECALL)) |
                 ((kind == "ok") & (rng.random(RUNS) < JUDGE_FPR)))

policies = {
    "keep-all": np.ones(RUNS, bool),
    "head 1%": rand < 0.01,
    "tail": (kind == "error") | (kind == "slow") | (rand < 0.01),
    "tail+eval": (kind == "error") | (kind == "slow") | flag | (rand < 0.01),
}

print(f"{'policy':<11}{'kept':>8}{'errors':>8}{'slow':>7}{'silent':>8}{'GB/day full':>12}{'$/day':>8}{'GB/day meta':>12}{'judge $/day':>12}")
for name, keep in policies.items():
    caught = {k: keep[kind == k].mean() for k in ["error", "slow", "silent"]}
    gb_full = keep.sum() * CONTENT_KB / 1e6
    gb_meta = keep.sum() * META_KB / 1e6
    judge = judged.sum() * JUDGE_COST if name == "tail+eval" else 0
    print(f"{name:<11}{keep.sum():>8,}{caught['error']:>8.0%}{caught['slow']:>7.0%}{caught['silent']:>8.0%}"
          f"{gb_full:>12.1f}{gb_full * GB_DAY_COST:>8.2f}{gb_meta:>12.2f}{judge:>12.0f}")

silent_total = (kind == "silent").sum()
print(f"\nSilent failures a day: {silent_total:,}. Flagged by the judge: {(flag & (kind == 'silent')).sum():,}"
      f" ({(flag & (kind == 'silent')).sum() / silent_total:.0%}); false flags on good runs: {(flag & (kind == 'ok')).sum():,}")

print("\nIf traces must be retained for 7 years (illustrative; record-keeping rules vary by jurisdiction and record type):")
for name, keep in policies.items():
    for label, kb in [("full content", CONTENT_KB), ("metadata only", META_KB)]:
        tb = keep.sum() * kb * 365 * 7 / 1e9
        print(f"  {name:<10} {label:<14} {tb:>7.1f} TB")
