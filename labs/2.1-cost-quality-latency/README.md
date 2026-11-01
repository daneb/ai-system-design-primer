# Lab 2.1: When does routing between models pay off?

Supports section [2.1 Cost vs quality vs latency](../../docs/2-trade-offs/2.1-cost-quality-latency.md).

**Question:** if a router sends easy requests to a cheap model and hard ones to an expensive model, how
much does the router's accuracy matter?

```sh
python3 cascade.py            # large model costs 10x the small one
python3 cascade.py --price-ratio 30
```

Needs Python 3.9+ and numpy. All parameters are illustrative: a small model that is strong on easy
requests and weak on hard ones, a large model that is strong almost everywhere, and a router that
estimates each request's difficulty with a small or a large error.

## Prediction (before the first run)

With a good router, sending about half the traffic to the small model costs only 1–2 points of
accuracy; a poor router loses noticeably more at the same cost.

## Result (run 2026-11-01)

Small model alone: 77.4% accuracy at 10% of the cost. Large model alone: 95.5% at 100%.

| Router | Share sent to large model | Accuracy | Cost vs all-large |
|---|---|---|---|
| Good | 60% | 94.6% | 64% |
| Good | 40% | 92.5% | 46% |
| Good | 20% | 87.6% | 28% |
| Poor | 60% | 92.1% | 64% |
| Poor | 40% | 88.9% | 46% |
| Poor | 20% | 84.3% | 28% |

The prediction held only in part. Sending 40% of traffic to the small model (60% large) cost under one
point; sending 60% to the small model cost three. The poor router was 2.5–3.6 points worse at every
setting.

## What it shows

- **Routing is a curve, not a free lunch.** Each step of savings costs some quality; where you stop is a
  business decision that needs your eval set (see 3.15) to measure.
- **The router is the product.** At identical cost, a poor router gave up 3.4 points of accuracy at the
  60% setting. Evaluate the router itself: how often does it send a request the small model gets wrong?
- **The price gap sets the prize.** Rerun with `--price-ratio 30`: savings grow when the tiers are
  further apart.

## Exercises

1. Add a fallback: if the small model's answer fails a cheap check (for example, a schema check), retry
   on the large model. What does that do to cost and accuracy?
2. Make the small model better on hard requests (change the slope in `p_small`). When does routing stop
   paying?
