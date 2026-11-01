# ADR 0007: Two layers per topic, a primer page and a deep dive

- Status: accepted
- Date: 2026-11-01
- Amends: [ADR 0005](0005-risk-and-controls-per-pattern.md), [ADR 0006](0006-ratio-first-dated-numbers.md)

## Context

After drafting Phase 1 we compared the result with the original System Design Primer (cloned
2026-11-01). The original's reference text is about 12,000 words over ~25 topics; a typical topic is
200–1,100 words, half its lines are bullets, 4% are tables, and each topic links 3–8 sources. Our
component sections were 1,400–2,400 words, a quarter table rows, with 12–42 links each. Sentence length
was the same (17.7 vs 16.6 words), so the writing was not the problem: the template was. Every section
carried its provider survey, numbers, risk and controls and cloud mapping inline, which made it a
handbook rather than a primer.

The rigour is worth keeping. A bank's architecture and model-risk reviewers need exactly that
material. Learners need it out of the reading path.

## Decision

Each topic has two files:

- a **primer page** in `docs/<part>/`, budgeted at 400–800 words (hubs 1,200), mostly bullets, one
  diagram, at most one table, 3–5 sources, flashcards; and
- a **deep dive** in `docs/deep-dives/`, with the same `id` and `layer: deep-dive`, holding the
  provider survey, numbers, risk and controls, cloud mapping, variants and full sources.

Research is done once, into the deep dive; the primer is written from it. The README table of contents
lists primer pages and links each deep dive beside it. Flashcards come only from primer pages.
`scripts/primer.py check` enforces the budgets, table and link limits on primer pages, and checks that
every deep dive has a matching primer page.

## Consequences

- A topic reads in about ten minutes, like the original.
- Risk and controls tables (ADR 0005) and dated numbers (ADR 0006) still exist for every pattern, in
  the deep dive. Appendices 5.1, 5.2 and 5.4 aggregate from deep dives.
- Two files can drift apart. The review checklist asks whether they agree; the deep dive is the record.
- Solved designs (Part 4) stay single files at 1,500–2,500 words, like the original's solutions, and
  may have a deep dive for platform mappings.
