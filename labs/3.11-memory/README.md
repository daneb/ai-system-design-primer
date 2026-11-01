# Lab 3.11: What should an agent remember, and how?

Supports section [3.11 Agent memory](../../docs/3-components/3.11-memory.md).

**Question:** over 50 sessions, a user states facts and sometimes changes them, and one tool result in
ten plants a false "fact". Compare no memory, replaying every transcript, appending extracted facts,
and extracting with consolidation (update the old version), with and without a check on where a fact
came from. How often does the agent recall the *current* fact, and what does memory cost per session?

```sh
python3 memory_policies.py
```

numpy only, seeded. Assumptions: extraction catches 90% of stated facts; consolidation merges
correctly 90% of the time; replaying transcripts picks the newer of two versions 70% of the time; a
planted fact is followed 80% of the time. Read the shape.

## Prediction (before running)

Replaying transcripts will recall best but cost the most. Consolidation will come close at a fraction
of the tokens. Appending without updates will slowly fill with stale facts.

## Result (run 2026-11-01)

| Policy | Recalled current fact | Stale | Poisoned | Missing | Memory tokens per session |
|---|---|---|---|---|---|
| None | 0% | 0% | 0% | 100% | 0 |
| Replay transcripts | 76% | 22% | 2% | 0% | 73,500 |
| Append extracted facts | 56% | 38% | 3% | 3% | 280 |
| Extract + consolidate | 88% | 7% | 3% | 2% | 270 |
| Consolidate + provenance check | 91% | 7% | 0% | 2% | 270 |

Prediction partly wrong. Consolidation didn't just come close to replaying transcripts; it beat
them, 88% to 76%, at under 0.4% of the tokens. Transcripts hold every old version, and the model has
to pick the right one.

## What it shows

- **Remembering everything isn't remembering well.** Full transcripts cost 73k tokens a session by
  session 50 and still answered with stale facts 22% of the time.
- **Updating beats appending.** Without consolidation, a memory of extracted facts fills with old
  versions: 38% stale.
- **Provenance is a cheap security control.** Writing only facts that came from the user removed
  poisoned recalls entirely.
- **Extraction misses things.** About 2% of recalls found nothing. Keep the full record in a system of
  record, and let memory hold the distilled facts.

## Exercises

1. Raise `CHANGE` to 0.6 (fast-changing preferences). How does append compare now?
2. Drop `CONSOLIDATE` to 0.7. Is consolidation still better than replaying transcripts?
3. Raise `POISON_RATE` to 0.5 (an agent reading lots of untrusted email). What happens without the
   provenance check?
