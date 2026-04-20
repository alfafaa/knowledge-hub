---
title: System Design Template
type: guide
status: draft
publish: false
---

# System Design Template

Use this as the starting point for `docs/02-architecture/system-design.md`.

Recommended frontmatter for a real system design page:

```yaml
---
title: System Design
type: reference
status: approved
owner: team-name
publish: true
audience: engineering
visibility: internal
publish_targets:
  - engineering-site
---
```

## Purpose

What system is being described and why does this page exist?

## Scope

What is in scope and what is out of scope?

## Components

- component 1
- component 2
- component 3

## Data Flow

Describe the important flows through the system.

## Boundaries

Explain ownership boundaries, external dependencies, and trust boundaries.

## Operational Notes

Add deployment, scale, resilience, or observability considerations that matter to engineers.

## Related Docs

Link to:

- ADRs
- RFCs
- runbooks
- reference pages
