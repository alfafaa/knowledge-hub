# Local Runtime Preview

## Purpose

This document defines the local browser preview step for `Alfafaa Knowledge Hub` before any real VPS deployment.

It is the correct testing order because it lets you verify:

- the pipeline output
- the deployed runtime layout
- target routing
- markdown rendering and navigation

without involving SSH, reverse proxies, or a live server.

## Files

The local preview layer now includes:

- [scripts/serve_local_preview.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/serve_local_preview.py)
- [build/local-preview-report.json](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/build/local-preview-report.json)

## Recommended Flow

1. Run the full pipeline.
2. Start the local preview server.
3. Open the generated localhost URLs in a browser.
4. Verify internal and engineering targets locally.
5. Only then move to SSH/VPS deployment.

## Commands

Build the current runtime:

```bash
python3 scripts/run_pipeline.py \
  --docs-root examples/sample-project-repo/docs \
  --branch main \
  --event push
```

Serve it locally:

```bash
python3 scripts/serve_local_preview.py
```

The default preview root is:

```text
http://127.0.0.1:8010/
```

## What It Serves

The preview server reads deployed targets from `deploy/runtime/`.

With the current sample data, it discovers:

- `internal-site`
- `engineering-site`

and exposes them under a single local root:

- `http://127.0.0.1:8010/internal-site/`
- `http://127.0.0.1:8010/engineering-site/`

## Runtime Model

This preview is intentionally lightweight.

It does not try to replace a full Quartz build. Instead, it provides:

- a single local index page
- per-target navigation
- markdown rendering for generated docs
- raw markdown access for inspection

That makes it good for validating the deploy contract before real hosting.

## Useful Options

Use a different port:

```bash
python3 scripts/serve_local_preview.py --port 8090
```

Use an automatic shutdown for scripted checks:

```bash
python3 scripts/serve_local_preview.py --shutdown-after 10
```

## Output Report

The script writes a report to:

- [build/local-preview-report.json](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/build/local-preview-report.json)

That report contains:

- root preview URL
- per-target URLs
- detected content roots
- generated file counts

## Recommendation

Make this the required validation step before:

- SSH deployment
- reverse-proxy setup
- public rollout

It is the lowest-friction way to confirm that the generated runtime is coherent before introducing VPS complexity.
