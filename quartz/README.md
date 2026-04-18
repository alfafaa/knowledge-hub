# Quartz Integration Workspace

This directory holds Quartz-ready target workspaces generated from the knowledge hub build outputs.

Current model:

- `workspaces/<target>/content/` is the content root for a target site
- `workspaces/<target>/site.config.json` describes the target
- `templates/` contains starter config files you can adapt when you add a real Quartz app

Recommended flow:

1. run `scripts/plan_publish.py`
2. run `scripts/prepare_quartz_workspace.py`
3. point a Quartz app at `quartz/workspaces/<target>/content`

This keeps the content pipeline independent from the eventual frontend/runtime choice.
