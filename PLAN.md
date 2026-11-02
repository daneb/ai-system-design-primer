# Plan

This file is the record of how the primer was built, the definition of done for a section, and the
live list of claims not yet verified. The forward plan is [ROADMAP.md](ROADMAP.md); live progress is
in the [README](README.md#progress) (`python3 scripts/primer.py status`).

Basis: [research/AI system design primer feasibility.md](research/AI%20system%20design%20primer%20feasibility.md)
(1 Nov 2026). Its verdict: feasible, with a stable core of roughly 25–35 converged patterns and a smaller
frontier that must be dated and rewritten on a schedule. The hard part is staying current, not writing.

## Status: first release (2 November 2026)

- **44 sections**, all reviewed by the author: 37 published, 7 in review until
  their open verification items are cleared.
- **26 deep dives, 31 labs (17 with charts), 54 diagrams, 8 ADRs**, and a flashcard deck exported as
  TSV and as an Anki package.
- **CI** checks front matter, review dates, the README, diagrams, links, flashcards and every lab.

## Definition of done for a section

1. **Read** at least two primary sources from different providers or independent research (paper,
   specification, provider documentation, engineering post). Note anything that conflicts.
2. **Write the deep dive first**, then the primer page as its summary, from the templates: key terms,
   how it works, a worked example, when to use and avoid, disadvantages, risk and controls, cloud
   mapping, sources ([ADR 0007](adr/0007-primer-and-deep-dive.md)).
3. **Draw** the diagram as a Mermaid source in `images/src/` and render it to SVG with alt text
   ([STYLE.md, Diagrams](STYLE.md#diagrams)).
4. **Prove one claim** where practical: a lab in `labs/<section-id>/` with the prediction written
   before the run, and a chart if it sweeps a number.
5. **Write 3–6 flashcards.**
6. **Verify** every number and link. Add anything not confirmed against a primary source to the table
   below, and mark it "not verified" where it appears in a page's tables. Set `last_verified`, `review_by` and
   `owner`, then run `primer.py check`, `readme`, `flashcards` and `labs`, and `diagrams.py check`.
7. **Status:** `draft` while writing; `review` once the author has reviewed it; `published` once two
   or fewer open verification items name it.

## How the first release was built

Built 1–2 November 2026, in the phase order of the original plan: the stable core first, the frontier
last. Each section followed the definition of done above.

- [x] Feasibility research; repository layout; section, deep-dive and solved-design templates
- [x] `scripts/primer.py` (check, status, readme, flashcards, anki, labs) and `scripts/diagrams.py`
- [x] CI: front matter and review dates, README freshness, diagrams, flashcards, labs, link check
- [x] ADRs 0001–0008, STYLE.md, CONTRIBUTING.md, licences, Code of Conduct, security policy
- [x] Roadmap P0 and P1 work: key terms and examples, glossary, diagram style and SVG rendering, lab
  charts, step-by-step mechanisms, Part 0 foundations, verification of stable sections ([ROADMAP.md](ROADMAP.md))

### Phase 0: Scaffold, orientation, method and foundations

- [x] **0** Orientation — published
- [x] **0.1** Tokens, context and sampling — published (1 open item)
- [x] **0.2** Inside a model call: prefill, decode and reasoning — published (1 open item)
- [x] **0.3** Tool calling and structured output — published
- [x] **1** How to approach an AI system design question — published (1 open item)
- [x] **5.6** Glossary — published

### Phase 1: The stable spine

- [x] **2.1** Cost vs quality vs latency — published
- [x] **2.2** Determinism vs autonomy — published (1 open item)
- [x] **2.4** Capability vs security — published (1 open item)
- [x] **2.6** Prompting vs RAG vs fine-tuning — published (1 open item)
- [x] **3.1** AI gateway and router — published (2 open items)
- [x] **3.2** Input guardrails — published (1 open item)
- [x] **3.4** Retrieval pipeline — published
- [x] **3.6** Vector stores — published (1 open item)
- [x] **3.12** Output guardrails and validation — published (1 open item)
- [x] **3.15** Evals — in review: 4 open verification items
- [x] **3.17** Security — in review: 4 open verification items
- [x] **4.2** Design an enterprise RAG assistant — published

### Phase 2: Serving and economics

- [x] **2.7** Throughput vs per-request latency in serving — published (1 open item)
- [x] **3.7** Model layer: selection, structured outputs, streaming — published (1 open item)
- [x] **3.8** Serving internals — in review: 4 open verification items
- [x] **3.13** Caching — published (1 open item)
- [x] **3.14** Asynchronism: batch, durable execution, back-pressure — published (1 open item)
- [x] **3.18** Model adaptation — in review: 3 open verification items
- [x] **4.1** Design an LLM inference API — published (1 open item)
- [x] **4.3** Design an enterprise AI gateway — published
- [x] **4.7** Design an eval and release pipeline — published
- [x] **5.1** Numbers every AI engineer should know — published (2 open items)

### Phase 3: Agents and the frontier

- [x] **2.3** Context stuffing vs retrieval — published (1 open item)
- [x] **2.5** Single-agent vs multi-agent — published
- [x] **3.3** Context engineering — published (1 open item)
- [x] **3.5** Agentic retrieval and the long-context boundary — published (2 open items)
- [x] **3.9** Workflows and agents — published
- [x] **3.10** Multi-agent topologies and protocols (MCP, A2A) — in review: 3 open verification items
- [x] **3.11** Agent memory — published (1 open item)
- [x] **3.16** Observability — published (1 open item)
- [x] **4.4** Design a regulated document-review assistant — published (1 open item)
- [x] **4.5** Design a customer-support agent — published (1 open item)
- [x] **4.6** Design a coding agent platform — published (1 open item)

### Phase 4: Cross-cutting appendices

- [x] **4.8** Additional design questions — published
- [x] **5.2** Cloud mapping: Azure, AWS, Google Cloud — in review: 10 open verification items
- [x] **5.3** Pattern crosswalk — published (2 open items)
- [x] **5.4** Governance crosswalk: OWASP, FINOS, EU AI Act — in review: 5 open verification items
- [x] **5.5** Real-world architectures and engineering blogs — published

## Verification debt

### What "confirmed" and "not verified" mean

A claim is **confirmed** when someone has read it in its primary source and it matches, on a recorded
date (the page's `last_verified`). The primary source is where the claim originates:

- **the provider's own documentation**, for prices, limits, defaults and features;
- **the paper itself**, for research results, not a blog post or abstract about it;
- **the standard or regulation**, for OWASP, FINOS, NIST and the EU AI Act;
- **our own arithmetic or lab**, for derived numbers. These are checked as calculations but are
  illustrative, not measurements of real systems, and the pages say so.

Confirmed means accurately sourced, not necessarily true: a vendor's benchmark can be quoted exactly
and still be a vendor's claim, and those are labelled "(vendor)". Confirmation is also a point in time;
providers change their documentation, which is why every section has a review date.

**Not verified** doesn't mean wrong. It means the claim hasn't met that standard yet. Every open claim
below has one of four kinds, which says what it takes to clear it:

| Kind | Meaning | To clear it | Open |
|---|---|---|---|
| Second-hand | Known only from a blog, summary, search snippet, aggregator or vendor claim | Find and read the primary source | 18 |
| Source not read | The primary source exists, but the relevant part hasn't been read in full | Read it | 11 |
| Not researched | Nobody has looked yet, often a cloud-mapping cell or a newer development | Research it | 10 |
| Needs an expert | A judgement, such as how a regulation applies, that a source can't settle | Ask a qualified reviewer, such as legal or compliance | 2 |

Sources read through automated tools can be misread; for legal, regulatory and high-stakes figures, a
person's own read of the source is the confirmation that counts.

### Open claims

Each row names the sections that use the claim. Where a claim appears in a page's table it is marked
"not verified". To clear one: read the primary source (or ask the expert), fix or confirm the page, set
its `last_verified`, delete the row, and add a changelog line in the
[glossary](docs/5-appendix/5.6-glossary.md#changelog). A section in review moves to published once two
or fewer rows name it.

| Claim | Kind | Problem | Needed by |
|---|---|---|---|
| Cache multipliers and TTLs per provider | Second-hand | Anthropic, OpenAI, Google, Azure and AWS Bedrock confirmed first-party (Nov 2026); per-model OpenAI read discounts and Anthropic automatic caching by default still via secondary sources | 3.13, 5.1 |
| Self-hosted cost per M output tokens | Second-hand | Single vendor worked example | 3.8, 4.1 |
| SGLang RadixAttention TTFT improvement | Second-hand | Unsourced vendor claim | 3.8 |
| TGI archive date | Second-hand | Secondary blog; cite Hugging Face's maintenance-mode note only | 3.8 |
| Managed agent memory (Foundry, Memory Bank, AgentCore) | Source not read | Docs seen via search snippets, not read in full; Foundry throughput figure secondary; OpenAI long-term memory API absence unconfirmed | 3.3, 3.11 |
| AWS and OpenAI first-party long-context-vs-RAG guidance | Not researched | Not found | 2.3 |
| Coding-agent search choices (Codex, Cline, Cursor) and Claude Code "agentic search beat RAG" | Second-hand | Secondary sources and an interview; arXiv 2608.01507 seen via abstract only | 3.5 |
| Bedrock agentic retrieval and Vertex AI Search agentic features | Second-hand | AWS blog only; Google not checked | 3.5 |
| A2A v1.0 operations, dates and agent-card fields; MCP revision list | Second-hand | Secondary sources; read a2a-protocol.org spec and MCP release list | 3.10 |
| Cloud MCP/A2A services (AgentCore Gateway/Identity, Apigee, Entra Agent ID, Agent Engine A2A) | Not researched | Not checked first-party | 3.10 |
| OTel GenAI conventions details (repo move, versions, operations); Google Cloud Trace for ADK; Anthropic telemetry | Second-hand | Secondary sources; Google and Anthropic not checked first-party | 3.16 |
| τ-bench policy-removal effect (−22.4% airline) | Source not read | Not found in the paper's HTML text (likely in a figure or appendix); Klarna, Stanford and the τ-bench pass^k figures confirmed 2026-11-02 | 4.5 |
| EU AI Act: contract review not high-risk | Needs an expert | Primer's reading of Annex III; confirm with legal | 4.4 |
| Coding-agent sandbox details (Codex two-phase, Copilot firewall and approvals) | Source not read | First-party docs seen via search; GitHub concept page redirected | 4.6 |
| Tokens per word, embedding dimensions, KV-cache bytes, GPU memory and bandwidth | Not researched | Tokens per word confirmed (OpenAI); KV-cache formula derived; GPU memory and bandwidth confirmed on NVIDIA's pages (2026-11-02); embedding dimensions not covered | 5.1 |
| Prompt → RAG → fine-tune → distill → RL ladder | Not researched | First three steps now sourced (Anthropic, OpenAI, AWS, Google, Thoughtworks; see 2.6). Distillation and RL steps still synthesis | 3.18 |
| Huyen's platform build-up order | Source not read | Secondary synthesis; check *AI Engineering* ch. 10 | 1, 3.1 |
| Lakshmanan & Hapke pattern names | Source not read | Possibly a revised edition; not mapped in 5.3 | 5.3 |
| Gulli chapter titles and Fowler pattern names in 5.3 | Source not read | From memory of the published contents; check against the book and article | 5.3 |
| FINOS AIGF risk IDs (AIR-SEC-0xx, AIR-OP-0xx) | Source not read | Read from the framework site's search snippets, not each risk page | 5.4 |
| EU AI Act article mapping per risk in 5.4 | Needs an expert | Primer's reading; confirm with legal | 5.4 |
| FINOS risk counts | Second-hand | Sources say 30, 46 and 25; the site doesn't state a total; 5.4 avoids counts | 5.4 |
| AWS S3 Vectors and MemoryDB as vector stores | Second-hand | Third-party source only | 3.6, 5.2 |
| AWS AgentCore Gateway token limits; Google learned routing | Second-hand | Third-party source only / not researched | 3.1, 5.2 |
| Prompt Shields input limits (2024 figures); Azure PII masking and custom categories; open-source guardrails (Llama Guard, Prompt Guard, NeMo, Presidio) | Not researched | Possibly outdated / not researched | 3.2, 5.2 |
| OpenAI structured outputs and guardrails-library hallucination check; Azure OpenAI structured outputs | Second-hand | Secondary sources only / not checked | 3.12, 5.2 |
| Microsoft deterministic exfiltration blocking | Source not read | MSRC post read via search excerpts and secondary summaries (OpenAI agent guide confirmed 2026-11-02) | 2.4, 3.17 |
| OWASP Agentic Top 10 2026 entry names (all ten in 5.4); MITRE ATLAS counts | Source not read | Several secondary sources agree on names; OWASP PDF and ATLAS pages not read directly | 3.17, 5.4 |
| Invariant Labs tool-poisoning and rug-pull disclosures (April 2025); malicious models on public hubs (JFrog, ReversingLabs) | Second-hand | Secondary sources only | 3.17, 3.10 |
| Tool-call authorisation, sandboxes and red-teaming services for Azure, Google, OpenAI | Not researched | Not researched | 3.17, 5.2 |
| Newer models' pass^k on τ-bench | Not researched | Paper figures confirmed (GPT-4o retail ≈61% pass^1, ≈25% pass^8); current leaderboards not checked | 2.2, 3.15 |
| OpenAI flex, priority and Scale Tier; Anthropic Priority Tier withdrawal; AWS priority on-demand | Second-hand | Via gateway documentation, not provider docs | 2.7, 5.2 |
| Chunked-prefill defaults in vLLM V1 and SGLang; Sarathi-Serve figures; managed endpoints for open models on Azure and AWS | Second-hand | Secondary sources / not researched | 3.8, 5.2 |
| Anthropic model fine-tuning via cloud partners | Not researched | Claude 3 Haiku tuning on Bedrock confirmed (GA Nov 2024); AWS blog says the model reached EOL 10 Sep 2026; any current Claude tuning option not verified | 2.6, 3.18, 5.2 |
| Azure and Google fine-tuning methods (DPO, RFT); OpenAI currently tunable models; Bedrock RFT accuracy claim | Not researched | Not researched / secondary | 3.18, 5.2 |
| Anthropic 529 overload semantics; OpenAI, Google, Azure, AWS batch limits | Second-hand | Secondary sources | 3.14 |
| OpenAI snapshot pinning guidance; Anthropic dateless IDs are pinned | Second-hand | Secondary sources quoting provider docs | 3.7 |
| Anthropic eval details: pass@k / pass^k, capability vs regression, grade outcomes not paths | Source not read | Page confirmed to exist and cover them; details read via secondary summaries | 3.15 |
| EU AI Act Art. 15 (accuracy for high-risk systems) | Source not read | Not checked against the regulation text | 3.15, 5.4 |
| Anthropic managed eval tooling; AWS and Google production monitoring of eval scores | Not researched | Not researched | 3.15, 5.2 |
| "Change temperature or top-p, not both" and reasoning models rejecting sampling settings | Second-hand | Azure confirmed first-party; Anthropic and OpenAI via secondary sources (Anthropic API reference didn't load in full, 2026-11-02) | 0.1, 0.2 |

## Research gaps

Topics the feasibility study didn't cover, and where they stand.

- **Covered:** gateway and router products and routing research (3.1; RouteLLM not yet read); GraphRAG
  (3.4); memory taxonomies (3.11); structured outputs (3.7, 3.12); MCP revisions (3.10, with open items
  above); Azure and Bedrock service mappings (5.2, with open items above).
- **Open:** Google's agent whitepapers (3.9).

## Decisions

| Decision | Outcome | Record |
|---|---|---|
| Licence | CC BY 4.0 for content, MIT for code | [ADR 0008](adr/0008-licences.md) |
| Visibility | Public, from the first release | 2 November 2026 |
| Hosting | github.com/daneb/ai-system-design-primer | — |
| Publishing sections as standalone articles | Open: decide where | — |
