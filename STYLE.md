# Style and method

How sections of this primer are researched and written. Read this before writing or reviewing a
section. [CONTRIBUTING.md](CONTRIBUTING.md) covers the mechanics (front matter, checks);
this file covers the craft.

## Who we write for

A working engineer learning on their own time. They are technical and busy. They want to understand
*why* a design works, be able to explain it to someone else, and know what to do on Monday.

Write for that person, not for a search engine, a vendor, or a reviewer who wants to see effort.

## Voice

- **Simple, technical, precise.** Use the correct term, then explain it in plain words the first time
  it appears. "Reciprocal Rank Fusion (RRF) merges ranked lists using only each document's position."
- **Short sentences, active voice, concrete nouns.** "The reranker reads the query and passage
  together" beats "Relevance assessment is performed jointly."
- **Explain before you list.** A paragraph that says how the parts fit comes before any bullet list
  of the parts.
- **One idea per paragraph.** If a paragraph needs a "Furthermore", it is two paragraphs.
- **Show the trade-off.** Every recommendation says what it costs and when it is wrong.
- **No hype, no filler.** Cut "powerful", "seamless", "game-changer", "it's important to note that",
  and any sentence that would fit in every section.
- **Name products only in Cloud mapping tables** ([ADR 0003](adr/0003-vendor-neutral-prose.md)).
- **Paraphrase sources.** Quote only a short phrase when the exact words matter, and never more than
  one quote per source in a section.

## Two layers: primer and deep dive

The original System Design Primer works because a topic can be read in a few minutes: a definition, a
picture, the types, the disadvantages, a handful of links. Its typical topic is 200–1,100 words and
half its lines are bullets. Our first Phase 1 drafts were two to four times longer and a quarter
tables, because every section carried its risk table, cloud mapping, numbers and provider survey
inline. They read like a handbook, not a primer.

So every topic now has two files ([ADR 0007](adr/0007-primer-and-deep-dive.md)):

- **The primer page** (`docs/<part>/<id>-<slug>.md`) is what a learner reads. It teaches the idea,
  the decision and the pitfalls, and nothing else. It is the page the README links to and the source
  of the flashcards.
- **The deep dive** (`docs/deep-dives/<id>-<slug>.md`) is the reference a reviewer, architect or
  auditor reads: the provider survey, numbers, risk and controls, cloud mapping, detailed variants
  and the full source list. The primer links to it once, near the end.

Research happens once, for the deep dive. The primer is written last, as a summary of it. If the two
disagree, the deep dive is the record and the primer is fixed.

## Length

Long is not thorough. The reader should finish a primer page in ten minutes.

| Kind | Primer body budget (words, excluding flashcards and sources) |
|---|---|
| Orientation and Method (Parts 0–1) | up to 1,400 |
| Trade-off (Part 2) | 400–800 |
| Component (Part 3) | 400–800 |
| Hub component (3.4, 3.9, 3.17) | up to 1,200 |
| Solved design (Part 4) | 1,000–2,500, excluding code blocks |
| Deep dive | no budget; organise it so a reader can jump to the table they need |

`scripts/primer.py check` warns when a primer page is over budget, has more than one table, or has
more than eight external links. If you are over: move it to the deep dive. Don't compress sentences
until they stop being clear.

## Shape of a primer page

Follow [templates/section.md](templates/section.md). Mirror the original primer's rhythm:

1. **One diagram** that shows flow or structure the prose can't. Small.
2. **What it is**: the problem, then the mechanism, in one to three short paragraphs.
3. **Key terms**: three to six terms, each in bold with a one-sentence plain definition, then a link
   to the glossary. Every term here must also be in the glossary. Not counted in the word budget.
4. **How it works** or **Types**: bullets, each a bolded term and one or two sentences.
5. **Example**: one concrete scenario with numbers, ideally from the section's lab, showing the idea
   changing a decision. Five to ten sentences.
6. **When to use / when to avoid**: bullets.
7. **Disadvantages**: bullets, the way the original lists "Disadvantage(s)". Include the main
   failure modes here.
8. **Go deeper**: one line linking the deep dive and the lab, saying what the reader will find.
9. **Flashcards** and **Sources** (3–5 links, primary sources first).

Rules of thumb:

- **Define before you use.** Spell out every acronym on first use in a page, and make sure it is in
  the glossary. `primer.py check` lists acronyms missing from the glossary.
- **Sentences of 30 words or fewer.** `primer.py check` flags longer ones in Parts 0–3.

- **Bullets over tables.** At most one table, and only when the reader genuinely compares rows.
- **Links:** other sections and labs inline; external sources mostly in the Sources list. Inline
  citations only for numbers and claims a reader would doubt.
