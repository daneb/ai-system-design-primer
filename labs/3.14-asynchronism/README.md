# Lab 3.14: Retries during an overload, and checkpoints for long runs

Supports section [3.14 Asynchronism](../../docs/3-components/3.14-asynchronism.md).

**Question:** 1,000 callers hit a model API during a ten-second capacity dip. How do three retry
policies compare? And for a 12-step agent run, what does resuming from a checkpoint save over
restarting on every transient failure?

```sh
python3 retries.py
```

numpy and the standard library, seeded. Part 1 is a 50 ms time-step simulation; the provider serves
20 calls per second for the first 10 seconds and 100 afterwards.

## Prediction (before running)

Immediate retries will multiply load enormously. Backoff will cut attempts; jitter will also finish
sooner by spreading retries out. Checkpoints will save a large share of repeated calls.

## Result (run 2026-11-01)

| Retry policy | Total attempts for 1,000 calls | Last call succeeds at (s) |
|---|---|---|
| retry immediately | 234,084 | 18.0 |
| exponential backoff | 8,687 | 361.8 |
| exponential backoff + full jitter | 5,569 | 45.3 |

| On a transient failure | Model calls per completed 12-step run | vs minimum (12) |
|---|---|---|
| restart the whole run | 17.1 | +42% |
| resume from the failed step (checkpoint) | 12.6 | +5% |

Prediction held, with one surprise: backoff *without* jitter finished last, by minutes.

## What it shows

- **Immediate retries are a self-inflicted attack.** 234 attempts per successful call. This model is
  generous: rejected attempts cost the provider nothing here, so everyone finished quickly once
  capacity returned. Real servers spend capacity rejecting requests, so a retry storm prolongs the
  outage it reacts to.
- **Backoff without jitter keeps callers in lock-step.** Everyone who failed together waits the same
  time and retries together, so each wave overflows capacity again; with a 30 s cap, stragglers took
  six minutes. Randomising the wait (full jitter) used the fewest attempts *and* finished in 45 s.
- **Checkpoints make long runs cheap to recover.** Restarting a 12-step run on any failure cost 42%
  extra model calls at a 5% per-step failure rate; resuming from the failed step cost 5%. Each saved
  call is tokens and time you don't pay twice, and side effects you don't repeat.

## Exercises

1. Raise `P_FAIL` to 10%. What happens to the restart policy's overhead?
2. Change the cap from 30 s to 5 s. Does plain backoff still finish last?
3. Model a cost for rejected attempts by reducing capacity by 1 call per 20 rejections. How does
   "retry immediately" behave now?
