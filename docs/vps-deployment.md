# VPS Deployment

## Purpose

This document defines the first VPS-oriented deployment step for the Alfafaa Knowledge Hub.

It focuses on:

- taking packaged deployable targets
- extracting them into VPS-style runtime directories
- preserving previous deployments safely
- keeping the actual hosting/proxy layer separate

## Files

The VPS deployment layer now includes:

- [deploy.vps.yaml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/deploy.vps.yaml)
- [scripts/deploy_to_vps.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/deploy_to_vps.py)
- [deploy/templates/Caddyfile.template](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/deploy/templates/Caddyfile.template)
- [deploy/templates/nginx-sites.template.conf](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/deploy/templates/nginx-sites.template.conf)

## Core Model

The current VPS deployment step is filesystem-based.

That means:

- package allowed targets
- extract them into target directories
- preserve previous versions when enabled

This is the correct first step because it works:

- locally for verification
- on a VPS directly
- over SSH later
- from CI artifacts

## Current Config

Default target configuration:

- `internal-site` -> enabled
- `engineering-site` -> enabled
- `public-site` -> disabled
- `admin-site` -> disabled

This matches the current approval model.

## Local Verification Command

```bash
python3 scripts/deploy_to_vps.py
```

This reads:

- `build/deploy/deploy-execution-report.json`
- `deploy.vps.yaml`

And writes:

- `build/deploy/vps-deploy-report.json`
- extracted runtime directories under `deploy/runtime/`

## Current Runtime Shape

With the default config, deploy targets land under:

- `deploy/runtime/internal-site/current`
- `deploy/runtime/engineering-site/current`

The packaged content is now flattened correctly, so `current/` is the real site root.

## Preserve Previous

If `preserve_previous: true`, the deploy step renames the old `current` directory to:

- `<target>/current-previous`

before replacing it.

This gives you a simple rollback-friendly pattern.

## Why This Is Useful

This step gives you a practical deploy contract before you add:

- Nginx
- Caddy
- SSO proxy
- public CDN/object-storage publishing
- preview environment routing

## Next VPS Layer

After this, the next logical additions are:

- reverse proxy config generation
- per-target web root layout
- internal/public hostname mapping
- SSH-based remote execution

Starter reverse-proxy templates are now included for:

- Caddy
- Nginx

## Recommendation

Use this current VPS deploy step as the first runtime handoff:

- CI builds and packages
- VPS extracts and switches current directories
- proxy/web server serves the chosen target roots
