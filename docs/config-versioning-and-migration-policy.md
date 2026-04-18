# Config Versioning And Migration Policy

## Purpose

This document defines how configuration used by the knowledge hub should evolve without breaking older repositories.

It answers:

- how to version config safely
- how to introduce new config features
- how to deprecate old fields
- how to migrate repositories over time
- how to keep the sync engine backward compatible

## Core Principle

Treat documentation config like an API.

That means:

- version it
- keep backward compatibility where possible
- deprecate gradually
- remove old behavior only after migration

This is the only safe way to scale across many repositories.

## What Must Be Versioned

At minimum, version these:

- `docs.config.yaml`
- sync behavior schema
- template version
- optional frontmatter schema when needed

Current foundation:

```yaml
docs_version: 1
```

## Required Rule

Every participating repository must declare:

```yaml
docs_version: <number>
```

This allows the validator and sync engine to interpret the repo correctly.

## Compatibility Model

The sync engine should support:

- current version
- previous supported version
- migration warnings for deprecated usage

Recommended baseline policy:

- support at least 2 active config versions at a time

Example:

- current: `docs_version: 2`
- still supported: `docs_version: 1`
- unsupported: `docs_version: 0`

## Safe Change Types

These are usually safe and should not require a breaking version bump:

- adding a new optional config field
- adding a new optional folder category
- adding a new publish target
- adding a new destination mapping capability
- adding new metadata fields that have defaults

## Breaking Change Types

These should require versioning and migration planning:

- renaming core config fields
- changing field meaning
- changing sync precedence
- changing required fields
- changing destination resolution behavior
- removing old folder semantics

## Deprecation Lifecycle

Use this lifecycle for any config feature:

1. `active`
2. `deprecated`
3. `removed`

### `active`

The feature is current and fully supported.

### `deprecated`

The feature still works, but:

- validator warns
- documentation marks it as old
- migration path is published

### `removed`

The feature no longer works in the current engine version.

Removal should only happen after:

- migration tooling exists
- active repos had time to upgrade
- support window has passed

## Recommended Deprecation Process

For any breaking improvement:

1. define the new config version
2. support old and new behavior in the sync engine
3. emit warnings for old behavior
4. provide migration guidance or tooling
5. migrate active repos
6. remove old behavior later

## Validator Behavior

The validator should:

- read `docs_version`
- validate according to that version
- warn on deprecated fields and structures
- fail only on unsupported or dangerous configurations

Good validator output:

- error for invalid config
- warning for deprecated config
- info for recommended upgrade path

## Migration Rules

### Rule 1: No silent semantic break

Do not change the meaning of an existing field without versioning.

### Rule 2: Prefer additive evolution

Add new fields before removing old ones.

### Rule 3: Migrate active repos first

Old inactive repos can lag temporarily, but active repos should move first.

### Rule 4: Automation must understand legacy versions

At least during the transition period.

## Example Evolution

### Version 1

```yaml
docs_version: 1
sync:
  include: []
  exclude: []
```

### Version 2

```yaml
docs_version: 2
sync:
  include: []
  exclude: []
  destinations: {}
```

During the transition:

- v1 repos still sync
- v2 repos use destinations
- validator warns v1 repos when destination routing is needed but missing

## Migration Tooling Recommendation

Over time, build tools for:

- config upgrade suggestions
- automatic field renames
- destination mapping insertion
- deprecated field detection

This is much safer than relying on manual repo-by-repo edits.

## Compatibility Matrix

Maintain a central compatibility table.

Recommended fields:

- config version
- support status
- deprecated fields
- migration notes
- removal target

Example:

| Version | Status | Notes |
|---|---|---|
| 1 | supported | base schema |
| 2 | current | adds destination routing |
| 0 | removed | no longer supported |

## Best-Practice Summary

- make `docs_version` mandatory
- support multiple active versions during transitions
- warn before breaking
- migrate with tooling
- remove old behavior only after a support window

## Final Recommendation

Treat config evolution like software API evolution.

That means:

- version it
- support compatibility
- deprecate gradually
- migrate explicitly

That is how you improve the system without breaking older repositories.
