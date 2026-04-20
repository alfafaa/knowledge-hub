---
title: Docs Config Preset Selection
type: standard
status: draft
publish: false
---

# Docs Config Preset Selection

Use one of the preset configs under `.starter-presets/docs-config/` as the starting point for `docs/docs.config.yaml`.

Pick based on the real repository type:

- backend/API service -> `service.docs.config.yaml`
- frontend/web app -> `frontend-app.docs.config.yaml`
- shared platform or infrastructure repo -> `platform.docs.config.yaml`
- small internal business or admin tool -> `internal-tool.docs.config.yaml`

## Selection Rule

Choose the preset by ownership and consumers, not by framework.

Use:

- `service`
  - if the repo mainly exposes backend logic, APIs, workers, or service runtime
- `frontend-app`
  - if the repo mainly owns web UI or frontend delivery
- `platform`
  - if the repo provides reusable infrastructure, shared runtime services, or organization-wide engineering capabilities
- `internal-tool`
  - if the repo serves internal business workflows more than broad engineering consumers

## After Copying A Preset

Review these values:

- `team-name`

Then review:

- `sync.include`
- `sync.overrides`
- `sync.destinations`
- public/internal/engineering guide routing

Important:

- `repo_name` is auto-resolved from the repository context
- `project_slug` defaults to the resolved repo identity unless you intentionally override it
- `project_slug` placeholders in destination paths are auto-resolved by the pipeline

So teams should not need to manually edit those unless they intentionally want a different central routing identity.
