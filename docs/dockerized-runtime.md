# Dockerized Runtime

## Purpose

This document defines the Docker runtime for the Alfafaa Knowledge Hub pipeline.

It gives you:

- a reproducible local execution environment
- a stable CI/runtime base
- a simple way to run the full pipeline without depending on host Python setup

## Files

The repository now includes:

- [Dockerfile](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/Dockerfile)
- [compose.yaml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/compose.yaml)
- [requirements.txt](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/requirements.txt)
- [.dockerignore](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/.dockerignore)

## What The Container Runs

The image is built as a pipeline runner, not as a web app container.

Default entrypoint:

```bash
python3 scripts/run_pipeline.py --docs-root examples/sample-project-repo/docs
```

## Build

```bash
docker build -t alfafaa-knowledge-hub:local .
```

## Run

```bash
docker run --rm -v "$PWD:/app" -w /app alfafaa-knowledge-hub:local
```

## Run With Explicit Context

```bash
docker run --rm -v "$PWD:/app" -w /app \
  alfafaa-knowledge-hub:local \
  --docs-root examples/sample-project-repo/docs \
  --branch main \
  --event push
```

## Docker Compose

Run with:

```bash
docker compose run --rm knowledge-hub
```

Or with explicit arguments:

```bash
docker compose run --rm knowledge-hub \
  --docs-root examples/sample-project-repo/docs \
  --branch main \
  --event push
```

## Why This Dockerization Is Correct

The project is currently a pipeline/tooling system, not a long-running server.

So the right first containerization model is:

- containerized pipeline runner
- mounted workspace
- reproducible dependency set

This is better than pretending the project is already a web service.

## Later Docker Extensions

When Quartz is added as a real app/runtime, you can extend this into:

- one build container for the pipeline
- one Quartz build/runtime container per target
- one reverse-proxy container for internal/public routing

## Current Recommendation

Use Docker now for:

- local reproducibility
- CI parity
- VPS execution consistency

Keep deployment hosting decisions separate from the pipeline container for now.
