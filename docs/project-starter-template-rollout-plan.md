# Project Starter Template Rollout Plan

## Purpose

This document defines how to turn the current project-level documentation standards into a real starter template that teams can download as a ZIP from a dedicated repository.

It covers:

- what the starter repo should contain
- how developers should use it
- how a source repository should manually trigger sync to the knowledge hub
- how the central knowledge hub should receive, ingest, build, and deploy the docs automatically

## Target Outcome

Build a dedicated `project starter template` repository that teams can use when creating a new project or repository.

That starter should include:

- the large-scale project docs structure
- repo-level docs configuration
- starter templates for ADRs, RFCs, runbooks, and publishable guides
- a manual GitHub Actions workflow in the source repo to push docs updates to the central knowledge hub

The central knowledge hub repository should then:

1. receive the source repo trigger
2. check out the source repo docs
3. run validation, ingestion, publish planning, Quartz build, and deploy
4. push updated sites to the VPS automatically

## Core Operating Model

Use a two-repository flow.

### 1. Source Project Repository

This is the real engineering repository where developers work.

It contains:

- application code
- local project docs
- a manual workflow to request docs sync to the knowledge hub

### 2. Central Knowledge Hub Repository

This is the current repository.

It remains responsible for:

- validation rules
- sync and ingestion
- audience-specific publish planning
- Quartz static builds
- deployment packaging
- VPS deployment

## Why This Model Is Correct

It keeps responsibilities clean.

- developers own their repo docs
- central knowledge hub owns publishing and deployment
- teams do not need to copy docs manually into the hub repo
- one central automation pipeline remains authoritative

Analogy:

- the project repo sends a shipment request
- the central hub is the warehouse and distribution center

## Recommended Trigger Model

Use a manual workflow in the source repository.

That workflow should:

- run only when a developer or maintainer chooses to push docs updates
- send a cross-repo GitHub event to the central knowledge hub repo
- tell the hub which repository, ref, and docs root to ingest

Recommended event type:

- `repository_dispatch`

Why:

- simple cross-repo trigger
- explicit
- does not require the source repo to duplicate the central pipeline

## Recommended End-To-End Flow

1. Developer updates docs in their project repo.
2. Developer manually triggers `Push Docs To Knowledge Hub`.
3. The source repo workflow sends a dispatch event to the knowledge hub repo.
4. The knowledge hub workflow checks out:
   - the knowledge hub repo itself
   - the source repo at the requested ref
5. The knowledge hub runs:
   - validation
   - ingestion
   - publish planning
   - Quartz build
   - deployment packaging
   - VPS deployment
6. The updated audience sites become available on staging or production.

## Required Implementation Pieces

## A. Starter Template Repository Contents

The dedicated starter template repo should include:

- `README.md`
- `.github/workflows/push-docs-to-knowledge-hub.yml`
- `docs/`
- `docs/docs.config.yaml`
- large-scale extension profile folders
- starter doc templates under `docs/98-meta/templates/`

### Required Docs Areas

The starter should include the large-scale extension profile, not only the minimal structure.

Recommended included sections:

- `00-overview/`
- `01-getting-started/`
- `02-architecture/`
- `03-decisions/`
- `04-development/`
- `05-operations/`
- `06-reference/`
- `07-release/`
- `08-quality/`
- `09-knowledge/`
- `10-integrations/`
- `11-guides/`
- `98-meta/`
- `90-archive/`

### Required Guide/Template Files

At minimum include:

- ADR template
- RFC template
- runbook template
- publishable guide template
- system design template
- Git workflow guide
- CI/CD documentation guide

## B. Source Repository Workflow

The source repository workflow should:

- be manual via `workflow_dispatch`
- send:
  - source repository name
  - source ref
  - docs root
  - optional config path
- authenticate using a GitHub token or PAT with permission to dispatch events to the knowledge hub repo

Recommended required secrets in the source repo:

- `KNOWLEDGE_HUB_TRIGGER_TOKEN`
- `KNOWLEDGE_HUB_OWNER`
- `KNOWLEDGE_HUB_REPO`

## C. Central Knowledge Hub Receiver Workflow

The knowledge hub repo should add a receiver workflow that listens for:

- `repository_dispatch`

Recommended payload fields:

- `source_repository`
- `source_ref`
- `docs_root`
- `config_path`
- `requested_by`

The receiver workflow should then:

1. check out the knowledge hub repo
2. check out the source repository into a local path
3. run the existing pipeline using the source repo docs root
4. deploy with the existing VPS deployment path

## D. Access And Token Model

This needs to be explicit.

### Source Repo -> Central Repo Trigger

Use a PAT or GitHub App token that can call `repository_dispatch` on the knowledge hub repo.

### Central Repo -> Source Repo Checkout

If source repos are private, the central workflow needs a token that can read those repos.

Recommended secret in the knowledge hub repo:

- `SOURCE_REPO_READ_TOKEN`

### Central Repo -> VPS Deployment

The central workflow needs existing SSH access or equivalent deploy credentials for VPS deployment.

Recommended secrets or runner setup:

- SSH private key
- known hosts
- any required deploy configuration values

## Implementation Constraints

These constraints matter now:

- the central pipeline already exists and should not be duplicated inside source repos
- the source repo should only trigger, not rebuild the central sites itself
- the workflow should be manual first, not automatic on every push
- the starter template should be exportable as a dedicated repo later without redesign

## Phase Plan

## Phase 1: Documentation Plan

Deliverable:

- this rollout plan

Exit criterion:

- the two-repo trigger model is clearly defined

## Phase 2: Starter Template Scaffold

Deliverables:

- dedicated starter-repo scaffold directory
- large-scale docs structure
- starter templates and guides
- source repo trigger workflow

Exit criterion:

- a team could copy this folder into a new repo and start using it

## Phase 3: Central Receiver Workflow

Deliverables:

- GitHub Actions workflow in the knowledge hub repo that receives source repo dispatch events
- source repo checkout support
- pipeline execution against external docs roots

Exit criterion:

- the central repo can process a source repo request without manual file copying

## Phase 4: Deployment Integration

Deliverables:

- receiver workflow runs the existing build/deploy pipeline
- deploys the updated hub outputs to VPS

Exit criterion:

- one real project repo can update the live knowledge hub through manual trigger

## Recommended First Production Target

Do not start with all sites.

Start with:

- `engineering-site`
- `internal-site`

Reason:

- these are already active in staging
- public/admin publishing can remain more tightly controlled

## What This Implementation Will Not Do Yet

To keep the rollout disciplined, the first implementation should not try to solve:

- automatic source repo registration at scale
- automatic push-on-every-commit syncing
- multi-repo orchestration dashboards
- full production DNS/TLS/SSO rollout

Those are later hardening steps.

## Final Recommendation

Implement this as:

- one exportable project starter template repo scaffold
- one manual source repo trigger workflow
- one central knowledge hub receiver workflow

That is the smallest real implementation that proves the operating model with actual project repositories.
