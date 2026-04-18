# Staging Deployment

## Current Staging Server

The current test staging server is:

- host: `89.167.69.232`
- access path used during setup: `connect test-stg`

## Active Deployment Paths

The current remote deployment root is:

- `/srv/alfafaa-knowledge-hub`

Current active site roots:

- `/srv/alfafaa-knowledge-hub/internal-site/current`
- `/srv/alfafaa-knowledge-hub/engineering-site/current`

## Active nginx Ports

The current staging nginx configuration serves:

- `internal-site` on `http://89.167.69.232:8088/`
- `engineering-site` on `http://89.167.69.232:8089/`

These high ports were chosen to avoid disturbing the existing application already bound into the server's current runtime.

## Files

The current staging deployment layer includes:

- [deploy.ssh.yaml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/deploy.ssh.yaml)
- [deploy.nginx.yaml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/deploy.nginx.yaml)
- [scripts/deploy_via_ssh.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/deploy_via_ssh.py)
- [scripts/generate_nginx_config.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/generate_nginx_config.py)
- [build/deploy/nginx/alfafaa-knowledge-hub-staging.conf](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/build/deploy/nginx/alfafaa-knowledge-hub-staging.conf)

## Current Commands

Build and stage locally:

```bash
python3 scripts/run_pipeline.py \
  --docs-root examples/sample-project-repo/docs \
  --branch main \
  --event push
```

Upload staged packages to the VPS:

```bash
python3 scripts/deploy_via_ssh.py
```

Regenerate nginx config locally:

```bash
python3 scripts/generate_nginx_config.py
```

## Current Status

Verified working:

- SSH package upload
- remote extraction
- nginx config installation
- nginx reload
- external HTTP reachability on staging ports

## Recommendation

Use this staging layer as the safe integration environment before:

- adding DNS-backed hostnames
- enabling TLS
- publishing `public-site`
- enabling `admin-site`
- adding SSO and restricted access enforcement
