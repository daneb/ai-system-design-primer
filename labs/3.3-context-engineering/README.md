# Lab 3.3: What each context strategy costs, and what it forgets

Supports section [3.3 Context engineering](../../docs/3-components/3.3-context-engineering.md).

**Question:** an agent runs for 40 turns, and every turn adds a 2,000-token tool result. Keep
everything, keep a sliding window, clear old tool results, or summarise? How many input tokens does
each spend over the session, and which facts survive to the end?

```sh
python3 context_budget.py
```

numpy only, seeded. The session shape is invented; summarisation keeping each fact with 90%
probability per pass is an assumption. Read the pattern, not the exact numbers.

## Prediction (before running)

The sliding window will be cheapest but forget the early constraint. Clearing tool results will cut
most of the cost and keep everything. Summarisation will sit in between and lose a little.

## Result (run 2026-11-01)

| Strategy | Input tokens, whole session | Peak context | Turn-1 constraint | Turn-15 constraint | Turn-8 tool ID |
|---|---|---|---|---|---|
| Keep all | 1,946,000 (100%) | 93,500 | kept | kept | kept |
| Sliding window (10 turns) | 876,500 (45%) | 24,500 | lost | lost | lost |
| Clear old tool results (keep 3) | 540,000 (28%) | 19,500 | kept | kept | **lost** |
| Clear tool results + notes | 541,980 (28%) | 19,560 | kept | kept | kept |
| Summarise at 30k tokens | 726,400 (37%) | 29,900 | 71% | 80% | 73% |

Prediction partly wrong. Clearing tool results was cheapest, not the window, because tool results
are most of the tokens. And clearing lost the one fact that lived only inside a tool result.

## What it shows

- **Tool results dominate.** In tool-heavy agents, clearing old tool results saves more than
  dropping whole turns, and it keeps what the user said.
- **Every strategy forgets something.** The window forgot the user's constraints; clearing forgot the
  ID in an old tool result; summarisation lost facts at random, and the loss compounds with each pass.
- **Notes fix it cheaply.** Writing the ID to a 60-token notes file kept every fact for about 0.4%
  more tokens. That is Anthropic's "structured note-taking" pattern.
- **Keeping everything costs 3.6 times as much** as clearing, and its 93k-token context is where
  context rot sets in.

## Exercises

1. Make the window 20 turns. Does it keep the turn-15 constraint? At what cost?
2. Set `KEEP_P` to 0.98. How many summarisation passes until a fact is likely lost?
3. Add prompt caching ([3.13](../../docs/3-components/3.13-caching.md)): clearing changes the prefix and
   breaks the cache. When does keeping everything become cheaper than clearing?
