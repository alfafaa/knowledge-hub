# Access Control And Role-Based Publishing

## Purpose

This document defines how user-based and role-based access should work in the centralized knowledge hub.

It answers:

- how to control access to specific docs or folders
- how metadata should express access intent
- how the sync pipeline should enforce policy
- how public, internal, engineering, and admin content should be delivered
- how to avoid relying on folders alone for security

## Core Principle

Do not treat folders as the real security boundary.

Folders are useful for:

- organization
- default publishing rules
- sync policies

Folders are not enough for:

- real authorization
- sensitive document protection
- role-based access enforcement

Real access control must be enforced in the delivery layer.

## The Three-Layer Access Model

Use these three layers together.

### 1. Metadata Layer

Each document declares its intended visibility and audience.

Example:

```yaml
---
title: Budget Approval Workflow
visibility: restricted
audience: admin
access_groups:
  - finance
  - leadership
access_level: confidential
publish: true
publish_targets:
  - admin-site
owner: finance-team
status: approved
last_reviewed: 2026-04-03
review_cycle_days: 90
---
```

This is the policy declaration layer.

### 2. Sync And Publishing Layer

The sync engine reads metadata and config, then decides:

- whether the doc can sync
- whether it is mirrored or indexed only
- which site it belongs to
- whether approval is required

This is the policy enforcement layer.

### 3. Delivery Layer

The final site or portal enforces actual user access.

Examples:

- public site: open access
- internal site: SSO required
- engineering site: only engineering group
- admin site: only finance, leadership, or admin groups

This is the real authorization layer.

## Why Folder-Based Access Is Not Enough

You can organize content like this:

```text
11-guides/public/
11-guides/internal/
11-guides/engineering/
```

That is useful for structure, but not for strong security.

Why:

- files can be misclassified
- folders do not validate identity
- static hosting does not know user roles by itself
- some documents in the same folder may still need different restrictions

So the correct model is:

- folder = organization
- metadata = policy
- site/auth layer = real access control

## Recommended Access Fields

Add these fields to the frontmatter schema for any controlled content.

```yaml
visibility: public | internal | restricted
audience: public | internal | engineering | admin
access_groups:
  - group-name
access_level: standard | sensitive | confidential
publish_targets:
  - public-site
  - internal-site
```

## Field Meanings

### `visibility`

- `public`
  - content may be published openly
- `internal`
  - content is only for authenticated internal users
- `restricted`
  - content is only for named roles or groups

### `audience`

Primary intended reader group.

Recommended values:

- `public`
- `internal`
- `engineering`
- `admin`

### `access_groups`

Explicit identity groups allowed to access the content.

Examples:

- `engineering`
- `support`
- `finance`
- `leadership`
- `product`
- `admin`

### `access_level`

Optional sensitivity indicator.

Recommended values:

- `standard`
- `sensitive`
- `confidential`

## Recommended Role Model

Start with clear group names rather than overly fine-grained permissions.

Recommended base groups:

- `public`
- `employee`
- `engineering`
- `product`
- `support`
- `operations`
- `marketing`
- `sales`
- `finance`
- `leadership`
- `admin`

You can then allow combinations per document.

Example:

```yaml
access_groups:
  - finance
  - leadership
```

## Recommended Site Separation Strategy

For Quartz and static publishing, the safest model is separate audience-targeted sites.

Recommended outputs:

- `public-site`
- `internal-site`
- `engineering-site`
- `admin-site`

### `public-site`

Contains:

- public docs
- public guides
- selected release notes
- public product help content

Access:

- open access

### `internal-site`

Contains:

- internal company docs
- company processes
- product context
- internal support guides

Access:

- authenticated employees

### `engineering-site`

Contains:

- engineering standards
- ADRs
- RFCs
- runbooks
- internal technical docs

Access:

- authenticated users in engineering-related groups

### `admin-site`

Contains:

- finance docs
- leadership docs
- restricted operational workflows
- legal or commercial sensitive content

Access:

- only allowed admin-related groups

## Why Separate Sites Are Recommended

This is simpler and safer than one giant site with mixed access paths.

Benefits:

- clearer isolation
- easier caching and hosting
- easier group-based protection
- lower risk of accidental public exposure

Trade-off:

- multiple site builds and deployments

That trade-off is usually worth it.

## Alternative: One Portal With Protected Sections

This is possible, but more complex.

Example:

```text
/public/
/internal/
/engineering/
/admin/
```

This requires:

- auth-aware routing
- middleware or proxy-based authorization
- careful cache and search separation

For static Quartz publishing, this is less attractive than separate builds.

## Recommended Policy Resolution

When deciding access, use this precedence:

1. central governance policy
2. site-level publishing rules
3. repo `docs.config.yaml`
4. document frontmatter
5. approval workflow

Meaning:

- a repo cannot force a public publish if central policy forbids it
- a document cannot bypass restricted access rules
- approval can still block publication

## Folder-Level Defaults

Folders can still provide useful defaults.

Example:

```yaml
sync:
  overrides:
    "docs/11-guides/public/**":
      visibility: public
      audience: public
      publish_targets:
        - public-site

    "docs/11-guides/internal/**":
      visibility: internal
      audience: internal
      publish_targets:
        - internal-site

    "docs/11-guides/engineering/**":
      visibility: internal
      audience: engineering
      publish_targets:
        - engineering-site
```

This is useful, but individual docs may still specify:

- narrower access groups
- different approval requirements
- restricted classification

## Example Access Scenarios

### Scenario 1: Public Product Guide

```yaml
visibility: public
audience: public
access_groups: []
publish_targets:
  - public-site
```

Delivery:

- public site, no login

### Scenario 2: Internal Support Workflow

```yaml
visibility: internal
audience: internal
access_groups:
  - support
  - operations
publish_targets:
  - internal-site
```

Delivery:

- internal site behind employee SSO
- optional route/group filtering if needed

### Scenario 3: Engineering Runbook

```yaml
visibility: internal
audience: engineering
access_groups:
  - engineering
  - operations
publish_targets:
  - engineering-site
```

Delivery:

- engineering site behind SSO group checks

### Scenario 4: Finance Approval Procedure

```yaml
visibility: restricted
audience: admin
access_groups:
  - finance
  - leadership
access_level: confidential
publish_targets:
  - admin-site
```

Delivery:

- restricted admin site behind group checks

## Approval Rules

Recommended mandatory approval cases:

- any `public` content
- any `restricted` content
- any `confidential` content
- policy documents
- security-sensitive docs
- legal or finance documents

## Search And Indexing Considerations

Access control must apply to search too.

Important rules:

- public search indexes must never include internal or restricted content
- engineering search indexes should not include admin-only content
- internal search must respect authorization boundaries

This is another reason separate site builds work well.

## How To Give Access To Specific Folders

If you want “folder access” in practice, implement it like this:

1. assign default metadata rules to that folder in `docs.config.yaml`
2. route matching docs to a specific publish target
3. protect that target site with SSO group rules

Example:

- all docs in `docs/11-guides/internal/admin/**`
  - route to `admin-site`
  - require groups `admin`, `leadership`

This gives folder-like access control, but enforced through the pipeline and delivery layer.

## Best Long-Term Recommendation

Use this model:

- folder structure for organization
- frontmatter for access policy
- repo config for defaults
- sync pipeline for routing
- SSO/group checks for real authorization

That is the scalable, future-proof approach for a company knowledge hub.
