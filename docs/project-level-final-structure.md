# Ultimate Project-Level Folder Structure

## Purpose

This document defines the final recommended documentation structure for a project or repository.

It is designed to be:

- clear for developers
- scalable for long-lived systems
- flexible across services, apps, platforms, and internal tools
- strict enough for consistency
- light enough to avoid confusion

The main rule is simple:

- standardize the important categories
- do not force empty folders
- create deeper sections only when the repository actually needs them

This means the structure is intentionally `core-first`, not `everything-first`.

That was deliberate, but for large and complex repositories, the structure should explicitly define an expansion path so engineers know where planning, research, feature work, and deeper operational material belong.

## Design Principles

1. Docs that change with code should live in the project repository.
2. Every repo should have the same high-level mental model.
3. Not every repo needs every subfolder.
4. Mandatory folders should exist in almost all engineering repos.
5. Recommended and optional folders should be created only when useful.

## Final Structure

```text
docs/
  _index.md
  docs.config.yaml

  00-overview/                 # recommended
    vision.md
    scope.md
    glossary.md
    repositories.md

  01-getting-started/          # mandatory
    setup.md
    installation.md
    environment.md

  02-architecture/            # mandatory
    system-design.md
    data-design.md
    api-design.md
    security-architecture.md
    observability-architecture.md

  03-decisions/               # mandatory
    adr-001-<slug>.md
    adr-002-<slug>.md
    rfc-001-<slug>.md

  04-development/             # mandatory
    coding-standards.md
    git-workflow.md
    local-development.md
    feature-flags.md
    migration-guides.md
    features/
    patterns/

  05-operations/              # mandatory
    deployment.md
    rollback.md
    ci-cd.md
    monitoring.md
    logging.md
    alerting.md
    incident-response.md
    backup-recovery.md
    secrets-management.md
    runbooks/

  06-reference/               # mandatory
    api/
      overview.md
      standards.md
      versioning.md
      endpoints/
      examples/
    database/
      schema.md
      migrations.md
    config/
      environment-variables.md
      permissions.md

  07-release/                 # mandatory
    changelog.md
    release-notes/

  08-quality/                 # recommended
    testing/
      strategy.md
      unit.md
      integration.md
      e2e.md
    performance.md
    security-testing.md

  09-knowledge/               # recommended
    learnings/
    pitfalls/
    playbooks/
    troubleshooting/

  10-integrations/            # optional
    integration-template.md
    stripe.md
    email.md
    analytics.md

  11-guides/                  # optional but strongly recommended for product-facing repos
    public/
      getting-started/
      usage/
      faq/
      troubleshooting/
      release-notes/
    internal/
      admin/
      operations/
      support/
      workflows/
    engineering/
      contributor/
      handoff/
      service-usage/

  98-meta/                    # optional
    assets/
    templates/
    workspace-notes/

  90-archive/                 # mandatory
```

## Folder Classification

### Mandatory

These should exist in almost every engineering repo:

- `01-getting-started/`
- `02-architecture/`
- `03-decisions/`
- `04-development/`
- `05-operations/`
- `06-reference/`
- `07-release/`
- `90-archive/`

### Recommended

Create these when the repo has enough complexity to justify them:

- `00-overview/`
- `08-quality/`
- `09-knowledge/`

### Optional

Create only when the repo actually uses these concerns:

- `10-integrations/`
- `11-guides/`
- `98-meta/`

## Detailed Use Cases

### `_index.md`

Use for:

- the main entry page for repository documentation
- quick links to the most important sections
- owner, status, and summary of the system

Do not use for:

- storing detailed architecture or operational steps

### `docs.config.yaml`

Use for:

- identifying repo type
- declaring which sections are mandatory or active
- enabling automation and validation rules later

Do not use for:

- human-readable documentation

### `00-overview/`

Use for:

- stable business or service context
- clarifying what the system is and why it exists
- glossary and important shared terms

Best for:

- core services
- major products
- shared platforms
- repositories that many teams touch

Skip it when:

- the repo is very small and the purpose is already obvious
- the broader product context lives clearly in the central hub

### `01-getting-started/`

Use for:

