# Sync Model: Project Repositories To Company Hub

## Purpose

This document defines how documentation should move from project repositories into the central company knowledge hub.

It answers:

- what should sync
- what should stay local
- what should be mirrored vs indexed only
- how publishing targets should work
- how synced docs should resolve destination paths in the hub
- how to avoid duplication and confusion

## Core Model

The correct model is:

- project repositories are the authoring source for implementation-coupled documentation
- the company hub is the aggregation, governance, discovery, and publishing layer
- publishing is controlled by metadata and policy

This means project docs do push into the company hub, but not as a full uncontrolled copy.

## Three Sync Modes

Use these three modes for all project documentation.

### 1. Local Only

The document stays in the project repository and is not mirrored into the company hub content tree.

Use this for:

- scratch notes
- temporary work-in-progress docs
- local setup details that are not useful outside the repo
- draft implementation notes
- highly sensitive documents not approved for hub ingestion

### 2. Indexed Only

The company hub knows the document exists, stores metadata about it, and can link to the source, but does not mirror the content as a managed hub page.

Use this for:

- low-value or highly repo-specific reference material
- docs that should be discoverable but not duplicated
- large generated references where linking is better than copying
- internal-only docs that should remain source-native

Think of this as a library catalog card, not a copied book.

### 3. Mirrored

The document content is copied or normalized into the company hub and becomes part of central navigation, governance, and publishing.

Use this for:

- approved architecture summaries
- ADRs and RFCs worth central discoverability
- shared runbooks
- troubleshooting guides
- release notes
- public-facing documentation
- reusable knowledge and cross-team references

This is the default for high-value documents with cross-team usefulness.

## Decision Table

| Document type | Default sync mode | Notes |
|---|---|---|
| ADR | Mirrored | high long-term value |
| RFC | Mirrored | useful for cross-team planning and review |
| runbook | Mirrored or Indexed Only | depends on sensitivity and reuse |
| service-specific setup note | Local Only | usually too local |
| architecture summary | Mirrored | especially if multiple teams depend on it |
| low-level generated API spec | Indexed Only or Mirrored | depends on publishing needs |
| public user guide | Mirrored | candidate for public site |
| troubleshooting guide | Mirrored | useful for support and engineering |
| scratch planning doc | Local Only | should not pollute hub |
| release note | Mirrored | often useful centrally |
| postmortem | Mirrored or Indexed Only | depends on sensitivity |

## Metadata Rules

These fields control sync behavior.

```yaml
---
publish: true
sync_mode: mirrored
audience: engineering
visibility: internal
status: approved
publish_targets:
  - engineering-site
source_repo: github.com/example/repo
source_path: docs/03-decisions/adr-001-use-postgres.md
owner: team-platform
last_reviewed: 2026-03-30
review_cycle_days: 180
---
```

## Required Sync Fields

- `publish`
- `audience`
- `visibility`
- `status`
- `owner`

## Recommended Sync Fields

- `sync_mode`
- `publish_targets`
- `source_repo`
- `source_path`
- `summary`

## `sync_mode` Values

- `local-only`
- `indexed-only`
- `mirrored`

If `sync_mode` is missing, use policy defaults by document type.

## Practical Sync Rules

### Rule 1: Draft docs should not publish broadly

If:

- `status: draft`

Then:

- do not publish to public or broad internal destinations

### Rule 2: Mirroring requires stable ownership

If:

- `sync_mode: mirrored`

Then require:

- `owner`
- `last_reviewed`
- valid `visibility`

### Rule 3: Public publishing requires explicit intent

If:

- `visibility: public`

Then require:

- `publish: true`
- approved status
- a public publish target

### Rule 4: Restricted docs should never auto-publish

If:

- `visibility: restricted`

Then:

- require approval workflow
- avoid public mirroring

## Recommended Hub Ingestion Paths

When mirrored, preserve provenance.

Recommended path pattern:

```text
hub/content/repos/<repo-slug>/<source-doc-path>.md
```

Examples:

```text
hub/content/repos/auth-service/docs/03-decisions/adr-001-use-postgres.md
hub/content/repos/billing-api/docs/05-operations/runbooks/payment-recovery.md
```

