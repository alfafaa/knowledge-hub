# Source Repo Manual Sync To Knowledge Hub

## Purpose

This document explains the actual implementation path for pushing docs from a real project repository into the central knowledge hub.

It covers:

- what lives in the source repo
- what lives in the central knowledge hub repo
- how the manual trigger works
- which secrets are required

## Current Implemented Model

The implementation now uses a two-repository flow.

### Source Repository

The source repository contains:

- project code
- project docs under `docs/`
- a manual GitHub Actions workflow that requests central sync

Implemented starter workflow:

- [starter-templates/project-starter-template-repo/.github/workflows/push-docs-to-knowledge-hub.yml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/starter-templates/project-starter-template-repo/.github/workflows/push-docs-to-knowledge-hub.yml)

### Central Knowledge Hub Repository

The central repository contains:

- validation
- sync and ingestion
- Quartz build
- deploy packaging
- VPS deployment
- the receiver workflow for cross-repo source sync

Implemented receiver workflow:

- [.github/workflows/knowledge-hub-source-sync.yml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/.github/workflows/knowledge-hub-source-sync.yml)

## Trigger Flow

The intended flow is:

1. developer updates docs in the source repo
2. developer manually triggers `Push Docs To Knowledge Hub`
3. source repo sends `repository_dispatch` to the central hub repo
4. central hub checks out the source repo at the requested ref
5. central hub runs the full docs pipeline against that source docs root
6. central hub deploys updated rendered outputs to VPS

## Required Source Repo Secrets

Configure these in the project repository:

- `KNOWLEDGE_HUB_TRIGGER_TOKEN`
- `KNOWLEDGE_HUB_OWNER`
- `KNOWLEDGE_HUB_REPO`

## Required Knowledge Hub Repo Secrets

Configure these in the central knowledge hub repository:

- `SOURCE_REPO_READ_TOKEN`
  - required when source repos are private
- `KNOWLEDGE_HUB_DEPLOY_SSH_KEY`
  - required if the workflow should deploy to VPS automatically

## Starter Template Location

The exportable starter scaffold now lives at:

- [starter-templates/project-starter-template-repo/README.md](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/starter-templates/project-starter-template-repo/README.md)

This is designed so it can later become its own dedicated repository for ZIP download and reuse.

## Operational Notes

- source repos trigger manually first
- central pipeline remains authoritative
- no manual copying into `hub/` is required
- the central repo remains the only place that builds and deploys the shared sites

## Recommended Next Real Test

The next real validation step is:

1. create one real pilot source repository from the starter
2. set the required secrets
3. trigger the manual source workflow
4. confirm the central hub ingests and deploys from that repository end to end
