# Sync Resolution Rules And Path Mapping

## Purpose

This document defines exactly how repository documentation paths should map into the central company hub.

It answers:

- how full folders are pushed
- how sub-project routing works
- how one local repo can map into a deeper hub path
- how multiple mapping rules are resolved
- how to preserve relative structure safely

## Core Principle

The local repository structure does not need to match the central hub structure.

The sync engine is responsible for:

- reading the source path
- matching routing rules
- resolving the destination path
- preserving the correct relative subtree

This is what makes the system flexible.

## Basic Path Mapping Rule

For any synced file:

1. identify the source rule that matched
2. remove the matched source root prefix
3. append the remaining relative path to the destination `hub_path`

Formula:

```text
destination = hub_path + relative_path_after_matched_prefix
```

## Example: Full Docs Folder To One Sub-Project

Local repository:

```text
docs/
  _index.md
  02-architecture/system-design.md
  03-decisions/adr-001-use-postgres.md
  11-guides/public/getting-started/overview.md
```

Config:

```yaml
sync:
  include:
    - "docs/**"

  destinations:
    "docs/**":
      hub_path: "hub/03-projects/billing-modernization/"
      product: "billing"
      project: "billing-modernization"
```

Results:

```text
docs/_index.md
-> hub/03-projects/billing-modernization/_index.md

docs/02-architecture/system-design.md
-> hub/03-projects/billing-modernization/02-architecture/system-design.md

docs/11-guides/public/getting-started/overview.md
-> hub/03-projects/billing-modernization/11-guides/public/getting-started/overview.md
```

This is the correct way to push one whole docs tree under a sub-project in the company hub.

## Example: Full Subtree Push

Local repository:

```text
docs/
  subprojects/
    billing/
      _index.md
      02-architecture/system-design.md
      03-decisions/adr-001.md
```

Config:

```yaml
sync:
  include:
    - "docs/subprojects/billing/**"

  destinations:
    "docs/subprojects/billing/**":
      hub_path: "hub/03-projects/billing-modernization/"
```

Results:

```text
docs/subprojects/billing/_index.md
-> hub/03-projects/billing-modernization/_index.md

docs/subprojects/billing/02-architecture/system-design.md
-> hub/03-projects/billing-modernization/02-architecture/system-design.md
```

The matched prefix is:

```text
docs/subprojects/billing/
```

Everything after that is preserved.

## Example: One Local Repo, One Local Docs Tree, Deeper Hub Destination

This is a common case.

Local repository:

```text
docs/
  _index.md
  05-operations/runbooks/payment-recovery.md
```

Config:

```yaml
sync:
  include:
    - "docs/**"

  destinations:
    "docs/**":
      hub_path: "hub/02-products/payments/subprojects/reconciliation-engine/"
```

Result:

```text
docs/05-operations/runbooks/payment-recovery.md
-> hub/02-products/payments/subprojects/reconciliation-engine/05-operations/runbooks/payment-recovery.md
```

So yes, a simple local docs tree can be pushed under a deeper central path.

## Example: More Specific Rules Override Broader Rules

Local repository:

```text
docs/
  11-guides/public/overview.md
  11-guides/internal/admin/billing-approval.md
  02-architecture/system-design.md
```

Config:

```yaml
sync:
  destinations:
    "docs/11-guides/public/**":
      hub_path: "hub/06-support/public-kb/billing/"

    "docs/11-guides/internal/admin/**":
      hub_path: "hub/10-relationships/clients/client-a/workflows/"

    "docs/**":
      hub_path: "hub/03-projects/billing-modernization/"
```

Results:

```text
docs/11-guides/public/overview.md
-> hub/06-support/public-kb/billing/overview.md

docs/11-guides/internal/admin/billing-approval.md
-> hub/10-relationships/clients/client-a/workflows/billing-approval.md

docs/02-architecture/system-design.md
-> hub/03-projects/billing-modernization/02-architecture/system-design.md
```

This works because the sync engine should always prefer the most specific matching rule.

## Required Resolution Order

When deciding destination path, use this order:

1. central governance restrictions
2. explicit document frontmatter destination
3. most specific `sync.destinations` match
4. broader `sync.destinations` match
5. repo-level fallback destination
6. system fallback location

## Most-Specific-Match Rule

If multiple destination patterns match the same file, choose the most specific one.

Usually that means:

- the longest matching path pattern wins

Example:

```yaml
"docs/**"
"docs/11-guides/**"
"docs/11-guides/public/**"
```

For:

```text
docs/11-guides/public/overview.md
```

Choose:

```yaml
"docs/11-guides/public/**"
```

## Include, Exclude, And Destination Relationship

Recommended evaluation order:

1. check `include`
2. check `exclude`
3. resolve `overrides`
4. resolve destination
5. apply approval and publication policy

Meaning:

- a destination does not matter if the file is excluded
- a destination only applies to syncable content

## Recommended Destination Fields

A destination mapping can include:

- `hub_path`
- `product`
- `project`
- `domain`
- `publish_targets`
- `visibility`
- `audience`

Example:

```yaml
sync:
  destinations:
    "docs/subprojects/billing/**":
      hub_path: "hub/03-projects/billing-modernization/"
      product: "billing"
      project: "billing-modernization"
      domain: "project"
      publish_targets:
        - internal-site
```

## Document-Level Destination Override

Use frontmatter override only in exceptional cases.

Example:

```yaml
---
hub_path: hub/04-engineering/shared-runbooks/payments/
project: billing-modernization
product: billing
---
```

Use this sparingly because too many per-document overrides make routing harder to reason about.

## Monorepo Model

For monorepos, declare route roots explicitly.

Example:

```yaml
sync:
  include:
    - "docs/subprojects/billing/**"
    - "docs/subprojects/auth/**"
    - "docs/platform/**"

  destinations:
    "docs/subprojects/billing/**":
      hub_path: "hub/03-projects/billing-modernization/"

    "docs/subprojects/auth/**":
      hub_path: "hub/03-projects/auth-unification/"

    "docs/platform/**":
      hub_path: "hub/04-engineering/platform/shared-services/"
```

This keeps one monorepo from collapsing into one fake central destination.

## Recommended Sync Engine Behavior

Pseudo-flow:

```text
for each changed file:
  if not included:
    skip
  if excluded:
    skip

  apply matching override rules

  if frontmatter has explicit hub_path:
    use it
  else:
    choose most specific destination match
  else:
    use fallback destination

  compute relative path after matched source root
  destination_path = hub_path + relative_path

  sync according to sync_mode
```

## Good Design Rule

Keep routing predictable:

- broad rule for default repo destination
- narrower rules for sub-projects and special sections
- rare document-level override only when necessary

This gives flexibility without chaos.

## Final Recommendation

If you want to push a whole folder under a sub-project, map the folder root to that sub-project hub path and preserve the relative subtree.

If one local repo has only one docs tree but must appear under a deeper sub-project in the hub, map `docs/**` to that sub-project destination.

If one repo contains multiple sub-projects, give each subtree its own destination mapping.
