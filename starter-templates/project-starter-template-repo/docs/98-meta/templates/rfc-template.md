---
title: Rfc Template
type: guide
status: draft
publish: false
---

# RFC Template

Copy this into `docs/03-decisions/rfc/rfc-<number>-<slug>.md` when a proposal needs review before implementation.

Recommended frontmatter for a real RFC:

```yaml
---
title: RFC - Introduce Queue-Based Retry Pipeline
type: rfc
status: review
owner: team-billing
publish: true
audience: engineering
visibility: internal
publish_targets:
  - engineering-site
---
```

## Problem

Describe the current problem and why existing behavior is insufficient.

## Goals

- goal 1
- goal 2

## Non-Goals

- non-goal 1
- non-goal 2

## Proposal

Describe the proposed approach.

## Trade-Offs

Explain what becomes better and what becomes more complex.

## Rollout Plan

Describe sequencing, migration, and validation.

## Open Questions

List anything that still needs review or confirmation.
