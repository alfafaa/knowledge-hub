# Alfafaa Knowledge Hub

This repository now defines the operating model for a centralized company knowledge hub built on a `docs-as-code` workflow.

The recommended long-term approach is:

- Teams keep technical and project-near documentation inside their own repositories.
- Automation collects approved documentation into a central knowledge system.
- The central system publishes separate audiences from the same source model:
  - Public
  - Internal/admin
  - Engineering
- Governance, metadata, ownership, and review rules keep the system maintainable over time.

## Core Documents

- [Knowledge Hub Blueprint](docs/knowledge-hub-blueprint.md)
- [Documentation Standards](docs/documentation-standards.md)
- [Automation Architecture](docs/automation-architecture.md)
- [Final Implementation Plan](docs/final-implementation-plan.md)
- [Project Starter Template Rollout Plan](docs/project-starter-template-rollout-plan.md)
- [Project Starter Template Publish Workflow](docs/project-starter-template-publish-workflow.md)
- [Scalability Assessment And Next Scale Steps](docs/scalability-assessment-and-next-scale-steps.md)
- [Where Docs Physically Live And Flow](docs/where-docs-physically-live-and-flow.md)
- [Domain And Site URL Strategy](docs/domain-and-site-url-strategy.md)
- [Source Repo Manual Sync To Knowledge Hub](docs/source-repo-manual-sync-to-knowledge-hub.md)

## Canonical Runtime Naming

- Central doc root display name: `Alfafaa Knowledge Hub`
- Canonical content root path: `hub/`

The runtime configuration for those values lives in [hub.config.yaml](hub.config.yaml).

## MVP Tooling

Initial implementation files:

- `schemas/`
- `scripts/validate_docs.py`
- `scripts/plan_sync.py`
- `scripts/ingest_sync.py`
- `scripts/plan_publish.py`
- `scripts/prepare_quartz_workspace.py`
- `scripts/build_quartz_sites.py`
- `scripts/plan_deploy.py`
- `scripts/generate_nginx_config.py`
- `scripts/execute_deploy.py`
- `scripts/deploy_to_vps.py`
- `scripts/deploy_via_ssh.py`
- `scripts/serve_local_preview.py`
- `scripts/run_pipeline.py`
- `examples/sample-project-repo/`
- `quartz/`
- `Dockerfile`
- `compose.yaml`
- `deploy/templates/`

## End-To-End Command

Run the current MVP pipeline with:

```bash
python3 scripts/run_pipeline.py --docs-root examples/sample-project-repo/docs
```

This runs:

1. validation
2. ingestion
3. publish planning
4. Quartz workspace preparation
5. Quartz static rendering
6. deployment planning
7. nginx config generation
8. deployment packaging
9. VPS deployment extraction

You can also simulate CI context locally:

```bash
python3 scripts/run_pipeline.py \
  --docs-root examples/sample-project-repo/docs \
  --branch main \
  --event push
```

## Local Preview

Before any VPS deployment, serve the locally extracted runtime in a browser:

```bash
python3 scripts/serve_local_preview.py
```

Default preview root:

```text
http://127.0.0.1:8010/
```

## Docker

The project is now containerized as a pipeline runtime.

Build:

```bash
docker build -t alfafaa-knowledge-hub:local .
```

Run:

```bash
docker run --rm -v "$PWD:/app" -w /app alfafaa-knowledge-hub:local
```

Compose:

```bash
docker compose run --rm knowledge-hub
```

## CI Integration

The repository now includes a first GitHub Actions workflow:

- [knowledge-hub-ci.yml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/.github/workflows/knowledge-hub-ci.yml)

Implementation notes:

- [CI/CD Integration](docs/ci-cd-integration.md)
- [Deployment Planning](docs/deployment-planning.md)
- [Deployment Execution](docs/deployment-execution.md)
- [Quartz Runtime Integration](docs/quartz-runtime-integration.md)
- [Media And Asset Handling](docs/media-and-asset-handling.md)
- [System Architecture And Workflow Diagrams](docs/system-architecture-and-workflow-diagrams.md)
- [Executive System View](docs/executive-system-view.md)
- [Local Runtime Preview](docs/local-runtime-preview.md)
- [VPS Deployment](docs/vps-deployment.md)
- [SSH Remote Deployment](docs/ssh-remote-deployment.md)
- [Staging Deployment](docs/staging-deployment.md)
- [Dockerized Runtime](docs/dockerized-runtime.md)

## Recommended Positioning

- Use project repositories as the source of truth for implementation-coupled docs.
- Use this hub as the source of truth for cross-company standards, policies, product context, and published aggregation.
- Use Quartz as the publishing layer for generated sites.
- Treat Obsidian as an optional editing client, not the canonical platform or access-control layer.
