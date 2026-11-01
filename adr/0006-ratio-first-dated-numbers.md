# ADR 0006: Ratio-first, dated numbers

- Status: accepted
- Date: 2026-11-01

## Context

The original's "latency numbers every programmer should know" stay roughly true for years. AI prices
and speeds change every quarter, and no authoritative 2026 equivalent table exists.

## Decision

Teach durable ratios (cache read ≈ 0.1× input at one provider; agents ≈ 4× chat tokens) in sections.
Absolute prices and speeds live only in appendix 5.1, each with a source and an "as of" date, refreshed
quarterly. Derived arithmetic is labelled as derived and shows its working.

## Consequences

- Back-of-the-envelope estimates stay valid longer.
- 5.1 is a frontier artefact and is reviewed every quarter.

## Amendment (2026-11-01)

Under [ADR 0007](0007-primer-and-deep-dive.md) the Numbers table lives in the deep dive. A primer
page carries at most one headline number, with its source and date.
