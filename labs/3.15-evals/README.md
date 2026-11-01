# Lab 3.15: How many eval cases do you need?

Supports section [3.15 Evals](../../docs/3-components/3.15-evals.md).

**Question:** if a prompt change quietly drops your pass rate from 80% to 75%, how big must the eval set
be for you to notice?

```sh
python3 eval_power.py
```

Needs Python 3.9+ and numpy. Pure simulation: no model calls, runs in under a second.

## Set-up

- Version A passes about 80% of cases, version B about 75%. Both run on the same cases.
- Cases vary in difficulty for both versions, so their results are correlated (0.26 here, a
  deliberately modest value).
- For each eval-set size, the experiment is repeated 2,000 times. We count how often a standard test
  (5% significance, two-sided, counting only detections in the right direction) concludes that B is
  worse.
  - **Unpaired:** compares the two pass rates as if they came from different cases.
  - **Paired:** compares the per-case differences, as recommended in Anthropic's
    [error-bars paper](https://arxiv.org/abs/2411.00640).

## Prediction (before the first run)

With 100 cases, the unpaired test catches the regression less than 20% of the time; the paired test
does better.

## Result (run 2026-11-01)

True rates in a large sample: A = 0.794, B = 0.746.

| Eval cases | 95% CI half-width on one pass rate | Unpaired test catches the drop | Paired test catches the drop |
|---|---|---|---|
| 25 | ±15.7% | 4% | 7% |
| 50 | ±11.1% | 6% | 10% |
| 100 | ±7.8% | 8% | 13% |
| 200 | ±5.5% | 15% | 23% |
| 500 | ±3.5% | 37% | 48% |
| 1,000 | ±2.5% | 67% | 76% |
| 2,000 | ±1.8% | 94% | 97% |

Prediction held. Sanity check (derived): the textbook sample size for 80% power to tell 80% from
75% with an unpaired test is (1.96 + 0.84)² × (0.8·0.2 + 0.75·0.25) ÷ 0.05² ≈ 1,090 cases per version,
consistent with the simulated curve.

## What it shows

1. **Small eval sets can't see small regressions.** With 100 cases, a real five-point drop is missed
   about nine times in ten. A 50-case "golden set" is a smoke test, not a release gate for small changes.
2. **Report the uncertainty.** At 100 cases, a single pass rate is only known to about ±8 points.
   A dashboard that shows 81% vs 79% without error bars invites wrong decisions.
3. **Pair your comparisons.** Running both versions on the same cases and analysing per-case differences
   always helped here, and helps more the more correlated the two versions are (exercise 1).
4. **Size the eval set to the change you need to detect.** Big regressions (80% → 60%) show up with
   tens of cases; subtle ones need hundreds to thousands, or repeated trials per case.

## Exercises

1. Raise `spread` in `simulate()` to make case difficulty matter more (higher correlation between A and
   B). How much does pairing help now?
2. Change `gap` so B is 10 points worse. How many cases do you need now?
3. Run each case three times per version and average. Does it beat tripling the number of cases?
