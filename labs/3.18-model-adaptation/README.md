# Lab 3.18: What LoRA trains, and when a fine-tune pays for itself

Supports section [3.18 Model adaptation](../../docs/3-components/3.18-model-adaptation.md).

**Question:** how small is a LoRA adapter compared with the model it adapts? And if a fine-tuned small
model can replace a large model plus a long few-shot prompt, at what monthly volume does that pay,
once you count the dataset, re-validation and hosting?

```sh
python3 adaptation_math.py
```

Standard library only. Model shapes are simplified; all prices are illustrative round numbers.

## Prediction (before running)

Adapters will be well under 1% of the base model. Per request, the tuned small model will be more
than 10× cheaper, so it will pay off at modest volume, unless it needs dedicated hosting.

## Result (run 2026-11-01)

| LoRA rank | Trainable parameters | Share of base model | Adapter size (16-bit) |
|---|---|---|---|
| 4 | 4.2 M | 0.052% | 8 MB |
| 8 | 8.4 M | 0.105% | 17 MB |
| 16 | 16.8 M | 0.210% | 34 MB |
| 64 | 67.1 M | 0.839% | 134 MB |

Per request: large model with a few-shot prompt $12.90 per 1,000; tuned small model $0.56 per 1,000.

| Hosting for the tuned model | Monthly fixed cost | Break-even requests per month | At 100k/month: saving per year |
|---|---|---|---|
| pay per token (no hosting fee) | $1,083 | 87,790 | $1,808 |
| dedicated capacity, $5/hour | $4,733 | 383,576 | −$41,992 |
| dedicated capacity, $20/hour | $15,683 | 1,270,935 | −$173,392 |

Prediction partly wrong: even pay-per-token only just broke even at 100,000 requests a month.

## What it shows

- **LoRA trains a sliver.** A rank-16 adapter is 0.2% of an 8B model and 34 MB on disk, which is why
  many adapters can share one base model.
- **The per-call saving is real, and isn't the whole bill.** The tuned model was 23× cheaper per call,
  yet the dataset ($8,000 here), training and re-validation on each base-model upgrade dominate at
  moderate volume. Count the people-time, not just the training run.
- **Dedicated hosting changes everything.** Where a platform requires reserved capacity for custom
  models, a fine-tune needs hundreds of thousands to millions of calls a month to pay back.
- **The alternative is cheap too.** Prompt caching cuts the long few-shot prompt's cost without any
  training ([3.13](../../docs/3-components/3.13-caching.md)); compare against that, not the uncached price.

## Exercises

1. Apply a 0.1× cache price to 3,000 of the large model's input tokens. What happens to the break-even?
2. Halve the dataset cost. At what volume does pay-per-token hosting break even now?
3. A fine-tune dies with its base model. Add a full rebuild every 12 months. Does the case survive?
