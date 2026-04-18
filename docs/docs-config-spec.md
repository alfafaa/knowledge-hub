# Docs Config Specification

## Purpose

This document defines the repository-level configuration file that controls how project documentation syncs to the central company hub.

Use this spec for:

- folder-level sync defaults
- include and exclude rules
- visibility defaults
- publish targets
- approval behavior
- handling developer-authored public and internal docs from project repositories

The goal is simple:

- developers write docs in their own repos
- the central hub decides how those docs become discoverable and publishable
- admins and stakeholders read from the central hub, not from scattered repos

## File Name

Each participating repository should contain:

```text
docs/docs.config.yaml
```

## Why This File Exists

This file provides default behavior so developers do not need to manually annotate every document.

It answers:

- which folders are synced
- which folders are ignored
- which docs are mirrored or indexed only
- which docs may become public
- which docs always require approval
- where synced docs should land in the central hub

## Recommended Precedence

Use this resolution order:

1. central system policy
2. repository `docs.config.yaml`
3. document frontmatter
4. approval workflow

Meaning:

- central governance can forbid dangerous publishing
- repo config defines normal defaults
- document metadata can refine behavior
- approval can still block risky changes

## Recommended Top-Level Structure

```yaml
repo_type: service
repo_name: auth-service
docs_version: 1

defaults:
  sync_mode: indexed-only
  visibility: internal
  audience: engineering
  publish: false
  publish_targets:
    - engineering-site

sync:
  include: []
  exclude: []
  overrides: {}
  destinations: {}

approval:
  required_for:
    public: true
    restricted: true
    policy: true
    security_sensitive: true

ownership:
  default_owner: team-platform
  require_owner: true
```

## Field Definitions

### `repo_type`

Examples:

- `service`
- `frontend-app`
- `library`
- `platform`
- `internal-tool`

Use this for policy branching later if needed.

### `repo_name`

Stable repository identifier used for hub ingestion and reporting.

### `docs_version`

Version of the config schema.

### `defaults`

Defines fallback behavior for docs in this repository unless overridden.

Fields:

- `sync_mode`
- `visibility`
- `audience`
- `publish`
- `publish_targets`

### `sync.include`

List of glob patterns eligible for sync.

Example:

```yaml
sync:
  include:
    - "docs/02-architecture/**"
    - "docs/03-decisions/**"
    - "docs/05-operations/runbooks/**"
    - "docs/07-release/release-notes/**"
```

### `sync.exclude`

List of glob patterns excluded from sync even if they match include rules.

Example:

```yaml
sync:
  exclude:
    - "docs/**/drafts/**"
    - "docs/**/scratch/**"
    - "docs/01-getting-started/private/**"
```

### `sync.overrides`

Path-specific behavior overrides.

Example:

```yaml
sync:
  overrides:
    "docs/06-reference/api/**":
      sync_mode: mirrored
      publish: true
      publish_targets:
        - engineering-site
```

### `sync.destinations`

Defines where matched docs should land inside the central hub.

Use this when:

- one repository supports multiple products
- one repository contains multiple sub-projects
- different doc areas need different company-level destinations

Example:

```yaml
sync:
  destinations:
    "docs/02-architecture/**":
      hub_path: "hub/04-engineering/platform/auth-service/"
    "docs/11-guides/public/**":
      hub_path: "hub/06-support/public-kb/auth-service/"
    "docs/11-guides/internal/**":
      hub_path: "hub/06-support/internal-kb/auth-service/"
```

### `approval.required_for`

Defines which content classes require approval before hub publication.

Recommended defaults:

- all `public` content
- all `restricted` content
- policy documents
- security-sensitive docs

### `ownership`

Controls owner requirements.

Recommended defaults:

- `default_owner` should be set
- `require_owner: true`

## Supported Sync Behaviors

### `sync_mode`

Allowed values:

- `local-only`
- `indexed-only`
- `mirrored`

### Meaning

- `local-only`
  - stays in repo
- `indexed-only`
  - central hub stores metadata and source link
- `mirrored`
  - central hub copies and manages the content

## Include/Exclude Rules

Use these rules:

1. A file must match `include` to be considered syncable.
2. If it matches `exclude`, it is blocked from sync.
3. If a path matches `overrides`, the override behavior applies.
4. Document frontmatter may refine the result, but cannot break central policy.
5. If a path matches `destinations`, that mapping provides the default hub destination.

## Recommended Default Config

This is a good starting point for most backend or service repositories.

```yaml
repo_type: service
repo_name: sample-service
docs_version: 1

defaults:
  sync_mode: indexed-only
  visibility: internal
  audience: engineering
  publish: false
  publish_targets:
    - engineering-site

sync:
  include:
    - "docs/_index.md"
    - "docs/02-architecture/**"
    - "docs/03-decisions/**"
    - "docs/05-operations/**"
    - "docs/06-reference/**"
    - "docs/07-release/**"
    - "docs/09-knowledge/**"
  exclude:
    - "docs/**/drafts/**"
    - "docs/**/scratch/**"
    - "docs/01-getting-started/private/**"
    - "docs/90-archive/**"
  overrides:
    "docs/05-operations/security/**":
      sync_mode: indexed-only
      visibility: restricted
      publish: false
  destinations:
    "docs/02-architecture/**":
      hub_path: "hub/04-engineering/platform/sample-service/"
    "docs/03-decisions/**":
      hub_path: "hub/04-engineering/patterns/sample-service/"
    "docs/05-operations/runbooks/**":
      hub_path: "hub/04-engineering/shared-runbooks/sample-service/"
    "docs/11-guides/public/**":
      hub_path: "hub/06-support/public-kb/sample-service/"
    "docs/11-guides/internal/**":
      hub_path: "hub/06-support/internal-kb/sample-service/"

approval:
  required_for:
    public: true
    restricted: true
    policy: true
    security_sensitive: true

ownership:
  default_owner: team-sample
  require_owner: true
```