Do not flatten all mirrored docs into one directory. That destroys context.

## Destination Path Resolution

Mirroring should not depend on guesswork.

Every synced document should resolve its destination in one of these ways:

1. explicit document frontmatter destination
2. repository `docs.config.yaml` destination mapping
3. system fallback path

Recommended frontmatter fields:

- `hub_path`
- `product`
- `project`

Recommended repo config section:

```yaml
sync:
  destinations:
    "docs/03-decisions/**":
      hub_path: "hub/04-engineering/patterns/auth-service/"
    "docs/subprojects/billing/**":
      hub_path: "hub/03-projects/billing-modernization/"
      product: "billing"
      project: "billing-modernization"
```

This is essential for monorepos and multi-project repositories.

## Multi-Project Repository Model

If one repository contains several sub-projects, each sub-project can route to a different company-level destination.

Example:

```text
repo/
  docs/
    subprojects/
      billing/
      auth/
      admin-portal/
```

Then route them independently:

```yaml
sync:
  destinations:
    "docs/subprojects/billing/**":
      hub_path: "hub/03-projects/billing-upgrade/"
    "docs/subprojects/auth/**":
      hub_path: "hub/03-projects/auth-unification/"
    "docs/subprojects/admin-portal/**":
      hub_path: "hub/02-products/admin-portal/"
```

That preserves local authorship without losing central structure.

## Central Views Built From Synced Docs

The company hub should generate higher-level views from mirrored or indexed docs.

Examples:

- engineering ADR catalog
- product release notes index
- support troubleshooting index
- owner-based review dashboard
- security-sensitive docs queue
- stale-doc report

This is why syncing matters. The hub is not just storage. It is a knowledge control plane.

## Mirror vs Index Guidelines

### Mirror when:

- the doc is reused across teams
- the doc should appear in central navigation
- the doc is part of a published site
- governance and review workflows should apply centrally

### Index only when:

- the doc is useful to find but not to duplicate
- the source format is generated or large
- the content should remain repo-native
- syncing full content adds little value

### Keep local only when:

- the document is unstable
- the audience is too narrow
- the content is temporary
- the content should not leave the repo

## What Usually Pushes To The Company Hub

These usually deserve mirroring or at least indexing:

- `_index.md`
- architecture summaries
- ADRs
- RFCs
- runbooks
- troubleshooting guides
- release notes
- API overviews
- onboarding docs useful beyond the repo
- lessons learned and playbooks

## What Usually Stays In The Repo

These usually stay local unless there is a strong reason to centralize them:

- local dev shortcuts
- temporary migration notes
- engineer scratch documents
- incomplete feature plans
- narrow environment-specific notes

## Publishing Targets

Use explicit publish targets instead of assuming one destination.

Common targets:

- `public-site`
- `internal-site`
- `engineering-site`

Examples:

### Internal engineering doc

```yaml
publish: true
sync_mode: mirrored
audience: engineering
visibility: internal
publish_targets:
  - engineering-site
```

### Public guide

```yaml
publish: true
sync_mode: mirrored
audience: public
visibility: public
publish_targets:
  - public-site
```

### Discoverable but not mirrored

```yaml
publish: false
sync_mode: indexed-only
audience: engineering
visibility: internal
```

## How This Prevents Confusion

Without this model, teams fall into one of two bad patterns:

1. copy everything to the central hub and create duplication rot
2. keep everything inside repos and lose discoverability

This sync model avoids both:

- repos remain the writing home for technical docs
- the hub becomes the discovery and publishing home
- metadata decides the movement

## Recommended Automation Flow

1. Developer updates docs in the project repository.
2. PR checks validate structure, metadata, and links.
3. Merge to main triggers sync logic.
4. Sync logic reads `sync_mode`, `publish`, `visibility`, and `publish_targets`.
5. Document is handled as local-only, indexed-only, or mirrored.
6. Central hub rebuilds indexes and Quartz outputs.

## Final Recommendation

Yes, project-level docs should push to the company hub.

But the correct rule is:

- write locally
- sync selectively
- mirror intentionally
- publish by metadata

That gives you one company source of truth without forcing engineers to maintain documentation in two places.
