# Quartz Runtime Integration

## Purpose

This document defines the real Quartz build integration for `Alfafaa Knowledge Hub`.

The earlier pipeline stopped at Quartz-ready workspaces. The current pipeline now goes further and produces deployable static site output.

## Added Runtime Layer

The Quartz runtime layer now includes:

- [quartz/app/README.md](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/quartz/app/README.md)
- [scripts/build_quartz_sites.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/build_quartz_sites.py)
- [build/rendered/summary.json](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/build/rendered/summary.json)

## Current Flow

The end-to-end pipeline now runs:

1. validation
2. ingestion
3. publish planning
4. Quartz workspace preparation
5. Quartz static rendering
6. deployment planning
7. nginx config generation
8. deployment packaging
9. VPS deployment extraction

## Build Inputs

Quartz still consumes the generated workspace content:

- `quartz/workspaces/<target>/content`

But before build, the pipeline copies that content into:

- `build/quartz-sources/<target>/content`

This gives the build step a clean source root and lets the pipeline generate a target landing page when a root `index.md` is missing.

## Build Outputs

Deployable static outputs now land under:

- `build/rendered/public-site/`
- `build/rendered/internal-site/`
- `build/rendered/engineering-site/`
- `build/rendered/admin-site/`

Those outputs contain real deployable assets such as:

- `index.html`
- `index.css`
- `prescript.js`
- `postscript.js`
- `static/`
- nested HTML pages for the generated docs
- linked documentation assets such as images and PDFs when they are mirrored with the owning document

## Quartz App Adjustments

The integrated Quartz app now uses pipeline-safe defaults:

- page title is driven by environment variables
- base URL is driven by environment variables
- analytics is disabled
- network-dependent OG image generation is disabled by default

This is important because the pipeline should build reliably in local, CI, and staging environments.

## Deployment Contract

The deployment plan now points to rendered static site roots, not just Quartz workspaces.

That means packaged deploy artifacts now contain real static site files that can be served directly by nginx.

## Recommendation

Treat this as the canonical publish path:

- source markdown lives in repos and the hub
- Quartz workspaces remain an intermediate content stage
- rendered static output is the deployable runtime artifact

For media-specific behavior, see:

- [Media And Asset Handling](docs/media-and-asset-handling.md)
