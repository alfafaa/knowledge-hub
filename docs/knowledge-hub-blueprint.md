# Knowledge Hub Blueprint

## Purpose

Build a company knowledge system that stays usable for years, scales across products and teams, and reduces documentation friction instead of increasing it.

This blueprint assumes:

- Git-based project repositories
- Markdown as the primary authoring format
- CI/CD available for automation
- Static publishing preferred over manual portal editing

## Recommended Strategic Model

Use a `federated source, centralized distribution` model.

- `Federated source`: each team keeps code-near docs in its own repository.
- `Centralized distribution`: a central hub ingests, validates, indexes, and publishes docs for different audiences.

This is the durable split:

- Project repos own the `how`
  - architecture details
  - ADRs
  - runbooks
  - API specs
  - troubleshooting
  - release notes tied to code
- Central hub owns the `company-wide why and where`
  - standards
  - product catalog
  - cross-repo navigation
  - governance
  - public knowledge base
  - company processes and policies

Analogy: each project repo is a specialist clinic; the hub is the hospital record system. Doctors work locally, but the patient history still needs one reliable place.

## Non-Negotiable Principles

1. Documentation must live as close as possible to the thing that changes it.
2. Publishing must be driven by metadata and policy, not manual copy-paste.
3. Every published page must have an owner and review cycle.
4. Internal and public visibility must be explicit.
5. Historical records should be versioned, superseded, or archived, not overwritten without trace.

## Canonical Knowledge Domains

Design the central hub around domains that survive org changes.

```text
00-governance/
01-company/
02-products/
03-projects/
04-engineering/
05-operations/
06-support/
07-security-risk/
08-people-enablement/
90-archive/
99-templates/
```

### What belongs in each domain

- `00-governance/`
  - writing standards
  - metadata schema
  - publishing policy
  - review policy
  - taxonomy
- `01-company/`
  - vision
  - strategy
  - org model
  - business processes
- `02-products/`
  - product overviews
  - PRDs
  - customer-facing concepts
  - lifecycle status
- `03-projects/`
  - cross-functional initiative pages
  - milestones
  - stakeholder summaries
  - repo index pages
- `04-engineering/`
  - engineering standards
  - architecture principles
  - platform guides
  - shared runbooks
- `05-operations/`
  - release operations
  - incident processes
  - vendor and infrastructure operations
- `06-support/`
  - KB articles
  - troubleshooting guides
  - FAQs
  - escalation flows
- `07-security-risk/`
  - policies
  - controls
  - review evidence
  - exception logs
- `08-people-enablement/`
  - onboarding
  - role guides
  - handbooks
  - training material
- `90-archive/`
  - retired content kept for audit and history
- `99-templates/`
  - standard page templates and examples

## How Much Structure Is Healthy

Yes, the company-level and project-level structures should be more detailed than a minimal sketch, but not infinitely detailed at the top level.

The durable pattern is:

- make the top-level structure stable and easy to memorize
- make second-level structure opinionated and rich
- make deeper structure optional and metadata-driven

If you try to pre-create a folder for every possible future scenario, the system becomes harder to use, and people stop following it. Future-proofing comes from `clear rules + optional extensions`, not from endless folders.

## Audience and Visibility Model

Do not model visibility as folders alone. Model it as policy plus metadata.

Recommended visibility classes:

- `public`
  - end-user help
  - usage guides
  - API docs intended for customers
  - release notes suitable for customers
- `internal`
  - company-wide internal docs
  - product plans
  - internal SOPs
- `restricted`
  - sensitive docs for named groups only
  - security details
  - commercial data
  - vendor contracts
- `engineering`
  - developer docs, ADRs, runbooks, architecture notes

Recommended audience fields:

- `audience: public`
- `audience: internal`
- `audience: engineering`
- `audience: restricted`

Recommended access fields:

- `access_groups: []`
- `publish_targets: [public-site, internal-site]`

## Source-of-Truth Rules

Use this decision table.

| Content type | Canonical home | Reason |
|---|---|---|
| API specs | project repo | changes with code |
| ADRs | project repo | tied to implementation decisions |
| Runbooks | project repo or platform repo | operationally coupled |
| PRDs | central hub product area | cross-functional ownership |
| Company policy | central hub | corporate ownership |
| Customer help content | central hub, optionally mirrored from repos | audience-driven publishing |
| Incident postmortems | project/platform repo with central index | local detail, central discoverability |
| Team playbooks | central hub | reused across repos |

## Recommended Project Repository Standard

Your proposed structure includes several good ideas worth keeping:

- overview and glossary pages
- ADRs as a first-class area
- testing broken down by depth
- separate releases from raw changelogs
- security and observability documentation
- integrations and operational knowledge

The main adjustment is this:

