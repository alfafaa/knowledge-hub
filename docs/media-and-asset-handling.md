# Media And Asset Handling

## Purpose

This document defines how `Alfafaa Knowledge Hub` currently handles non-Markdown files referenced from documentation.

Examples:

- images such as `.png`, `.jpg`, `.svg`, `.webp`
- PDFs such as runbook attachments or reference manuals
- other local binary files linked from a Markdown page

## Default Asset Model

The project-level default is now a hybrid model:

- use `docs/98-meta/assets/` by default so the visible documentation folders stay clean
- allow page-near asset folders such as `page.assets/` only as an exception for tightly coupled media

That gives you both:

- a cleaner day-to-day docs tree for authors and managers
- portability when a document genuinely needs its assets beside it

## Current Supported Model

The current implementation supports linked local assets for mirrored Markdown documents.

In practical terms:

- if a mirrored Markdown file links to a local asset
- the ingestion step discovers that asset
- the asset is copied into the mirrored hub destination beside the document
- the publish planner stages that asset into the audience-specific site
- Quartz includes that asset in the rendered static output
- the deployed runtime serves that asset normally

This now works end to end for the main publish path.

## Supported Link Styles

The ingestion layer currently detects:

- standard Markdown image links
  - `![Diagram](../98-meta/assets/architecture/billing-flow.svg)`
  - `![Diagram](./system-design.assets/billing-flow.svg)`
- standard Markdown file links
  - `[Manual](./attachments/recovery-guide.pdf)`
- Obsidian image embed links
  - `![[billing-flow.svg]]`
  - `![[attachments/recovery-guide.pdf]]`

External links are ignored and are not mirrored:

- `https://...`
- `http://...`
- `mailto:...`
- `tel:...`
- `#anchor`

## Implemented Flow

### 1. Authoring

The source Markdown file lives in a project repository.

Example:

- `docs/02-architecture/system-design.md`

and links a local asset such as:

- `docs/98-meta/assets/architecture/billing-flow.svg`

### 2. Ingestion

During ingestion:

- the Markdown file is mirrored into the hub
- linked local assets are discovered
- each asset is copied to the mirrored destination relative to the mirrored document

Example result:

- source doc:
  - `docs/02-architecture/system-design.md`
- source asset:
  - `docs/98-meta/assets/architecture/billing-flow.svg`
- mirrored doc:
  - `hub/03-projects/billing-modernization/02-architecture/system-design.md`
- mirrored asset:
  - `hub/03-projects/billing-modernization/98-meta/assets/architecture/billing-flow.svg`

### 3. Catalog

Mirrored assets are also written into the central catalog as `type: asset` entries with:

- `action: mirrored-asset`
- inherited audience/visibility/publish settings
- `linked_from` pointing back to the Markdown source

### 4. Publish Planning

During publish planning:

- mirrored assets are staged with mirrored docs
- assets use the same publish target rules as the owning doc

### 5. Quartz Build And Runtime

Quartz then copies those staged files into the rendered site output, and the deployed runtime serves them as normal static files.

## Files That Implement This

- [scripts/sync_lib.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/sync_lib.py)
- [scripts/ingest_sync.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/ingest_sync.py)
- [scripts/plan_publish.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/plan_publish.py)

## Verified Example

The sample repo now includes:

- [system-design.md](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/examples/sample-project-repo/docs/02-architecture/system-design.md)
- [billing-flow.svg](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/examples/sample-project-repo/docs/98-meta/assets/architecture/billing-flow.svg)

This asset was verified through these pipeline layers:

- hub mirror
- staged publish content
- Quartz workspace
- rendered site output
- deployed local runtime
- incremental `--changed` sync mode using only the asset path

## Current Constraints

The implementation is useful and real, but not complete in every scenario.

### Supported Well

- repo-level shared assets under `98-meta/assets/`
- local assets linked from mirrored Markdown docs
- page-near asset folders such as `page.assets/`
- asset-only incremental sync by resolving changed assets back to the owning Markdown docs
- broken local asset-link validation in the docs validator
- publish-target inheritance from the owning document
- static serving in Quartz/nginx runtime

### Not Yet First-Class

- standalone asset publishing without a linked Markdown owner
- deep media governance rules by file type or file size
- automatic validation of broken asset references
- asset deduplication across multiple docs

## Current Limitation

The planner now handles asset-only changed-file input by resolving assets back to the Markdown docs that reference them.

That closes the main incremental gap, but one important limitation still remains:

- assets are still governed through the owning Markdown document
- standalone assets without a linked Markdown owner are not yet first-class publish items

That is a reasonable model for now because it keeps asset visibility, audience, and publish rules attached to the document that actually owns the content.

## Best Practice For Authors Right Now

- keep assets in `98-meta/assets/` by default so normal doc folders remain clean
- use page-near folders such as `system-design.assets/` only when the document and its media are tightly coupled
- prefer relative links
- do not rely on raw absolute filesystem paths

## Recommended Next Improvements

1. Add optional asset policy rules for file types and size limits.
2. Add shared-asset support beyond page-near relative links when needed.
3. Decide whether standalone governed asset publishing is ever truly needed.
