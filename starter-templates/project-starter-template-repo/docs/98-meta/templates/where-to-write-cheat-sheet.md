---
title: Where To Write Cheat Sheet
type: standard
status: draft
publish: false
---

# Where To Write Cheat Sheet

Use this when someone asks:

- where should I put this doc?
- should this be architecture, decision, feature work, or guide content?

## Quick Routing Rules

- current system explanation -> `02-architecture/`
- why a decision was made -> `03-decisions/`
- large feature implementation work -> `04-development/features/`
- how to operate or recover the system -> `05-operations/`
- stable API, config, or database facts -> `06-reference/`
- release history -> `07-release/`
- troubleshooting and reusable lessons -> `09-knowledge/`
- audience-facing usage docs -> `11-guides/`
- shared assets and doc support files -> `98-meta/`

If the content is broad business or roadmap planning, it usually belongs in the central hub, not this repo.

## Common Cases

Use:

- `00-overview/`
  - what the project is, why it exists, glossary, repo map
- `01-getting-started/`
  - setup, install, local bootstrap, quick start
- `02-architecture/`
  - current technical shape of the system
- `02-architecture/research/`
  - technical option analysis before a decision is finalized
- `03-decisions/adr/`
  - architecture or engineering decisions that were made
- `03-decisions/rfc/`
  - proposals still being discussed or reviewed
- `04-development/features/<feature-name>/`
  - feature-specific implementation planning for large work
- `04-development/patterns/`
  - reusable project-specific engineering patterns
- `05-operations/runbooks/`
  - incident recovery and operational procedures
- `06-reference/`
  - stable facts such as API, config, database reference
- `07-release/release-notes/`
  - release summaries and changes over time
- `09-knowledge/troubleshooting/`
  - recurring issues and fixes
- `11-guides/public/`
  - customer-facing or end-user docs
- `11-guides/internal/`
  - internal admin, support, operations, workflow docs
- `11-guides/engineering/`
  - contributor or service-consumer guidance

## Decision Shortcuts

If you are unsure, use this test:

- explains current system state -> `02-architecture/`
- records why a choice was made -> `03-decisions/`
- helps build one feature -> `04-development/features/`
- helps operate the system -> `05-operations/`
- helps someone use the system -> `11-guides/`
- stores reusable supporting material -> `98-meta/`

## What Not To Put In This Repo

- broad company strategy
- product roadmap
- stakeholder planning
- general market research
- unrelated meeting notes

Those belong in the central hub, not in project-level docs.
