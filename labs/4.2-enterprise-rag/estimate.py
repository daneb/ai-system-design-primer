"""Lab 4.2: back-of-the-envelope for the enterprise RAG assistant, lever by lever.

Prices are ILLUSTRATIVE ($ per million tokens). Change them with flags.
Standard library only.
"""
import argparse

def cost(req_day, sys_tok, chunks, chunk_tok, hist_tok, out_tok, p_in, p_out,
         cached_prefix=0, cache_ratio=0.1, small_share=0.0, small_ratio=0.2, guard_calls=0, guard_tok=0):
    inp = sys_tok + chunks * chunk_tok + hist_tok
    cached = min(cached_prefix, inp)
    big = 1 - small_share
    per_req_in = (inp - cached) * p_in + cached * p_in * cache_ratio
    per_req = (per_req_in + out_tok * p_out) * (big + small_share * small_ratio)
    per_req += guard_calls * guard_tok * p_in * small_ratio   # checks run on a small model
    return req_day * per_req / 1e6, inp

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=5000)
    ap.add_argument("--per-user", type=int, default=20)
    ap.add_argument("--p-in", type=float, default=3.0)
    ap.add_argument("--p-out", type=float, default=15.0)
    a = ap.parse_args()
    req = a.users * a.per_user
    base = dict(req_day=req, sys_tok=1500, chunks=8, chunk_tok=500, hist_tok=1500, out_tok=400,
                p_in=a.p_in, p_out=a.p_out)
    steps = [
        ("Baseline (Method worked example)", {}),
        ("+ rerank 50 candidates, send 4 chunks", {"chunks": 4}),
        ("+ cache the 1,500-token system prefix", {"chunks": 4, "cached_prefix": 1500}),
        ("+ summarise history to 500 tokens", {"chunks": 4, "cached_prefix": 1500, "hist_tok": 500}),
        ("+ route 40% of questions to a small model (0.2x price)",
         {"chunks": 4, "cached_prefix": 1500, "hist_tok": 500, "small_share": 0.4}),
        ("+ two small-model checks per answer (input + grounding, 2k tokens each)",
         {"chunks": 4, "cached_prefix": 1500, "hist_tok": 500, "small_share": 0.4,
          "guard_calls": 2, "guard_tok": 2000}),
    ]
    print(f"{req:,} requests/day; prices ${a.p_in}/M input, ${a.p_out}/M output (illustrative)\n")
    print("| Design step | Input tokens/request | Cost/day | Cost/month (22 days) | vs baseline |")
    print("|---|---|---|---|---|")
    first = None
    for name, over in steps:
        c, inp = cost(**{**base, **over})
        first = first or c
        print(f"| {name} | {inp:,} | ${c:,.0f} | ${c*22:,.0f} | {c/first:.0%} |")

if __name__ == "__main__":
    main()
