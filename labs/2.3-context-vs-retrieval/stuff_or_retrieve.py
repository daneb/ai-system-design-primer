"""Lab 2.3: when is putting the whole corpus in the prompt cheaper than retrieval?

Daily input cost of three ways to answer questions over a corpus:
  stuff         - send the whole corpus with every question
  stuff+cache   - same, with prompt caching (reads 0.1x, writes 1.25x, 5-minute lifetime
                  refreshed on each hit; queries spread evenly over the day)
  retrieve      - send ~2,500 retrieved tokens per question, plus a fixed daily cost for
                  the search index
Also prints time to first token if prefill runs at PREFILL tokens/s; a cache hit is assumed to
cut that by 85% (the "up to" figure Anthropic quotes), which is optimistic.
Prices are illustrative placeholders; read the ratios. Standard library only.
"""
PRICE = 3.00 / 1e6          # $ per input token (illustrative)
READ, WRITE, TTL_MIN = 0.10, 1.25, 5
QUESTION, RETRIEVED = 200, 2_500
INDEX_PER_DAY = 10.00       # managed search index, illustrative
PREFILL = 10_000            # tokens per second, illustrative


def stuff(c, q):
    return q * (c + QUESTION) * PRICE


def stuff_cached(c, q):
    gap_min = 24 * 60 / q
    if gap_min > TTL_MIN:                     # cache expires between questions: every call writes
        return q * (c * WRITE + QUESTION) * PRICE
    return (c * WRITE + (q - 1) * c * READ + q * QUESTION) * PRICE   # one write, then reads


def retrieve(c, q):
    return q * (RETRIEVED + QUESTION) * PRICE + INDEX_PER_DAY


print(f"{'corpus':>9} {'questions/day':>14} {'stuff':>10} {'stuff+cache':>12} {'retrieve':>10}  cheapest")
for c in [20_000, 100_000, 500_000, 1_000_000]:
    for q in [50, 1_000, 20_000]:
        costs = {"stuff": stuff(c, q), "stuff+cache": stuff_cached(c, q), "retrieve": retrieve(c, q)}
        best = min(costs, key=costs.get)
        print(f"{c:>9,} {q:>14,} " + " ".join(f"${v:>9,.2f}".rjust(11) for v in costs.values()) + f"  {best}")

print("\nBreak-even corpus size (stuff+cache = retrieve), warm cache:")
for q in [1_000, 20_000]:
    lo, hi = 1_000, 10_000_000
    while hi - lo > 100:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if stuff_cached(mid, q) < retrieve(mid, q) else (lo, mid)
    print(f"  {q:>6,} questions/day: about {lo:,} tokens")

print("\nTime to first token from prefill (cache miss / hit / retrieval incl. ~150 ms search):")
for c in [20_000, 100_000, 500_000, 1_000_000]:
    miss = (c + QUESTION) / PREFILL
    print(f"  {c:>9,} tokens: {miss:5.1f} s / {miss * 0.15:4.1f} s / {(RETRIEVED + QUESTION) / PREFILL + 0.15:.1f} s")
