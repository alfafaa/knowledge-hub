# Metadata Schema

## Required Fields

- `id`
- `title`
- `type`
- `audience`
- `visibility`
- `status`
- `owner`
- `publish`
- `last_reviewed`
- `review_cycle_days`

## Standard Example

```yaml
---
id: sample-doc-id
title: Sample Document
type: guide
domain: engineering
product: sample-product
project: sample-project
audience: engineering
visibility: internal
status: approved
owner: team-platform
tags:
  - sample
publish: true
publish_targets:
  - engineering-site
last_reviewed: 2026-03-30
review_cycle_days: 180
summary: Replace this with a one-line summary.
---
```
