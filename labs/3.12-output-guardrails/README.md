# Lab 3.12: How far does a quote check get you?

Supports section [3.12 Output guardrails and validation](../../docs/3-components/3.12-output-guardrails.md).

**Question:** if every claim in an answer must cite a source and quote it (Anthropic's "verify with
citations" pattern), how much can a cheap, deterministic check catch by confirming the quote really is in
the source?

```sh
python3 verify_quotes.py
```

Standard library only. `cases.json` holds three short fictional sources and nine claims, labelled by
hand before the checker was written.

## Prediction (before running)

The check catches fabricated quotes and quotes attributed to the wrong source, and misses claims that
cite a real quote but say something the quote doesn't support.

## Result (run 2026-11-01)

| Claim | Quote check | Human label | Agrees |
|---|---|---|---|
| c1, c2, c4, c6 | pass | supported | yes |
| c9 (spacing and case differ) | pass | supported | yes |
| c3 | fail | fabricated quote | yes |
| c8 | fail | wrong source cited | yes |
| c5 "Domestic payments after 14:00…" citing the international rule | pass | real quote, wrong claim | **no** |
| c7 "Cash gifts may be accepted…" citing "Cash gifts must always be refused" | pass | real quote, contradicted claim | **no** |

Agreement 7 of 9. Prediction held.

## What it shows

- **Exact checks are cheap and catch fabrication.** A made-up or misattributed quote fails instantly, for
  free, with no model call. Normalising whitespace and case avoids false failures.
- **A real quote is not proof of a true claim.** Both misses quote the source correctly and then claim
  something it doesn't say: c7 claims the opposite. Catching these needs a semantic check: a grounding
  service, an entailment model or an LLM judge comparing claim and quote.
- **Layer them.** Run the cheap exact check on everything, and the semantic check on what passes (or on
  high-stakes answers only). The same cheapest-first ordering as input guardrails.

## Exercises

1. Add a semantic check: ask a model "does this quote support this claim? yes/no" for each passing
   claim. Does it catch c5 and c7? Does it wrongly reject any supported claim?
2. Write three claims of your own that would fool both checks.