- local setup
- installation
- environment requirements
- developer bootstrap instructions

Best for:

- onboarding new engineers quickly
- reducing tribal setup knowledge

Without this folder, repos become expensive to join.

### `02-architecture/`

Use for:

- current system design
- boundaries between components
- data model explanations
- API shape and system flows
- security and observability architecture

Best for:

- explaining the current state of the system
- helping engineers reason about change safely

Do not use for:

- historical debates or decision logs

Those belong in `03-decisions/`.

### `03-decisions/`

Use for:

- ADRs
- RFCs
- major technical trade-offs
- changes that need traceable reasoning

Best for:

- architecture decisions
- infrastructure choices
- service boundaries
- migration plans

This folder is one of the highest long-term value areas in the repo.

### `04-development/`

Use for:

- repo-specific coding rules
- branching or git workflow notes
- local development patterns
- feature flag conventions
- migration or change procedures

Best for:

- things developers need while actively working in the codebase

Do not duplicate:

- global engineering standards from the central hub unless the repo has local exceptions

Recommended nested folders for larger repos:

- `features/`
  - feature-specific implementation notes
  - rollout details
  - constraints and edge cases
- `patterns/`
  - reusable repo-specific implementation patterns
  - examples that are too local for the central engineering hub

### `05-operations/`

Use for:

- deployment and rollback
- CI/CD behavior
- monitoring and alerting setup
- runbooks
- incident response
- recovery and secrets handling

Best for:

- SRE, DevOps, and on-call engineers
- operational continuity

If the service can fail in production, this folder matters.

Recommended nested folders when operations are complex:

- `runbooks/`
  - one procedure per operational task or incident class
- `monitoring/`
  - dashboards, SLO notes, metric definitions
- `recovery/`
  - restore, failover, backup, disaster recovery
- `security/`
  - service-level operational security procedures

### `06-reference/`

Use for:

- API references
- schema documentation
- config and permissions reference
- stable technical facts

Best for:

- information people need to look up repeatedly
- source-adjacent documentation such as OpenAPI and schema docs

Think of this as the repo encyclopedia.

### `07-release/`

Use for:

- raw changelog tracking
- human-readable release notes
- release communication history

Best for:

- separating machine-like change history from curated release summaries

Rule:

- `changelog.md` is append-only and factual
- `release-notes/` is curated and audience-oriented

### `08-quality/`

Use for:

- testing strategy
- unit, integration, and end-to-end guidance
- performance expectations
- security testing notes

Best for:

- systems with complex testing needs
- teams that need consistent quality gates

Skip it when:

- quality rules are trivial or fully inherited from a company-wide standard

### `09-knowledge/`

Use for:

- lessons learned
- recurring pitfalls
- troubleshooting patterns
- reusable playbooks

Best for:

- reducing repeated mistakes
- preserving operational learning
- helping future engineers understand the system faster

This is where teams convert experience into reusable company knowledge.

### `10-integrations/`

Use for:

- third-party systems
- external services
- internal platform dependencies
- integration-specific constraints and playbooks

Best for:

- repos that rely on payment providers, email vendors, analytics tools, auth systems, or external APIs

Skip it when:

- integrations are minimal or already fully covered elsewhere

### `11-guides/`

Use for:

- audience-specific guidance that developers maintain close to the product or service
- internal workflow guides
- public usage guides
- admin/operator instructions
- engineering consumer guidance for other teams using the service

Best for:

- product repositories
- platform repositories consumed by other teams
- systems where usage guidance changes together with implementation

Recommended nested audiences:

- `public/`
  - customer-facing help, onboarding, feature usage, FAQ, public troubleshooting
- `internal/`
  - internal workflows, admin steps, support playbooks, operational procedures for non-engineering readers
- `engineering/`
  - contributor handoff, integration usage, service consumer guidance, internal engineering how-tos

Important rule:

- `11-guides/` is for audience-facing guidance
- `06-reference/` is for factual technical reference
- `05-operations/` is for operating the system itself

If you mix those together, the docs become hard to navigate.

### `98-meta/`

Use for:

