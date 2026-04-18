# Final Implementation Plan

## Purpose

This document converts the knowledge hub design into an executable implementation plan.

It answers:

- what to build first
- what depends on what
- how to roll the system out safely
- how to avoid overbuilding too early
- how to move from design to production

## Final Goal

Build a centralized company knowledge hub where:

- teams write docs inside their own repositories
- selected docs sync automatically to a central hub
- public, internal, engineering, and admin content publish safely
- admins and managers can work in Obsidian
- governance, structure, versioning, and RBAC remain maintainable over time

## Implementation Strategy

Use a phased rollout.

Do not try to build everything at once.

Build in this order:

1. foundation
2. validation
3. sync and routing
4. publishing
5. access control
6. migration and scale

This reduces risk and gives you a working system early.

## Phase 0: Finalize Canonical Decisions

### Objective

Lock the key operating decisions before coding starts.

### Deliverables

- approve company-level structure
- approve project-level structure
- approve sync model
- approve config model
- approve access model
- approve storage/infrastructure model

### Output

Treat the following documents as canonical inputs:

- `docs/company-level-final-structure.md`
- `docs/project-level-final-structure.md`
- `docs/docs-config-spec.md`
- `docs/sync-model-project-to-company-hub.md`
- `docs/sync-resolution-rules-and-path-mapping.md`
- `docs/access-control-and-role-based-publishing.md`
- `docs/infrastructure-recommendation-for-central-knowledge-hub.md`

### Exit Criteria

- no open structural questions that block implementation

## Phase 1: Build The Foundation Repository

### Objective

Turn the current design repository into the real central hub base.

### Tasks

- keep `hub/` as the canonical central content root
- keep `99-templates/` as the template source
- add implementation directories:
  - `schemas/`
  - `scripts/`
  - `examples/`
  - `build/` if needed later
- define one official metadata schema
- define one official `docs.config.yaml` schema

### Deliverables

- schema files for frontmatter and repo config
- example company content
- example product
- example project
- example synced repo subtree

### Exit Criteria

- the repository contains executable schema definitions, not only prose docs

## Phase 2: Implement Validation

### Objective

Reject invalid structure and unsafe metadata before sync or publish.

### Tasks

- implement frontmatter validation
- implement `docs.config.yaml` validation
- implement folder-structure validation
- implement deprecated-structure warnings
- implement `docs_version` handling

### Validator Should Check

- required frontmatter fields
- allowed enum values
- ownership presence
- review metadata presence
- supported `docs_version`
- allowed publish targets
- allowed visibility values
- valid destination mappings
- duplicate or conflicting rules

### Deliverables

- CLI validator
- machine-readable validation output
- warning vs error classification

### Exit Criteria

- one repo can be validated locally and in CI

## Phase 3: Implement Sync Resolver

### Objective

Build the engine that decides what happens to each doc.

### Tasks

- read changed files from a repo
- evaluate `include` and `exclude`
- apply `overrides`
- resolve destination path
- apply frontmatter overrides when allowed
- determine `local-only`, `indexed-only`, or `mirrored`
- compute final publish targets

### Resolver Rules

- most specific destination match wins
- frontmatter cannot bypass central policy
- restricted docs require approval path
- relative subtree must be preserved
- missing destination directories should auto-create minimally

### Deliverables

- sync resolution module
- dry-run output mode
- per-file sync decision report

### Exit Criteria

- given a repo and changed file set, the system can compute the exact action for every file

## Phase 4: Implement Central Hub Ingestion

### Objective

Write resolved content into the hub safely and predictably.

### Tasks

- create destination folders if missing
- mirror content into resolved paths
- preserve provenance fields
- support indexed-only catalog entries
- maintain source repo and source path references
- avoid duplicate conflicting writes

### Deliverables

- ingestion logic
- mirrored content writer
- metadata catalog for indexed-only docs
- provenance fields in mirrored content

### Exit Criteria

- synced docs arrive in the correct hub location with traceable origin

## Phase 5: Build Quartz Publishing

### Objective

Turn central content into usable reading portals.

### Initial Recommendation

Start with:

- `internal-site`

Then expand to:

- `engineering-site`
- `public-site`
- `admin-site`

### Tasks

- configure Quartz against the hub content
- define navigation strategy
- define generated views
- define audience-specific builds
- ensure Obsidian-friendly markdown renders correctly

### Required Generated Views

- product index
- project index
- engineering ADR index
- support knowledge index
- owner/reviewer dashboard pages if feasible

