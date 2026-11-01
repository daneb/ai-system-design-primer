#!/usr/bin/env python3
"""Lab 3.4: keyword vs dense vs hybrid (RRF) retrieval on a tiny labelled corpus.

Needs only Python 3.9+ and numpy.

The "dense" retriever here is latent semantic analysis (LSA): TF-IDF reduced with a truncated SVD.
It is a classical dense method, far weaker than a modern neural embedding model, and stands in only
because this lab runs offline. To try a real embedding model, replace `embed()` below.

Usage: python3 hybrid_rrf.py [--k 3] [--rank 12] [--verbose]
"""
import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
STOP = set("a an and are as at be by can do does for from get how i if in is it may must my of on or "
           "some the their to under up was we what when who will with without you your".split())


def tokenize(text):
    # Keep identifiers such as tx-4471 or hr-208 as single tokens.
    return [t for t in re.findall(r"[a-z]+-\d+|[a-z0-9]+", text.lower()) if t not in STOP]


class BM25:
    def __init__(self, docs, k1=1.5, b=0.75):
        self.docs = [tokenize(d) for d in docs]
        self.k1, self.b = k1, b
        self.avgdl = sum(len(d) for d in self.docs) / len(self.docs)
        df = Counter(t for d in self.docs for t in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query):
        q = tokenize(query)
        out = []
        for d in self.docs:
            tf = Counter(d)
            s = 0.0
            for t in q:
                if t in tf:
                    num = tf[t] * (self.k1 + 1)
                    den = tf[t] + self.k1 * (1 - self.b + self.b * len(d) / self.avgdl)
                    s += self.idf[t] * num / den
            out.append(s)
        return np.array(out)


class LSA:
    """TF-IDF + truncated SVD. Swap `embed` for a neural embedding model to make this realistic."""

    def __init__(self, docs, rank=12):
        toks = [tokenize(d) for d in docs]
        self.vocab = {t: i for i, t in enumerate(sorted({t for d in toks for t in d}))}
        n = len(docs)
        df = Counter(t for d in toks for t in set(d))
        self.idf = np.array([math.log(n / df[t]) + 1 for t in sorted(self.vocab)])
        X = np.stack([self._tfidf(d) for d in toks])
        u, s, vt = np.linalg.svd(X, full_matrices=False)
        self.vt = vt[:rank]
        self.doc_vecs = self._norm(X @ self.vt.T)

    def _tfidf(self, tokens):
        v = np.zeros(len(self.vocab))
        for t, c in Counter(tokens).items():
            if t in self.vocab:
                v[self.vocab[t]] = (1 + math.log(c)) * self.idf[self.vocab[t]]
        return v

    @staticmethod
    def _norm(m):
        return m / np.maximum(np.linalg.norm(m, axis=-1, keepdims=True), 1e-12)

    def embed(self, text):
        return self._norm(self._tfidf(tokenize(text)) @ self.vt.T)

    def scores(self, query):
        return self.doc_vecs @ self.embed(query)


def ranking(scores, ids):
    order = np.argsort(-scores, kind="stable")
    return [ids[i] for i in order if scores[i] > 0] or [ids[i] for i in order]


def rrf(rankings, c=60):
    """Reciprocal Rank Fusion (Cormack, Clarke & Buettcher, SIGIR 2009): sum of 1 / (c + rank)."""
    fused = Counter()
    for r in rankings:
        for pos, doc_id in enumerate(r, start=1):
            fused[doc_id] += 1.0 / (c + pos)
    return [d for d, _ in fused.most_common()]


def evaluate(rank_list, relevant, k):
    hit = any(d in relevant for d in rank_list[:k])
    rr = next((1.0 / i for i, d in enumerate(rank_list, start=1) if d in relevant), 0.0)
    return hit, rr


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--k", type=int, default=3, help="cut-off for recall@k")
    p.add_argument("--rank", type=int, default=12, help="LSA dimensions")
    p.add_argument("--verbose", action="store_true")
    a = p.parse_args()

    data = json.loads((HERE / "corpus.json").read_text())
    ids = [d["id"] for d in data["docs"]]
    texts = [f"{d['title']}. {d['text']}" for d in data["docs"]]
    bm25, lsa = BM25(texts), LSA(texts, rank=a.rank)

    systems = ["keyword (BM25)", "dense (LSA)", "hybrid (RRF)"]
    results = {s: {} for s in systems}
    for q in data["queries"]:
        r_kw = ranking(bm25.scores(q["text"]), ids)
        r_dn = ranking(lsa.scores(q["text"]), ids)
        r_hy = rrf([r_kw, r_dn])
        for s, r in zip(systems, (r_kw, r_dn, r_hy)):
            results[s].setdefault(q["type"], []).append(evaluate(r, set(q["relevant"]), a.k))
            results[s].setdefault("all", []).append(evaluate(r, set(q["relevant"]), a.k))
        if a.verbose:
            print(f"{q['id']} [{q['type']}] {q['text']!r} -> relevant {q['relevant']}")
            for s, r in zip(systems, (r_kw, r_dn, r_hy)):
                print(f"    {s:15} {r[:5]}")

    types = ["exact", "paraphrase", "mixed", "all"]
    print(f"\nrecall@{a.k} / MRR by query type ({len(data['queries'])} queries, {len(ids)} docs)\n")
    print(f"| System | " + " | ".join(types) + " |")
    print("|---|" + "---|" * len(types))
    for s in systems:
        cells = []
        for t in types:
            rows = results[s][t]
            rec = sum(h for h, _ in rows) / len(rows)
            mrr = sum(rr for _, rr in rows) / len(rows)
            cells.append(f"{rec:.2f} / {mrr:.2f}")
        print(f"| {s} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