- **Provider guidance:** when the providers agree, say so in one sentence ("Anthropic, OpenAI,
  Google, AWS and Microsoft all advise...") and put who said what in the deep dive.
- **No product names** in primer prose ([ADR 0003](adr/0003-vendor-neutral-prose.md)); they live in
  the deep dive's cloud mapping.
- **One headline number at most**, sourced and dated, if it changes the reader's intuition.

## Diagrams

Diagrams are Mermaid sources rendered to SVG, so they look the same on GitHub, in a PDF and offline.

- **Where they live:** source in `images/src/<page-stem>.mmd`, rendered file in `images/<page-stem>.svg`. Deep-dive diagrams use a `dd-` prefix. Never put a ```` ```mermaid ```` block in a page.
- **How a page shows one:** `![alt text](../../images/<stem>.svg)` with `<!-- source: images/src/<stem>.mmd; render with scripts/diagrams.py -->` on the next line.
- **Alt text:** the first line of the source is `%% alt: ...`. Write one sentence saying what the diagram shows, not what it looks like. `scripts/diagrams.py sync-alt` copies it into the pages.
- **Flow:** left to right (`flowchart LR`) unless the idea is a stack. Use invisible links (`~~~`) to sit two panels side by side.
- **Labels:** short nouns. Put the section number on a component that has its own page, for example `Gateway 3.1`.
- **Colour means something.** Tag nodes with a class; plain nodes stay white. Add no other colours.

| Class | Use for | Look |
|---|---|---|
| `model` | an LLM call | indigo |
| `tool` | a tool, API or code step | green |
| `data` | a store, index or document | amber |
| `human` | a person or approval step | grey |
| `untrusted` | input you do not control | red, dashed |
| `control` | a guardrail, gateway or policy check | violet |

- **Render:** `python3 scripts/diagrams.py render` (needs Node; uses `@mermaid-js/mermaid-cli` and `images/mermaid-config.json`). Commit the `.mmd`, the `.svg` and `images/.hashes.json` together.
- **Check:** `python3 scripts/diagrams.py check` fails on inline Mermaid, missing alt text, a missing source or SVG, or an SVG older than its source. CI runs it.

### Lab charts

A lab with a numeric sweep draws it with `labs/chart.py` and writes `result.svg` beside its README.
The README shows the chart above its results table, with alt text that states the finding in numbers.

- **One chart per lab,** of its main sweep; comparisons of named options stay as tables.
- **The title states the finding** ("Tool search keeps the per-call cost flat"), not the axes.
- **At most three series,** in the helper's fixed colour order, with a legend and labels at the line
  ends. Mark a threshold or baseline with the dashed reference line.
- **Charting comes after the tables** in the script and must not change them; matplotlib is optional
  locally, and `primer.py labs` (run in CI) fails if a chart is missing or not shown.

## Shape of a deep dive

Follow [templates/deep-dive.md](templates/deep-dive.md): where the providers agree and differ,
variants in detail, limitation → mitigating pattern, numbers, failure modes and antipatterns, risk
and controls ([ADR 0005](adr/0005-risk-and-controls-per-pattern.md)), cloud mapping, lab results,
full sources.

## Research method

Every section is researched the same way, so readers can trust that a claim isn't one vendor's view.

1. **Start from primary sources.** The paper that introduced the idea, the standard, or the vendor's own
   engineering post or documentation. Use a secondary source only when the primary is unavailable, and
   say so in the citation.
2. **Survey the major providers, every time** (recorded in the deep dive). Check how each of these describes the pattern, and note
   where they agree and where they differ:
   - **Anthropic** (engineering blog, docs)
   - **OpenAI** (developer docs, guides, cookbook)
   - **Google** (Cloud Architecture Center, Vertex AI docs, Google Research)
   - **AWS** (Prescriptive Guidance, Bedrock docs, Builder/re:Post articles by AWS staff)
   - **Microsoft** (Azure Architecture Center, Azure AI docs, Microsoft Research)

   Add the research literature, standards bodies (OWASP, NIST, FINOS, ISO) and respected practitioners
   (for example Thoughtworks) where they cover the topic. If a provider has nothing on the topic, that is
   a finding: say so rather than padding.
3. **Look for convergence.** When independent providers describe the same pattern, that is the stable
   core: teach it as such. Where they disagree or only one vendor describes it, mark it as frontier or
   vendor-specific.
4. **Separate what's verified from what isn't.** If a claim, number or mapping could not be confirmed
   from a primary source, mark it in the text ("not verified") and add it to the verification debt in
   [PLAN.md](PLAN.md). Never round a gap into a confident sentence.
5. **Prove one claim yourself** where practical: a small lab under `labs/<section-id>/`, with the
   expected result written down before running it. Report what happened, including when the result
   contradicts the expectation; that is often the best lesson.

## Numbers

- Every figure has a source and an "as of" date ([ADR 0006](adr/0006-ratio-first-dated-numbers.md)).
- Prefer ratios and orders of magnitude over absolute prices.
- Say what a benchmark measured. A retrieval metric is not an answer-quality metric.
- Label your own arithmetic as derived and show the working.

## Review checklist

- [ ] Could a busy engineer read the primer page in ten minutes and explain the idea afterwards?
- [ ] Is it within budget, mostly bullets, with at most one table and one diagram?
- [ ] Does the diagram follow the Diagrams rules, and does `scripts/diagrams.py check` pass?
- [ ] Is every term explained the first time it appears?
- [ ] Does the deep dive cover at least three of the five major providers, plus primary literature?
- [ ] Are agreements and disagreements between sources stated in the deep dive?
- [ ] Is every number sourced and dated, and every unverified claim marked?
- [ ] Do the primer and the deep dive agree?
- [ ] Do the flashcards test understanding, not recall of trivia?
