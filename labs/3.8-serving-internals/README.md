# Lab 3.8: Cache arithmetic and when speculation pays

Supports section [3.8 Serving internals](../../docs/3-components/3.8-serving-internals.md).

**Question:** how much memory does one long request's attention cache take, and how much do
grouped-query attention and 8-bit caches save? When does speculative decoding speed things up, and
when does it slow them down?

```sh
python3 serving_math.py
```

Standard library only. Pure arithmetic from the published formulas; model shapes are illustrative.

## Prediction (before running)

A 128k-token request on an 8B model will need tens of gigabytes of cache without grouped-query
attention. Speculative decoding will help at high acceptance rates and hurt when the draft model is
expensive and often wrong.

## Result (run 2026-11-01)

| Model shape | Cache bytes | Per token | 8k-token request | 128k-token request |
|---|---|---|---|---|
| 8B, full multi-head attention (32 KV heads) | 16-bit | 512 KB | 4.29 GB | 68.7 GB |
| 8B, full multi-head attention (32 KV heads) | 8-bit | 256 KB | 2.15 GB | 34.4 GB |
| 8B, grouped-query attention (8 KV heads) | 16-bit | 128 KB | 1.07 GB | 17.2 GB |
| 8B, grouped-query attention (8 KV heads) | 8-bit | 64 KB | 0.54 GB | 8.6 GB |
| 70B, grouped-query attention (8 KV heads) | 16-bit | 320 KB | 2.68 GB | 42.9 GB |
| 70B, grouped-query attention (8 KV heads) | 8-bit | 160 KB | 1.34 GB | 21.5 GB |

| Acceptance rate | Draft length | Tokens per target pass | Speed-up (draft cost 5%) | Speed-up (draft cost 20%) |
|---|---|---|---|---|
| 30% | 3 | 1.42 | 1.23x | 0.89x |
| 30% | 6 | 1.43 | 1.10x | 0.65x |
| 50% | 3 | 1.88 | 1.63x | 1.17x |
| 50% | 6 | 1.98 | 1.53x | 0.90x |
| 70% | 3 | 2.53 | 2.20x | 1.58x |
| 70% | 6 | 3.06 | 2.35x | 1.39x |
| 85% | 3 | 3.19 | 2.77x | 1.99x |
| 85% | 6 | 4.53 | 3.48x | 2.06x |

Prediction held.

## What it shows

- **Long context is a memory problem.** One 128k-token request on an 8B model with full multi-head
  attention needs 69 GB of cache, more than four times the model's own 16 GB of weights. Grouped-query
  attention (sharing each key and value across several query heads) cuts it 4×, and an 8-bit cache
  halves it again.
- **Bigger models aren't always worse per token.** The 70B shape here uses less cache per token than
  the 8B model without grouped-query attention, because architecture matters as much as size.
- **Speculation is a bet on the acceptance rate.** At 70–85% acceptance with a cheap draft, 2–3.5×
  faster decoding is realistic, matching the published 2–3×. At 30% acceptance with a draft costing
  20% of the target, it is *slower* than not speculating, and longer drafts make it worse.
- **What the formula leaves out:** it assumes a verification pass costs one ordinary step, which holds
  at small batches. On a busy server the spare capacity speculation uses is already taken by other
  requests, so the gain shrinks.

## Exercises

1. A 16-bit 70B model has 140 GB of weights. On two 80 GB accelerators, how many 8k-token requests'
   caches fit alongside it?
2. Find the lowest acceptance rate at which a 3-token draft costing 20% still breaks even.
3. Why does a code-completion workload usually get a higher acceptance rate than open-ended chat?
