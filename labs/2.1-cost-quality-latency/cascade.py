#!/usr/bin/env python3
"""Lab 2.1: when does routing between a small and a large model pay off?

Needs Python 3.9+ and numpy. Simulation with illustrative parameters; no model calls.

Each request has a hidden difficulty. A small model is cheap but fails more often on hard requests;
a large model costs 10x more and fails less. A router estimates difficulty (with some error) and sends
requests above a threshold to the large model. We sweep the threshold and compare a good router with a
poor one.

Usage: python3 cascade.py [--price-ratio 10] [--seed 3]
"""
import argparse

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--price-ratio", type=float, default=10.0, help="large-model cost / small-model cost")
    p.add_argument("--seed", type=int, default=3)
    a = p.parse_args()
    rng = np.random.default_rng(a.seed)

    n = 200_000
    difficulty = rng.normal(size=n)
    p_small = sigmoid(2.0 - 2.0 * difficulty)   # good on easy requests, poor on hard ones
    p_large = sigmoid(3.5 - 1.0 * difficulty)   # good almost everywhere
    ok_small = rng.random(n) < p_small
    ok_large = rng.random(n) < p_large

    all_large_acc = ok_large.mean()
    print(f"Small model alone: accuracy {ok_small.mean():.1%}, cost {1 / a.price_ratio:.0%} of large")
    print(f"Large model alone: accuracy {all_large_acc:.1%}, cost 100%\n")

    print("| Router | Share sent to large | Accuracy | Cost vs all-large |")
    print("|---|---|---|---|")
    curves, shares = {}, [i / 20 for i in range(1, 20)]
    for label, noise in (("good (small error)", 0.3), ("poor (large error)", 1.5)):
        estimate = difficulty + rng.normal(scale=noise, size=n)
        curves[f"{label.split()[0].capitalize()} router"] = [
            np.where(estimate > np.quantile(estimate, 1 - sh), ok_large, ok_small).mean() for sh in shares]
        for share_large in (0.2, 0.4, 0.6):
            threshold = np.quantile(estimate, 1 - share_large)
            to_large = estimate > threshold
            acc = np.where(to_large, ok_large, ok_small).mean()
            cost = (to_large.mean() * a.price_ratio + (~to_large).mean()) / a.price_ratio
            print(f"| {label} | {to_large.mean():.0%} | {acc:.1%} | {cost:.0%} |")


    # ---- Chart (optional; needs matplotlib) --------------------------------------------------------
    import pathlib as _pl, sys as _sys
    _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
    from chart import line_chart
    CHART_PATH = _pl.Path(__file__).with_name("result.svg")
    line_chart(CHART_PATH, shares, curves,
               title="A good router gets near large-model accuracy at half the cost",
               xlabel="Share of requests sent to the large model (cost rises with it)",
               ylabel="Accuracy", xpercent=True, ypercent=True,
               ref=(all_large_acc, f"large model alone {all_large_acc:.1%}"))

if __name__ == "__main__":
    main()