## Handling Developer-Written Public Or Internal Docs

Yes, developers can write public or internal guidelines and usage docs inside their own repositories.

That is a strong model, as long as publication is policy-driven.

Use this pattern:

- developers author the docs in their project repo
- repo config marks the folder as syncable
- frontmatter marks the audience and visibility
- central approval workflow decides whether it can publish
- central hub becomes the reading destination

This is exactly how you keep authorship close to the product while still giving the company one reading portal.

## Destination Routing For Multi-Project Repositories

This is essential for monorepos and shared repos.

Some repositories contain:

- multiple sub-projects
- multiple services
- multiple product areas

In that case, one repo should not have only one default destination.

Use destination mappings by path:

```yaml
sync:
  include:
    - "docs/subprojects/billing/**"
    - "docs/subprojects/auth/**"

  destinations:
    "docs/subprojects/billing/**":
      hub_path: "hub/03-projects/billing-modernization/"
      product: "billing"
      project: "billing-modernization"

    "docs/subprojects/auth/**":
      hub_path: "hub/03-projects/auth-unification/"
      product: "platform"
      project: "auth-unification"
```

This makes routing explicit instead of relying on repo-level guesswork.

## Recommended Destination Fields

Each destination mapping may define:

- `hub_path`
- `product`
- `project`
- `domain`
- `publish_targets`

For exceptional cases, allow document frontmatter such as:

```yaml
hub_path: hub/03-projects/payments-replatform/
product: payments
project: payments-replatform
```

Prefer config-based destination mapping over per-document overrides whenever possible.

## Recommended Folder Pattern For Audience-Specific Docs

If developers will maintain end-user or internal usage docs in the repository, define explicit folders in the repo template.

Example:

```text
docs/
  06-reference/
  07-release/
  11-guides/
    internal/
    public/
```

Recommended meaning:

- `11-guides/internal/`
  - internal operational or administrative guidance
- `11-guides/public/`
  - customer-facing usage, setup, and workflow docs

This is optional, but it becomes very useful when a product team owns both technical docs and usage guidance.

## Recommended Config For Public/Internal Guides

Example:

```yaml
sync:
  include:
    - "docs/11-guides/internal/**"
    - "docs/11-guides/public/**"

  overrides:
    "docs/11-guides/internal/**":
      sync_mode: mirrored
      visibility: internal
      audience: internal
      publish: true
      publish_targets:
        - internal-site

    "docs/11-guides/public/**":
      sync_mode: mirrored
      visibility: public
      audience: public
      publish: true
      publish_targets:
        - public-site
```

## Important Rule For Public Docs

Public docs should never publish automatically just because they are inside a `public/` folder.

Require all of these:

- path matches allowed public folder rules
- document status is `approved` or `active`
- owner exists
- required review fields exist
- approval workflow passes

This protects against accidental public exposure.

## Suggested Frontmatter For Public/Internal Guides

### Internal guide

```yaml
---
title: Support Workflow For Failed Payments
type: guide
audience: internal
visibility: internal
status: approved
publish: true
publish_targets:
  - internal-site
owner: team-payments
last_reviewed: 2026-03-30
review_cycle_days: 180
---
```

### Public guide

```yaml
---
title: How To Retry A Failed Payment
type: guide
audience: public
visibility: public
status: approved
publish: true
publish_targets:
  - public-site
owner: team-payments
last_reviewed: 2026-03-30
review_cycle_days: 90
---
```

## Admin And Team Member Reading Model

This is the intended user experience:

- developers write in repositories
- hub sync brings approved docs into central navigation
- admins read workflow and policy-relevant docs from the hub
- internal team members read internal guidelines from the hub
- customers read approved public docs from the public hub

So yes, the central place becomes the reading interface, while repositories remain the writing interface.

## Recommended Path Strategy For The Hub

When mirrored into the hub:

```text
hub/content/repos/<repo-slug>/<source-doc-path>.md
```

When promoted into curated audience spaces:

```text
hub/06-support/public-kb/<product-slug>/...
hub/06-support/internal-kb/<team-or-domain>/...
hub/04-engineering/patterns/...
```

This gives you both provenance and readable information architecture.

## Best-Practice Rules

1. Use repo config for folder-level policy.
2. Use frontmatter for document-level exceptions.
3. Require approval for public or restricted docs.
4. Keep developers writing where they build.
5. Keep admins and readers consuming from the central hub.
6. Do not make teams maintain the same document in two places.

## Final Recommendation

Yes, use config to define which folders or files should sync and which should not.

And yes, developers can absolutely author public and internal guidance from their own repositories.

The safe long-term model is:

- write in repo
- control with config
- refine with metadata
- approve when sensitive
- read from the hub
