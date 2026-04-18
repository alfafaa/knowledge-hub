# Infrastructure Recommendation For Central Knowledge Hub

## Purpose

This document defines the recommended infrastructure model for the central company knowledge hub.

It answers:

- where the central documentation should live
- how admins and managers should use it with Obsidian
- where Quartz and sync automation should run
- where backups and assets should be stored
- how to support future role-based access control safely

## Final Recommendation

Use this model:

- `private Git repository` as the canonical source of truth
- `VPS` as the runtime layer for sync, Quartz publishing, and access control
- `Hetzner Object Storage` for backups, assets, and build artifacts
- `Hetzner Storage Box` only for backup/archive or shared file access if needed

This is the cleanest long-term setup.

## Why This Model Is Best

Because your system needs all of these at once:

- version control
- collaboration
- automation
- Obsidian editing
- future access control
- public and internal publishing

No single storage product solves all of that cleanly by itself.

So the right approach is to separate responsibilities.

## Recommended Responsibility Split

### 1. Private Git Repository

Use as:

- the canonical source of truth
- the place where central hub markdown, templates, and config live
- the place where sync automation writes mirrored docs

Best options:

- GitHub private repository
- GitLab private repository
- self-hosted Gitea or GitLab on a VPS

Why Git should be primary:

- full history
- branching and review
- easy automation
- good fit for docs-as-code
- works well with Obsidian because Obsidian can open normal folders

## 2. VPS

Use as:

- the runtime host for Quartz builds
- the sync pipeline execution environment
- the auth and reverse-proxy layer
- optional self-hosted Git service host

The VPS is where the system becomes operational.

Typical responsibilities:

- pull from Git
- build Quartz sites
- run validation
- resolve sync rules
- publish to public/internal/engineering/admin outputs
- enforce SSO or access policies through a proxy or portal layer

## 3. Hetzner Object Storage

Use as:

- backup destination
- artifact storage
- static media/object storage
- exported site bundle storage
- long-term backup of snapshots

Good for:

- build outputs
- backup archives
- shared media files
- disaster recovery copies

Do not use as:

- the main authoring location
- the canonical documentation source

## 4. Hetzner Storage Box

Use only if you specifically need:

- backup over SFTP/rsync/WebDAV
- simple file archive
- shared file access for operational reasons

Good for:

- offsite backup
- archive storage
- manual recovery access

Do not use as:

- the central authoring platform
- the main docs governance layer

## Recommended Architecture

```text
Authors
  -> local working copies in Obsidian
  -> commit to private Git repo

Project Repos
  -> docs in each repo
  -> sync to central hub repo

Central Hub Git Repo
  -> canonical company hub content
  -> templates
  -> metadata
  -> mirrored docs

VPS
  -> validation
  -> sync resolver
  -> Quartz builds
  -> SSO/reverse proxy
  -> internal/public/admin publishing

Hetzner Object Storage
  -> backups
  -> artifacts
  -> static shared assets
  -> exported bundles

Hetzner Storage Box
  -> optional backup/archive layer
```

## Obsidian Usage Model

Admins, managers, and knowledge owners should use the Git repository through a local folder opened in Obsidian.

Recommended workflow:

1. clone the private central hub repo locally
2. open that folder in Obsidian
3. edit notes normally
4. commit and push through Git or a Git plugin
5. let the VPS pipeline validate and publish

This works well because Obsidian edits normal markdown folders.

Important rule:

- Obsidian is the editing interface
- Git is the source of truth
- Quartz or internal portals are the reading interface

## Why Not Use Object Storage Or Storage Box As The Main Source

Because they are storage systems, not documentation workflow systems.

Problems:

- weak authoring workflow
- no native version review workflow like Git
- harder automation for selective doc sync
- harder metadata governance
- poor fit for docs-as-code branching and review

They are excellent support layers, but not the best canonical layer.

## Future Role-Based Access Control

If you want future restricted access by folder or role, Git storage alone is not the right enforcement point.

Use this model:

- keep source docs in Git
- use metadata to classify visibility and audience
- sync and publish to different site outputs
- enforce access in the delivery layer

Recommended outputs:

- `public-site`
- `internal-site`
- `engineering-site`
- `admin-site`

For highly sensitive material, consider:

- separate restricted repository
- or separate restricted publish target

This is safer than trying to secure folders inside one static file store.

## Recommended Hosting Paths

### Smallest Practical Setup

- private GitHub or GitLab repo
- one VPS for Quartz builds and internal hosting
- Hetzner Object Storage for backups

### More Controlled Setup

- self-hosted Gitea on VPS
- CI runner on VPS
- Quartz sites on VPS
- reverse proxy with SSO
- Hetzner Object Storage for backups and artifacts

### Higher Security Setup

- separate public and internal deployment targets
- separate admin/restricted site
- optional separate restricted repo for finance/legal/security docs
- Object Storage for encrypted backups

## Recommended Repository Strategy

Use at least these repositories:

- `knowledge-hub-central`
  - company hub content
  - templates
  - governance
- project repositories
  - repo-local docs
- optional restricted repository
  - finance/legal/security content if needed later

This gives you room to scale into stronger security later.

## Best-Practice Recommendation

If you want the most future-proof model:

1. keep canonical docs in private Git
2. let people edit through Obsidian on local clones
3. run publishing and sync from a VPS
4. store backups and large artifacts in Hetzner Object Storage
5. use Storage Box only if you need an extra archive/file-access layer

## Final Answer

The central docs should primarily live in a private Git repository.

That is the best place for:

- Obsidian-based editing
- version history
- structured automation
- selective sync from project repos
- future publishing and RBAC support

The VPS should run the system.

Hetzner Object Storage and Storage Box should support the system, not replace its source of truth.
