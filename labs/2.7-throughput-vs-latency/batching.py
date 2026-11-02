"""Lab 2.7: why batching raises throughput, what it costs each user, and why you can't run at 100%.

Part 1: a roofline estimate of one decode step for an 8B-parameter model on one accelerator.
Part 2: queueing delay as utilisation rises (single server, Poisson arrivals, fixed service time).
numpy only; all hardware figures are ROUND ILLUSTRATIVE NUMBERS, not a benchmark.
"""
import numpy as np

# ---- Part 1: decode step time vs batch size --------------------------------------------
PARAMS = 8e9                 # model parameters
BYTES_PER_PARAM = 2          # 16-bit weights
HBM_GB = 80                  # accelerator memory
BW = 2.0e12                  # memory bandwidth, bytes/s
FLOPS = 4.0e14               # usable compute, FLOP/s (well below peak)
KV_PER_TOKEN = 2 * 32 * 8 * 128 * 2   # K and V, 32 layers, 8 KV heads, head dim 128, 2 bytes = 131 kB
CONTEXT = 2000               # tokens of context held per sequence

weights = PARAMS * BYTES_PER_PARAM
kv_seq = KV_PER_TOKEN * CONTEXT
max_batch = int((HBM_GB * 1e9 - weights) // kv_seq)

def step_time(b):
    mem = (weights + b * kv_seq) / BW          # read all weights once, plus each sequence's KV cache
    comp = 2 * PARAMS * b / FLOPS              # ~2 FLOPs per parameter per token
    return max(mem, comp)

print(f"Weights {weights/1e9:.0f} GB; KV cache per sequence {kv_seq/1e6:.0f} MB; memory fits {max_batch} sequences\n")
print("| Batch | Step time (ms) | Tokens/s per user | Tokens/s total | Meets 30 ms per-token SLO? |")
print("|---|---|---|---|---|")
for b in [1, 8, 32, 64, 128, 192, max_batch]:
    t = step_time(b)
    print(f"| {b} | {t*1e3:.1f} | {1/t:.0f} | {b/t:,.0f} | {'yes' if t <= 0.030 else 'no'} |")

# ---- Part 2: queueing delay vs utilisation ----------------------------------------------
rng = np.random.default_rng(3)
SERVICE = 0.2                # seconds of work per request (e.g. a prefill), fixed
N = 200_000
print("\n| Utilisation | Mean wait (ms) | p95 wait (ms) | p99 wait (ms) |")
print("|---|---|---|---|")
for rho in [0.5, 0.7, 0.85, 0.95]:
    gaps = rng.exponential(SERVICE / rho, N)
    arrive = np.cumsum(gaps)
    start = np.empty(N); done_prev = 0.0
    for i in range(N):                       # Lindley recursion, single server
        start[i] = max(arrive[i], done_prev)
        done_prev = start[i] + SERVICE
    wait = (start - arrive) * 1e3
    print(f"| {rho:.0%} | {wait.mean():,.0f} | {np.percentile(wait,95):,.0f} | {np.percentile(wait,99):,.0f} |")

# ---- Chart (optional; needs matplotlib) --------------------------------------------------------
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from chart import line_chart
CHART_PATH = _pl.Path(__file__).with_name("result.svg")
bs = list(range(1, max_batch + 1, 4))
line_chart(CHART_PATH, bs, {"Decode step time": [step_time(b) * 1e3 for b in bs]},
           title="Bigger batches slow every user's tokens; the latency target caps the batch",
           xlabel="Sequences in the batch", ylabel="Time per output token (ms)",
           ref=(30, "30 ms per-token target"))
