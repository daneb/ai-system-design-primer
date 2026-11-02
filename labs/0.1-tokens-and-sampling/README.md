# Lab 0.1: What a token is, and what temperature does

Supports section [0.1 Tokens, context and sampling](../../docs/0-orientation/0.1-tokens-context-and-sampling.md).

**Question:** if a tokenizer learns its pieces from English text, how many more tokens does the same
message need in another language or as JSON? And how often do two sampled answers match at different
temperatures?

```sh
python3 tokens.py
```

Standard library only; seeded; about five seconds. Part 1 trains a byte-pair encoding (BPE) tokenizer
with 1,000 merges on this primer's Part 2 and 3 pages. Production tokenizers have 100,000 or more
entries and many languages in their training data, so compare the ratios, not the absolute counts.
Part 2 samples a 40-token answer 500 times from fixed next-token scores, where the model is fairly
sure at every step.

## Prediction (before running)

Afrikaans will need about 1.5 times as many tokens as English, and JSON more again. At temperature 0
every run will match; at 0.3 most will; at 0.7 and above few will.

## Result (run 2026-11-01)

| Text | Characters | Tokens | Characters per token | Tokens vs English |
|---|---|---|---|---|
| English | 202 | 72 | 2.8 | 1.00x |
| Afrikaans (same message) | 199 | 100 | 2.0 | 1.39x |
| JSON (same facts) | 152 | 108 | 1.4 | 1.50x |
| Numbers | 82 | 65 | 1.3 | n/a (different content) |

English split: `Y|our| pay|ment| of| two| h|un|d|red| r|and| to| the| e|le|ct|ric|ity| acc|oun|t| was| dec ...`

| Setting | Chance the likeliest token is picked, per step | Distinct answers in 500 runs | Runs identical to the greedy answer |
|---|---|---|---|
| temperature 0 (greedy) | 100% | 1 | 100% |
| temperature 0.3 | 99% | 68 | 63% |
| temperature 0.7 | 86% | 500 | 0% |
| temperature 1.0 | 73% | 500 | 0% |
| temperature 1.0, top-p 0.9 | 79% | 500 | 0% |

The prediction held for the tokens and failed for sampling: even 0.3 changed a third of the answers.

## What it shows

- **Tokens follow the training text.** Words the tokenizer saw often ("payment", " the", " account")
  are one or two tokens. Afrikaans words it rarely saw break into pieces, so the same message costs
  39% more. JSON pays for every brace, quote and underscore.
- **Numbers are expensive.** At 1.3 characters per token, an account number or a balance costs about
  twice as much per character as English prose. This tokenizer splits digits one at a time, as several
  production tokenizers do.
- **Small randomness compounds.** At temperature 0.3 the likeliest token won 99% of the time, yet over
  40 tokens a third of the answers differed from the greedy one. At 0.7, no two of 500 answers matched.
- **So:** measure token counts on your own languages and formats with the provider's counter. Use low
  temperature where you need consistency, and a template where you need identical wording.

## Exercises

1. Set `MERGES` to 200 and then 3,000. How do the English and Afrikaans counts change, and why?
2. Add an isiZulu or Spanish translation to `samples`. Predict the ratio before you run it.
3. Make the model less sure: change the first score in `steps` from 4.0 to 2.5. What happens at 0.3?