### Deliverables

- first working internal Quartz site
- audience-separated build configuration
- generated landing pages

### Exit Criteria

- internal users can browse central docs meaningfully

## Phase 6: Implement Access Control

### Objective

Protect audience-specific content safely.

### Recommended Order

1. public site without auth
2. internal site behind SSO
3. engineering site with group restriction
4. admin site with restricted groups

### Tasks

- define SSO provider integration
- map `access_groups` to real identity groups
- protect audience-specific sites
- ensure search indexing respects visibility boundaries

### Deliverables

- role/group mapping document
- protected internal and engineering delivery
- protected admin delivery for restricted content

### Exit Criteria

- restricted docs are not accessible outside allowed groups

## Phase 7: Pilot Rollout

### Objective

Prove the system on a small number of real repositories.

### Recommended Pilot Set

- 1 backend service repo
- 1 frontend app repo
- 1 internal/admin system repo
- central hub repo

### Tasks

- add `docs.config.yaml` to pilot repos
- align pilot repo docs to the standard
- enable validation in CI
- enable sync into central hub
- publish first internal site

### Success Signals

- docs sync without manual copying
- managers can read in the hub
- developers still write locally
- routing and metadata work in real cases

## Phase 8: Add Migration Support

### Objective

Make the system safe for long-term evolution.

### Tasks

- implement support for at least two config versions
- add deprecated-structure warnings
- create migration helper scripts
- publish compatibility matrix

### Deliverables

- migration scripts
- upgrade checklist
- compatibility reporting

### Exit Criteria

- older repos can coexist with newer ones without breaking sync

## Phase 9: Scale To Company-Wide Adoption

### Objective

Move from pilot to company standard.

### Tasks

- create onboarding guide for engineers
- create onboarding guide for admins/managers using Obsidian
- create team adoption checklist
- publish templates for new repos
- make validator part of default repo setup

### Deliverables

- rollout guide
- onboarding docs
- default starter template usage

### Exit Criteria

- new repositories start with the standard by default

## Recommended Technical Workstreams

Run the implementation in these workstreams.

### Workstream A: Schema And Validation

Owns:

- frontmatter schema
- `docs.config.yaml` schema
- validator
- deprecation warnings

### Workstream B: Sync And Routing

Owns:

- include/exclude logic
- override logic
- destination mapping
- path resolution
- mirrored/indexed/local-only decisions

### Workstream C: Publishing

Owns:

- Quartz setup
- audience-specific builds
- generated navigation and indexes

### Workstream D: Access Control

Owns:

- SSO
- group mapping
- protected delivery
- restricted publishing workflow

### Workstream E: Adoption And Governance

Owns:

- templates
- onboarding
- migration
- versioning policy

## Recommended MVP

Do not make the first version too large.

### MVP Scope

- one frontmatter schema
- one `docs.config.yaml` schema
- local validator
- sync resolver
- central hub ingestion
- one internal Quartz site
- one pilot repo syncing successfully

### Exclude From MVP

- perfect multi-site RBAC
- full migration tooling
- advanced analytics
- large-scale search optimization

Those can come after the system works end-to-end.

## Key Risks

### Risk 1: Overengineering Before Adoption

Mitigation:

- build MVP first
- validate on real repos

### Risk 2: Too Many Exceptions

Mitigation:

- prefer config defaults over per-document overrides
- require justification for special routing

### Risk 3: Docs Rot

Mitigation:

- owner field
- review cycle
- stale-doc reporting

### Risk 4: Public Exposure Mistakes

Mitigation:

- require approval for public content
- separate site builds
- strict validation

### Risk 5: Confusing Structure

Mitigation:

- keep top-level stable
- keep templates current
- onboard teams with examples

## Recommended Timeline

### Stage 1

- Phase 1
- Phase 2

### Stage 2

- Phase 3
- Phase 4

### Stage 3

- Phase 5
- Phase 7

### Stage 4

- Phase 6
- Phase 8
- Phase 9

## Final Execution Order

Build in this order:

1. schemas
2. validator
3. sync resolver
4. ingestion
5. internal Quartz site
6. pilot rollout
7. access control expansion
8. migration support
9. company-wide adoption

## Final Recommendation

The best next step is not more design.

It is to start implementation with a strict MVP:

- schema
- validator
- sync resolver
- central ingestion
- one internal site

Once that works end-to-end on one or two real repositories, the rest of the system can scale safely.
