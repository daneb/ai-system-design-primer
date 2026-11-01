# Lab 2.5: One agent or several?

Supports section [2.5 Single-agent vs multi-agent](../../docs/2-trade-offs/2.5-single-vs-multi-agent.md).

**Question:** on a breadth task (ten independent sub-topics) and a chain task (six dependent steps),
how do one agent, one agent with compaction, unchecked parallel sub-agents and an orchestrator with
sub-agents compare on quality, input tokens and time?

```sh
python3 teams.py
```

numpy only, seeded. The reliability numbers are assumptions: 92% per sub-task in a fresh context,
minus 20 points per 100k tokens of context; a 15% chance that a hand-off drops something the next
step needed; a fresh reviewer catches 60% of bad results, self-review 30%. Read the shape.

## Prediction (before running)

Multi-agent will win the breadth task and lose the chain task. Multi-agent will use more tokens
everywhere.

## Result (run 2026-11-01)

Breadth task (share of sub-topics answered correctly):

| Design | Quality | Input tokens | Minutes |
|---|---|---|---|
| Single agent | 83% | 3,775,000 | 30 |
| Single agent + compaction | 93% | 737,500 | 30 |
| Independent sub-agents | 92% | 500,000 | 4 |
| Orchestrator + sub-agents | 96% | 738,810 | 7 |

Chain task (share of runs with every step right):

| Design | Quality | Input tokens | Minutes |
|---|---|---|---|
| Single agent | 47% | 986,126 | 18 |
| Single agent + compaction | 67% | 295,387 | 18 |
| Independent sub-agents | 27% | 256,255 | 20 |
| Orchestrator + sub-agents | 52% | 417,019 | 23 |

(Chain token figures are averages and include runs that stopped at the first failed step.)

Prediction partly wrong. Multi-agent won breadth and lost the chain, as expected. But it did **not**
use more tokens than a single agent doing the *same* work. The naive single agent was the most
expensive, because it re-sends an ever-growing context on every call.

## What it shows

- **Compare against a good single agent.** Compaction alone took the single agent from 83% to 93% on
  breadth and from 47% to 67% on the chain, at a fifth of the tokens.
- **Breadth: parallel sub-agents win on time.** Same or better quality in 7 minutes instead of 30.
- **Chains: hand-offs cost more than they save.** Every hand-off can drop a decision the next step
  needed. The single agent with compaction beat the orchestrator by 15 points.
- **Unchecked parallel agents are fragile.** On the chain, independent sub-agents were worst (27%);
  a reviewing lead recovered much of the loss.
- **Why real multi-agent systems cost more:** they're used to do *more* work (more searches, more
  breadth) in the same time. Anthropic reports about 15× the tokens of a chat, against 4× for one agent.

## Exercises

1. Set `HANDOFF` to 0.05 (very good briefs). Does the orchestrator beat the single agent on the chain?
2. Set `ROT` to 0.05 (a model that handles long context well). How much does multi-agent still add on
   breadth, apart from speed?
3. Make the breadth task 30 sub-topics. What happens to the single agent without compaction?
