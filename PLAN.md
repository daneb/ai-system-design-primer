# Plan

The primer is also a learning vehicle: writing each section is one learning unit. The plan below is
the backlog. Live progress is in the [README](README.md#progress) (`python3 scripts/primer.py status`).

Basis: [research/AI system design primer feasibility.md](research/AI%20system%20design%20primer%20feasibility.md)
(1 Nov 2026). Its verdict: feasible, with a stable core of roughly 25–35 converged patterns and a smaller
frontier that must be dated and rewritten on a schedule. The hard part is staying current, not writing.

## Definition of done for a section (one learning unit)

1. **Read** at least two primary sources (paper, spec, vendor engineering post). Note anything that
   conflicts.
2. **Write** the section from the template: what it is, variants, when to use/avoid, trade-offs,
   limitation → mitigation, numbers, failure modes, risk and controls, cloud mapping, sources.
3. **Draw** the diagram as text (Mermaid or Excalidraw).
4. **Prove one claim** where practical: a small spike, a measurement, or a worked calculation. Record it
   under `labs/<section-id>/` and link it from the section.
5. **Write 3–6 flashcards.**
6. **Verify** every number and link; set `last_verified`, `review_by`, `owner`; run
   `scripts/primer.py check`, `readme`, `flashcards`.
7. **Move status** to `review`, and to `published` after a second read on a different day.

Suggested pace: one unit per week. Phase 1 is then about three months.

## Phase 0: Scaffold, orientation and method

- [x] Feasibility research
- [x] Repo layout, one stub per section with front matter
- [x] Section and solved-design templates
- [x] `scripts/primer.py`: check, status, README regeneration, flashcard export
- [x] CI: front matter, overdue reviews, README freshness, flashcards, link check (weekly as well)
- [x] ADRs 0001–0006 for the primer's own design decisions
- [x] STYLE.md: audience, voice, length budgets (enforced by `check`), multi-provider research method
- [ ] **0** Orientation (first draft written; needs review)
- [ ] **1** Method (first draft written; needs review and a worked example check)
- [ ] **5.6** Glossary and changelog (seeded; grows with every section)
- [ ] Decide the open questions below (license, visibility)

## Phase 1: The stable spine

Order matters: start where the evidence is most stable and governance is easiest to make concrete.

Reworked 2026-11-01 into primer pages plus deep dives ([ADR 0007](adr/0007-primer-and-deep-dive.md)) after
comparing with the original primer. Second reads should check each primer page against its deep dive.

- [ ] **3.4** Retrieval pipeline (first read 2026-11-01; needs second read and the "not verified" cloud cells)
- [ ] **3.6** Vector stores (draft 2026-11-01; lab done; needs second read and "not verified" cells)
- [ ] **3.15** Evals (draft 2026-11-01; lab done; needs second read)
- [ ] **2.6** Prompting vs RAG vs fine-tuning (draft 2026-11-01; no lab: a fine-tune can't be run offline here; needs second read)
- [ ] **2.1** Cost vs quality vs latency (draft 2026-11-01; lab done; needs second read)
- [ ] **3.1** AI gateway and router (draft 2026-11-01; no lab: availability claim is derived arithmetic; needs second read)
- [ ] **3.2** Input guardrails (draft 2026-11-01; lab done; needs second read)
- [ ] **3.12** Output guardrails and validation (draft 2026-11-01; lab done; needs second read)
- [ ] **2.4** Capability vs security (draft 2026-11-01; lab done; needs second read)
- [ ] **3.17** Security (draft 2026-11-01; lab done; needs second read and "not verified" cloud cells)
- [ ] **2.2** Determinism vs autonomy (draft 2026-11-01; lab done; needs second read)
- [ ] **4.2** Solved design: enterprise RAG assistant (draft 2026-11-01; lab done; needs second read)

## Phase 2: Serving and economics

- [ ] **2.7** Throughput vs per-request latency (draft 2026-11-01; lab done; needs second read)
- [ ] **3.8** Serving internals (draft 2026-11-01; lab done; needs second read)
- [ ] **3.13** Caching (draft 2026-11-01; lab done; needs second read)
- [ ] **3.7** Model layer (draft 2026-11-01; lab done; needs second read)
- [ ] **3.14** Asynchronism (draft 2026-11-01; lab done; needs second read)
- [ ] **3.18** Model adaptation (draft 2026-11-01; lab done; needs second read)
- [ ] **5.1** Numbers every AI engineer should know (draft 2026-11-01; aggregates deep dives; needs second read)
- [ ] **4.1** Solved design: LLM inference API (draft 2026-11-01; lab done; needs second read)
- [ ] **4.3** Solved design: enterprise AI gateway (draft 2026-11-01; needs second read)
- [ ] **4.7** Solved design: eval and release pipeline (draft 2026-11-01; needs second read)

## Phase 3: Agents and the frontier

- [ ] **3.9** Workflows and agents (draft 2026-11-01; lab done; needs second read)
- [ ] **3.3** Context engineering (draft 2026-11-01; lab done; needs second read)
- [ ] **2.3** Context stuffing vs retrieval (draft 2026-11-01; lab done; needs second read)
- [ ] **3.5** Agentic retrieval (draft 2026-11-01; lab done; needs second read)
- [ ] **2.5** Single-agent vs multi-agent (draft 2026-11-01; lab done; needs second read)
- [ ] **3.10** Multi-agent topologies and protocols (draft 2026-11-01; lab done; needs second read)
- [ ] **3.11** Agent memory (draft 2026-11-01; lab done; needs second read)
- [ ] **3.16** Observability (draft 2026-11-01; lab done; needs second read)
- [ ] **4.6** Solved design: coding agent platform (draft 2026-11-01; needs second read)
- [ ] **4.5** Solved design: customer-support agent (draft 2026-11-01; needs second read)
- [ ] **4.4** Solved design: regulated document-review assistant (draft 2026-11-01; needs second read)

## Phase 4: Cross-cutting appendices

- [ ] **5.2** Cloud mapping (Azure, AWS Bedrock, GCP), sourced from first-party docs (draft 2026-11-01; generated from deep dives)
- [ ] **5.3** Pattern crosswalk (Anthropic, Gulli, Lakshmanan & Hapke, Fowler, Azure) (draft 2026-11-01; Lakshmanan & Hapke not yet mapped)
- [ ] **5.4** Governance crosswalk (OWASP LLM and Agentic Top 10, FINOS, EU AI Act) (draft 2026-11-01)
- [ ] **5.5** Real-world architectures and engineering blogs (draft 2026-11-01)
- [ ] **4.8** Additional design questions (draft 2026-11-01)
- [ ] First quarterly frontier review (all `frontier` sections): moved to [ROADMAP.md](ROADMAP.md)

## Verification debt

Claims from the research notes that must not enter the primer as stated. Clear each one in the
section that needs it.

| Claim | Problem | Needed by |
|---|---|---|
| Claude list prices and context windows | Aggregator only (BenchLM), internally inconsistent | 5.1 |
| Batch API discounts | ~50%: Anthropic confirmed first-party; OpenAI via a reliable secondary; Google, Azure, AWS via a secondary compilation of their docs | 2.1, 3.14, 5.1 |
| Cache multipliers and TTLs per provider | Anthropic, OpenAI, Google, Azure confirmed first-party (Nov 2026); Bedrock lifetimes and per-model OpenAI read discounts via secondary sources | 3.13, 5.1 |
| Self-hosted cost per M output tokens | Single vendor worked example | 3.8, 4.1 |
| SGLang RadixAttention TTFT improvement | Unsourced vendor claim | 3.8 |
| TGI archive date | Secondary blog; cite Hugging Face's maintenance-mode note only | 3.8 |
| PagedAttention throughput figures | From memory; read arXiv 2309.06180 | 3.8 |
| OpenAI "A practical guide to building agents" details | Seen via summary only | 3.9 |
| Managed agent memory (Foundry, Memory Bank, AgentCore) | Docs seen via search snippets, not read in full; Foundry throughput figure secondary; OpenAI long-term memory API absence unconfirmed | 3.3, 3.11 |
| Self-Route cost savings (65% Gemini, 39% GPT-4o); LaRA findings | Secondary summaries; read arXiv 2407.16833 and 2502.09977 | 2.3 |
| AWS and OpenAI first-party long-context-vs-RAG guidance | Not found | 2.3 |
| Coding-agent search choices (Codex, Cline, Cursor) and Claude Code "agentic search beat RAG" | Secondary sources and an interview; arXiv 2608.01507 seen via abstract only | 3.5 |
| Bedrock agentic retrieval and Vertex AI Search agentic features | AWS blog only; Google not checked | 3.5 |
| MAST category shares (44.2% system design); Kim et al. sequential-task figures (39–70% vs "−70%") | Secondary sources and abstracts; read both papers | 2.5 |
| A2A v1.0 operations, dates and agent-card fields; MCP revision list | Secondary sources; read a2a-protocol.org spec and MCP release list | 3.10 |
| Cloud MCP/A2A services (AgentCore Gateway/Identity, Apigee, Entra Agent ID, Agent Engine A2A) | Not checked first-party | 3.10 |
| OTel GenAI conventions details (repo move, versions, operations); Google Cloud Trace for ADK; Anthropic telemetry | Secondary sources; Google and Anthropic not checked first-party | 3.16 |
| τ-bench policy-removal effect (−22.4% airline) and later domains; Klarna figures; Stanford legal-tool rates | Secondary summaries for τ-bench detail and Klarna; Stanford via HAI summary | 4.4, 4.5 |
| EU AI Act: contract review not high-risk | Primer's reading of Annex III; confirm with legal | 4.4 |
| Coding-agent sandbox details (Codex two-phase, Copilot firewall and approvals) | First-party docs seen via search; GitHub concept page redirected | 4.6 |
| Chroma context-rot figures | Secondary summaries; read the report's charts before quoting any percentage | 3.3 |
| Tokens per word, embedding dimensions, KV-cache bytes, GPU memory and bandwidth | Tokens per word confirmed (OpenAI); KV-cache formula derived; GPU specs via a reseller page, NVIDIA datasheet not read; embedding dimensions not covered | 5.1 |
| Prompt → RAG → fine-tune → distill → RL ladder | First three steps now sourced (Anthropic, OpenAI, AWS, Google, Thoughtworks; see 2.6). Distillation and RL steps still synthesis | 3.18 |
| Contextual retrieval −35% and absolute failure rates | −49/−67%, $1.02, 50–100 tokens and the 200k threshold confirmed from Anthropic; −35% and 5.7% → 1.9% still from secondary reports | 3.4 |
| Huyen's platform build-up order | Secondary synthesis; check *AI Engineering* ch. 10 | 1, 3.1 |
| Lakshmanan & Hapke pattern names | Possibly a revised edition; not mapped in 5.3 | 5.3 |
| Gulli chapter titles and Fowler pattern names in 5.3 | From memory of the published contents; check against the book and article | 5.3 |
| EU AI Act Digital Omnibus dates | Provisional agreement (7 May 2026) and Parliament vote (16 June 2026) via law-firm summaries; final Official Journal text not checked | 5.4 |
| FINOS AIGF risk IDs (AIR-SEC-0xx, AIR-OP-0xx) | Read from the framework site's search snippets, not each risk page | 5.4 |
| EU AI Act article mapping per risk in 5.4 | Primer's reading; confirm with legal | 5.4 |
| FINOS risk counts | Sources say 30, 46 and 25; the site doesn't state a total; 5.4 avoids counts | 5.4 |
| pgvector HNSW defaults (m, ef_construction, ef_search) | Seen via a documentation mirror, not the pgvector repository | 3.6 |
| AWS S3 Vectors and MemoryDB as vector stores | Third-party source only | 3.6, 5.2 |
| AWS AgentCore Gateway token limits; Google learned routing | Third-party source only / not researched | 3.1, 5.2 |
| Prompt Shields input limits (2024 figures); Azure PII masking and custom categories; open-source guardrails (Llama Guard, Prompt Guard, NeMo, Presidio) | Possibly outdated / not researched | 3.2, 5.2 |
| OpenAI structured outputs and guardrails-library hallucination check; Azure OpenAI structured outputs | Secondary sources only / not checked | 3.12, 5.2 |
| OpenAI agent guide (tool risk ratings, human-intervention triggers); Microsoft deterministic exfiltration blocking | PDF and MSRC post read via search excerpts and secondary summaries | 2.4, 3.17 |
| OWASP Agentic Top 10 2026 entry names (all ten in 5.4); MITRE ATLAS counts | Several secondary sources agree on names; OWASP PDF and ATLAS pages not read directly | 3.17, 5.4 |
| Invariant Labs tool-poisoning and rug-pull disclosures (April 2025); malicious models on public hubs (JFrog, ReversingLabs) | Secondary sources only | 3.17, 3.10 |
| Tool-call authorisation, sandboxes and red-teaming services for Azure, Google, OpenAI | Not researched | 3.17, 5.2 |
| τ-bench figures (GPT-4o retail pass@1 ~61%, pass^8 ~25%); newer models' pass^k | Figures from the paper abstract and summaries; current leaderboards not checked | 2.2, 3.15 |
| OpenAI flex, priority and Scale Tier; Anthropic Priority Tier withdrawal; AWS priority on-demand | Via gateway documentation, not provider docs | 2.7, 5.2 |
| Chunked-prefill defaults in vLLM V1 and SGLang; Sarathi-Serve figures; managed endpoints for open models on Azure and AWS | Secondary sources / not researched | 3.8, 5.2 |
| Anthropic model fine-tuning via cloud partners | Claude 3 Haiku tuning on Bedrock confirmed (GA Nov 2024); AWS blog says the model reached EOL 10 Sep 2026; any current Claude tuning option not verified | 2.6, 3.18, 5.2 |
| Azure and Google fine-tuning methods (DPO, RFT); OpenAI currently tunable models; Bedrock RFT accuracy claim | Not researched / secondary | 3.18, 5.2 |
| Anthropic 529 overload semantics; OpenAI, Google, Azure, AWS batch limits | Secondary sources | 3.14 |
| OpenAI snapshot pinning guidance; Anthropic dateless IDs are pinned | Secondary sources quoting provider docs | 3.7 |
| Anthropic eval details: pass@k / pass^k, capability vs regression, grade outcomes not paths | Page confirmed to exist and cover them; details read via secondary summaries | 3.15 |
| EU AI Act Art. 15 (accuracy for high-risk systems) | Not checked against the regulation text | 3.15, 5.4 |
| Anthropic managed eval tooling; AWS and Google production monitoring of eval scores | Not researched | 3.15, 5.2 |

## Research gaps

Not covered by the feasibility study. Each is the first task of the section named.

- ~~Gateway and router products; routing research → 3.1~~ covered for Azure, AWS, Google, Anthropic and FrugalGPT (Nov 2026); RouteLLM not yet read
- GraphRAG maturity → 3.4, 3.5
- Memory taxonomies → 3.11
- Structured-output maturity → 3.7
- Google's agent whitepapers → 3.9
- MCP 2026 spec changes → 3.10
- Azure and Bedrock service mappings → 5.2

## Open decisions

- **License.** The original uses CC BY 4.0 for content. Options: CC BY 4.0 (maximum reuse), CC BY-SA 4.0
  (derivatives stay open), plus MIT for `scripts/`.
- **Visibility.** Public from the start, or private until Phase 1 is published.
- **Publishing.** Each finished section can also go out as a standalone article; decide where.
- **Git.** The folder is not yet a git repository. Run `git init` and push when ready.
