#!/usr/bin/env python3
"""Lab 3.6: what approximate search and filtering do to recall.

Needs Python 3.9+ and numpy. Synthetic data; runs in a few seconds.

Part A builds an IVF index (k-means partitions, search only the nearest `nprobe` partitions) and
measures recall@10 against exact search as nprobe grows.

Part B gives every vector a tenant attribute and compares filtering after the vector search
(post-filter) with filtering before it (pre-filter) when the filter matches 1% of vectors.

Usage: python3 ann_and_filters.py [--seed 7]
"""
import argparse

import numpy as np


def normalise(x):
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def make_data(rng, n=20_000, dim=64, clusters=50, queries=200):
    centres = rng.normal(size=(clusters, dim))
    labels = rng.integers(0, clusters, size=n)
    data = normalise(centres[labels] + 0.6 * rng.normal(size=(n, dim))).astype(np.float32)
    q_labels = rng.integers(0, clusters, size=queries)
    qs = normalise(centres[q_labels] + 0.6 * rng.normal(size=(queries, dim))).astype(np.float32)
    return data, qs


def kmeans(rng, x, k, iters=10):
    c = x[rng.choice(len(x), size=k, replace=False)].copy()
    for _ in range(iters):
        assign = np.argmax(x @ c.T, axis=1)  # cosine on normalised vectors
        for j in range(k):
            members = x[assign == j]
            if len(members):
                c[j] = members.mean(axis=0)
        c = normalise(c)
    return c, np.argmax(x @ c.T, axis=1)


def exact_topk(data, q, k, mask=None):
    s = data @ q
    if mask is not None:
        s = np.where(mask, s, -np.inf)
    idx = np.argpartition(-s, k)[:k]
    idx = idx[np.isfinite(s[idx])]
    return set(idx[np.argsort(-s[idx])].tolist())


def ivf_topk(data, centres, assign, q, k, nprobe):
    lists = np.argsort(-(centres @ q))[:nprobe]
    cand = np.flatnonzero(np.isin(assign, lists))
    s = data[cand] @ q
    top = cand[np.argsort(-s)[:k]]
    return top.tolist(), len(cand)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=7)
    a = p.parse_args()
    rng = np.random.default_rng(a.seed)
    data, qs = make_data(rng)
    n, k, nlist = len(data), 10, 100
    centres, assign = kmeans(rng, data, nlist)
    truth = [exact_topk(data, q, k) for q in qs]

    print(f"Part A: IVF with {nlist} partitions, {n:,} vectors, {len(qs)} queries, recall@{k}\n")
    print("| nprobe | recall@10 | vectors scored (share of index) |")
    print("|---|---|---|")
    curve_x, curve_y = [], []
    for nprobe in (1, 2, 4, 8, 16, 32, 100):
        rec, scanned = [], []
        for q, t in zip(qs, truth):
            got, c = ivf_topk(data, centres, assign, q, k, nprobe)
            rec.append(len(t & set(got)) / k)
            scanned.append(c / n)
        print(f"| {nprobe} | {np.mean(rec):.3f} | {np.mean(scanned):.1%} |")
        curve_x.append(float(np.mean(scanned))); curve_y.append(float(np.mean(rec)))

    tenant = rng.integers(0, 100, size=n)  # each tenant owns ~1% of vectors
    print(f"\nPart B: filter tenant == 0 (matches {np.mean(tenant == 0):.1%} of vectors), k = {k}\n")
    print("| Strategy | results returned (mean) | recall vs filtered truth |")
    print("|---|---|---|")
    mask = tenant == 0
    ftruth = [exact_topk(data, q, k, mask) for q in qs]
    for label, cand_k in (("post-filter: top-10 ANN, then filter", 10),
                          ("post-filter: top-100 ANN, then filter", 100)):
        returned, rec = [], []
        for q, t in zip(qs, ftruth):
            got, _ = ivf_topk(data, centres, assign, q, cand_k, nprobe=8)
            kept = [i for i in got if mask[i]][:k]
            returned.append(len(kept))
            rec.append(len(t & set(kept)) / k)
        print(f"| {label} | {np.mean(returned):.1f} | {np.mean(rec):.3f} |")
    returned = [len(exact_topk(data, q, k, mask)) for q in qs]
    print(f"| pre-filter: search only tenant 0's vectors | {np.mean(returned):.1f} | 1.000 |")


    # ---- Chart (optional; needs matplotlib) --------------------------------------------------------
    import pathlib as _pl, sys as _sys
    _sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
    from chart import line_chart
    CHART_PATH = _pl.Path(__file__).with_name("result.svg")
    line_chart(CHART_PATH, curve_x, {"IVF, 100 partitions": curve_y},
               title="Scoring 4% of the index already finds almost every true neighbour",
               xlabel="Share of the index scored (more partitions searched)", ylabel="Recall@10",
               logx=True, xpercent=True, xticks=[0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0],
               xticklabels=["1%", "2%", "5%", "10%", "20%", "50%", "100%"], ylim=(0.7, 1.02))

if __name__ == "__main__":
    main()
