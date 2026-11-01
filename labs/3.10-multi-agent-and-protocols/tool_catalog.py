"""Lab 3.10: what does connecting more tools cost, and does tool search pay?

Part 1 - integrations. M agent apps each need N systems. Point-to-point needs M x N connectors;
a shared protocol (MCP) needs M clients + N servers.
Part 2 - context. Each tool definition costs ~950 tokens (Anthropic's example: 58 tools, ~55k
tokens). Compare loading every tool on every call with a tool-search tool (~500 tokens) that
loads ~5 matching definitions on demand, at one extra model round trip.
Prompt caching (reads at 0.1x) applies to tools loaded up front; searched-in tools change per
request and are treated as uncached here.
Part 3 - search misses. If tool search finds the right tool with recall R, the rest fail unless
the agent searches again.
Prices illustrative. Standard library only.
"""
PER_TOOL, SEARCH_TOOL, LOADED = 950, 500, 5
PRICE = 3.00 / 1e6
CALLS_PER_DAY = 10_000
ROUND_TRIP_TOKENS = 3_000          # system prompt + history re-sent for the extra search call

print("Part 1: connectors to build and maintain")
print(f"  {'apps':>5} {'systems':>8} {'point-to-point':>15} {'shared protocol':>16}")
for m, n in [(3, 5), (10, 20), (30, 60)]:
    print(f"  {m:>5} {n:>8} {m * n:>15} {m + n:>16}")

print("\nPart 2: tool-definition tokens per call, and daily input cost for those tokens")
print(f"  {'tools':>6} {'all loaded':>11} {'cost/day':>9} {'cached':>8} {'search':>8} {'cost/day':>9}")
for tools in [10, 58, 150, 500, 2_000]:
    all_tok = tools * PER_TOOL
    all_cost = all_tok * PRICE * CALLS_PER_DAY
    cached = all_cost * 0.1
    search_tok = SEARCH_TOOL + LOADED * PER_TOOL + ROUND_TRIP_TOKENS
    search_cost = search_tok * PRICE * CALLS_PER_DAY
    flag = "" if all_tok < 200_000 else "  (exceeds a 200k window)"
    print(f"  {tools:>6} {all_tok:>11,} {'$' + format(all_cost, ',.0f'):>9} {'$' + format(cached, ',.0f'):>8}"
          f" {search_tok:>8,} {'$' + format(search_cost, ',.0f'):>9}{flag}")

print("\nPart 3: share of tasks that get the right tool, by search recall")
for recall in [0.98, 0.64, 0.40]:
    one = recall
    two = 1 - (1 - recall) ** 2
    print(f"  recall {recall:.0%}: one search {one:.0%}, with one retry {two:.0%}")
