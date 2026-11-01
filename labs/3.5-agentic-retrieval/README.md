# Lab 3.5: Single-shot retrieval, query fan-out, or an agent loop?

Supports section [3.5 Agentic retrieval](../../docs/3-components/3.5-agentic-retrieval.md).

**Question:** for a one-fact lookup, a three-part question ("compare A, B and C") and a three-hop
chain (the query for fact 2 needs fact 1's answer), how often does each strategy retrieve everything
it needs, and what does it cost in model calls and sequential rounds?

```sh
python3 hops.py
```

numpy only, seeded. All retrieval probabilities are assumptions: a focused query finds its fact 85% of
the time, a mixed query 60% per fact, a query for a fact it can't name yet 20%. The agent notices a miss
80% of the time and stops too early 7% of the time per fact. Read the shape.

## Prediction (before running)

The agent will win on multi-hop and lose on cost everywhere. Fan-out will match the agent on
multi-part questions at lower latency.

## Result (run 2026-11-01)

| Question | Strategy | Correct | Model calls | Searches | Sequential rounds |
|---|---|---|---|---|---|
| Lookup | single | 85% | 1.0 | 1.0 | 1.0 |
| Lookup | fan-out | 85% | 2.0 | 1.0 | 2.0 |
| Lookup | agent | 90% | 2.1 | 1.1 | 1.1 |
| Multi-part | single | 21% | 1.0 | 1.0 | 1.0 |
| Multi-part | fan-out | 61% | 2.0 | 3.0 | 2.0 |
| Multi-part | agent | 72% | 4.1 | 3.1 | 3.1 |
| Multi-hop | single | 3% | 1.0 | 1.0 | 1.0 |
| Multi-hop | fan-out | 3% | 2.0 | 3.0 | 2.0 |
| Multi-hop | agent | 72% | 4.1 | 3.1 | 3.1 |

Prediction partly wrong. The agent won multi-hop as expected, but it also beat fan-out on multi-part
questions, because it could retry a missed sub-query. Fan-out was still faster (2 rounds vs 3.1).

## What it shows

- **Single-shot retrieval fails on anything compound.** One mixed query found all three parts only
  21% of the time.
- **Fan-out fixes independent parts, not chains.** Sub-queries planned up front can't name what a
  later hop needs, so multi-hop stayed at 3%.
- **The loop is what solves chains.** Search, read, then search again with what you learned.
- **It costs about four times the model calls** and runs sequentially. For lookups it bought five
  points over a single search.
- **Route by question type.** Single-shot for lookups, fan-out for multi-part, an agent for multi-hop.

## Exercises

1. Combine them: fan out first, then let an agent fill the gaps. What does multi-part cost now?
2. Set `NOTICE` to 0.5 (an agent that rarely notices misses). How much of its advantage is left?
3. Raise `EARLY` to 0.2, as in the code-search study in the deep dive, where agents often stopped
   with a confident wrong answer. Does single-shot ever win?
