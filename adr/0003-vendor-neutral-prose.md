# ADR 0003: Vendor-neutral prose, products only in mappings

- Status: accepted
- Date: 2026-11-01

## Context

Product names and features change far faster than concepts. Vendor catalogues (Azure, AWS, Google) are
good but each covers only its own services.

## Decision

Section prose names concepts (gateway, router, prefix cache). Product and service names appear only in a
section's "Cloud mapping" table and in appendix 5.2.

## Consequences

- Most churn is concentrated in a few tables that are easy to review.
- Readers working on Azure or Bedrock still get a direct mapping.
- Mappings must come from first-party documentation (none were verified by the feasibility study).
