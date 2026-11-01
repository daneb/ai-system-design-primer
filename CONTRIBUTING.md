# Contributing

## Writing a section

Read [STYLE.md](STYLE.md) first: it sets the audience, voice, length budgets and research method.


1. Pick an item from [ROADMAP.md](ROADMAP.md), or a section from [PLAN.md](PLAN.md). Section stubs already exist under `docs/`.
2. Research into a deep dive first: copy [templates/deep-dive.md](templates/deep-dive.md) to
   `docs/deep-dives/<id>-<slug>.md`. Then write the primer page from
   [templates/section.md](templates/section.md) into the stub (or
   [templates/solved-design.md](templates/solved-design.md) for Part 4). Keep the stub's `id`, `title`,
   `phase` and `maturity`. See [ADR 0007](adr/0007-primer-and-deep-dive.md).
3. Set `status: draft`, `owner`, `last_verified` (the day you checked the sources) and `review_by`:
   - `stable`: within 12 months
   - `mixed`: within 6 months
   - `frontier` / `speculative`: within 3 months
4. Run the checks:
   ```sh
   python3 scripts/primer.py check
   python3 scripts/primer.py readme
   python3 scripts/primer.py flashcards
   ```

## Rules for content

- **Primary sources first.** Cite the paper, spec, or vendor engineering post, not a summary of it.
  If only a secondary source is available, say so in the citation.
- **Every number carries a source and an "as of" date.** Prefer ratios (cache read ≈ 0.1× input) to
  absolute prices. Derived arithmetic is labelled "derived" and shows its working.
- **No product names in primer prose.** Products go in the deep dive's Cloud mapping table and
  [5.2](docs/5-appendix/5.2-cloud-mapping.md).
- **Paraphrase.** Summarise sources in your own words; quote only short phrases where the exact wording
  matters.
- **Diagrams as text.** Mermaid inline, or Excalidraw files committed next to the section.
- **Flashcards.** 3–6 cards per primer page, in the form:
  ```
  Q: What three capabilities make up the lethal trifecta?
  A: Access to private data, exposure to untrusted content, and a way to communicate externally.
  ```
  A question and its answer are separated by a newline; cards are separated by a blank line.

## Reviewing an overdue section

When CI reports an overdue review, re-check each source and number, update or remove what has moved,
add a line to the changelog in [5.6](docs/5-appendix/5.6-glossary.md) if anything material changed,
and bump `last_verified` and `review_by`.
