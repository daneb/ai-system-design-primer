# ADR 0008: Licences

- Status: accepted
- Date: 2026-11-02

## Context

The primer is meant to be read, copied into internal wikis, translated and adapted, like the
original System Design Primer, which is licensed CC BY 4.0. It also contains code: the lab scripts,
`scripts/` and the CI workflow. Content licences are a poor fit for code, and code licences are a poor
fit for prose.

## Decision

- **Content** (everything outside `scripts/`, `labs/**/*.py` and `.github/`): Creative Commons
  Attribution 4.0 International (CC BY 4.0), in [LICENSE](../LICENSE).
- **Code** (`scripts/`, `labs/**/*.py`, `.github/`): MIT, in [LICENSE-CODE](../LICENSE-CODE).
- Contributions are accepted under the same licences (stated in the pull request template).

## Consequences

- Anyone may reuse, adapt and redistribute, including commercially, with attribution.
- A share-alike licence (CC BY-SA 4.0) was rejected: it would stop companies adapting the primer
  into internal standards, which is one of its intended uses.
- Third-party material quoted in pages stays under its own licence; quotes are kept short and cited.
