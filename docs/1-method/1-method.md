---
id: "1"
title: "How to approach an AI system design question"
phase: 0
maturity: stable
status: published
last_verified: 2026-11-01
review_by: 2027-11-01
owner: "@daneb"
---

# 1 How to approach an AI system design question

The classic primer's method has four steps: outline use cases and constraints, create a high-level
design, design the core components, then scale. AI systems need two changes to that method:

- **The quality bar comes first.** A web service is correct or it is not. A model-backed feature is
  correct some percentage of the time, so "how will we know it works?" must be answered before the
  design, not after. Thoughtworks puts evals second in its pattern list, straight after direct
  prompting ([martinfowler.com](https://www.martinfowler.com/articles/gen-ai-patterns/)).
- **Hardening is its own step.** Prompt injection, data leakage and unbounded agent actions are design
  constraints, not features to bolt on.

That gives six steps.

![Diagram for 1 How to approach an AI system design question: 1 Use cases, constraints, quality bar, 2 Back-of-the- envelope, 3 High-level design on the ladder, 4 Core components, 5 Harden, 6 Scale and optimise](../../images/1-method.svg)
<!-- source: images/src/1-method.mmd; render with scripts/diagrams.py -->

## Key terms

- **Quality bar:** what a good answer looks like and how it will be measured, agreed before design starts.
- **Back-of-the-envelope:** rough arithmetic on tokens, requests per second, cost and latency to size the system.
- **Complexity ladder:** single call → workflow → single agent → multi-agent; start at the lowest rung that meets the bar.
- **Hardening:** designing against prompt injection, data leakage and unsafe actions as a step of its own.
- **Eval (evaluation):** a repeatable test of output quality, run before release and sampled in production.

More in the [glossary](../5-appendix/5.6-glossary.md).

## Step 1: Use cases, constraints and the quality bar

Ask until you can write these down:

**Use cases and users**
- Who uses it, and for what decisions? Who is harmed if an answer is wrong?
- What is in scope, and what is explicitly out?
- What does the system read (documents, databases, the web) and what can it change (send, write,
  execute)?

**Constraints**
- Volume: users, requests per user per day, peak factor.
- Latency: time to first visible output, and end-to-end.
- Spend: a monthly ceiling, or a cost per request.
- Data: classification, residency, retention, who may see what.
- Regulation: is this a regulated decision, and does a human need to sign off?

**Quality bar**
- What does a good answer look like? Write two or three examples, and one that must be refused.
- How will it be measured before launch: a labelled test set, a rubric scored by a model judge
  calibrated against humans, task success rate?
- How will it be measured after launch: user feedback, sampling, escalation rate?
- What change in score blocks a release?

If the interviewer will not give numbers, state assumptions and move on.

## Step 2: Back-of-the-envelope

The classic primer estimates requests per second and storage. For an AI system the dominant quantities
are **tokens**: they drive cost, latency and capacity.

1. **Tokens per request.** Split input into system prompt, retrieved context and conversation history,
   then estimate output separately. Output tokens are generated one at a time, so they dominate latency.
2. **Requests per second.** Average and peak.
3. **Tokens per day**, input and output separately.
4. **Cost per day** = input tokens × input price + output tokens × output price. Use dated prices from
   [5.1](../5-appendix/5.1-numbers.md).
5. **Latency** ≈ retrieval and other pre-processing + time to first token + output tokens ÷ output
   tokens per second.
6. **Multipliers.** Agents and multi-agent systems multiply token use. Anthropic reports agents using
   about 4× the tokens of a chat interaction and its multi-agent research system about 15×
   ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)).

### Worked example

An internal assistant answering questions over policy documents for 5,000 staff.

| Assumption | Value |
|---|---|
| Questions per user per working day | 20 |
| Working hours per day | 10 |
| Peak factor | 3× |
| Input tokens per request | 1,500 system and instructions + 4,000 retrieved (8 chunks × 500) + 1,500 history = 7,000 |
| Output tokens per request | 400 |
| Prices | **Illustrative only:** $3 per million input tokens, $15 per million output tokens |

Derived (working shown):

- Requests: 5,000 × 20 = 100,000 per day. Over 10 hours that is 100,000 ÷ 36,000 s ≈ 2.8 requests/s
  on average, ≈ 8 requests/s at a 3× peak.
