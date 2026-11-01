# Lab 3.2: What a guardrail's error rates mean at volume

Supports section [3.2 Input guardrails](../../docs/3-components/3.2-input-guardrails.md).

**Question:** a prompt-attack detector catches 95% of attacks and wrongly flags 1% of legitimate
requests. That sounds good. What does it do to a million requests a day?

```sh
python3 base_rates.py
python3 base_rates.py --requests 50000
```

Standard library only. Pure arithmetic: the numbers are illustrative, the effect is not.

## Prediction (before running)

When attacks are rare, most blocked requests will be legitimate users.

## Result

| Attack rate | Catches | False alarms | Attacks blocked | Attacks missed | Legitimate requests blocked | Blocks that are real attacks |
|---|---|---|---|---|---|---|
| 0.1% | 95% | 1.0% | 950 | 50 | 9,990 | 9% |
| 0.1% | 95% | 0.1% | 950 | 50 | 999 | 49% |
| 0.1% | 99% | 0.1% | 990 | 10 | 999 | 50% |
| 1.0% | 95% | 1.0% | 9,500 | 500 | 9,900 | 49% |
| 1.0% | 95% | 0.1% | 9,500 | 500 | 990 | 91% |

Prediction held.

## What it shows

- **The base rate dominates.** At a 0.1% attack rate, a filter with a 1% false-alarm rate blocks ten
  legitimate users for every attacker. Improving the catch rate from 95% to 99% barely changes this;
  cutting false alarms does.
- **Blocking is a user-experience decision.** Ten thousand wrongly blocked requests a day need a
  response: a clear message, a way to rephrase, or a route to a person. For borderline scores, flagging
  for review or routing to a more careful path may serve better than a hard block.
- **Missed attacks still get through.** Even the best row lets attacks through every day. That is why
  input guardrails are one layer, and why the architecture must limit what a successful attack can do
  ([2.4](../../docs/2-trade-offs/2.4-capability-vs-security.md)).
- **Measure your own rates.** Vendor detectors publish few error rates for your traffic. Build a labelled
  set of real and attack inputs and measure ([3.15](../../docs/3-components/3.15-evals.md)).

## Exercises

1. Plug in the volume and an estimated attack rate for a system you know. How many people a day would
   be wrongly blocked?
2. Add a second, independent detector and block only when both flag. What happens to false alarms, and
   to missed attacks?
