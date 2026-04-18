# Deployment Planning

## Purpose

This document defines the first deployment-planning layer for the Alfafaa Knowledge Hub pipeline.

It answers:

- which targets should deploy in which environment
- how pull requests differ from `main`
- how public, internal, engineering, and admin targets should be gated
- how to prepare deployment manifests before binding to a real hosting provider

## Core Principle

Do not deploy directly from raw pipeline outputs without an explicit deployment decision layer.

Use deployment planning to decide:

- what is deployable
- to which environment
- with which approval level
- from which git context

## Recommended Environment Model

Use these environments:

- `preview`
- `internal`
- `production`

## Recommended Target Rules

### Pull Request

- `public-site`
  - preview only
- `internal-site`
  - preview only
- `engineering-site`
  - preview only
- `admin-site`
  - no automatic preview by default

### Push To `main`

- `internal-site`
  - internal deploy allowed
- `engineering-site`
  - internal deploy allowed
- `public-site`
  - plan as production-candidate, but require explicit approval
- `admin-site`
  - internal restricted deploy only, preferably after approval

### Tagged Release Or Manual Release

- `public-site`
  - production deploy allowed
- `internal-site`
  - internal deploy allowed
- `engineering-site`
  - internal deploy allowed
- `admin-site`
  - restricted deploy allowed after approval

## Why This Split Works

- PR builds are good for previews and review
- `main` is good for internal environments
- public and restricted targets should not deploy casually

This avoids accidental public exposure while still keeping internal iteration fast.

## Deployment Manifest Fields

Each target deployment plan should include:

- `target`
- `environment`
- `allowed`
- `reason`
- `requires_approval`
- `workspace`
- `generated_files`
- `content_summary`

## Recommended Gating Rules

Require approval for:

- `public-site` production deploy
- `admin-site` deploy
- any target with `restricted` content

Allow automatic deploy for:

- internal preview environments
- engineering preview/internal environments
- internal-site main-branch internal environment

## Current Recommendation

At the current MVP stage:

- generate deploy manifests only
- do not perform live deployment yet

This keeps the pipeline auditable and safe while the hosting layer is still undecided.
