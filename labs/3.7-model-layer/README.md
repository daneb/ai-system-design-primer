# Lab 3.7: Picking the cheapest model that "meets the bar", with a noisy eval

Supports section [3.7 Model layer](../../docs/3-components/3.7-model-layer.md).

**Question:** the common advice is to hit your accuracy target with the best model, then switch to the
cheapest model that still meets it. If the eval that decides "meets it" has only 100 cases, how often
do you ship a model that is actually below target?

```sh
python3 pick_model.py
```

numpy only, seeded. Five made-up models from 92% to 83% true accuracy; target 88%; each trial
measures every model on *n* cases and applies a selection rule.

## Prediction (before running)

Choosing on the measured score will often pick a below-target model at 100 cases. Requiring the lower
confidence bound to clear the target will be safe but expensive.

## Result (run 2026-11-01)

| Eval cases | Rule | Picked a model truly below target | Average relative cost | Most common pick |
|---|---|---|---|---|
| 50 | measured ≥ target | 57% | 1.9 | small-a (34%) |
| 50 | lower bound ≥ target | 3% | 8.8 | large (83%) |
| 100 | measured ≥ target | 41% | 2.3 | medium-b (34%) |
| 100 | lower bound ≥ target | 1% | 9.0 | large (84%) |
| 300 | measured ≥ target | 19% | 2.8 | medium-b (44%) |
| 300 | lower bound ≥ target | 0% | 8.2 | large (71%) |
| 1000 | measured ≥ target | 4% | 2.9 | medium-b (50%) |
| 1000 | lower bound ≥ target | 0% | 6.4 | medium-a (56%) |
| 3000 | measured ≥ target | 0% | 3.0 | medium-b (51%) |
| 3000 | lower bound ≥ target | 0% | 4.3 | medium-a (92%) |

Prediction held.

## What it shows

- **"Cheapest model that passes" rewards luck.** With 100 cases, 41% of the time the chosen model was
  truly below target: a cheaper model scored above its real accuracy and won. Scanning many candidates
  makes this worse, because the more models you test, the more likely one gets a lucky score.
- **Caution costs money when evals are small.** Requiring the lower bound to clear the target almost
  never shipped a weak model, but with 100 cases it fell back to the largest model 84% of the time, at
  nine times the cost.
- **A bigger eval buys the saving safely.** At 1,000–3,000 cases both rules converge on genuinely
  adequate cheaper models. The eval set is what lets you trade down ([3.15](../../docs/3-components/3.15-evals.md)).

## Exercises

1. Set `TARGET` to 0.90. Which rule and size now picks well?
2. Add ten more small models at 84–87%. What happens to Rule A's error rate at 300 cases?
3. Change the cost of `medium-b` to 3.5. Is the saving still worth a 1,000-case eval?
