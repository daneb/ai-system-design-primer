# Lab 3.10: What does connecting more tools cost, and does tool search pay?

Supports section [3.10 Multi-agent topologies and protocols](../../docs/3-components/3.10-multi-agent-and-protocols.md).

**Question:** how many connectors does a shared protocol save? As an agent connects more MCP
servers, what do tool definitions cost per call? When does loading tools on demand with a tool-search
tool beat loading them all, with and without prompt caching?

```sh
python3 tool_catalog.py
```

Standard library only. About 950 tokens per tool definition comes from Anthropic's example (58 tools,
about 55k tokens). Price ($3 per million input tokens), 10,000 calls a day and the 3k-token cost of
the extra search round trip are illustrative.

## Prediction (before running)

Tool search will be cheaper than loading every tool from a few dozen tools upward.

## Result (run 2026-11-01)

| Apps × systems | Point-to-point connectors | With a shared protocol |
|---|---|---|
| 3 × 5 | 15 | 8 |
| 10 × 20 | 200 | 30 |
| 30 × 60 | 1,800 | 90 |

Tool-definition cost at 10,000 calls a day:

| Tools | Tokens, all loaded | Cost/day | Cached | Tokens, tool search | Cost/day |
|---|---|---|---|---|---|
| 10 | 9,500 | $285 | $28 | 8,250 | $248 |
| 58 | 55,100 | $1,653 | $165 | 8,250 | $248 |
| 150 | 142,500 | $4,275 | $428 | 8,250 | $248 |
| 500 | 475,000 | $14,250 | $1,425 | 8,250 | $248 |

At 500 tools the definitions alone exceed a 200k-token window.

Right tool found with one search, and with one retry: recall 98% → 98% / 100%; recall 64% → 64% / 87%;
recall 40% → 40% / 64%.

Prediction partly wrong. Without caching, tool search was cheaper from about 10 tools. With caching,
loading all 58 tools ($165 a day) was *cheaper* than searching ($248), and the crossover moved to
about 90 tools.

## What it shows

- **A protocol turns M × N integrations into M + N.** That is MCP's main value.
- **Tool definitions are a real cost.** Fifty-odd tools can take 55k tokens before the user's question.
- **Caching changes the answer.** A stable, cached tool list is cheap. Tool search wins on cost only for
  large catalogs, or where tools change per request.
- **Cost isn't the only reason.** Anthropic reports large catalogs also hurt tool *selection*, and
  tool search improved accuracy on its MCP evals. But search can miss: independent tests on catalogs of
  thousands of tools found 34–64% search accuracy. Test recall before relying on it.

## Exercises

1. Set the per-tool size to 300 tokens (lean descriptions). Where is the crossover now?
2. Give the search round trip 20k tokens (a long conversation). Does tool search still win at 150 tools?
3. Split the 150 tools across three sub-agents of 50 each. What does each call cost?
