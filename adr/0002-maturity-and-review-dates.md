# ADR 0002: Maturity tags and review dates, enforced by CI

- Status: accepted
- Date: 2026-11-01

## Context

The original primer went stale silently. Its decay shows only through broken links and admissions such
as "could use some updates". AI patterns change far faster than load balancers.

## Decision

Every section carries `maturity` (`stable`, `mixed`, `frontier`, `speculative`), `last_verified`,
`review_by` and `owner`. The maximum review interval depends on maturity: 12 months for stable,
6 for mixed, 3 for frontier and speculative. `scripts/primer.py check` fails when `review_by` has passed
or the interval is exceeded. CI also runs weekly, so a review goes red without anyone pushing.

## Consequences

- Readers can tell how much to trust a section.
- The maintainer gets a forcing function. The cost is a steady review load, which is kept small by
  keeping frontier sections short.
- A changelog (in 5.6) records what moved; the churn itself becomes teaching material.
