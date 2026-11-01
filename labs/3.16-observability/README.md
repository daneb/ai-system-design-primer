# Lab 3.16: Which agent traces should you keep?

Supports section [3.16 Observability](../../docs/3-components/3.16-observability.md).

**Question:** 200,000 agent runs a day. 0.5% fail with an error, 1% are slow, and 3% give a wrong or
unsafe answer with no error at all. Which failures does each sampling policy keep: everything, a random
1% chosen up front (head sampling), every error and slow run plus 1% (tail sampling), or tail sampling
plus an online judge on a 10% sample? What does it cost to store, with and without prompt content?

```sh
python3 sampling.py
```

numpy only, seeded. Failure rates, trace sizes (60 KB with content, 4 KB metadata only), storage price
and the judge's cost and accuracy (70% recall, 5% false positives) are assumptions.

## Prediction (before running)

Tail sampling will catch every error at a few percent of the storage. Storage will be the main cost of
keeping everything.

## Result (run 2026-11-01)

| Policy | Traces kept | Errors kept | Slow kept | Silent failures kept | GB/day (full) | $/day | GB/day (metadata) | Judge $/day |
|---|---|---|---|---|---|---|---|---|
| Keep all | 200,000 | 100% | 100% | 100% | 12.0 | 6.00 | 0.80 | 0 |
| Head 1% | 1,957 | 1% | 1% | 1% | 0.1 | 0.06 | 0.01 | 0 |
| Tail | 4,940 | 100% | 100% | 1% | 0.3 | 0.15 | 0.02 | 0 |
| Tail + online judge | 6,304 | 100% | 100% | 8% | 0.4 | 0.19 | 0.03 | 40 |

Silent failures a day: 5,899. The judge flagged 415 of them (7%), and flagged 965 good runs by mistake.

Kept for 7 years: everything with content ≈ 31 TB; metadata only ≈ 2 TB; tail sampling with content ≈ 0.8 TB.

Prediction partly wrong. Tail sampling did catch every error and slow run. But storage was cheap at
this scale ($6 a day to keep everything); the judge cost more than storage. And the real gap was
silent failures, which no sampling policy based on errors or latency can see.

## What it shows

- **Head sampling throws away the failures you need.** 1% random kept 1% of errors.
- **Tail sampling keeps all errors and slow runs** for about 2.5% of the traces.
- **The dangerous failures don't raise errors.** Wrong answers need an evaluator to find them, and a
  judge on a 10% sample found 7%. Raise the sample, or add cheap checks on every run ([3.15](../../docs/3-components/3.15-evals.md)).
- **At low base rates, most flags are false.** 965 false flags against 415 true ones: route flags to
  review, not straight to action.
- **Content is the privacy and retention problem, not the cost problem.** Prompts and tool results are
  15× the size of metadata and contain personal data. Decide what you capture, redact it, and restrict
  who can read it.

## Exercises

1. Judge every run (`EVAL_SAMPLE = 1.0`). What share of silent failures is caught, and what does it cost?
2. Drop `JUDGE_FPR` to 0.01. How many false flags now?
3. Keep content only for kept traces and metadata for all. What does seven-year retention come to?
