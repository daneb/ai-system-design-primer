# Roadmap

What comes after the first draft. [PLAN.md](PLAN.md) records how the first draft was built and the
verification debt; this file is the forward plan. Every item has a check you can run or see, so "done"
isn't a matter of opinion.

**State on 2026-11-02:** first release; all 44 sections reviewed by the author (Parts 0–5), with 26 deep dives, 31 labs and
231 flashcards. The author has signed off Phases 1–3 for now.

## Baseline audit (2026-11-01)

Measured by a quick scan of the primer pages, to set targets below:

| Measure | 2026-11-01 start → now | Target |
|---|---|---|
| Diagrams | 42 Mermaid flowcharts; no rendered images → **43 rendered SVGs with alt text, one style** | Every page has a rendered, consistent diagram with alt text |
| Primer pages with no worked example | 29 of 41 → **0 in Parts 0–3** (Parts 4–5 are worked cases already) | 0 |
| Sentences over 30 words in primer pages | 110 → **0 in Parts 0–3** | Under 20 |
| Acronyms used in primer pages but not in the glossary | ~37 → **0** | 0 |
| Lab results shown as charts | 0 (tables only) → **17 of 17 labs with a numeric sweep** | Every lab with a numeric sweep has a chart |
| Verification-debt rows | 50 | Under 15, none on a stable section |

## Theme 1: Clearer definitions and fuller explanations

Readers should never meet a term they can't look up, and every idea should come with a concrete case.

- [x] **P0 · Key terms box on every primer page.** Three to six terms, each defined in one plain
  sentence, linked to the glossary. *Check:* `primer.py check` warns when a page lacks the box or uses a
  glossary term in its heading without defining it. *Done 2026-11-01:* Parts 0–3 have the box; terms are outside the word budget.
- [x] **P0 · Acronym rule.** Spell out on first use in each page; every acronym in the glossary.
  *Check:* a new `check` rule lists acronyms missing from the glossary (the audit above, automated). *Done 2026-11-01:* `check` warns on acronyms missing from the glossary (Part 5 exempt).
- [x] **P0 · One worked example per page.** A short, concrete case with numbers: "a 40-turn agent
  that…", "a bank with 50 apps…". *Check:* every primer page has a `### Example` subsection. *Done 2026-11-01:* Parts 0–3 have an example, mostly drawn from the labs.
- [x] **P1 · Part 0 foundations: "How a language model works, for system designers".** Tokens,
  context window, sampling and temperature, embeddings, attention and the KV cache, tool calling,
  reasoning models. Two or three short pages so Parts 2–3 can assume them. *Check:* pages exist and
  Part 2–3 pages link to them instead of re-explaining. *Done 2026-11-01:* 0.1 tokens, context and sampling; 0.2 inside a model call (prefill, decode,
  KV cache, reasoning); 0.3 tool calling and structured output; each with a lab. Linked from 2.1, 2.7,
  3.3, 3.7, 3.8 and 3.9.
- [x] **P1 · "How it works, step by step" for the hardest mechanisms**, in the deep dives: KV cache and
  paged attention, continuous batching, speculative decoding, HNSW search, reciprocal rank fusion,
  LoRA, prompt caching, pass^k. Each with a small diagram and a worked number. *Check:* list complete. *Done 2026-11-02:* all eight, each with a diagram and a worked
  number, in deep dives 3.4, 3.6, 3.8, 3.13, 3.15 and 3.18.
- [x] **P1 · Sentence-length pass.** Split sentences over 30 words; target under 20 across the primer.
  *Check:* `check` reports the count. *Done 2026-11-01:* 0 sentences over 30 words in Parts 0–3.
- [x] **P1 · Glossary cleanup.** Remove duplicates (two were found and removed on 2026-11-01), one
  definition per term, consistent style, link every term to its main section. *Check:* `check` fails on
  duplicate terms. *Done 2026-11-01:* `check` fails on duplicate terms; ~110 terms added. Linking every term to its section is still open.
- [ ] **P2 · "Common misconceptions" per part,** e.g. "a bigger context window means you don't need
  retrieval", "multi-agent is more capable", "RAG eliminates hallucination". Each answered with a lab or
  source.
- [ ] **P2 · Reading paths** for three audiences: engineers new to AI, architects, and risk and audit
  reviewers.

## Theme 2: Higher-quality images

The original primer is known for its diagrams. Ours are Mermaid flowcharts: easy to maintain, but
plain, inconsistent in layout and rendered differently by every viewer.

- [x] **P0 · Diagram style guide** in STYLE.md: one palette, shape meaning (model, tool, data store,
  human, untrusted input), left-to-right request flow, section numbers on components, alt text rule. *Done 2026-11-01:* STYLE.md § Diagrams.
- [x] **P0 · Render diagrams to SVG in the build.** Keep Mermaid as source; render with `mmdc` and a
  shared theme into `images/`, and link the SVG with alt text from each page. *Check:* `check` fails
  when a page's diagram has no rendered SVG or no alt text. *Done 2026-11-01:* 43 sources in `images/src/`, `scripts/diagrams.py check` in CI.
- [ ] **P2 · Hero diagrams**, drawn by hand (Excalidraw or draw.io sources committed under
  `images/src/`): the request path through Parts 3 (README), the complexity ladder, the lethal trifecta,
  the agent loop, the retrieval pipeline, the sandbox in 4.6. These are the images people will share.
