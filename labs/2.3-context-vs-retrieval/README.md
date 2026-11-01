# Lab 2.3: When is the whole corpus in the prompt cheaper than retrieval?

Supports section [2.3 Context stuffing vs retrieval](../../docs/2-trade-offs/2.3-context-vs-retrieval.md).

**Question:** for corpora from 20k to 1M tokens and 50 to 20,000 questions a day, what does it cost to
send the whole corpus every time, to send it with prompt caching, or to retrieve about 2,500 tokens per
question? How long does the user wait for the first token?

```sh
python3 stuff_or_retrieve.py
```

Standard library only. Prices, the search-index cost ($10 a day) and prefill speed are illustrative;
caching uses Anthropic-style multipliers (write 1.25×, read 0.1×, 5-minute lifetime). Read the ratios.

## Prediction (before running)

With caching, stuffing will stay cheaper than retrieval up to about 200k tokens, the size Anthropic
suggests you can simply put in the prompt.

## Result (run 2026-11-01)

Daily input cost:

| Corpus | Questions/day | Stuff | Stuff + cache | Retrieve | Cheapest |
|---|---|---|---|---|---|
| 20k | 50 | $3 | $4 | $10 | stuff |
| 20k | 1,000 | $61 | $7 | $18 | stuff + cache |
| 20k | 20,000 | $1,212 | $132 | $172 | stuff + cache |
| 100k | 1,000 | $301 | $31 | $18 | retrieve |
| 100k | 20,000 | $6,012 | $612 | $172 | retrieve |
| 1M | 1,000 | $3,001 | $304 | $18 | retrieve |
| 1M | 20,000 | $60,012 | $6,015 | $172 | retrieve |

Break-even with a warm cache: about 58k tokens at 1,000 questions a day, 27k at 20,000.

Time to first token from prefill: 1M tokens takes 100 s uncached and 15 s on a cache hit;
retrieval about 0.4 s.

Prediction wrong. On token cost alone, retrieval wins from about 30–60k tokens, not 200k. At 50
questions a day caching *raised* cost, because the cache expired between questions and every call
paid the write premium.

## What it shows

- **Small corpora: stuff and cache.** Below a few tens of thousands of tokens, stuffing is cheapest
  and needs no pipeline.
- **Caching needs traffic.** If questions arrive further apart than the cache lifetime, every call pays
  the write premium.
- **Large corpora: retrieve.** Cost grows with corpus × questions for stuffing, but only with questions
  for retrieval.
- **Latency matters as much as cost.** Even cached, a million-token prompt is slow to start.
- **The lab leaves out the cost of building and running a retrieval pipeline**, which is why advice
  like Anthropic's sets the line higher. It also ignores quality: with a strong model, stuffing often
  answers better ([deep dive](../../docs/deep-dives/2.3-context-vs-retrieval.md)).

## Exercises

1. Add $500 a day of engineering time to retrieval. Where is the break-even now?
2. Set the cache lifetime to 60 minutes. What happens at 50 questions a day?
3. Route: stuff for questions that need the whole corpus (10%), retrieve for the rest. What does a day
   at 1,000 questions cost on a 500k corpus?
