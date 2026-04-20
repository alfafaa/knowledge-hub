# Where Docs Physically Live And Flow

## Purpose

This document answers a simple but important question:

- in the current system, do all docs get stored in `hub/` first?

Short answer:

- no

Only some docs physically land in `hub/`.

## Core Storage Model

There are three different physical states in the current implementation.

### 1. Source Repo Only

The document lives only in the project repository.

This happens when the sync result is:

- `local-only`

In that case:

- the project repo is the only physical home
- nothing is mirrored into `hub/`
- nothing is centrally stored except whatever local Git history exists in that repo

### 2. Source Repo + Central Catalog Metadata

The document still lives only in the project repository as content, but the central system stores metadata about it.

This happens when the sync result is:

- `indexed-only`

In that case:

- the full doc body is not mirrored into `hub/` as a managed content page
- the central system stores a catalog entry in:
  - [hub/98-meta/publishing/indexed-docs-catalog.json](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/hub/98-meta/publishing/indexed-docs-catalog.json)
- the system can still use that metadata for discovery, planning, and generated views

Think of this as:

- source repo = real book
- central hub catalog = library card

### 3. Source Repo + Mirrored Hub Content

The document lives in the project repo and is also mirrored into `hub/`.

This happens when the sync result is:

- `mirrored`

In that case:

- the source repo remains the authoring source of truth
- the central hub gets a physical mirrored copy under the resolved destination path
- publishing and audience-specific staging use that mirrored hub content

Example:

- source:
  - `examples/sample-project-repo/docs/02-architecture/system-design.md`
- mirrored hub destination:
  - [hub/03-projects/billing-modernization/02-architecture/system-design.md](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/hub/03-projects/billing-modernization/02-architecture/system-design.md)

## Current Flow Table

| Sync mode | Authoring source | Stored in `hub/` as content | Stored in central catalog | Publishable from central system |
|---|---|---|---|---|
| `local-only` | project repo | no | no | no |
| `indexed-only` | project repo | no | yes | discoverable only, unless generated as catalog view |
| `mirrored` | project repo | yes | yes | yes |

## What `hub/` Is In The Current System

`hub/` is not a giant dump of every document.

It is:

- the central aggregated content root
- the place where mirrored docs physically land
- the place where central company-owned docs live directly
- the source for central publish/build flows

So the correct model is:

- project repos are the operational authoring source
- `hub/` is the central managed aggregation and publishing root

## What Is Stored Centrally Even When A Doc Is Not Mirrored

Even when a doc is not mirrored, the current system may still store central metadata about it.

That metadata includes things like:

- repo name
- source path
- intended destination
- audience
- visibility
- publish targets
- sync action

That lives in central publishing metadata such as:

- [hub/98-meta/publishing/indexed-docs-catalog.json](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/hub/98-meta/publishing/indexed-docs-catalog.json)

## Current Build Behavior

The publish/build pipeline works like this:

1. source repo docs are evaluated
2. sync mode is resolved
3. mirrored docs are written into `hub/`
4. indexed-only docs are represented in the central catalog
5. publish planning stages content for each target
6. Quartz builds static sites from the staged content

That means the answer to:

- "does everything go into `hub/` first?"

is still:

- no

Only mirrored content does.

## Best Mental Model

Use this model:

- project repo = authoring workshop
- `hub/` = central showroom and managed publishing inventory
- catalog = central directory for things known centrally but not fully copied

That is the current implementation model.
