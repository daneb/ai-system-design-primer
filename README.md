# The AI System Design Primer

[![CI](https://github.com/daneb/ai-system-design-primer/actions/workflows/ci.yml/badge.svg)](https://github.com/daneb/ai-system-design-primer/actions/workflows/ci.yml)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Code: MIT](https://img.shields.io/badge/code-MIT-lightgrey.svg)](LICENSE-CODE)

> **Status: first draft.** Every section is written and checked by CI, but none has had an independent
> review yet. Figures we couldn't confirm against a primary source are marked "not verified" on the page
> and listed in [PLAN.md](PLAN.md#verification-debt). Corrections are very welcome.

Learn how to design systems built on large language models: the trade-offs, the components, and the
patterns that have converged across the industry, along with the ones that are still moving.

![The request path through the primer's components. A user's request passes through the gateway (3.1), input guardrails (3.2) and context engineering (3.3), then retrieval (3.4 to 3.6) and a workflow or agent (3.9 to 3.11), reaches the model layer (3.7, 3.8), and returns through output checks (3.12). Caching, asynchronism, evals, observability and security support the path.](images/readme.svg)
<!-- source: images/src/readme.mmd; render with scripts/diagrams.py -->

## Motivation

> Learn how to design AI systems that hold up in production.
> Prepare for the AI system design conversation.

Building on models is now a core engineering skill, and the field moves fast. Most of what's written
about it is a product announcement, a framework tutorial or a single team's experience. This primer is
an organised collection of what has converged across providers and researchers, with every trade-off
named and every number dated and sourced.

It is modelled on Donne Martin's [System Design Primer](https://github.com/donnemartin/system-design-primer):
the same arc of method, trade-offs, components, solved designs and reference numbers, rebuilt for
systems whose core component is probabilistic, priced per token, and open to prompt injection.

**Learn how to design AI systems.** Each topic is a short page you can read in ten minutes, with a
diagram, when to use it, when not to, and its disadvantages. A deep dive per topic holds the provider
survey, numbers, risk controls and cloud mappings.

**Prepare for the AI system design conversation,** in an interview or a design review. Work through the
[method](docs/1-method/1-method.md), the [solved designs](#ai-system-design-questions-with-solutions)
and the [practice questions](docs/4-solved-designs/4.8-unsolved-questions.md).

## Anki flashcards

Every page ends in question-and-answer flashcards. Build the deck with either command (standard
library only):

```sh
python3 scripts/primer.py anki         # writes build/ai-system-design-primer.apkg: double-click to import
python3 scripts/primer.py flashcards   # writes build/flashcards.tsv: plain text for Anki's File > Import
```

The package has one sub-deck per part. Re-importing a newer build updates answers in place and keeps
your review history; a reworded question arrives as a new card. Cards are tagged by section and
maturity, so you can study one part, or suspend `maturity::frontier` cards when they go stale.

## Labs

Most topics come with a small, runnable lab: a simulation or calculation, numpy or the standard
library only, with the prediction written down before the run and an honest note when it was wrong.

| Lab | Question |
|---|---|
| [0.1](labs/0.1-tokens-and-sampling/README.md) | What a token is, and what temperature does |
| [0.2](labs/0.2-inside-a-model-call/README.md) | Prefill, decode, the KV cache and reasoning tokens |
| [0.3](labs/0.3-tool-calling/README.md) | The tool-calling loop, its token bill, and what checks catch |
| [2.1](labs/2.1-cost-quality-latency/README.md) | When does routing between models pay off? |
| [2.2](labs/2.2-determinism-vs-autonomy/README.md) | What autonomy costs in reliability and predictability |
| [2.3](labs/2.3-context-vs-retrieval/README.md) | When is the whole corpus in the prompt cheaper than retrieval? |
| [2.4](labs/2.4-capability-vs-security/README.md) | Count to three, then size what a detector leaves behind |
| [2.5](labs/2.5-single-vs-multi-agent/README.md) | One agent or several? |
| [2.7](labs/2.7-throughput-vs-latency/README.md) | Batching, per-user speed, and why you can't run at 100% |
| [3.2](labs/3.2-input-guardrails/README.md) | What a guardrail's error rates mean at volume |
| [3.3](labs/3.3-context-engineering/README.md) | What each context strategy costs, and what it forgets |
| [3.4](labs/3.4-retrieval-pipeline/README.md) | Keyword vs dense vs hybrid retrieval |
| [3.5](labs/3.5-agentic-retrieval/README.md) | Single-shot retrieval, query fan-out, or an agent loop? |
| [3.6](labs/3.6-vector-stores/README.md) | Approximate search and filtering |
| [3.7](labs/3.7-model-layer/README.md) | Picking the cheapest model that "meets the bar", with a noisy eval |
| [3.8](labs/3.8-serving-internals/README.md) | Cache arithmetic and when speculation pays |
| [3.9](labs/3.9-workflows-and-agents/README.md) | An evaluator loop is only as good as its evaluator |
| [3.10](labs/3.10-multi-agent-and-protocols/README.md) | What does connecting more tools cost, and does tool search pay? |
| [3.11](labs/3.11-memory/README.md) | What should an agent remember, and how? |
| [3.12](labs/3.12-output-guardrails/README.md) | How far does a quote check get you? |
| [3.13](labs/3.13-caching/README.md) | When a prompt cache pays, and what a semantic cache gets wrong |
| [3.14](labs/3.14-asynchronism/README.md) | Retries during an overload, and checkpoints for long runs |
| [3.15](labs/3.15-evals/README.md) | How many eval cases do you need? |
| [3.16](labs/3.16-observability/README.md) | Which agent traces should you keep? |
| [3.17](labs/3.17-security/README.md) | Pin your tools, and see what pinning can't see |
| [3.18](labs/3.18-model-adaptation/README.md) | What LoRA trains, and when a fine-tune pays for itself |
| [4.1](labs/4.1-inference-api/README.md) | How many accelerators does a self-hosted inference API need? |
| [4.2](labs/4.2-enterprise-rag/README.md) | Where the money goes in an enterprise RAG assistant |
| [4.4](labs/4.4-document-review/README.md) | What 98% recall costs in lawyer time |
| [4.5](labs/4.5-support-agent/README.md) | Consistency with policy in the prompt or in a policy engine |
| [4.6](labs/4.6-coding-agent/README.md) | Review capacity caps merged work |

## Contributing

> Learn from the community.

Pull requests are welcome to fix errors, improve sections and add new ones. Read [STYLE.md](STYLE.md)
for how sections are researched and written (learner-first, several providers per topic, every claim
sourced) and [CONTRIBUTING.md](CONTRIBUTING.md) for the mechanics. Decisions about the primer itself
are recorded in [adr/](adr/). Work still to do is in [ROADMAP.md](ROADMAP.md).

## Index of AI system design topics

> Summaries of AI system design topics, including pros and cons. **Everything is a trade-off.**
>
> Each section links to its deep dive. Maturity is marked `S` (stable core), `S/F` (stable concept,
> volatile specifics) or `F` (frontier, expect rewrites).

<!-- toc:start -->
**Part 0: Orientation**

- [0 Orientation](docs/0-orientation/0-orientation.md) `S`
- [0.1 Tokens, context and sampling](docs/0-orientation/0.1-tokens-context-and-sampling.md) `S`
- [0.2 Inside a model call: prefill, decode and reasoning](docs/0-orientation/0.2-inside-a-model-call.md) `S`
- [0.3 Tool calling and structured output](docs/0-orientation/0.3-tool-calling.md) `S`

**Part 1: Method**

- [1 How to approach an AI system design question](docs/1-method/1-method.md) `S`

**Part 2: Trade-offs**

- [2.1 Cost vs quality vs latency](docs/2-trade-offs/2.1-cost-quality-latency.md) `S` · [deep dive](docs/deep-dives/2.1-cost-quality-latency.md)
- [2.2 Determinism vs autonomy](docs/2-trade-offs/2.2-determinism-vs-autonomy.md) `S/F` · [deep dive](docs/deep-dives/2.2-determinism-vs-autonomy.md)
- [2.3 Context stuffing vs retrieval](docs/2-trade-offs/2.3-context-vs-retrieval.md) `S/F` · [deep dive](docs/deep-dives/2.3-context-vs-retrieval.md)
- [2.4 Capability vs security](docs/2-trade-offs/2.4-capability-vs-security.md) `S/F` · [deep dive](docs/deep-dives/2.4-capability-vs-security.md)
- [2.5 Single-agent vs multi-agent](docs/2-trade-offs/2.5-single-vs-multi-agent.md) `S/F` · [deep dive](docs/deep-dives/2.5-single-vs-multi-agent.md)
- [2.6 Prompting vs RAG vs fine-tuning](docs/2-trade-offs/2.6-prompt-rag-finetune.md) `S` · [deep dive](docs/deep-dives/2.6-prompt-rag-finetune.md)
- [2.7 Throughput vs per-request latency in serving](docs/2-trade-offs/2.7-throughput-vs-latency.md) `S` · [deep dive](docs/deep-dives/2.7-throughput-vs-latency.md)

**Part 3: Components, in request order**

- [3.1 AI gateway and router](docs/3-components/3.1-ai-gateway-and-router.md) `S` · [deep dive](docs/deep-dives/3.1-ai-gateway-and-router.md)
- [3.2 Input guardrails](docs/3-components/3.2-input-guardrails.md) `S` · [deep dive](docs/deep-dives/3.2-input-guardrails.md)
- [3.3 Context engineering](docs/3-components/3.3-context-engineering.md) `S/F` · [deep dive](docs/deep-dives/3.3-context-engineering.md)
- [3.4 Retrieval pipeline](docs/3-components/3.4-retrieval-pipeline.md) `S` · [deep dive](docs/deep-dives/3.4-retrieval-pipeline.md)
- [3.5 Agentic retrieval and the long-context boundary](docs/3-components/3.5-agentic-retrieval.md) `F` · [deep dive](docs/deep-dives/3.5-agentic-retrieval.md)
- [3.6 Vector stores](docs/3-components/3.6-vector-stores.md) `S/F` · [deep dive](docs/deep-dives/3.6-vector-stores.md)
- [3.7 Model layer: selection, structured outputs, streaming](docs/3-components/3.7-model-layer.md) `S/F` · [deep dive](docs/deep-dives/3.7-model-layer.md)
- [3.8 Serving internals](docs/3-components/3.8-serving-internals.md) `S/F` · [deep dive](docs/deep-dives/3.8-serving-internals.md)
- [3.9 Workflows and agents](docs/3-components/3.9-workflows-and-agents.md) `S` · [deep dive](docs/deep-dives/3.9-workflows-and-agents.md)
- [3.10 Multi-agent topologies and protocols (MCP, A2A)](docs/3-components/3.10-multi-agent-and-protocols.md) `F` · [deep dive](docs/deep-dives/3.10-multi-agent-and-protocols.md)
- [3.11 Agent memory](docs/3-components/3.11-memory.md) `F` · [deep dive](docs/deep-dives/3.11-memory.md)
- [3.12 Output guardrails and validation](docs/3-components/3.12-output-guardrails.md) `S` · [deep dive](docs/deep-dives/3.12-output-guardrails.md)
- [3.13 Caching](docs/3-components/3.13-caching.md) `S/F` · [deep dive](docs/deep-dives/3.13-caching.md)
- [3.14 Asynchronism: batch, durable execution, back-pressure](docs/3-components/3.14-asynchronism.md) `S` · [deep dive](docs/deep-dives/3.14-asynchronism.md)
- [3.15 Evals](docs/3-components/3.15-evals.md) `S` · [deep dive](docs/deep-dives/3.15-evals.md)
- [3.16 Observability](docs/3-components/3.16-observability.md) `S/F` · [deep dive](docs/deep-dives/3.16-observability.md)
- [3.17 Security](docs/3-components/3.17-security.md) `S/F` · [deep dive](docs/deep-dives/3.17-security.md)
- [3.18 Model adaptation](docs/3-components/3.18-model-adaptation.md) `S` · [deep dive](docs/deep-dives/3.18-model-adaptation.md)

**Part 4: Solved designs**

- [4.1 Design an LLM inference API](docs/4-solved-designs/4.1-llm-inference-api.md) `S`
- [4.2 Design an enterprise RAG assistant](docs/4-solved-designs/4.2-enterprise-rag-assistant.md) `S/F` · [deep dive](docs/deep-dives/4.2-enterprise-rag-assistant.md)
- [4.3 Design an enterprise AI gateway](docs/4-solved-designs/4.3-enterprise-ai-gateway.md) `S`
- [4.4 Design a regulated document-review assistant](docs/4-solved-designs/4.4-regulated-document-review.md) `S/F`
- [4.5 Design a customer-support agent](docs/4-solved-designs/4.5-customer-support-agent.md) `F`
- [4.6 Design a coding agent platform](docs/4-solved-designs/4.6-coding-agent.md) `F`
- [4.7 Design an eval and release pipeline](docs/4-solved-designs/4.7-eval-and-release-pipeline.md) `S`
- [4.8 Additional design questions](docs/4-solved-designs/4.8-unsolved-questions.md) `S/F`

**Part 5: Appendix**

- [5.1 Numbers every AI engineer should know](docs/5-appendix/5.1-numbers.md) `S/F`
- [5.2 Cloud mapping: Azure, AWS Bedrock, GCP](docs/5-appendix/5.2-cloud-mapping.md) `F`
- [5.3 Pattern crosswalk](docs/5-appendix/5.3-pattern-crosswalk.md) `S/F`
- [5.4 Governance crosswalk: OWASP, FINOS, EU AI Act](docs/5-appendix/5.4-governance-crosswalk.md) `F`
- [5.5 Real-world architectures and engineering blogs](docs/5-appendix/5.5-real-world-architectures.md) `F`
- [5.6 Glossary](docs/5-appendix/5.6-glossary.md) `S`
<!-- toc:end -->

## Study guide

> Suggested topics to review based on your timeline.

| | Short (days) | Medium (weeks) | Long (months) |
|---|---|---|---|
| Read [Orientation](docs/0-orientation/0-orientation.md), the foundations ([0.1](docs/0-orientation/0.1-tokens-context-and-sampling.md)–[0.3](docs/0-orientation/0.3-tool-calling.md)) and the [method](docs/1-method/1-method.md) | ✓ | ✓ | ✓ |
| Read the trade-offs (Part 2) | Some | All | All |
| Read the components (Part 3) | 3.1, 3.4, 3.9, 3.15, 3.17 | Most | All, plus deep dives |
| Read [Numbers](docs/5-appendix/5.1-numbers.md) and the [Glossary](docs/5-appendix/5.6-glossary.md) | ✓ | ✓ | ✓ |
| Work the solved designs (Part 4) | Some | Many | All |
| Run the labs and their exercises | Some | Many | All |
| Practise the [additional questions](docs/4-solved-designs/4.8-unsolved-questions.md) | Some | Many | Most |
| Read [real-world architectures](docs/5-appendix/5.5-real-world-architectures.md) | Some | Many | All |
| Map your platform with [cloud](docs/5-appendix/5.2-cloud-mapping.md) and [governance](docs/5-appendix/5.4-governance-crosswalk.md) crosswalks | — | Some | All |

## How to approach an AI system design question

> How to tackle an AI system design question, in an interview or a design review.

The classic four steps, with two changes: the **quality bar comes first**, because a model-backed
feature is right only some of the time; and **hardening is its own step**, because prompt injection,
data leakage and runaway agents are design constraints, not add-ons.

1. **Use cases, constraints and the quality bar.** Who, what, how many, how fast, what data, and how
   you'll know it works.
2. **Back-of-the-envelope.** Tokens per request, requests per second, cost per day, latency.
3. **High-level design on the complexity ladder.** Single call → workflow → single agent →
   multi-agent. Start at the lowest rung that meets the bar.
4. **Core components.** Retrieval, context, tools, model choice, output checks.
5. **Harden.** Which legs of the lethal trifecta are present, and which does the design break?
6. **Scale and optimise.** Bottlenecks in order; caching, routing, batching.

Full walkthrough with a worked example: [How to approach an AI system design question](docs/1-method/1-method.md).

## AI system design questions with solutions

> Common AI system design questions with sample discussions, numbers and diagrams.

| Question | |
|---|---|
| Design an LLM inference API | [Solution](docs/4-solved-designs/4.1-llm-inference-api.md) |
| Design an enterprise RAG assistant | [Solution](docs/4-solved-designs/4.2-enterprise-rag-assistant.md) |
| Design an enterprise AI gateway | [Solution](docs/4-solved-designs/4.3-enterprise-ai-gateway.md) |
| Design a regulated document-review assistant | [Solution](docs/4-solved-designs/4.4-regulated-document-review.md) |
| Design a customer-support agent | [Solution](docs/4-solved-designs/4.5-customer-support-agent.md) |
| Design a coding agent platform | [Solution](docs/4-solved-designs/4.6-coding-agent.md) |
| Design an eval and release pipeline | [Solution](docs/4-solved-designs/4.7-eval-and-release-pipeline.md) |
| Add an AI system design question | [Contribute](CONTRIBUTING.md) |

More practice: [additional design questions](docs/4-solved-designs/4.8-unsolved-questions.md).

## Appendix

- [Numbers every AI engineer should know](docs/5-appendix/5.1-numbers.md): tokens, speed, cost
  ratios, memory, retrieval and eval figures, each dated and sourced.
- [Cloud mapping](docs/5-appendix/5.2-cloud-mapping.md): each capability on Azure, AWS, Google Cloud,
  OpenAI, Anthropic and open source.
- [Pattern crosswalk](docs/5-appendix/5.3-pattern-crosswalk.md): the same patterns under each
  provider's and author's names.
- [Governance crosswalk](docs/5-appendix/5.4-governance-crosswalk.md): OWASP LLM and Agentic Top 10,
  FINOS, EU AI Act, mapped to primer sections.
- [Real-world architectures](docs/5-appendix/5.5-real-world-architectures.md): engineering write-ups
  and independent studies.
- [Glossary](docs/5-appendix/5.6-glossary.md) and changelog.

## How this primer differs from the original, and from a blog post

- **Trade-offs first.** Every pattern says which trade-off it moves and in which direction.
- **Quality bar first.** Evals are part of the method, not an afterthought.
- **Maturity is labelled and dated.** Each page carries `last_verified` and `review_by`; the checker
  fails when a review is overdue. Frontier pages are reviewed every three months.
- **Several providers on every topic.** Anthropic, OpenAI, Google, AWS and Microsoft, with the names
  each uses.
- **Vendor-neutral prose.** Product names live in the deep dives and the cloud mapping.
- **Risk and controls on every topic,** with the evidence an auditor would ask for.
- **Runnable labs** with predictions recorded before the run.

## Progress

<!-- status:start -->
| Phase | Sections | Planned | Draft | Review | Published |
|---|---|---|---|---|---|
| 0 | 6 | 0 | 6 | 0 | 0 |
| 1 | 12 | 0 | 11 | 1 | 0 |
| 2 | 10 | 0 | 10 | 0 | 0 |
| 3 | 11 | 0 | 11 | 0 | 0 |
| 4 | 5 | 0 | 5 | 0 | 0 |
<!-- status:end -->

See [ROADMAP.md](ROADMAP.md) for what's next and [PLAN.md](PLAN.md) for the build plan and the
verification debt (claims still waiting for a first-party source).

## Credits

- Donne Martin's [System Design Primer](https://github.com/donnemartin/system-design-primer), whose
  structure this follows.
- The provider guides, papers and engineering write-ups cited in each section; see
  [real-world architectures](docs/5-appendix/5.5-real-world-architectures.md).

## Contact info

Open an issue to discuss errors, missing topics or new solved designs. Report security problems, or
guidance that would make a system less safe, privately as described in [SECURITY.md](SECURITY.md).
Participation is covered by the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

- **Content** (pages, diagrams, flashcards, lab READMEs) is licensed under
  [Creative Commons Attribution 4.0 International](LICENSE) (CC BY 4.0), the same licence as the
  original System Design Primer.
- All diagrams and charts are original to this repository and covered by the content licence.
- **Code** (`scripts/`, the lab scripts and the CI workflow) is licensed under the [MIT License](LICENSE-CODE).
- Contributions are accepted under the same terms. The reasoning is in [ADR 0008](adr/0008-licences.md).

## How this was written

The author researched and wrote this primer with an AI assistant, under the method in
[STYLE.md](STYLE.md): primary sources from several providers for every claim, a dated `last_verified`
on every page, runnable labs instead of asserted numbers, and a public list of what isn't yet verified.
Mistakes are still possible; please report them with a source.