- product context like personas and use cases should not be mandatory in every engineering repo
- project repos should be optimized for implementation-coupled docs
- broader business context should live in the central product and project domains

Use this layered repository standard.

### Mandatory in every engineering repo

```text
docs/
  _index.md
  01-getting-started/
  02-architecture/
  03-decisions/
  04-development/
  05-operations/
  06-reference/
  07-release/
  90-archive/
```

### Recommended when relevant

```text
docs/
  00-overview/
  08-quality/
  09-knowledge/
  10-integrations/
```

### Detailed project repo structure

```text
docs/
  _index.md
  docs.config.yaml

  00-overview/
    vision.md
    scope.md
    glossary.md
    repositories.md

  01-getting-started/
    setup.md
    installation.md
    environment.md

  02-architecture/
    system-design.md
    data-design.md
    api-design.md
    security-architecture.md
    observability-architecture.md

  03-decisions/
    adr-001-<slug>.md
    adr-002-<slug>.md
    rfc-001-<slug>.md

  04-development/
    coding-standards.md
    git-workflow.md
    local-development.md
    feature-flags.md
    migration-guides.md

  05-operations/
    deployment.md
    rollback.md
    ci-cd.md
    monitoring.md
    logging.md
    alerting.md
    runbooks/
    incident-response.md
    backup-recovery.md
    secrets-management.md

  06-reference/
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

  07-release/
    release-notes/
    changelog.md

  08-quality/
    testing/
      strategy.md
      unit.md
      integration.md
      e2e.md
    performance.md
    security-testing.md

  09-knowledge/
    learnings/
    pitfalls/
    playbooks/
    troubleshooting/

  10-integrations/
    integration-template.md
    stripe.md
    email.md
    analytics.md

  90-archive/
```

### Practical rule for project repos

Not every repo needs every folder on day one.

Create a folder only when one of these is true:

- it is required by the engineering standard
- the repo has at least two documents of that kind
- automation or publishing depends on that category

This avoids empty-folder theater.

## Recommended Central Hub Structure

```text
hub/
  00-governance/
    metadata-schema.md
    writing-style.md
    publishing-policy.md
    lifecycle-policy.md
    taxonomy.md
    templates/
    examples/
  01-company/
    strategy/
      vision.md
      principles.md
      roadmap.md
    policies/
      security-policy.md
      data-policy.md
      communication-policy.md
    processes/
      engineering.md
      product.md
      support.md
      operations.md
  02-products/
    product-slug/
      _index.md
      product-overview.md
      audience.md
      personas.md
      use-cases.md
      glossary.md
      requirements/
      research/
      roadmap.md
      releases/
      links.md
  03-projects/
    project-slug/
      _index.md
      initiative-overview.md
      scope.md
      stakeholders.md
      milestones.md
      decisions.md
      repositories.md
  04-engineering/
    standards/
      coding/
      architecture/
      testing/
      api/
    platform/
      developer-experience/
      infrastructure/
      shared-services/
    shared-runbooks/
    patterns/
    integrations/
  05-operations/
    release-management/
    incident-management/
    reliability/
    business-continuity/
  06-support/
    public-kb/
    internal-kb/
    troubleshooting/
    faq/
  07-security-risk/
    controls/
    reviews/
    exceptions/
    compliance/
  08-people-enablement/
    onboarding/
    role-guides/
    training/
    ways-of-working/
  90-archive/
  99-templates/
```

### Practical rule for the central hub

The central hub can be more detailed than project repos because it is the cross-company navigation layer. Still, keep only the first two levels standardized globally. Below that, allow products and domains to extend as needed.

## Long-Term Scalability Rules

- Keep top-level domains stable for years.
- Allow products, projects, and teams to change underneath them.
- Avoid folder names tied to current org charts unless they are under a clearly temporary branch.
- Prefer slugs over human-formatted numbering in long-lived paths.
- Use metadata for classification; use folders for primary ownership and navigation.

Bad long-term pattern:

- `engineering-team-new-final-2026/`

Good long-term pattern:

- `04-engineering/platform/authentication/`

## Recommendation on Quartz and Obsidian

Use Quartz as the publishing layer for public and internal knowledge sites.

Use Obsidian only if you want:

- an editor for markdown authors
- wikilinks during drafting
- personal or team vault workflows before publication

Do not make Obsidian Publish your core company platform if you need durable automation and granular enterprise access control. It is better treated as a publishing convenience tool than a long-term governance platform.

## Final Recommendation

Adopt this operating model:

1. `Repos own technical truth`
2. `Central hub owns discovery, governance, and cross-functional truth`
3. `Automation moves approved docs to the right audience`
4. `Quartz publishes audience-specific sites from the same metadata model`
5. `Review cycles and ownership prevent documentation rot`
