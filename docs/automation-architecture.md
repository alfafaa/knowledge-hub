# Automation Architecture

## Target Outcome

Developers should update docs where they already work. The central system should handle ingestion, validation, classification, publishing, indexing, and retention with minimal manual effort.

## Recommended Architecture

```text
Project Repositories
  -> repo-local docs and metadata
  -> CI validation
  -> sync event

Ingestion Layer
  -> fetch changed docs
  -> validate frontmatter and schema
  -> normalize links and assets
  -> classify by policy

Central Hub Repository / Content Store
  -> canonical aggregated content
  -> search index inputs
  -> ownership and lifecycle metadata

Publishing Layer
  -> public Quartz site
  -> internal Quartz site
  -> engineering Quartz site

Governance Layer
  -> review alerts
  -> stale content reports
  -> publish approvals for restricted material
```

## System Components

### 1. Repo-Local Documentation

Each project repository contains docs in a standard `docs/` layout plus frontmatter metadata.

Required automation at repo level:

- markdown lint
- link check
- frontmatter validation
- required-owner check
- optional docs coverage checks for selected paths

### 2. Sync Trigger

Each repo emits an event when eligible docs change.

Good triggers:

- merge to `main`
- release tag created
- manual publish workflow for sensitive content

Payload should include:

- repository
- commit SHA
- changed file paths
- environment
- actor

## 3. Ingestion Service

The ingestion service can be implemented as:

- GitHub Actions plus a central repo workflow for simple setups
- a small internal service for larger multi-repo environments

Responsibilities:

- pull changed files
- reject invalid metadata
- compute destination path
- preserve source references
- attach commit SHA and timestamp
- route by `publish`, `visibility`, and `publish_targets`

## 4. Central Hub Repository

The central hub should store:

- normalized markdown
- copied assets
- generated indexes
- cross-repo catalog pages
- stale-content reports

Recommended generated path pattern:

```text
content/repos/<repo-slug>/<original-doc-path>.md
content/products/<product-slug>/...
content/projects/<project-slug>/...
```

Do not flatten everything into one folder. Preserve provenance.

## 5. Publishing Strategy

Use separate builds for separate audiences.

Recommended outputs:

- `public-site`
  - only `visibility: public`
- `internal-site`
  - `visibility: internal` and approved public docs
- `engineering-site`
  - `audience: engineering` plus shared internal standards

For stronger access control, put internal and engineering Quartz sites behind SSO or a reverse proxy with group-based access.

## Publishing Rules

### Auto-publish

Allow automatic publishing when all are true:

- `publish: true`
- `status` is `approved` or `active`
- `visibility` is not `restricted`
- validation passes

### Approval-gated publish

Require explicit approval when any are true:

- `visibility: restricted`
- `type: policy` and owner is not final approver
- document contains compliance or security-sensitive areas
- document changes customer-visible guidance in regulated flows

## Versioning Model

You need two kinds of versioning.

### Content history

Use Git history for every source document.

### Published versioning

Version selected docs by:

- product release
- API version
- major policy revision

Recommended version fields:

- `version`
- `effective_date`
- `supersedes`
- `superseded_by`

Not every document needs public version trees. Keep versioned navigation for APIs, product docs, and major standards.

## Search and Discovery

Search quality depends more on metadata and structure than on the UI.

Ensure the system indexes:

- title
- summary
- tags
- body text
- product
- project
- owner
- audience
- status

Also generate:

- product landing pages
- project landing pages
- owner pages
- tag pages

## Governance Model

Assign clear responsibilities.

- Document owner
  - maintains accuracy
- Domain steward
  - maintains taxonomy and standards
- Publisher or approver
  - approves sensitive publication
- Platform owner
  - owns the ingestion and publishing pipeline

## Anti-Rot Controls

This is where most systems fail.

Add these controls from day one:

- stale document alerts from `last_reviewed + review_cycle_days`
- dashboards showing docs without owners
- dashboards showing broken links
- PR checks for required docs in critical repos
- archive workflow for deprecated content
- weekly or monthly domain review reports

## Recommended Rollout Phases

### Phase 1

- define metadata schema
- standardize repo `docs/` layout
- build central hub structure
- publish one internal Quartz site

### Phase 2

- add sync automation from pilot repos
- enforce linting and validation
- add search, tags, and generated indexes

### Phase 3

- split public and internal publishing
- add approval workflow for restricted docs
- add stale-content governance

### Phase 4

- add product versioning
- add usage analytics
- add service catalog and ownership views

## Best-Practice Summary

- Keep creation local, governance central, and publishing automated.
- Use metadata as the policy engine.
- Keep access control outside the markdown editor and inside your delivery layer.
- Treat docs like product assets, not side notes.
- Optimize for low-friction updates and strong downstream automation.
