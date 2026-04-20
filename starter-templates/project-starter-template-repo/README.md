# Project Starter Template

This folder is a full repository starter, not only a docs fragment.

Use it when a team starts a new project or repository and needs:

- the large-scale project docs structure
- documentation templates
- short developer guidance on what to write, where to write, and how to write
- manual docs push to the central knowledge hub
- a clean starting point that can later be reduced if the repo is smaller

## Intended Usage

1. Download this starter from the dedicated starter-template repository as a ZIP.
2. Extract it into the new project repository.
3. Rename placeholders such as:
   - `project-slug`
   - `repo-slug`
   - `team-name`
4. Adjust `docs/docs.config.yaml` destination paths.
5. Set the GitHub Actions secrets required for central sync.
6. Manually trigger `Push Docs To Knowledge Hub` when docs should be ingested centrally.

## Required Source Repo Secrets

- `KNOWLEDGE_HUB_TRIGGER_TOKEN`
- `KNOWLEDGE_HUB_OWNER`
- `KNOWLEDGE_HUB_REPO`

## Included

- `docs/` with the large-scale extension profile
- `.github/workflows/push-docs-to-knowledge-hub.yml`
- reusable templates under `docs/98-meta/templates/`
- starter guides for Git workflow and CI/CD documentation

## Quick Authoring Help

Use these first:

- `docs/98-meta/templates/where-to-write-cheat-sheet.md`
- `docs/98-meta/templates/how-to-write-docs.md`
- `docs/98-meta/templates/new-doc-checklist.md`

## Important Rule

Keep authoring in the source repository.

Do not copy docs manually into the knowledge hub repository.

Use the manual workflow trigger and let the central hub ingest, build, and deploy.
