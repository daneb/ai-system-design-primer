# The AI System Design Primer

Learn how to design systems built on large language models: the trade-offs, the components, and the
patterns that have converged across the industry, along with the ones that are still moving.

Modelled on Donne Martin's [System Design Primer](https://github.com/donnemartin/system-design-primer):
the same arc of method, trade-offs, components in request order, solved designs and reference numbers,
rebuilt for AI systems.

> **Work in progress.** See [PLAN.md](PLAN.md) for the roadmap and [research/](research/) for the
> feasibility study behind it.

## How this primer differs from a blog post

- **Trade-offs first.** Every pattern says which trade-off it moves and in which direction.
- **Maturity is labelled.** Each section is tagged `S` (stable core), `S/F` (stable concept, volatile
  specifics) or `F` (frontier, expect rewrites), and carries a `last_verified` date. CI fails when a
  review is overdue.
- **Vendor-neutral.** The prose names concepts. Products appear only in the deep dives' cloud mappings.
- **Two layers.** Each topic is a short primer page you can read in ten minutes, plus a deep dive with
  the provider survey, numbers, risk and controls (OWASP, FINOS, EU AI Act, with the evidence an
  auditor would ask for) and cloud mappings.
- **Flashcards.** Every section ends in Q/A pairs, exported to an Anki deck by
  `python3 scripts/primer.py flashcards`.

Start with [Orientation](docs/0-orientation/0-orientation.md), then the
[Method](docs/1-method/1-method.md).

## Contents

<!-- toc:start -->
**Part 0: Orientation**

- [0 Orientation](docs/0-orientation/0-orientation.md) `S`

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
- [3.11 Agent memory](docs/3-components/3.11-memory.md) `F` _(planned)_
- [3.12 Output guardrails and validation](docs/3-components/3.12-output-guardrails.md) `S` · [deep dive](docs/deep-dives/3.12-output-guardrails.md)
- [3.13 Caching](docs/3-components/3.13-caching.md) `S/F` · [deep dive](docs/deep-dives/3.13-caching.md)
- [3.14 Asynchronism: batch, durable execution, back-pressure](docs/3-components/3.14-asynchronism.md) `S` · [deep dive](docs/deep-dives/3.14-asynchronism.md)
- [3.15 Evals](docs/3-components/3.15-evals.md) `S` · [deep dive](docs/deep-dives/3.15-evals.md)
- [3.16 Observability](docs/3-components/3.16-observability.md) `S/F` _(planned)_
- [3.17 Security](docs/3-components/3.17-security.md) `S/F` · [deep dive](docs/deep-dives/3.17-security.md)
- [3.18 Model adaptation](docs/3-components/3.18-model-adaptation.md) `S` · [deep dive](docs/deep-dives/3.18-model-adaptation.md)

**Part 4: Solved designs**

- [4.1 Design an LLM inference API](docs/4-solved-designs/4.1-llm-inference-api.md) `S`
- [4.2 Design an enterprise RAG assistant](docs/4-solved-designs/4.2-enterprise-rag-assistant.md) `S/F` · [deep dive](docs/deep-dives/4.2-enterprise-rag-assistant.md)
- [4.3 Design an enterprise AI gateway](docs/4-solved-designs/4.3-enterprise-ai-gateway.md) `S`
- [4.4 Design a regulated document-review assistant](docs/4-solved-designs/4.4-regulated-document-review.md) `S/F` _(planned)_
- [4.5 Design a customer-support agent](docs/4-solved-designs/4.5-customer-support-agent.md) `F` _(planned)_
- [4.6 Design a coding agent platform](docs/4-solved-designs/4.6-coding-agent.md) `F` _(planned)_
- [4.7 Design an eval and release pipeline](docs/4-solved-designs/4.7-eval-and-release-pipeline.md) `S`
- [4.8 Additional design questions](docs/4-solved-designs/4.8-unsolved-questions.md) `S/F` _(planned)_

**Part 5: Appendix**

- [5.1 Numbers every AI engineer should know](docs/5-appendix/5.1-numbers.md) `S/F`
- [5.2 Cloud mapping: Azure, AWS Bedrock, GCP](docs/5-appendix/5.2-cloud-mapping.md) `F` _(planned)_
- [5.3 Pattern crosswalk](docs/5-appendix/5.3-pattern-crosswalk.md) `S/F` _(planned)_
- [5.4 Governance crosswalk: OWASP, FINOS, EU AI Act](docs/5-appendix/5.4-governance-crosswalk.md) `F` _(planned)_
- [5.5 Real-world architectures and engineering blogs](docs/5-appendix/5.5-real-world-architectures.md) `F` _(planned)_
- [5.6 Glossary](docs/5-appendix/5.6-glossary.md) `S`
<!-- toc:end -->

## Progress

<!-- status:start -->
| Phase | Sections | Planned | Draft | Review | Published |
|---|---|---|---|---|---|
| 0 | 3 | 0 | 3 | 0 | 0 |
| 1 | 12 | 0 | 11 | 1 | 0 |
| 2 | 10 | 0 | 10 | 0 | 0 |
| 3 | 11 | 5 | 6 | 0 | 0 |
| 4 | 5 | 5 | 0 | 0 | 0 |
<!-- status:end -->

## Contributing

See [STYLE.md](STYLE.md) for how sections are researched and written, and
[CONTRIBUTING.md](CONTRIBUTING.md) for the mechanics. Architectural decisions about the primer itself are recorded in
[adr/](adr/).