- [ ] **P2 · Anatomy diagrams** for mechanisms in Theme 1 (KV cache, continuous batching, HNSW, LoRA,
  caching prefixes), drawn to scale where numbers matter.
- [x] **P1 · Lab charts.** Each lab writes an SVG chart next to its README (matplotlib, optional
  dependency); READMEs show the chart above the table. *Check:* labs with a sweep have `result.svg`. *Done 2026-11-02:* 14 labs with sweeps draw `result.svg` via `labs/chart.py`;
  the rest compare named options and keep tables. `primer.py labs` checks the charts.
- [ ] **P2 · Dark-mode and accessibility check:** contrast, readable at mobile width, text not baked
  into images where avoidable. *Partly done 2026-11-03:* every diagram fits GitHub's column with text
  at 11 px or more (`diagrams.py check` enforces it) and has hand-written alt text. Dark mode and
  mobile width still open.
- [x] **P2 · Image licensing** recorded alongside the content licence. *Done 2026-11-02:* all diagrams and charts are original and covered by CC BY 4.0;
  stated in the README.

## Theme 3: Prioritised backlog

### P0: before going public

- [x] **Decide the licence, visibility and publishing** (open decisions in PLAN.md). Suggested: CC BY
  4.0 for content, MIT for code, matching the original. *Licence decided 2026-11-02:* CC BY 4.0 + MIT
  ([ADR 0008](adr/0008-licences.md)); Code of Conduct, SECURITY.md, issue and PR templates added.
  Visibility and publishing remain the author's call.
- [x] **`git init`, first commit, push.**
- [x] **CI:** run `primer.py check`, `primer.py readme --check`, the relative-link check and every lab
  on each pull request. *Check:* green badge in README. *Done 2026-11-01:* labs job added. Badge added 2026-11-02.
- [x] **Clear verification debt on stable sections first:** batch discounts and cache multipliers
  (2.1, 3.13, 5.1), PagedAttention figures (3.8), contextual-retrieval figures (3.4), pgvector defaults
  (3.6), OpenAI agent guide details (3.9, 2.4). *Done 2026-11-02:* all six checked against primary sources;
  one correction (vLLM's throughput figures). Five debt rows cleared, two narrowed.
- [x] **External link checker** (weekly, with a cache) so dead provider links surface early. *Done:* lychee weekly in CI.

### P1: next quarter

- [ ] **First quarterly frontier review, due 2027-02-01:** 3.5, 3.10, 3.11, 4.5, 4.6, 5.2, 5.4, 5.5.
  Re-check MCP and A2A versions, managed memory and agent services, EU AI Act guidance
  and standards, and any `(not verified)` cells in the cloud mapping.
- [x] **Refresh 5.1 Numbers with Phase 3 figures:** tool-definition token costs, agent and multi-agent
  token multipliers, pass^k, context-rot findings, trace sizes. *Done 2026-11-02:* new tables for model calls, agents and tools,
  context and memory, operations; Part 0 and security figures added.
- [x] **Read the papers behind second-hand figures:** Self-Route, MAST, Kim et al., τ-bench, Chroma
  context rot, Mem0, Stanford legal AI. *Done 2026-11-02:* all seven read. Corrected Kim et al. (v3: 260 configurations,
  −39% to −70% sequential) and MAST (41–86.7%); τ-bench's −22.4% policy-removal figure not found in the text.
- [x] **Labs for the solved designs that lack one:** 4.4 (recall vs review time), 4.5 (pass^k on a toy
  policy), 4.6 (review capacity vs merged work). *Done 2026-11-02:* Labs 4.4, 4.5 and 4.6, each with a chart.
  Lab 4.4 found 98% recall needs 58–69 lawyer minutes with moderate separation, not 30; 4.4 now says so.
- [x] **Anki package build** (`.apkg`) as an optional extra, keeping the TSV as the zero-dependency path. *Done 2026-11-02:* `primer.py anki`, standard library only;
  one sub-deck per part; stable GUIDs so re-imports update cards.
- [x] **Second reads** of Phase 0 and the appendices (Parts 4.8 and 5). *Done 2026-11-02:* Part 0 updated for the foundations, labs and Anki
  package; 4.8 links the foundations; 5.2 title fixed; 5.4 now cites the Omnibus as law (Regulation (EU)
  2026/1744, in force 27 July 2026).

### P2: later

- [ ] **Map Lakshmanan and Hapke** into the pattern crosswalk (5.3) from the published edition; check
  Gulli and Fowler names against their sources.
- [ ] **New solved designs** from 4.8, in order of reader value: text-to-SQL analytics assistant,
  real-time voice agent, deep-research agent, web-grounded answer engine.
- [ ] **Static site** (for example MkDocs) with search, rendered diagrams and the deep dives side by
  side; keep Markdown in the repository as the source.
- [ ] **Interactive labs** (notebooks) alongside the scripts.
- [ ] **Printable PDF** of the primer pages.
- [ ] **Translations,** once the structure is stable.
- [ ] **Add real-world architectures** to 5.5 as teams publish write-ups with scale and lessons.

## How items move

1. Pick the highest-priority unchecked item.
2. Research and write per STYLE.md; run the checks.
3. Tick the box here, add a changelog row in the glossary, and close any verification-debt rows it
   clears in PLAN.md.
