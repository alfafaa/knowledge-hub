# Structure Evolution Policy

## Purpose

This document defines how the folder structure and documentation conventions should evolve over time without breaking existing repositories or confusing teams.

It answers:

- how to improve structure safely
- how to handle old and new folder patterns
- how to deprecate folder conventions
- how to keep documentation stable during structural growth

## Core Principle

Folder structure should evolve slowly and predictably.

Do not treat the structure as something to rewrite casually.

A stable structure is part of the product.

## What Should Be Stable

These should change very rarely:

- company-level top domains
- project-level mandatory categories
- meaning of core folder names

Examples of stable concepts:

- `02-architecture/`
- `03-decisions/`
- `05-operations/`
- `06-reference/`
- `11-guides/`

## What Can Evolve More Freely

These can change more easily:

- optional folders
- second- or third-level nested patterns
- template refinements
- new guide subcategories
- new metadata fields

## Recommended Evolution Rule

Prefer:

- adding new optional structure

Over:

- renaming existing core structure

Additive changes are much safer than destructive changes.

## Backward Compatibility Rule

If a core folder convention changes, the system should temporarily support both the old and new pattern.

Examples:

- old: `02-rfcs-adrs/`
- new: `03-decisions/`

During migration:

- both should be recognized
- old should produce warnings
- new should be the recommended template

## Folder Deprecation Lifecycle

Use this lifecycle:

1. `active`
2. `deprecated`
3. `removed`

### `active`

Folder is current and recommended.

### `deprecated`

Folder still works, but:

- new templates no longer use it
- validator warns
- migration path exists

### `removed`

Folder is no longer recognized by the active system version.

Removal should be rare.

## Safe Structural Changes

Usually safe:

- add `11-guides/`
- add `98-meta/`
- add `sync.destinations`
- add new nested folders under `05-operations/`

Riskier:

- rename `03-decisions/`
- move `05-operations/` into another domain
- redefine `06-reference/` to mean something else

## Migration Strategy For Structural Changes

When structure changes:

1. publish the new structure
2. update templates
3. update validator rules
4. support legacy structure during transition
5. warn old repos
6. migrate active repos
7. remove legacy support only later

## Template Rule

Templates should always represent the newest recommended structure.

But old repositories should not be forced to instantly match the newest template.

This is important:

- template = future direction
- validator = compatibility guard
- migration tooling = transition support

## Sync Engine Rule

The sync engine should understand semantic intent, not only exact folder names.

Meaning:

- if an old repo still stores ADRs in an older location
- the engine should still classify them correctly during the support window

This reduces migration pressure on older repos.

## Governance Rule For Big Changes

Before changing core structure:

1. define the problem with the current structure
2. explain the benefit of the new structure
3. define the migration path
4. assign support window
5. update templates and specs

Do not change core structure just because a newer layout looks cleaner.

## Recommended Compatibility Window

For active repositories:

- support deprecated core structure for at least one planned migration cycle

For inactive repositories:

- allow longer lag if they do not block current operations

## Good Example

### Safe evolution

- add `98-meta/` as optional
- old repos remain valid
- new template includes it

### Risky evolution handled safely

- old folder: `issues/`
- new preferred folder: `09-knowledge/troubleshooting/`

Safe transition:

- support both
- warn on old
- migrate over time

## Best-Practice Summary

- keep top-level structure stable
- evolve by addition first
- deprecate before removing
- let templates move faster than old repos
- keep validator and sync engine compatibility-aware

## Final Recommendation

If you need to improve structure later, do it like a product upgrade:

- introduce
- support both
- warn
- migrate
- remove later

That is how the knowledge system evolves without breaking the past.