- repository-level documentation support files
- shared media reused across several docs in the repo
- repo-specific templates or workspace notes
- Obsidian-friendly support files for authors

Best for:

- keeping shared assets in one predictable place when multiple repo docs reuse them

Do not use for:

- normal architecture, development, operations, reference, or guide documents
- dumping temporary notes that should not live long term

### `98-meta/assets/`

Use for:

- repeated diagrams
- shared screenshots
- repo-wide icons or visuals

Do not use for:

- media used by only one page when local colocated assets are clearer

## Large-Scale Extension Profile

If the repository is large, long-lived, or operated by multiple engineers or teams, expand the core structure with these nested areas.

```text
docs/
  00-overview/
    vision.md
    scope.md
    glossary.md
    repositories.md

  01-getting-started/
    setup.md
    installation.md
    environment.md
    quick-start.md

  02-architecture/
    system-design.md
    context-diagram.md
    container-diagram.md
    component-diagram.md
    data-design.md
    api-design.md
    security-architecture.md
    observability-architecture.md
    research/
      solution-options.md
      trade-off-analysis.md
      constraints.md

  03-decisions/
    adr/
    rfc/

  04-development/
    coding-standards.md
    git-workflow.md
    local-development.md
    feature-flags.md
    migration-guides.md
    features/
      feature-name/
        overview.md
        design.md
        rollout.md
        known-issues.md
    patterns/
      pattern-name.md

  05-operations/
    deployment.md
    rollback.md
    ci-cd.md
    monitoring/
    logging/
    alerting/
    runbooks/
    recovery/
    security/

  06-reference/
    api/
    database/
    config/

  07-release/
    changelog.md
    release-notes/
      2026/

  08-quality/
    testing/
    performance/
    security-testing/

  09-knowledge/
    learnings/
    pitfalls/
    playbooks/
    troubleshooting/

  10-integrations/
    third-party-name.md

  11-guides/
    public/
      getting-started/
      usage/
      faq/
      troubleshooting/
    internal/
      admin/
      operations/
      support/
      workflows/
    engineering/
      contributor/
      service-usage/

  98-meta/
    assets/
      diagrams/
      screenshots/
    templates/
    workspace-notes/

  90-archive/
```

## Where Planning And Research Should Live

This is the part that needs precision.

### Planning

Project-level planning can exist in a repository, but only when it is tightly coupled to implementation.

Good repo-local planning examples:

- migration plan for a database change
- rollout plan for a major feature
- implementation sequencing for a service split

These should usually live in:

- `03-decisions/rfc/`
- `04-development/features/<feature-name>/`

Broader planning should usually stay outside the repo in the central hub:

- business roadmap
- stakeholder planning
- product prioritization
- cross-team initiative planning

### Research

Research can be useful in a repo, but only technical research that directly supports implementation.

Good repo-local research examples:

- comparing queue technologies
- evaluating auth approaches
- benchmarking storage options

These should usually live in:

- `02-architecture/research/`
- or be summarized and formalized into `03-decisions/`

Broad user, market, or product research should live in the central hub, not in engineering repos.

## Why It Was Not Added As Mandatory Everywhere

Because if you make `plan`, `research`, `features`, `reviews`, `communication`, and similar categories mandatory in all repos, you create two problems:

1. Small and medium repositories become cluttered with empty or overlapping folders.
2. Engineers stop knowing whether a document belongs in `plan`, `research`, `architecture`, `decisions`, or `development`.

That is why the right model is:

- `core mandatory structure for all repos`
- `explicit extension profile for large repos`
- `central hub for business and cross-functional material`

## Recommended Rule Of Thumb

Use this split:

- if it explains the current technical system: `02-architecture/`
- if it records why a choice was made: `03-decisions/`
- if it describes implementing a specific feature: `04-development/features/`
- if it explains how to operate or recover the system: `05-operations/` and `05-operations/runbooks/`
- if it explains how a specific audience should use or work with the system: `11-guides/`
- if it is a shared support file, reusable media, or workspace helper for docs authors: `98-meta/`
- if it is broad product or business planning: central hub, not repo docs

## Universal Audience Guide Model

To keep the structure universal and flexible, treat `11-guides/` as an audience layer rather than a product-specific layer.

