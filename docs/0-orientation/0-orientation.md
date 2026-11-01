---
id: "0"
title: "Orientation"
phase: 0
maturity: stable
status: draft
last_verified: 2026-11-01
review_by: 2027-11-01
owner: "@daneb"
---

# 0 Orientation

## Key terms

- **Large language model (LLM):** a model trained on large amounts of text that writes text in response to a prompt.
- **Primer page and deep dive:** each topic has a short page to learn from and a longer reference page with provider details, numbers and controls.
- **Maturity tag:** how settled a section is: stable (`S`), mixed (`S/F`), frontier (`F`) or speculative (`?`).
- **last_verified / review_by:** when a section's sources were last checked, and when they must be checked again.
- **Lab:** a small runnable script that tests a claim from the section, with the prediction written down first.

More in the [glossary](../5-appendix/5.6-glossary.md).

## What this is

A primer on designing systems built around large language models: gateways, retrieval, agents,
serving, evals, security and governance. It follows the arc of the
[System Design Primer](https://github.com/donnemartin/system-design-primer), which taught a generation
of engineers that every design decision is a trade-off:

| Part | What it gives you | Classic equivalent |
|---|---|---|
| 1 Method | A repeatable way to work through any AI design question | "How to approach a system design interview question" |
| 2 Trade-offs | The handful of tensions behind almost every decision | Performance vs scalability, latency vs throughput, CAP |
| 3 Components | Each building block, in the order a request meets it | DNS → CDN → load balancer → … → security |
| 4 Solved designs | Worked end-to-end designs on a shared template | Pastebin, Twitter timeline, web crawler |
| 5 Appendix | Reference numbers, cloud mappings, crosswalks, glossary | Latency numbers, real-world architectures |

## Who it is for

- **Interview candidates.** "GenAI system design" is now a recognised interview round at AI labs and
  AI-heavy companies, often with a separate evaluation round
  ([techinterview.org](https://www.techinterview.org/post/3233476396/what-genai-engineer-interviews-test/)).
  Parts 1, 2 and 4 are the core.
- **Practising engineers** building on model APIs. Parts 2 and 3, then the solved design closest to
  your system.
- **Enterprise architects and review boards.** Every pattern has a "Risk and controls" table that maps
  to OWASP, FINOS and EU AI Act references. Start with 3.17 Security and appendix 5.4.

## How to read a section

Every topic has the same shape. The primer page covers what it is, key terms, a worked example, when
to use it, when to avoid it, its disadvantages and flashcards. The deep dive holds the provider survey,
numbers, risk and controls, and cloud mapping.

Each section is also labelled with how settled its content is:

| Tag | Maturity | Meaning | Reviewed |
|---|---|---|---|
| `S` | stable | Independent sources agree on the concept and the names | Every 12 months |
| `S/F` | mixed | The concept is stable; the specifics (products, standards, numbers) are moving | Every 6 months |
| `F` | frontier | Still being worked out in public; expect rewrites | Every 3 months |
| `?` | speculative | Research-grade or contested | Every 3 months |

The `last_verified` date at the top of a section is the day its sources were last checked. The build
fails when a review is overdue, so a date in the past is a promise that someone looked.

AI moves fast, but less of it moves than it seems. The stable core is small. It's the five workflow
patterns and agent loop from Anthropic's
[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents). It's also
the retrieval pipeline, gateways and caching, evals, guardrails and the prompt-injection threat model.
What churns is mostly products, protocols and multi-agent designs. Learn the core well and treat the
frontier as news.

## Example

An engineer has a week before a design interview at a company building AI products. They read the
method (Part 1), then trade-offs 2.1, 2.2 and 2.4, then the five components marked in the study guide.
On day four they work the enterprise RAG assistant (4.2) on paper before reading the solution, and
compare their token estimate with the one in the page. Each evening they review that day's flashcards.
On day six they run Lab 2.4 and classify the tools in their own team's chatbot. That last step is the
one most likely to come up: "What could an injected instruction make your system do?"

## Study guide

The classic primer offered short, medium and long study plans. The same idea, by time available:

| | 1 week | 1 month | 3 months |
|---|---|---|---|
| Method (Part 1) | Read | Read, practise twice | Practise on every solved design |
| Trade-offs (Part 2) | 2.1, 2.2, 2.4 | All | All |
| Components (Part 3) | 3.1, 3.4, 3.9, 3.15, 3.17 | All stable (`S`) sections | All, including frontier |
| Solved designs (Part 4) | 4.2 | 4.1, 4.2, 4.3 | All, then 4.8 unaided |
| Numbers (5.1) | Skim | Learn the ratios | Re-derive them |
| Flashcards | Part 2 deck | Parts 1–3 | Everything, daily |

## Using the flashcards

Run `python3 scripts/primer.py flashcards` and import `build/flashcards.tsv` into Anki
(File → Import). Cards are tagged by section and maturity, so you can suspend frontier cards when a
section is rewritten.

## Flashcards

Q: What are the five parts of the primer after Orientation?
A: Method, Trade-offs, Components (in request order), Solved designs, Appendix.

Q: What does a maturity tag of S/F mean?
A: The concept is stable but its specifics (products, standards, numbers) are still moving; reviewed every 6 months.

Q: What does a section's last_verified date promise?
A: That its sources and numbers were re-checked on that date; CI fails once the review_by date passes.

## Sources and further reading

- [System Design Primer](https://github.com/donnemartin/system-design-primer): the model for this primer's
  structure.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
  (Anthropic, Dec 2024): the clearest statement of the stable workflow patterns.
- [Emerging patterns in building GenAI products](https://www.martinfowler.com/articles/gen-ai-patterns/)
  (Thoughtworks / martinfowler.com, 2025): patterns framed by the limitation each one addresses.
- Chip Huyen, *AI Engineering* (O'Reilly, Dec 2024): the most complete single book on the field.
