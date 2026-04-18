# Deployment Execution

## Purpose

This document defines the first deployment execution layer for the Alfafaa Knowledge Hub pipeline.

It focuses on:

- taking the deploy plan and materializing deployable packages
- packaging only targets that are currently allowed
- keeping the system provider-neutral until a real hosting target is chosen

## Core Principle

Do not push directly to production infrastructure yet.

Instead:

- plan deployment
- package allowed targets
- upload packages as CI artifacts
- connect those packages to a real hosting target later

This gives you:

- auditability
- repeatability
- safer approval flow

## Current Execution Model

The execution step reads:

- `build/deploy/deploy-plan.json`

Then:

- selects targets with `allowed: true`
- packages their Quartz workspace
- writes a deployment execution report

## Current Output

Generated outputs:

- `build/deploy/packages/`
- `build/deploy/deploy-execution-report.json`

Each allowed target gets:

- a `.tar.gz` package of the Quartz workspace

## Why Packaging First Is Correct

Because the current system is still deciding:

- final hosting provider
- preview deployment strategy
- auth/reverse proxy integration
- production gating for public/admin content

Packaging first keeps the delivery contract stable while the hosting layer remains flexible.

## Current Recommended Use

- PRs:
  - package preview-eligible targets
- `main`:
  - package internal deploy targets
- public/admin:
  - keep gated until approval-driven deployment is added

## Next Step After Packaging

Once you choose the actual hosting/runtime path, connect packages to:

- VPS deployment
- S3/Object Storage publishing
- reverse-proxy-backed internal site hosting
- preview environment hosting for PRs