That means the same model works for:

- SaaS products
- internal tools
- platform services
- APIs
- admin portals
- support systems

Recommended audience mapping:

- `11-guides/public/`
  - external end-user or customer-facing guidance
- `11-guides/internal/`
  - internal business users, admins, operations, and support teams
- `11-guides/engineering/`
  - engineers using, extending, integrating with, or contributing to the system

This is more universal than folders like `user-docs/` or `admin-docs/` alone, because different repositories serve different audiences.

## Scenario Examples

### Scenario 1: Customer-Facing SaaS App

Useful guide folders:

- `11-guides/public/getting-started/`
- `11-guides/public/usage/`
- `11-guides/public/faq/`
- `11-guides/internal/support/`
- `11-guides/internal/admin/`

### Scenario 2: Internal Admin System

Useful guide folders:

- `11-guides/internal/workflows/`
- `11-guides/internal/operations/`
- `11-guides/engineering/contributor/`

### Scenario 3: Shared Platform Service

Useful guide folders:

- `11-guides/engineering/service-usage/`
- `11-guides/engineering/handoff/`
- `11-guides/internal/operations/`

### Scenario 4: Public API Or SDK Repo

Useful guide folders:

- `11-guides/public/getting-started/`
- `11-guides/public/usage/`
- `11-guides/engineering/service-usage/`

## Publishing Recommendations For `11-guides/`

Recommended defaults:

- `11-guides/public/**`
  - candidate for `public-site`
- `11-guides/internal/**`
  - candidate for `internal-site`
- `11-guides/engineering/**`
  - candidate for `engineering-site`

Still require:

- owner
- review cycle
- approved status
- policy checks

### `90-archive/`

Use for:

- deprecated docs
- replaced guides
- historical material that should remain discoverable

Best for:

- preserving history without polluting active navigation

Rule:

- do not delete important historical docs unless there is a legal or security reason

## Recommended Usage By Repository Type

### Backend Service

Usually create:

- `01-getting-started/`
- `02-architecture/`
- `03-decisions/`
- `04-development/`
- `05-operations/`
- `06-reference/`
- `07-release/`
- `08-quality/`
- `09-knowledge/`
- `10-integrations/` if external dependencies exist

### Frontend App

Usually create:

- `01-getting-started/`
- `02-architecture/`
- `03-decisions/`
- `04-development/`
- `05-operations/`
- `06-reference/`
- `07-release/`
- `08-quality/`

Often optional:

- `09-knowledge/`
- `10-integrations/`

### Shared Platform Or Infrastructure Repo

Usually create:

- `00-overview/`
- `01-getting-started/`
- `02-architecture/`
- `03-decisions/`
- `04-development/`
- `05-operations/`
- `06-reference/`
- `07-release/`
- `08-quality/`
- `09-knowledge/`
- `10-integrations/`

### Small Internal Tool

Usually create:

- `01-getting-started/`
- `02-architecture/`
- `03-decisions/`
- `04-development/`
- `05-operations/`
- `07-release/`

Often skip at first:

- `00-overview/`
- `08-quality/`
- `09-knowledge/`
- `10-integrations/`

## Rules To Prevent Confusion

1. Do not create folders just because the template shows them.
2. Do not put the same topic in multiple places.
3. Put historical reasoning in `03-decisions/`, not `02-architecture/`.
4. Put operational steps in `05-operations/`, not random markdown files in the repo root.
5. Put reusable facts in `06-reference/`, not inside meeting notes.
6. Move dead content to `90-archive/` instead of leaving it mixed with active docs.

## Final Recommendation

If you want a structure that lasts for years, optimize for recognition, not exhaustiveness.

A good developer should be able to guess where a document belongs in a few seconds:

- how to start: `01-getting-started/`
- how it works: `02-architecture/`
- why it was chosen: `03-decisions/`
- how to work on it: `04-development/`
- how to run and recover it: `05-operations/`
- facts and specs: `06-reference/`
- what changed: `07-release/`
- how quality is handled: `08-quality/`
- what the team learned: `09-knowledge/`
- how outside systems connect: `10-integrations/`
