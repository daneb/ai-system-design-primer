# Trade-offs, not products, will make this primer last

An "AI System Design Primer" modelled on donnemartin/system-design-primer is feasible to start now. The research found a stable core of roughly 25–35 patterns, which is about the same number of concepts the original covers. Independent sources (Anthropic, Thoughtworks/Fowler, CSIRO, OWASP, Chip Huyen, the hyperscaler architecture centres) name and define these patterns in much the same way. They include the retrieval pipeline, the workflow/agent taxonomy, gateways and caching, evals, guardrails, prompt-injection threat models and the prompt → RAG → fine-tune ladder. The original succeeded mainly through its format: one canonical page, "everything is a trade-off" framing, a repeatable interview method, solved designs on a shared template, flashcards and reference numbers. That format has not been reproduced for AI at any scale. The popular AI repos are framework-bound notebook collections. The repos explicitly branded "AI system design" have hundreds of stars and often lead to paid courses. The best structured equivalents are paid books. The main risk is decay, not a lack of material. The original stopped adding content around 2020 and now gets only link-rot fixes, and AI facts (prices, protocols, telemetry standards, agent topologies) go stale several times faster than DNS or CDN facts. The primer is worth building if it uses trade-off axes as its spine, splits a dated "frontier" layer from the "stable core", stamps every section with a last-verified date, and attaches governance controls to each pattern. That last element is a differentiator for a regulated bank, and none of the surveyed resources offers it. The recommended next step is a phased backlog: scaffolding and templates first, then the stable spine with one solved enterprise-RAG design, then serving and agents, and the frontier last.

## A 374k-star guide that won on structure and stopped changing in 2020

