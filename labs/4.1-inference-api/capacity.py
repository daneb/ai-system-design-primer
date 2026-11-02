"""Lab 4.1: how many accelerators does a self-hosted inference API need?

Roofline estimate (same assumptions as Lab 2.7), for a 70B-parameter model in 8-bit weights served with
2-way tensor parallelism on 80 GB, 3.35 TB/s accelerators. Illustrative, not a benchmark: real engines
reach a fraction of these bounds, so we apply an efficiency factor.
Standard library only.
"""
import math

PARAMS = 70e9; BYTES = 1.0                    # 8-bit weights
TP = 2; HBM = 80e9; BW = 3.35e12; FLOPS = 1.0e15   # per accelerator (usable, 8-bit, generous)
EFF = 0.5                                     # engines reach maybe half the roofline
KV_TOKEN = 2 * 80 * 8 * 128 * 1               # 80 layers, 8 KV heads, dim 128, 8-bit cache = 160 KB
IN_TOK, OUT_TOK = 3000, 300                   # per request
TPOT_SLO = 0.050                              # 50 ms per output token (20 tok/s per user)

weights = PARAMS * BYTES
kv_req = KV_TOKEN * (IN_TOK + OUT_TOK)
max_batch_mem = int((TP * HBM * 0.9 - weights) // kv_req)

def step(b):        # one decode step for a replica of TP accelerators
    mem = (weights + b * kv_req) / (TP * BW)
    comp = 2 * PARAMS * b / (TP * FLOPS)
    return max(mem, comp) / EFF

b = 1
while b < max_batch_mem and step(b + 1) <= TPOT_SLO:
    b += 1
decode_tps = b / step(b)
prefill_s = 2 * PARAMS * IN_TOK / (TP * FLOPS * EFF)           # compute-bound
# share of time a replica spends on prefill vs decode, per request
req_per_s_replica = 1 / (prefill_s + OUT_TOK / decode_tps)

print(f"Weights {weights/1e9:.0f} GB over {TP} accelerators; cache per request {kv_req/1e6:.0f} MB; memory fits {max_batch_mem} requests")
print(f"Largest batch within {TPOT_SLO*1000:.0f} ms/token: {b}; decode {decode_tps:,.0f} tokens/s per replica")
print(f"Prefill of {IN_TOK:,} tokens: {prefill_s*1000:.0f} ms; sustainable ≈ {req_per_s_replica:.1f} requests/s per replica\n")
print("| Peak requests/s | Replicas at 100% | Replicas at 60% target utilisation | Accelerators (+1 replica spare) |")
print("|---|---|---|---|")
for peak in (1, 5, 10, 25, 50):
    full = peak / req_per_s_replica
    r60 = math.ceil(peak / (req_per_s_replica * 0.6))
    print(f"| {peak} | {full:.1f} | {r60} | {(r60 + 1) * TP} |")

# ---- Chart (optional; needs matplotlib) --------------------------------------------------------
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from chart import line_chart
CHART_PATH = _pl.Path(__file__).with_name("result.svg")
peaks = list(range(1, 51))
line_chart(CHART_PATH, peaks, {"Accelerators": [(math.ceil(p / (req_per_s_replica * 0.6)) + 1) * TP for p in peaks]},
           title="Accelerators needed at 60% target utilisation, plus one spare replica",
           xlabel="Peak requests per second", ylabel="Accelerators (2 per replica)")
