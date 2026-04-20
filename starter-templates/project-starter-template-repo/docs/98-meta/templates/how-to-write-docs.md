---
title: How To Write Docs
type: standard
status: draft
publish: false
---

# How To Write Docs

Use this as the baseline writing discipline for all docs in this repository.

## Core Rules

- start with the problem or purpose
- keep one page focused on one concern
- use clear headings
- prefer examples over abstract language
- update docs when behavior changes, not later

## Recommended Page Shape

For most docs, use this flow:

1. purpose
2. scope or boundaries
3. main content
4. examples or operational notes
5. links to related docs

## Writing Style

- prefer direct language over marketing language
- prefer concrete examples over vague explanation
- prefer short sections over long walls of text
- explain decisions and trade-offs when they matter
- avoid duplicating content that already exists elsewhere

## Good Practice

- one doc = one clear responsibility
- link to the decision doc instead of repeating the full history
- link to the runbook instead of hiding procedures inside design docs
- link to reference docs for stable details

## Publishable Docs

For publishable docs:

- set owner
- set audience and visibility
- set publish targets
- keep review dates current

## Frontmatter Minimum

For all docs, include at least:

- `title`
- `type`
- `status`

For publishable docs, also include:

- `owner`
- `publish`
- `audience`
- `visibility`
- `publish_targets`

## Asset Rules

- use `98-meta/assets/` by default
- use page-near asset folders only when the media belongs tightly to one page
- use relative links
- avoid absolute machine-local paths

## Smell Checks

The doc probably needs improvement if:

- the title does not explain the purpose
- the reader cannot tell who the page is for
- the content mixes design, operations, and release notes in one file
- the page duplicates another page instead of linking to it
