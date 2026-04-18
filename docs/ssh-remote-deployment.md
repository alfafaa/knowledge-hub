# SSH Remote Deployment

## Purpose

This document defines the first SSH-based remote deployment path for the Alfafaa Knowledge Hub.

It focuses on:

- uploading deploy packages to a VPS
- invoking the VPS extraction flow remotely
- keeping the deployment contract package-based
- supporting dry runs before real server execution

## Files

The SSH deployment layer now includes:

- [deploy.ssh.yaml](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/deploy.ssh.yaml)
- [scripts/deploy_via_ssh.py](/media/sibbir/MyDrive/Projects/Office/Alfafaa/knowledge-hub/scripts/deploy_via_ssh.py)

## Core Model

The current remote model is:

1. pipeline packages allowed targets
2. SSH deploy uploads the packages with `rsync`
3. SSH deploy runs a remote extraction script
4. remote VPS runtime switches `current/` directories

This keeps the remote step simple and auditable.

## Dry Run

Start with:

```bash
python3 scripts/deploy_via_ssh.py --dry-run
```

This writes:

- `build/deploy/ssh-deploy-report.json`

without making any network changes.

## Real Run

After setting `deploy.ssh.yaml`:

```bash
python3 scripts/deploy_via_ssh.py
```

## Current Safety Model

- opt-in only
- not part of the default pipeline
- dry-run supported
- target enablement controlled in `deploy.ssh.yaml`

This is the correct way to introduce remote deployment.

## Recommendation

Use the SSH deploy path only after:

- the VPS user exists
- the target directories are ready
- your reverse proxy layout is decided
- you have tested the dry run report
