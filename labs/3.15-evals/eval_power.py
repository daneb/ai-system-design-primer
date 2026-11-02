#!/usr/bin/env python3
"""Lab 3.15: how many eval cases do you need to catch a regression?

Needs Python 3.9+ and numpy. Simulation only; no model calls. Runs in a few seconds.

Version A passes about 80% of cases; version B (a "small" regression) passes about 75%. Both run on
the SAME cases, and some cases are harder than others for both versions, so their results are
correlated. For each eval-set size we repeat the experiment many times and count how often each test
says "B is worse" at the 5% significance level:

  - unpaired: compare the two pass rates as if they came from different cases
  - paired:   compare per-case differences (the approach Anthropic's error-bars paper recommends)

Usage: python3 eval_power.py [--trials 2000] [--seed 11]
"""
import argparse
import math

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def simulate(rng, n, trials, base=1.85, gap=0.33, spread=1.5):
    d = rng.normal(size=(trials, n))                       # case difficulty, shared by A and B
    pa, pb = sigmoid(base + spread * d), sigmoid(base - gap + spread * d)
    a = (rng.random((trials, n)) < pa).astype(float)
    b = (rng.random((trials, n)) < pb).astype(float)
    return a, b


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--trials", type=int, default=2000)
    p.add_argument("--seed", type=int, default=11)
    args = p.parse_args()
    rng = np.random.default_rng(args.seed)

    a, b = simulate(rng, 20_000, 1)
    print(f"True pass rates (large sample): A = {a.mean():.3f}, B = {b.mean():.3f}, "
          f"per-case correlation = {np.corrcoef(a[0], b[0])[0, 1]:.2f}\n")

    z = 1.96
    print("| Eval cases | 95% CI half-width on one pass rate | Unpaired test detects B < A | Paired test detects B < A |")
    print("|---|---|---|---|")
    ns, curve_u, curve_p = (25, 50, 100, 200, 500, 1000, 2000), [], []
    for n in ns:
        a, b = simulate(rng, n, args.trials)
        ma, mb = a.mean(1), b.mean(1)
        se_unpaired = np.sqrt(ma * (1 - ma) / n + mb * (1 - mb) / n)
        diff = a - b
        se_paired = diff.std(1, ddof=1) / math.sqrt(n)
        with np.errstate(divide="ignore", invalid="ignore"):
            unpaired = np.mean((ma - mb) / se_unpaired > z)
            paired = np.mean(np.nan_to_num((ma - mb) / se_paired) > z)
        half = z * math.sqrt(0.8 * 0.2 / n)
        curve_u.append(unpaired); curve_p.append(paired)
        print(f"| {n} | ±{half:.1%} | {unpaired:.0%} | {paired:.0%} |")


    # ---- Chart (optional; needs matplotlib) --------------------------------------------------------
    import pathlib as _pl, sys as _sys
    _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
    from chart import line_chart
    CHART_PATH = _pl.Path(__file__).with_name("result.svg")
    line_chart(CHART_PATH, list(ns), {"Paired test": curve_p, "Unpaired test": curve_u},
               title="Catching a 5-point regression takes about a thousand cases",
               xlabel="Eval cases", ylabel="Chance the test detects B < A", ypercent=True, logx=True,
               xticks=list(ns), ylim=(0, 1.02), ref=(0.8, "80% power"))

if __name__ == "__main__":
    main()
