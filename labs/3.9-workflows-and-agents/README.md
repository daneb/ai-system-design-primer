# Lab 3.9: An evaluator loop is only as good as its evaluator

Supports section [3.9 Workflows and agents](../../docs/3-components/3.9-workflows-and-agents.md).

**Question:** a generator gets a task right 60% of the time. Add an evaluator that checks each draft
and sends it back for revision, up to three rounds. How much does accuracy improve with a perfect code
check, a strong judge, a weak judge, or an evaluator that accepts everything? And how many rounds are
worth paying for?

```sh
python3 evaluator_loop.py
```

numpy only, seeded. Assumes each revision with feedback raises the chance of a correct draft by 10
points; that gain is a guess, so read the shape, not the exact numbers.

## Prediction (before running)

A good evaluator will lift accuracy well above 60%; a weak one only slightly; most of the gain will
come in the first extra round.

## Result (run 2026-11-01)

| Evaluator | True-accept rate | False-accept rate | Final accuracy (up to 3 rounds) | Calls per task |
|---|---|---|---|---|
| none (single call) | — | — | 60% | 1.0 |
| code check (exact) | 100% | 0% | 98% | 3.0 |
| strong judge | 95% | 10% | 92% | 3.0 |
| weak judge | 85% | 40% | 78% | 2.8 |
| rubber stamp | 100% | 100% | 60% | 2.0 |

| Rounds allowed (strong judge) | Final accuracy | Calls per task |
|---|---|---|
| 1 | 60% | 2.0 |
| 2 | 84% | 2.8 |
| 3 | 93% | 3.0 |
| 5 | 94% | 3.1 |
| 8 | 95% | 3.1 |

Prediction held. (92% and 93% for the same setting are sampling noise.)

## What it shows

- **The evaluator is the ceiling.** A deterministic check lifted accuracy from 60% to 98%; a weak
  judge that waves through 40% of bad drafts reached only 78%; an evaluator that accepts everything
  doubled the cost and added nothing. Anthropic's advice to rely on "ground truth from the environment"
  (tests, tool results) is this result.
- **Diminishing returns after two or three rounds.** Most of the gain came from the first revision;
  beyond three rounds, accuracy barely moved. Cap the loop.
- **Calibrate judges before looping on them** ([3.15](../../docs/3-components/3.15-evals.md)).

## Exercises

1. Set the revision `gain` to 0. How much of the improvement came from re-sampling alone?
2. Make the generator 85% accurate. Is the loop still worth three calls per task?
3. Give the weak judge a 10% false-accept rate but a 70% true-accept rate. What happens to cost?
