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
    for label, noise in (("good (small error)", 0.3), ("poor (large error)", 1.5)):
        estimate = difficulty + rng.normal(scale=noise, size=n)
        for share_large in (0.2, 0.4, 0.6):
            threshold = np.quantile(estimate, 1 - share_large)
            to_large = estimate > threshold
            acc = np.where(to_large, ok_large, ok_small).mean()
            cost = (to_large.mean() * a.price_ratio + (~to_large).mean()) / a.price_ratio
            print(f"| {label} | {to_large.mean():.0%} | {acc:.1%} | {cost:.0%} |")


if __name__ == "__main__":
    main()
