# ADR 0004: Flashcards generated from sections

- Status: accepted
- Date: 2026-11-01

## Context

The original ships three hand-built Anki decks that drift from the text. None of the surveyed AI
resources offers flashcards.

## Decision

Each section ends with a `## Flashcards` block of `Q:` / `A:` pairs. `scripts/primer.py flashcards`
exports them to `build/flashcards.tsv`, which Anki imports directly. Cards are tagged with the section id
and its maturity so learners can suspend frontier cards when they are rewritten. Standard library only;
no `genanki` dependency.

## Consequences

- Cards stay in step with the text because they live next to it.
- Plain-text import loses Anki note types and media. Acceptable for now.
