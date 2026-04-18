
1# Documentation Standards

## Writing Goals

Documentation should be:

- easy to scan
- easy to update
- easy to trust
- easy to publish automatically

If a page cannot be classified by owner, audience, and lifecycle, it is not ready for the hub.

## Frontmatter Standard

Use a tiered frontmatter model.

That means:

- all docs should carry minimal structure
- publishable docs need stronger metadata
- public and restricted docs need the strongest governance metadata

This keeps authoring lighter for employees while keeping published documentation safe and traceable.

```yaml
---
id: auth-session-rotation
title: Session Rotation Strategy
type: standard
domain: engineering
product: platform
project: auth-service
audience: engineering
visibility: internal
status: approved
owner: team-platform
reviewers:
  - lead-platform
tags:
  - auth
  - sessions
  - security
source_repo: github.com/alfafaa/auth-service
source_path: docs/architecture/session-rotation.md
publish: true
publish_targets:
  - engineering-site
last_reviewed: 2026-03-30
review_cycle_days: 180
version: 1.0
supersedes: []
related:
  - adr-012-session-invalidation
summary: How session rotation works across services.
---
```

## Required Fields

### Tier 1: Required For All Docs

- `title`
- `type`
- `status`

### Tier 2: Required For Publishable Docs

Require these when `publish: true`:

- `owner`
- `publish`
- `audience`
- `visibility`
- `publish_targets`

### Tier 3: Required For Governed Docs

Require these when a doc is both publishable and `public` or `restricted`:

- `last_reviewed`
- `review_cycle_days`

## Optional But Useful Fields

- `id`
- `summary`
- `product`
- `project`
- `access_groups`
- `access_level`

These should be added when they provide value, but they should not be mandatory for every simple internal draft.

## Recommended Enumerations

### `type`

- `policy`
- `standard`
- `guide`
- `runbook`
- `reference`
- `adr`
- `rfc`
- `prd`
- `faq`
- `postmortem`
- `release-note`
- `glossary`

### `status`

- `draft`
- `review`
- `approved`
- `active`
- `deprecated`
- `archived`

### `visibility`

- `public`
- `internal`
- `restricted`

## Naming Conventions

Use stable, descriptive filenames.

Good:

- `session-rotation.md`
- `deploy-runbook.md`
- `adr-012-use-event-bus.md`
- `prd-billing-reconciliation.md`

Avoid:

- `final-doc.md`
- `new architecture latest.md`
- `notes1.md`

## Folder Naming Rules

- Use lowercase kebab-case for directories and files.
- Use singular nouns for page types where possible.
- Keep folder semantics stable.
- Do not encode dates in folder names unless the folder is archival.

## Structure Rules

Use a three-level discipline:

- Level 1: globally standardized across the company
- Level 2: standardized by domain or repo type
- Level 3+: flexible, based on real usage

This is the safest way to stay organized without freezing future evolution.

## Mandatory vs Optional Folders

Do not require every repo to contain every possible doc category.

Use these labels in standards and templates:

- `mandatory`
  - must exist in all repos of that type
- `recommended`
  - should exist when the repo has that kind of work
- `optional`
  - create only when needed

Example:

- `02-architecture/` is usually `mandatory`
- `08-quality/testing/` may be `recommended`
- `10-integrations/` is often `optional`

## ADR Naming Standard

```text
adr-001-use-postgres.md
adr-002-introduce-event-bus.md
adr-003-split-auth-service.md
```

ADR pages should include:

- context
- decision
- consequences
- alternatives considered
- links to follow-up work

## RFC Naming Standard

```text
rfc-001-observability-pipeline.md
rfc-002-tenant-isolation.md
```

RFC pages should include:

- problem
- goals
- non-goals
- proposal
- trade-offs
- rollout plan

## Product and Project Index Pages

Each product or project folder should contain an `_index.md` page that answers:

- what this thing is
- who owns it
- which repos are involved
- where the key docs live
- what its current status is

This prevents the common problem where folders become graves of disconnected markdown files.

## What Should Not Be Forced Into Every Engineering Repo

These are useful topics, but they should be conditional rather than universal:

- personas
- stakeholder communication logs
- business strategy notes
- leadership notes
- broad research repositories

Those fit better in the central hub unless the repository itself is the primary owner.

## Tagging Guidelines

Use tags for secondary classification, not primary organization.

Recommended tag families:

- domain tags
  - `domain/engineering`
  - `domain/product`
- system tags
  - `system/auth`
  - `system/billing`
- lifecycle tags
  - `lifecycle/active`
  - `lifecycle/deprecated`
- audience tags
  - `audience/public`
  - `audience/engineering`

Do not create free-form tag sprawl. Maintain an approved tag catalog in governance docs.

## Authoring Guidelines

Prefer this page structure:

## Asset Link Validation

Local asset references should be valid before publish/build.

The validator now checks linked local non-Markdown assets such as:

- images
- SVG diagrams
- PDFs
- other linked binary files

Validation rule:

- publishable docs: broken local asset links are `error`
- non-publishable docs: broken local asset links are `warning`

This is the right tradeoff:

- local drafts stay flexible
- broken published docs are blocked early

Best practice:

- keep repo-level media under `docs/98-meta/assets/` by default
- use relative links
- use page-near asset folders only when one page owns the media tightly

```markdown
# Title

## Purpose
Why this page exists.

## Scope
What it covers and what it does not.

## Background
Only the minimum context required.

## Main Content
The decision, guide, reference, or runbook itself.

## Risks or Trade-offs
What can go wrong, or what was intentionally not chosen.

## Related Documents
Links to ADRs, PRDs, specs, tickets, dashboards, or repos.
```

## Validation Principle

The rule should be:

- easy to write
- strict to publish

Do not force every employee note to be production-grade at creation time.

## Writing Rules

- One page should answer one primary question.
- Put the answer early.
- Prefer examples over abstract explanation.
- Separate decisions from discussion notes.
- Move unstable brainstorming into RFCs or working notes, not standards.
- If a page contains operational steps, include rollback or failure handling.

## Review and Lifecycle Rules

- `draft`: not publishable to broad audiences
- `review`: awaiting approval
- `approved` or `active`: publishable
- `deprecated`: still visible but replaced
- `archived`: removed from active navigation

Every page should have a review cadence:

- 90 days for operational and security docs
- 180 days for standards and product docs
- 365 days for stable reference and historical material

## Traceability Rules

Every important page should link to at least one of:

- a repository
- an ADR or RFC
- an issue or ticket
- a dashboard or service
- a parent product or project page

If a document changes company behavior, it should leave a traceable decision record.
