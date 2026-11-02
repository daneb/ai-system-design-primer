"""Lab 0.2: why output tokens cost more than input tokens, why the KV cache exists, and what
reasoning tokens do to a bill and a wait.

Part 1: a roofline estimate of prefill (whole prompt at once) and decode (one token per step) for an
8B-parameter model on one accelerator, using the same round numbers as Lab 2.7.
Part 2: arithmetic for generating 500 tokens after a 2,000-token prompt, with and without a KV cache.
Part 3: one 300-token answer with different amounts of hidden reasoning.
Standard library only. All hardware figures are ROUND ILLUSTRATIVE NUMBERS, not a benchmark.
"""
PARAMS = 8e9                 # model parameters
WEIGHTS = PARAMS * 2         # 16-bit weights, bytes
BW = 2.0e12                  # memory bandwidth, bytes/s
FLOPS = 4.0e14               # usable compute, FLOP/s (well below peak)
KV_PER_TOKEN = 2 * 32 * 8 * 128 * 2   # K and V, 32 layers, 8 KV heads, head dim 128, 2 bytes

def prefill_s(tokens):
    return max(2 * PARAMS * tokens / FLOPS, WEIGHTS / BW)       # compute-bound for real prompts

def decode_step_s(batch, context):
    mem = (WEIGHTS + batch * context * KV_PER_TOKEN) / BW       # read weights + every KV cache
    return max(mem, 2 * PARAMS * batch / FLOPS)

# ---- Part 1 -----------------------------------------------------------------------------------
print("| Work | Time | Tokens per second | Accelerator-seconds per 1,000 tokens |")
print("|---|---|---|---|")
for n in (500, 2000, 8000):
    s = prefill_s(n)
    print(f"| Prefill a {n:,}-token prompt | {s*1000:.0f} ms | {n/s:,.0f} | {1000*s/n:.3f} |")
for b in (1, 16, 64):
    s = decode_step_s(b, 2000)
    print(f"| Decode, batch {b}, 2,000 tokens of context | {s*1000:.1f} ms per step | {b/s:,.0f} | {1000*s/b:.3f} |")

# ---- Part 2 -----------------------------------------------------------------------------------
P, N = 2000, 500
with_cache = 2 * PARAMS * (P + N)                                # each token's layers computed once
without = sum(2 * PARAMS * (P + i) for i in range(1, N + 1))     # re-run the whole sequence per token
print(f"\nGenerate {N} tokens after a {P:,}-token prompt:")
print(f"- with a KV cache: {with_cache/1e12:,.0f} TFLOP; without: {without/1e12:,.0f} TFLOP "
      f"({without/with_cache:.0f}x more work)")
print(f"- cost of holding it: {KV_PER_TOKEN*(P+N)/1e6:.0f} MB of accelerator memory for this one request")

# ---- Part 3 -----------------------------------------------------------------------------------
IN, OUT, ANSWER, PROMPT = 1.0, 5.0, 300, 2000      # price per token: output 5x input (relative units)
step = decode_step_s(16, 4000)                     # a moderately busy server
print("\n| Hidden reasoning tokens | Output tokens billed | Relative cost of the call | Time to finish at batch 16 |")
print("|---|---|---|---|")
base = PROMPT * IN + ANSWER * OUT
for r in (0, 1000, 4000, 12000):
    cost = PROMPT * IN + (ANSWER + r) * OUT
    t = prefill_s(PROMPT) + (ANSWER + r) * step
    print(f"| {r:,} | {ANSWER + r:,} | {cost/base:.1f}x | {t:.1f} s |")
