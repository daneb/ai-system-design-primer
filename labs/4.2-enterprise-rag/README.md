# Lab 4.2: Where the money goes in an enterprise RAG assistant

Supports section [4.2 Design an enterprise RAG assistant](../../docs/4-solved-designs/4.2-enterprise-rag-assistant.md).

**Question:** starting from the Method's worked example (100,000 questions a day, 7,000 input tokens
each), which design choices move the bill most, and what do the safety checks cost?

```sh
python3 estimate.py
python3 estimate.py --p-in 1.25 --p-out 10     # try your own prices
```

Standard library only. Prices are illustrative; ratios matter more than dollars.

## Prediction (before running)

Sending fewer chunks will be the biggest single lever, because the system is input-bound. Routing will
come second. Guardrail checks will add back less than a quarter of what the levers saved.

## Result (run 2026-11-01)

| Design step | Input tokens/request | Cost/day | Cost/month (22 days) | vs baseline |
|---|---|---|---|---|
| Baseline (Method worked example) | 7,000 | $2,700 | $59,400 | 100% |
| + rerank 50 candidates, send 4 chunks | 5,000 | $2,100 | $46,200 | 78% |
| + cache the 1,500-token system prefix | 5,000 | $1,695 | $37,290 | 63% |
| + summarise history to 500 tokens | 4,000 | $1,395 | $30,690 | 52% |
| + route 40% of questions to a small model (0.2x price) | 4,000 | $949 | $20,869 | 35% |
| + two small-model checks per answer (2k tokens each) | 4,000 | $1,189 | $26,149 | 44% |

Prediction partly wrong: routing (−$446/day) saved slightly *less* than fewer chunks (−$600/day) but
more than caching (−$405/day); the checks added back $240/day, about 14% of the $1,751 saved.

## What it shows

- **Input tokens are the bill.** Three of the four levers cut input. Measure retrieval quality before
  cutting chunks: fewer chunks only helps if a reranker keeps the right ones
  ([3.4](../../docs/3-components/3.4-retrieval-pipeline.md)).
- **Routing depends on the router.** The 40% figure assumes a router that rarely sends a hard question
  to the small model ([Lab 2.1](../2.1-cost-quality-latency/README.md)).
- **Safety checks are affordable.** Two checks on a small model cost under a fifth of what the levers
  saved. Cost is rarely a good reason to skip them.
- **Left out:** the reranker's own per-query price, embeddings, vector store, and the gateway. Add them
  for a real estimate; they are usually small next to generation at this volume.

## Exercises

1. Set `--users 50000`. Which costs scale linearly, and which (index, platform) don't appear here?
2. What routing share would make the small model cheaper than caching plus fewer chunks combined?
3. Replace the illustrative prices with your provider's current list prices.
