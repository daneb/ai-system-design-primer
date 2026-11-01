# ADR 0005: A risk and controls block in every pattern

- Status: accepted
- Date: 2026-11-01

## Context

Governance frameworks (OWASP LLM Top 10, OWASP Agentic Top 10, FINOS AI Governance Framework, EU AI
Act) sit apart from design catalogues. Architects in regulated industries have to do the mapping
themselves.

## Decision

Every pattern includes a "Risk and controls" table: the risk, the framework reference, the
control, and the evidence an auditor would ask for. Appendix 5.4 aggregates these into a crosswalk.

## Consequences

- The primer becomes usable by architecture and model-risk review boards, not only for interviews.
- References must cite stable identifiers (for example OWASP LLM06) and be re-verified when frameworks
  release new editions.

## Amendment (2026-11-01)

Under [ADR 0007](0007-primer-and-deep-dive.md) the table lives in the pattern's deep dive, not its
primer page.
