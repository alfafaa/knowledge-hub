# Obsidian Working Conventions

## Purpose

This document defines how to use the knowledge hub and project documentation structure comfortably in Obsidian while keeping it compatible with automation and Quartz publishing.

It answers:

- how to place attachments
- how to name files and images
- how to use wikilinks safely
- how to handle folder notes
- how to keep Obsidian-friendly workflows compatible with the central hub

## Core Principle

Obsidian is an editing interface, not the canonical governance layer.

That means:

- authors should be able to work naturally in Obsidian
- file structure must still remain clear outside Obsidian
- links and assets should not depend on Obsidian-only behavior
- Quartz publishing should remain predictable

## Recommended Vault Rules

Use these settings as the default team convention:

- default new notes location:
  - current folder when working inside a domain
- attachment location:
  - prefer folder-specific or page-near assets for local content
  - use `98-meta/assets/` only for shared reusable media
- auto-update internal links:
  - enabled
- use wikilinks:
  - enabled
- detect all file extensions:
  - enabled if the team stores mixed reference files

## Attachment Rules

This is the most important convention for long-term cleanliness.

### Use local colocated assets when:

- an image belongs to one page or one small topic
- a screenshot is specific to one guide
- a diagram is used only by one document or one narrow folder

Recommended pattern:

```text
02-architecture/
  system-design.md
  system-design.assets/
    context-diagram.png
```

Or:

```text
11-guides/public/usage/
  payment-flow.md
  payment-flow.assets/
    step-1.png
    step-2.png
```

### Use `98-meta/assets/` when:

- the same asset is reused across many notes
- the asset is generic and stable
- the asset belongs to the workspace more than to one page

Examples:

- brand logo
- shared icon set
- common architecture diagram reused in many pages
- repeated screenshots used across multiple docs

## Asset Placement Strategy

Use this rule:

- page-specific asset -> keep near the page
- repo-wide shared asset -> `docs/98-meta/assets/`
- company-wide shared asset -> `hub/98-meta/assets/`

This avoids one giant messy attachments folder.

## Asset Naming Rules

Use descriptive kebab-case names.

Good:

- `context-diagram.png`
- `payment-retry-flow.png`
- `admin-dashboard-overview.png`

Avoid:

- `image1.png`
- `final-final.png`
- `screenshot (4).png`

When useful, prefix by topic:

- `billing-payment-retry-flow.png`
- `auth-session-lifecycle.png`

## Folder Notes

Use folder notes carefully.

Recommended rule:

- use `_index.md` as the folder note for important folders
- treat `_index.md` as the navigation and summary page
- do not create both `_index.md` and another competing “folder home” note

Examples:

- `hub/02-products/product-slug/_index.md`
- `docs/_index.md`

This keeps Obsidian and non-Obsidian workflows aligned.

## Wikilink Rules

Obsidian wikilinks are useful, but only when controlled.

Recommended:

- use `[[note-name]]` for nearby stable links
- prefer unique filenames within a meaningful domain
- when ambiguity is possible, link by path-aware note naming strategy or use normal markdown links

For public or long-lived docs, prefer links that remain readable outside Obsidian as well.

Recommended practical approach:

- Obsidian authors may use wikilinks while drafting
- publishing pipeline should normalize them if needed for Quartz

## Link Safety Rules

Avoid:

- relying on identical filenames in many different folders without a naming convention
- linking to temporary scratch notes
- linking to unpublished private notes from public-facing content

Good rule:

- if a page will publish broadly, link only to stable approved docs

## Frontmatter Rules In Obsidian

Always preserve YAML frontmatter at the top of the note.

Do not allow visual editing habits to break:

- `id`
- `owner`
- `status`
- `visibility`
- `publish`
- `last_reviewed`

These fields are essential for sync and publishing.

## Recommended New Note Patterns

### Company-level note

Create inside the owning domain and start from a template.

Example:

```text
hub/01-company/business/marketing/brand-positioning.md
```

### Product note

Create inside the product folder.

Example:

```text
hub/02-products/payments/product-overview.md
```

### Project-repo note

Create inside the correct `docs/` category.

Example:

```text
docs/05-operations/runbooks/payment-recovery.md
```

## Recommended Obsidian Behavior By Folder Type

### Content domains

Examples:

- `01-company/`
- `02-products/`
- `04-engineering/`

Use for:

- actual knowledge notes
- durable documentation

### `98-meta/`

Use for:

- workspace helpers
- shared assets
- conventions
- publishing notes

Do not use for:

- regular content pages

### `90-archive/`

Use for:

- retired material that should remain readable

Recommended Obsidian behavior:

- keep it searchable
- keep it out of active writing workflows

## Quartz Compatibility Rules

To keep Obsidian authoring compatible with Quartz:

- prefer `_index.md` for section home pages
- keep filenames stable
- avoid depending on plugins that rewrite content into proprietary syntax
- keep embeds and links simple where possible
- use markdown and standard frontmatter as the canonical format

If you use Obsidian-specific features, make sure the publishing pipeline knows how to transform or ignore them.

## Image Embeds

Prefer simple, portable embeds where possible.

If the team uses Obsidian embeds like:

```text
![[context-diagram.png]]
```

make sure the publishing workflow can resolve them.

If portability is more important, prefer standard markdown:

```markdown
![Context diagram](./system-design.assets/context-diagram.png)
```

My recommendation:

- use standard markdown image links for published docs
- allow Obsidian embeds for private drafting only if the pipeline can normalize them

## Tagging In Obsidian

Use tags sparingly.

Recommended:

- keep structural meaning in folders and frontmatter
- use tags only for secondary discovery
- avoid creating personal ad hoc tag vocabularies

## Daily Workflow Recommendation

1. Open the hub or repo in Obsidian.
2. Navigate to the correct owning domain.
3. Create or edit the note using the appropriate template.
4. Add frontmatter correctly.
5. Place assets locally or in `98-meta/assets/` based on reuse.
6. Link to stable notes only.
7. Let sync and publishing automation handle distribution.

## Best-Practice Summary

- Use Obsidian as the writing experience.
- Use the folder structure as the ownership model.
- Use `_index.md` as the folder note convention.
- Use local assets by default and shared assets only when truly shared.
- Use `98-meta/` for workspace support, not for normal content.
- Keep everything Quartz-compatible by favoring standard markdown and frontmatter.