The System Design Primer is a single, very long README-driven Markdown guide. Donne Martin started it in February 2017, while a tech lead at Facebook, and licensed it personally under CC BY 4.0 ([LICENSE](https://github.com/donnemartin/system-design-primer/blob/master/LICENSE.txt)). As of November 2026 it has **about 374.3k stars and 58.9k forks** and is one of the most-starred repositories on GitHub. It is still adding stars, roughly 13k between August and November 2026 ([GitHub](https://github.com/donnemartin/system-design-primer); [remio](https://www.remio.ai/post/donnemartin-system-design-primer-is-trending-but-no-new-release-explains-it)). It describes itself as "an organized collection of resources" that pulls together material "scattered throughout the web". The value was curation and synthesis, not new research ([README](https://github.com/donnemartin/system-design-primer)).

The structure follows a clear teaching arc, and an AI version should copy that arc more than any of its content. The 1,839-line README opens with orientation: motivation, Anki decks, a study guide by short/medium/long timeline, and a frank FAQ ("do I need to know everything here? No"). Next comes method, a four-step interview approach (use cases and constraints → high-level design → core components → scale), followed by **eight solved designs** such as Pastebin, the Twitter timeline and a web crawler. Each solved design follows the same template, with basic and scaled diagrams and Python snippets. The concept chapters then begin with three abstract trade-off chapters: performance vs scalability, latency vs throughput, and availability vs consistency/CAP. After that they walk the request path: DNS → CDN → load balancer → reverse proxy → application layer → database → cache → asynchronism → communication → security. It closes with an appendix of reference numbers (powers of two, "latency numbers every programmer should know", availability nines) and tables of real-world architectures ([README](https://github.com/donnemartin/system-design-primer/blob/master/README.md)). Nearly every topic uses the same micro-format: an attributed diagram, 2–6 paragraphs of plain-English summary, sub-variants, a **"Disadvantage(s)" block**, and a **"Source(s) and further reading" block**. The README carries roughly 352 external links. The original text is short and synthesised, and the depth is left to the linked sources.

These devices form a learning loop: learn the concept with its trade-offs, retain it through Anki, apply it with the method and solved designs, calibrate with the numbers, then generalise from real architectures. That loop explains why the repo works as a self-study course rather than a link list. It was the first free, well-organised synthesis aimed at a high-stakes career need, the FAANG system design interview, and translations and an EPUB build widened its reach.

Its weaknesses are just as instructive. Commit activity fell from **185 commits in 2017 to roughly four per year from 2021 to 2026**, and every recent commit is a link or grammar fix. One author wrote about 51% of all commits, and **341 pull requests sit open** ([GitHub](https://github.com/donnemartin/system-design-primer)). The "Under development" list (MapReduce, consistent hashing, scatter-gather) has gone unwritten since about 2017. The Security section admits it "could use some updates", and examples such as Mint.com and 2009–2016 highscalability posts have aged badly ([README](https://github.com/donnemartin/system-design-primer/blob/master/README.md)). Critics say the solved designs do not carry through deployment, migrations, observability, incidents or cost, that the sample set is small, and that memorising it "can produce diagrams that look polished but collapse under a changed requirement" ([PracHub](https://prachub.com/resources/is-github-s-system-design-primer-enough-for-senior-interviews)). Others note that diagrams leave out budgets, compliance and cloud-specific services, and that "popularity increases the cost of stale guidance" ([remio](https://www.remio.ai/post/donnemartin-system-design-primer-is-trending-but-no-new-release-explains-it)). Both critique sources sell competing products, and the research found no independent critique. The direct repo evidence still supports their main points. For an AI primer, three of these failure modes matter most: a single-maintainer bottleneck, no per-section review dates, and interview framing that skips production concerns. AI content would hit all three sooner.

## Roughly 30 patterns have converged, enough for a stable core

The feasibility question depends on whether independent authors now describe the same patterns in the same terms. In most areas they do. Anthropic's "Building effective agents" (December 2024, still maintained as of October 2026) separates **workflows** ("LLMs and tools are orchestrated through predefined code paths") from **agents** (LLMs that "dynamically direct their own processes"). It names the augmented LLM, prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer and the autonomous agent loop, and advises adding complexity "only when it demonstrably improves outcomes" ([Anthropic](https://www.anthropic.com/research/building-effective-agents)). OpenAI's guide reaches the same "start with a single agent" conclusion, distinguishes manager from decentralised multi-agent designs, and advises starting with the most capable model and downsizing ([Maginative summary of OpenAI](https://www.maginative.com/article/how-to-build-ai-agents-a-detailed-practical-guide-from-openai/)). Azure's Architecture Center states a matching complexity ladder (direct call → single agent → multi-agent) and gives five orchestration patterns, each with when-to-use and when-to-avoid guidance ([Microsoft Learn](https://learn.microsoft.com/azure/architecture/ai-ml/guide/ai-agent-design-patterns)). The CSIRO academic catalogue lists 18 agent patterns that overlap heavily: plan generators, self/cross/human reflection, guardrails and RAG ([arXiv 2405.10467](https://arxiv.org/html/2405.10467v4)). Patterns found in 2023–2024 sources (RAG, embeddings, evals, guardrails, reflection, plan generation, the fine-tuning decision) still appear in 2025–2026 sources, and that persistence is the stability signal a primer needs.

Retrieval is stable at the level of building blocks: embeddings, hybrid BM25-plus-dense retrieval, query rewriting and reranking ([Fowler/Thoughtworks](https://www.martinfowler.com/articles/gen-ai-patterns/)). Contextualising chunks before indexing is reported to cut retrieval failures by **35% with contextual embeddings, 49% with contextual BM25 added, and up to 67% with reranking** ([Maginative summary of Anthropic](https://www.maginative.com/article/anthropics-contextual-retrieval-technique-enhances-rag-accuracy-by-67)). The framing around those blocks is less settled. Hamel Husain argues that "RAG is dead" really targets naive vector search for coding agents and that "the question is not whether to retrieve, but how" ([Hamel.dev](https://hamel.dev/blog/posts/evals-faq/is-rag-dead.html)). Anthropic recommends "just-in-time" retrieval through tools as a first-class alternative ([Anthropic Engineering](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents)). The primer should present pre-computed versus agentic retrieval as a trade-off axis, not treat one as a variant of the other.

Security has the most rigorous convergent literature, and it fits the primer format best because it already has a CAP-like impossibility result. Simon Willison's **"lethal trifecta"** says that private data, untrusted content and external communication together create exfiltration risk ([Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)). A 2025 paper by authors from IBM, ETH, Google and Microsoft formalised six architectural defences: Action-Selector, Plan-Then-Execute, LLM Map-Reduce, Dual LLM, Code-Then-Execute and Context-Minimization. Its premise is that filtering cannot solve prompt injection ([Willison](https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/); [arXiv 2506.08837](https://arxiv.org/pdf/2506.08837)). Prompt injection has stayed **#1 on the OWASP LLM Top 10** from 2023 through 2025 ([Coralogix](https://coralogix.com/ai-blog/owasp-top-10-for-llm-applications/)), and a separate OWASP Agentic Top 10 followed in December 2025 ([OWASP](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)).

The serving vocabulary is also settled: prefill vs decode, the KV cache, paged KV memory, continuous batching, prefix caching, TTFT/ITL and goodput ([Inference Handbook](https://handbook.modular.com/inference-optimization/prefill-decode-disaggregation/)). The engine landscape is not. Hugging Face put TGI into maintenance mode and now points users to vLLM and SGLang ([HF](https://huggingface.co/docs/text-generation-inference/index)).

The churn is real, and the primer should name it openly. "Prompt engineering" became "context engineering" in September 2025. **As of July 2026, not one OpenTelemetry `gen_ai.*` attribute was marked Stable**, after six semconv releases and a repository split in the first half of 2026 ([DEV/Azena](https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke)). Anthropic's own data shows multi-agent systems using about **15× the tokens of chat**, with a narrow fit ([Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)). Protocols are moving in the stabilising direction: MCP and A2A now sit under the Linux Foundation's Agentic AI Foundation, which has grown to more than 250 members ([Axios](https://axios.com/2026/08/17/a2a-agentic-ai-foundation-open-ai-standards)). Their specifications are still being versioned, though. Thoughtworks itself called its February 2025 catalogue "early days" with no "gold standards" ([Fowler](https://www.martinfowler.com/articles/gen-ai-patterns/)). The working rule: teach roles, mechanisms and trade-offs with confidence, and give anything that names a product, an attribute key or a price an expiry date.

| Area | Stable core | Dated frontier | Speculative |
|---|---|---|---|
| Retrieval | Embeddings, hybrid retrieval, query rewriting, reranking, chunk contextualisation, metadata filters | Agentic vs indexed retrieval, long-context boundary, vector DB choice | GraphRAG, chunking heuristics |
| Agentic | Augmented LLM, chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, tool loop, reflection, plan-and-execute, HITL checkpoints | Context engineering, multi-agent topologies, memory, harness design, MCP/A2A details | Debate/voting cooperation, agent registries |
| Serving | Gateway, router, fallbacks, exact and prefix caching, streaming, rate limiting, prefill/decode, KV cache, batching, quantization concepts | Semantic caching, cost-aware routing, PD disaggregation, engine choice, FP4 formats | — |
| Reliability | Offline/online evals, LLM-as-judge with rubric and human calibration, input/output guardrails, trace span model | OTel attribute names, eval tooling | — |
| Security | Prompt injection, lethal trifecta, OWASP LLM Top 10, least privilege, sandboxing, dual-LLM, plan-then-execute | OWASP Agentic Top 10 (first edition), inter-agent security | CaMeL capability tracking |
| Adaptation | Prompt → RAG → fine-tune ladder, LoRA/QLoRA, SFT | RL fine-tuning with graders, distillation practice | — |

## Prior art leaves a free, vendor-neutral, governed primer unclaimed

The prior art is plentiful, but it is split across formats, and none of it takes the original primer's position. The most-starred AI repos are runnable galleries and courses: awesome-llm-apps (~100.7k stars), llm-course (~84.8k), ai-engineering-hub (~38.6k), RAG_Techniques (~30.1k) and GenAI_Agents (~24.6k). They are tied to LangChain, LlamaIndex or CrewAI, and several show slowing maintenance ([oosmetrics](https://oosmetrics.com/repo/Shubhamsaboo/awesome-llm-apps); [gittrend](https://gittrend.io/repo/mlabonne/llm-course); [star-history](https://www.star-history.com/patchy631/ai-engineering-hub); [gittrend](https://gittrend.io/repo/NirDiamant/RAG_Techniques)). The repos that explicitly call themselves "AI system design" are small. amitshekhariitbhu/ai-system-design has 818 stars and funnels to a paid programme ([GitHub](https://github.com/amitshekhariitbhu/ai-system-design/wiki)). alirezadir/Agentic-AI-Systems has 467 ([gittrend](https://gittrend.io/repo/alirezadir/Agentic-AI-Systems)).

The books are stronger but either paid or narrow. Chip Huyen's *AI Engineering* is the foundational reference ([O'Reilly](https://oreilly.com/library/view/ai-engineering/9781098166298)). Lakshmanan and Hapke catalogue 32 GenAI patterns ([O'Reilly](https://www.oreilly.com/library/view/-/9798341622654/)), and Gulli's *Agentic Design Patterns* covers 21 agentic patterns ([PPC Land](https://ppc.land/google-engineer-releases-free-400-page-guide-to-agentic-ai-systems/)). ByteByteGo's *Generative AI System Design Interview* is centred on 2024-era model training (face, image and video generation), and a reviewer notes it has no chapters on agentic workflows, production evaluation, AI observability or inference economics ([PracHub review](https://prachub.com/resources/generative-ai-system-design-interview-book-review-2026-is-it-still-enough)). The closest structural match is Caio Incau's Leanpub *AI-Assisted System Design*, a $15–19 book whose 16 chapters run from a framework through an LLM gateway, caching, vector search, worked designs (chat service, enterprise RAG, moderation, coding assistant) and cost, reliability and observability to reference tables ([Leanpub](https://leanpub.com/ai-system-design-en)). It is paid, has one author, and is not a living repository. Its existence confirms that the primer's shape is right, and it sets the quality bar to beat.

The hyperscaler guidance (Azure orchestration patterns, AWS Prescriptive Guidance agentic series, Google Cloud agentic architecture centre) is well structured, but each covers only its own cloud's implementations ([Microsoft Learn](https://learn.microsoft.com/azure/architecture/ai-ml/guide/ai-agent-design-patterns); [AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/introduction.html); [Google Cloud](https://docs.cloud.google.com/architecture/agentic-ai-overview?authuser=0)). Governance lives in yet another artefact. FINOS's AI Governance Framework v2.0 (November 2025) adds an agentic risk catalogue with mitigations cross-referenced to OWASP, MITRE and the EU AI Act, but it is not attached to any design catalogue ([FINOS](https://www.finos.org/blog/finos-ai-governance-framework-v2.0-addressing-agentic-ai-risks-in-a-rapidly-evolving-landscape)).

The demand side also favours a concept-first approach. Interview loops now feature "design an LLM inference API", enterprise RAG and agent infrastructure. Interviewers grade trade-off articulation, evaluation design, cost and latency as constraints, and restraint in not over-building agents ([techinterview.org](https://www.techinterview.org/post/3233474919/ai-in-system-design-interviews-2026/); [techinterview.org](https://www.techinterview.org/post/3233476396/what-genai-engineer-interviews-test/)). The gap therefore has five parts, and nobody combines them:

1. a unified, trade-off-first taxonomy that crosswalks the competing vocabularies;
2. modern solved designs centred on building on top of foundation models;
3. method plus flashcards;
4. governance controls per pattern;
5. explicit staleness discipline.

The honest counterweight is that the primer's novelty comes from curation, framing and maintenance, not original research, and paid titles already cover much of the worked-design ground.

## A proposed table of contents that mirrors the original's arc

The outline below keeps the original's six movements: orientation, method, trade-offs, components in request order, solved designs, appendix. Each section is tagged **[S]** for stable core (review annually), **[F]** for dated frontier (review quarterly, expected to be rewritten), or **[S/F]** where a stable concept carries volatile specifics. The request path replaces DNS → CDN → load balancer with gateway → guardrails → context → model → tools → caching → evals/observability → security. This follows Huyen's platform build-up order: model API, context construction, guardrails, router and gateway, caching, agent patterns, cross-cutting observability ([synthesis of Huyen ch.10](https://agentic-ai.readthedocs.io/en/latest/ReferenceArchitecture/ai-engineering-architecture/)).

| # | Part / section | Mirrors original | Maturity |
|---|---|---|---|
| **0** | **Orientation**: motivation; who it is for (interviewee, practitioner, enterprise architect); study guide by timeline *and* role; how maturity tags and last-verified dates work; flashcards | Motivation, study guide, Anki | [S] |
| **1** | **Method: how to approach an AI system design question**: (1) use cases, quality bar and eval criteria first; (2) estimate tokens, cost and latency budget; (3) high-level design climbing the complexity ladder (single call → workflow → single agent → multi-agent); (4) core components; (5) harden (guardrails, security, governance); (6) scale and optimise | 4-step interview method + back-of-envelope | [S] |
| **2** | **Trade-offs: everything is a trade-off** | Performance vs scalability; latency vs throughput; CAP | |
| 2.1 | Cost ↔ quality ↔ latency (model tiers, cascades, caching, reasoning tokens) | | [S] |
| 2.2 | Determinism ↔ autonomy (workflows vs agents) | | [S] |
| 2.3 | Context stuffing ↔ retrieval (context rot; pre-computed vs just-in-time) | | [S/F] |
| 2.4 | Capability ↔ security (lethal trifecta: remove one leg) | | [S] |
| 2.5 | Single-agent ↔ multi-agent (parallelism and isolation vs ~15× tokens) | | [S/F] |
| 2.6 | Prompt ↔ RAG ↔ fine-tune (iteration speed vs behavioural depth) | | [S] |
| 2.7 | Throughput ↔ per-request latency in serving (batching, goodput) | Latency vs throughput | [S] |
| **3** | **Components, in request order** | DNS → … → security | |
| 3.1 | AI gateway and router: one interface, auth, quotas, rate limiting, cost attribution, version pinning, fallbacks, model cascades | Load balancer, reverse proxy | [S] (routing research [F]) |
| 3.2 | Input guardrails: PII, injection screening, relevance classifiers | — | [S] |
| 3.3 | Context engineering: system prompts at the "right altitude", tool design (ACI), examples, compaction, notes | Application layer | [S/F] |
| 3.4 | Retrieval pipeline: ingest/chunk → contextualise → hybrid index → rewrite → retrieve → rerank → assemble with citations | Database (+ indexing) | [S] |
| 3.5 | Agentic retrieval and the long-context boundary | — | [F] |
| 3.6 | Vector stores: ANN plus metadata filtering; product choice | NoSQL | concept [S], products [F] |
| 3.7 | Model layer: selection, structured outputs, streaming | Communication | [S/F] |
| 3.8 | Serving internals: prefill/decode, KV cache, continuous batching, quantization, speculative decoding, parallelism; PD disaggregation and engines | — | [S]; disaggregation/engines [F] |
| 3.9 | Workflows and agents: augmented LLM, chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, agent loop, plan-and-execute, HITL | Microservices | [S] |
| 3.10 | Multi-agent topologies and inter-agent protocols (MCP, A2A roles) | Service discovery, RPC vs REST | [F] |
| 3.11 | Memory: short/long-term, episodic/semantic | — | [F] |
| 3.12 | Output guardrails and validation | — | [S] |
| 3.13 | Caching: exact, provider prompt/prefix, semantic; never share user-scoped cache | Cache | exact/prefix [S], semantic [F] |
| 3.14 | Asynchronism: batch APIs, durable execution for long-running agents, back-pressure | Asynchronism | [S] |
| 3.15 | Evals: offline and online, LLM-as-judge with rubric, human calibration, regression gates | — (new first-class chapter) | [S] (tooling [F]) |
| 3.16 | Observability: agent → LLM → tool span trees; OTel GenAI status | — | concept [S], attributes [F] |
| 3.17 | Security: OWASP LLM Top 10, Agentic Top 10, six injection-defence patterns, sandboxing, least-privilege tools | Security (the original's weakest section) | [S]; agentic list [F] |
| 3.18 | Model adaptation: ladder, LoRA/QLoRA, distillation, preference/RL tuning | — | [S]; RL tuning [F] |
| **4** | **Solved designs (shared template)** | 8 solved designs | |
| 4.1 | LLM inference API (streaming, batching, KV cache, multi-tenant isolation, billing) | Pastebin (the "starter") | [S] |
| 4.2 | Enterprise RAG assistant (e.g., 2M documents, 2-second budget, fixed monthly spend) | Twitter search | [S] |
| 4.3 | Enterprise AI gateway for many teams and providers | Scaling to millions on AWS | [S] |
| 4.4 | Regulated document-review assistant (extraction, citation, human sign-off) | Mint.com (domain design) | [S/F] |
| 4.5 | Customer-support agent with handoff and escalation | — | [F] |
| 4.6 | Coding agent / agent infrastructure (sandboxing, tools, traces) | Web crawler | [F] |
| 4.7 | Eval and release pipeline ("how do you know a prompt change didn't make things worse?") | — | [S] |
| 4.8 | Additional unsolved prompts with curated references | Additional questions table | mixed |
| **5** | **Appendix** | Appendix | |
| 5.1 | Numbers every AI engineer should know (dated, ratio-first) | Latency numbers, powers of two | ratios [S], absolutes [F] |
| 5.2 | Cloud mapping table: concept → Azure / AWS Bedrock / GCP | — | [F] |
| 5.3 | Pattern crosswalk: primer ↔ Anthropic, Gulli, Lakshmanan/Hapke, Fowler, CSIRO, Azure | — | [S/F] |
| 5.4 | Governance crosswalk: pattern ↔ OWASP / FINOS / EU AI Act control | — | [F] |
| 5.5 | Real-world architectures (e.g., Anthropic's multi-agent research system) and engineering blogs | Real-world architectures | [F] |
| 5.6 | Glossary and changelog | — | [S] |

Three choices in this outline are deliberate. First, evals get their own first-class chapter and appear in step 1 of the method. Thoughtworks makes evals the second pattern and says fine-tuning is warranted only "if evals remain unsatisfactory" ([Fowler](https://www.martinfowler.com/articles/gen-ai-patterns/)), and interview loops now run a separate evaluation round ([techinterview.org](https://www.techinterview.org/post/3233476396/what-genai-engineer-interviews-test/)). Second, the starter solved design is the inference API, not a chatbot, because it is the most-asked AI-era prompt and it reuses classic primer concepts. Third, every frontier section stays deliberately small so that rewriting it is cheap.

## Six design decisions that keep the primer from going stale

**Staleness handling is the main design problem.** The original has no per-section dates. Its decay is visible only through broken links and admissions such as "could use some updates", and it already relies on 14 web.archive.org rewrites to patch link rot ([README](https://github.com/donnemartin/system-design-primer/blob/master/README.md)). The AI primer should put YAML front matter on every section with `maturity`, `last_verified`, `review_by` and `owner` fields. CI should fail or warn when `review_by` passes, run an automated link checker, and archive cited URLs on merge. Stable sections get annual review and frontier sections quarterly. Frontier material should live in its own files so that a rewrite never touches the core. A public changelog of what moved, for example "TGI → maintenance mode" or "OWASP Agentic Top 10 added", turns the churn itself into teaching material.

**A strict per-section template** should extend the original's summary → variants → disadvantages → sources schema with the elements that critics found missing:

```markdown
---
maturity: stable | frontier | speculative
last_verified: 2026-11-01
review_by: 2027-11-01
owner: "@handle"
---
## <Pattern name>  (aka: <names in Anthropic / Gulli / Lakshmanan-Hapke / Azure>)
Diagram (Mermaid/Excalidraw source committed)
**What it is**: 2–4 paragraphs, vendor-neutral
**When to use / when to avoid**: Azure-style
**Trade-offs**: which axis from Part 2 it moves, and in which direction
**Limitation → mitigating pattern**: Fowler-style table
**Numbers**: dated, sourced, ratio-first
**Failure modes & antipatterns**
**Risk & controls**: OWASP/FINOS IDs, required control, evidence an auditor would ask for
**Cloud mapping**: Azure | AWS Bedrock | GCP | self-hosted
**Flashcards**: 3–6 Q/A pairs
**Sources & further reading**
```

The "when to use / when to avoid" element borrows from Azure's pattern pages ([Microsoft Learn](https://learn.microsoft.com/azure/architecture/ai-ml/guide/ai-agent-design-patterns)). The limitation → mitigation table borrows from Fowler ([martinfowler.com](https://www.martinfowler.com/articles/gen-ai-patterns/)). Diagrams should be text-sourced (Mermaid or Excalidraw), not OmniGraffle as in the original, so contributors can edit them.

**Flashcards should be generated from the template, not hand-maintained.** The original ships three hand-built `.apkg` decks ([README](https://github.com/donnemartin/system-design-primer)), and none of the surveyed AI resources offers flashcards at all. A build script that extracts each section's Q/A block into an Anki deck, tagged with maturity, lets learners suspend frontier cards when they go stale. The same pipeline can produce an EPUB, as the original's `generate-epub.sh` does.

**Vendor-neutral prose with cloud mappings at the edge.** The body should describe concepts such as a gateway, a router or a prefix cache. Product names belong in a mapping row and the 5.2 appendix, which is where nearly all churn is concentrated. This also answers the critique that the original ignored cloud-specific services. One caveat: this research did not verify specific service mappings (for example Azure API Management's AI gateway features or Bedrock's prompt routing), so that table needs first-party sourcing before publication.

**Governance and risk controls per pattern** are the strongest differentiator and the most relevant to a bank. FINOS v2.0 already pairs agentic risks (prompt injection and memory poisoning, persistent agent compromise, chain-of-thought leakage, agent supply-chain tampering) with mitigations cross-referenced to OWASP, MITRE and the EU AI Act ([FINOS](https://www.finos.org/blog/finos-ai-governance-framework-v2.0-addressing-agentic-ai-risks-in-a-rapidly-evolving-landscape)). The OWASP lists provide stable IDs to cite, such as LLM06 Excessive Agency, LLM10 Unbounded Consumption and ASI08 Cascading Failures ([Coralogix](https://coralogix.com/ai-blog/owasp-top-10-for-llm-applications/); [OWASP](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)). Putting a "Risk & controls" block in every section turns the primer from interview prep into something a model-risk or architecture review board can use.

**Numbers should be ratio-first and dated.** No authoritative 2026 "numbers every AI engineer should know" table exists. Teach durable ratios, each with a date stamp:

- Provider cache reads cost about **0.1×** input at Anthropic, and **0.25–0.5×** at OpenAI and Gemini ([OpenRouter](https://openrouter.ai/docs/prompt-caching)).
- Agents use about **4×** the tokens of chat, and multi-agent systems about **15×** ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)).
- Sub-agent summaries run about 1–2K tokens ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- QLoRA fine-tuned a 65B model on one 48 GB GPU ([QLoRA](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1feb87871436031bdc0f2beaa62a049b-Abstract.html)).
- Reported output speeds for frontier models cluster around 60–110 tok/s ([Artificial Analysis](https://artificialanalysis.ai/embed/llm-performance-leaderboard)).

Absolute prices should go in a quarterly-refreshed table. One more caveat: "time to first chunk" for reasoning models includes thinking time and is not comparable to classic TTFT.

## Claims in the notes that need verification before publishing

Several claims in the research notes do not yet meet a primer's own standard, and they should not enter the primer as stated.

| Claim | Status | Required action |
|---|---|---|
| Claude list prices and context windows (e.g., Opus 5.5 $4/$20 per M tokens) | Aggregator only (BenchLM); anthropic.com/pricing was not fetchable. Internally inconsistent: a listed $0.10 Sonnet 5.5 cache read implies 0.05× input, which contradicts the 0.1× multiplier | Source from first-party pricing pages |
| Anthropic Batch API 50% discount stacking with caching | Aggregator only | Confirm first-party; OpenAI/Gemini batch discounts not sourced at all |
| Cache multipliers and TTLs for all providers | Via OpenRouter docs, not provider docs | Acceptable for ratios; verify before quoting exact values |
| Self-hosted cost of ~$0.15–0.65 per M output tokens on A100/H100 | Single vendor blog (Spheron) worked example | Label as illustrative or re-derive |
| SGLang RadixAttention "20–40% lower TTFT" | Unsourced vendor claim | Exclude or find a benchmark |
| TGI repo archived 21 Mar 2026 | Secondary blog; HF confirms maintenance mode but gives no date | Cite HF only |
| PagedAttention near-zero waste / 2–4× throughput | From memory; paper not fetched | Read arXiv 2309.06180 |
| OpenAI agent guide details (e.g., "orchestration" tool type) | Secondary summary; PDF not fetched | Read primary PDF |
| Tokens-per-word (~0.75), embedding dimensions, KV-bytes formula values, GPU HBM capacities and bandwidths, "TTFT < 500 ms feels instant" | Not sourced | Source or omit from the numbers appendix |
| Model-tier price ratios (5–50×), output ≈ 4–5× input, bytes-per-parameter rules | Writer's derived arithmetic | Present as derived, show working |
| Prompt → RAG → fine-tune → distill → RL ladder (full five-step form) | Synthesis; only the first three steps are sourced (Thoughtworks) | Mark as synthesis |
| Contextual retrieval −35/−49/−67% | Secondary summary of Anthropic's post; "up to" figures | Cite Anthropic's original |
| Huyen platform order | Secondary synthesis, not Huyen's text | Check against *AI Engineering* ch.10 |
| Lakshmanan/Hapke pattern names (e.g., "Harness Engineering") | Possibly from a revised edition | Confirm edition |
| FINOS risk counts (30 → 46) | Do not reconcile with "six additions" | Cite framework site directly |
| Repo star counts for AI prior art | Third-party trackers with varied snapshot dates | Present as approximate |
| Critiques of the original primer | All from vendors selling alternatives (remio, PracHub, DesignGurus) | Pair with direct repo evidence, as done above |

There are also coverage gaps. The research did not cover gateway/router products and routing research (FrugalGPT, RouteLLM), GraphRAG maturity, memory taxonomies, structured-output maturity, the contents of Google's agent whitepapers, the MCP spec's 2026 breaking changes, or any demand data such as search volume. These are the first research tasks inside the corresponding backlog items, not reasons to delay.

## Conclusion

**Verdict: feasible, and worth doing, with conditions.** The stable core is large enough and has converged enough to support a primer the size of the original. The open position (free, vendor-neutral, trade-off-first, with governance and flashcards) is real. Writing the primer will not be the hard part. Keeping it alive will be, because the original shows that a well-built guide can collect 374k stars and still go stale. For a learning vehicle this is a useful property: every section forces a primary-source read, a trade-off argument and a controls mapping, which is the skill set a bank's AI architecture function needs. Each finished section also stands alone as a publishable article.

The recommended next step is a phased section backlog, where each item is one learning unit that ends with the template filled in, flashcards written and a last-verified date set:

- **Phase 0 (scaffold):** repo, section template, maturity legend, front-matter schema, link-check and review-date CI, Anki/EPUB build. Write the Orientation and Method chapters (Parts 0–1).
- **Phase 1 (stable spine):** trade-off axes 2.1, 2.2, 2.4 and 2.6; gateway (3.1); guardrails (3.2, 3.12); retrieval pipeline (3.4); evals (3.15); security (3.17); and solved design 4.2, enterprise RAG, which exercises all of them.
- **Phase 2 (serving and economics):** serving internals (3.8), caching (3.13), asynchronism (3.14), model layer (3.7), adaptation (3.18), the dated numbers appendix (5.1), and solved designs 4.1 (inference API) and 4.3 (enterprise gateway).
- **Phase 3 (agents and frontier):** workflows and agents (3.9), context engineering (3.3), agentic retrieval (3.5), multi-agent and protocols (3.10), memory (3.11), observability (3.16), and solved designs 4.6 (coding agent), 4.5 (support agent) and 4.4 (regulated document review).
- **Phase 4 (cross-cutting appendices):** cloud mapping (5.2), pattern crosswalk (5.3), governance crosswalk (5.4), real-world architectures (5.5), and the first quarterly frontier review.

Start Phase 1 with the retrieval pipeline and the enterprise-RAG solved design. That is where the evidence is most stable and where governance controls are easiest to make concrete. Before publishing anything, clear the verification table above.
