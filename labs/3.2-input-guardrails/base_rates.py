#!/usr/bin/env python3
"""Lab 3.2: what a guardrail's error rates mean at production volume.

Standard library only. Arithmetic, not simulation: for a detector with a given true-positive rate (share
of attacks it catches) and false-positive rate (share of legitimate requests it wrongly flags), how many
blocks per day are real attacks?

Usage: python3 base_rates.py [--requests 1000000]
"""
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--requests", type=int, default=1_000_000, help="requests per day")
    a = p.parse_args()
    n = a.requests

    print(f"{n:,} requests per day\n")
    print("| Attack rate | Catches (TPR) | False alarms (FPR) | Attacks blocked | Attacks missed | Legitimate requests blocked | Share of blocks that are real attacks |")
    print("|---|---|---|---|---|---|---|")
    for attack_rate in (0.001, 0.01):
        for tpr, fpr in ((0.95, 0.01), (0.95, 0.001), (0.99, 0.001)):
            attacks = n * attack_rate
            legit = n - attacks
            caught, missed = attacks * tpr, attacks * (1 - tpr)
            false_blocks = legit * fpr
            precision = caught / (caught + false_blocks)
            print(f"| {attack_rate:.1%} | {tpr:.0%} | {fpr:.1%} | {caught:,.0f} | {missed:,.0f} | "
                  f"{false_blocks:,.0f} | {precision:.0%} |")


if __name__ == "__main__":
    main()