- Tokens per day: 100,000 × 7,000 = 700 M input; 100,000 × 400 = 40 M output.
- Cost per day: 700 × $3 + 40 × $15 = $2,100 + $600 = **$2,700**. Input is 78% of the bill.
- Generation time: hosted frontier models were measured at roughly 60–110 output tokens/s in November
  2026 ([Artificial Analysis](https://artificialanalysis.ai/embed/llm-performance-leaderboard)).
  At 80 tokens/s, 400 tokens take about 5 s, so a 2-second budget is only reachable for the *first*
  visible token. The design must stream.

What the estimate teaches before any boxes are drawn:

- **Retrieval-heavy systems are input-bound.** Halving retrieved context (8 → 4 chunks) saves
  100,000 × 2,000 = 200 M input tokens a day, $600/day at the illustrative price. A reranker that lets
  you send fewer, better chunks pays for itself.
- **The stable prefix is cacheable.** If the 1,500-token system prompt is served from a provider prompt
  cache at about 0.1× the input price (Anthropic's read rate,
  [Anthropic](https://docs.claude.com/en/docs/build-with-claude/prompt-caching); cache writes cost
  extra and are ignored here; see [3.13](../3-components/3.13-caching.md)), it saves roughly 150 M × $3 ÷ 1 M × 0.9 ≈ $400/day.
- **Climbing the ladder is expensive.** Turning this into an agent at ~4× tokens moves the bill from
  ~$2,700 to ~$11,000 a day. That needs a quality gain to justify it.

## Step 3: High-level design on the complexity ladder

Start at the lowest rung that can meet the quality bar, and justify each step up. Azure's agent
guidance recommends the same ordering: a direct model call, then a single agent with tools, then
multiple agents ([Microsoft Learn](https://learn.microsoft.com/azure/architecture/ai-ml/guide/ai-agent-design-patterns)).
Anthropic's advice is to find the simplest solution and add complexity only when it demonstrably
improves results ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).

| Rung | Shape | Choose it when |
|---|---|---|
| 1 Single call | One prompt, maybe with retrieval | The task is answerable in one pass |
| 2 Workflow | Fixed code paths: chaining, routing, parallelization, evaluator-optimizer | The steps are known in advance |
| 3 Single agent | A model choosing tools in a loop | The steps depend on what it finds |
| 4 Multi-agent | Several agents, usually an orchestrator and workers | The work splits into independent, broad sub-tasks worth ~15× tokens |

Draw the request path end to end before detailing anything: client → gateway → guardrails → context
assembly (prompt, retrieval, memory) → model → tools → output validation → client, with evals and
tracing alongside.

## Step 4: Core components

Walk the request path and design each component that matters for this problem, using the Part 3
sections. For each, state the choice, the alternative, and the trade-off axis it moves
([Part 2](../2-trade-offs/)). Typical depth questions:

- Retrieval: how documents are chunked, indexed (keyword, vector or both) and reranked; how citations
  reach the answer; how access control is enforced at query time.
- Model: which tier for which step; structured outputs; streaming; fallbacks.
- Tools: what each tool can do, with what permissions, and what needs human approval.
- Evals: the offline test set, the online signal, and the release gate.

## Step 5: Harden

- **Prompt injection.** Check for the *lethal trifecta*: access to private data, exposure to untrusted
  content, and the ability to communicate externally. If all three are present, an attacker who controls
  the content can exfiltrate the data. Remove a leg rather than relying on filters
  ([Simon Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)).
- **Guardrails** on input (PII, relevance, injection screening) and output (schema, policy, grounding).
- **Least privilege** for tools; sandbox any code execution.
- **Human review points** for consequential actions.
- **Governance.** Map the design to the relevant controls (OWASP LLM Top 10 and Agentic Top 10, FINOS,
  EU AI Act) and name the evidence you would keep: eval results, traces, approvals, model and prompt
  versions.

## Step 6: Scale and optimise

Find the bottleneck, apply the pattern, repeat:

| Bottleneck | Patterns |
|---|---|
| Cost | Smaller model tiers and cascades, prompt caching, fewer and better retrieved chunks, batch APIs for offline work |
| Latency | Streaming, parallel calls, smaller models for easy steps, caching, shorter outputs |
| Throughput / rate limits | Gateway quotas, multiple deployments or providers, queues and back-pressure |
| Quality | Better retrieval and reranking before a bigger model; evaluator-optimizer loops; fine-tuning only if evals still fail |
| Reliability | Fallback models, timeouts and retries, durable execution for long-running agents |

## Common mistakes

- Designing an agent before showing a single call or workflow fails.
- No quality bar, so no way to tell whether a change helped.
- Estimating requests but not tokens.
- Treating prompt injection as a filtering problem.
- Naming products instead of explaining the component and its trade-off.

## Flashcards

Q: What are the six steps of the AI system design method?
A: Use cases, constraints and quality bar; back-of-the-envelope; high-level design on the complexity ladder; core components; harden; scale and optimise.

Q: Why does the quality bar come before the design in AI systems?
A: Model output is correct only some of the time, so you need an agreed measurement (evals) to judge any design choice or change.

Q: What are the four rungs of the complexity ladder?
A: Single call, workflow, single agent, multi-agent. Start at the lowest rung that meets the quality bar.

Q: In a retrieval-heavy assistant, which side of the token bill usually dominates, and what follows?
A: Input tokens. Trimming retrieved context, reranking and prompt caching are the main cost levers.

Q: Roughly how much more token use do agents and multi-agent systems need than chat, per Anthropic?
A: About 4× for agents and about 15× for its multi-agent research system.

Q: What is the lethal trifecta?
A: Access to private data, exposure to untrusted content, and the ability to communicate externally. With all three, prompt injection can exfiltrate data.

## Sources and further reading

- [System Design Primer: how to approach a system design interview question](https://github.com/donnemartin/system-design-primer#how-to-approach-a-system-design-interview-question):
  the four-step method this extends.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
  (Anthropic, Dec 2024): simplicity first, and the workflow patterns behind the ladder.
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
  (Anthropic): source of the token multipliers.
- [AI agent orchestration patterns](https://learn.microsoft.com/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
  (Microsoft Learn): the simplest-first ladder and when-to-avoid guidance.
- [Emerging patterns in building GenAI products](https://www.martinfowler.com/articles/gen-ai-patterns/)
  (Thoughtworks): evals as an early pattern.
- [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) (Simon Willison,
  Jun 2025).
- [What GenAI engineer interviews test](https://www.techinterview.org/post/3233476396/what-genai-engineer-interviews-test/):
  what the interview round looks for.
