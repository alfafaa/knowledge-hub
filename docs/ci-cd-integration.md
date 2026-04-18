# CI/CD Integration

## Purpose

This document defines the first CI integration for the Alfafaa Knowledge Hub pipeline.

It focuses on:

- running validation and publishing prep automatically
- preserving artifacts for review
- creating a stable base for later deployment automation

## Current Workflow

The repository now includes:

- [knowledge-hub-ci.yml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/.github/workflows/knowledge-hub-ci.yml)

## What The Workflow Does

On:

- push to `main`
- pull requests
- manual dispatch

It runs:

1. checkout
2. Python setup
3. `pyyaml` install
4. `scripts/run_pipeline.py` with real GitHub branch and event context
5. artifact upload

## Current Pipeline Scope

The workflow currently runs the sample docs root:

```text
examples/sample-project-repo/docs
```

This is intentional for the MVP.

It proves the pipeline in CI before wiring real repositories or multi-repo triggers.

## Uploaded Artifacts

The workflow uploads:

- `build/`
- `hub/98-meta/publishing/`
- `quartz/workspace-summary.json`
- `quartz/workspaces/`

These artifacts let you inspect:

- pipeline reports
- publish manifests
- indexed-doc catalogs
- Quartz-ready site workspaces

## Why Artifact Upload Matters

At this stage, CI should not only fail or pass.

It should also show:

- what the pipeline generated
- what content would publish
- what workspaces Quartz would consume

That makes debugging and stakeholder review much easier.

## Recommended Next CI Improvements

After this MVP workflow, the next upgrades should be:

### 1. Multiple docs roots

Expand the matrix to cover:

- more example repos
- real pilot repos

### 2. Separate validation and build jobs

Split:

- validation
- ingestion/publish planning
- deployment

This gives clearer failure boundaries.

### 3. Deployment gating

Only deploy from:

- `main`
- approved tags
- protected branches

### 4. Real Quartz build job

Once a Quartz app is added, extend CI to:

- install Node dependencies
- build target site(s)
- upload built site artifacts

### 5. Environment-specific publishing

Add:

- preview builds for pull requests
- internal release build on main
- public/admin deploy only after explicit approval

## GitHub Actions Note

The current workflow is written for GitHub Actions because it is the fastest path from local MVP to automated execution.

If you later move to:

- GitLab CI
- self-hosted runners
- a VPS-based cron/worker model

the pipeline command stays the same:

```bash
python3 scripts/run_pipeline.py --docs-root <path>
```

That is why the orchestration command was added first.

## Final Recommendation

Use the current GitHub Actions workflow as the first automation layer.

It is enough to:

- prove the pipeline in CI
- generate inspectable artifacts
- prepare for real deployment later

Do not wire production deployment until at least one real pilot repository is running through the same flow successfully.

## CI Context Passed To Deployment Planning

The workflow now passes:

- branch name
- GitHub event name

into the pipeline runner.

That means deployment planning can distinguish:

- pull request preview context
- `main` branch context
- manual dispatch context

without hardcoding `local` for every CI run.
