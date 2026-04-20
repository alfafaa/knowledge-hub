# Project Starter Template Publish Workflow

This workflow publishes the starter template from the knowledge hub repository into the dedicated starter template repository.

## Purpose

The source of truth stays here:

- `starter-templates/project-starter-template-repo/`

The publish workflow turns that folder into a standalone repository and pushes it into:

- `alfafaa/project-starter-template`

This is a strict mirror publish model.

That means:

- the target repository is treated as generated output
- the target branch is replaced to match the exported starter template exactly
- extra files in the target repository are removed on publish

Analogy:

- this repository is the mold
- the target repository is the cast product

Do not make manual edits in the target repository unless you are willing to lose them on the next publish.

## Manual Workflow

Use:

- [.github/workflows/publish-project-starter-template.yml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/.github/workflows/publish-project-starter-template.yml)

Trigger it manually with `workflow_dispatch`.

Inputs:

- `target_repository`
  - default: `alfafaa/project-starter-template`
- `target_branch`
  - default: `main`
- `create_release_zip`
  - `true` creates a GitHub Release in the target repository with a zip asset
- `release_tag`
  - optional
- `release_title`
  - optional

## What The Workflow Does

1. Exports `starter-templates/project-starter-template-repo/` into a clean standalone repository tree.
2. Optionally builds a release zip from that exported tree.
3. Clones the target repository.
4. Replaces the target branch contents with the exported tree.
5. Commits and pushes the new mirror state.
6. Optionally creates a GitHub Release in the target repository and uploads the zip asset.

## Required Secret

- `PROJECT_STARTER_TEMPLATE_PUSH_TOKEN`

Recommended token scope:

- repository write access to `alfafaa/project-starter-template`
- release creation permission for that repository

If you use a classic personal access token, `repo` scope is the practical baseline.

## Supporting Script

The export step uses:

- [scripts/export_project_starter_template.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/export_project_starter_template.py)

Example local export:

```bash
python3 scripts/export_project_starter_template.py \
  --output-dir /tmp/project-starter-template-export \
  --zip-path /tmp/project-starter-template.zip
```

## Operational Rules

- treat the target repository as generated output
- do not keep hand-maintained files there
- make starter template changes here first
- publish only after validating the starter template locally

## Validation Before Publish

Recommended local check:

```bash
python3 scripts/validate_docs.py --docs-root starter-templates/project-starter-template-repo/docs
```
