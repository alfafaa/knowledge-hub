# Ultimate Company-Level Folder Structure

## Purpose

This document defines the final recommended structure for the central company knowledge hub.

It is designed to be:

- stable for many years
- flexible across products, teams, and business changes
- understandable by engineering, product, operations, support, and leadership
- detailed enough to capture real company knowledge
- structured enough to support automation, publishing, and governance

This is the structure for the `central hub`, not for individual project repositories.

## Core Principle

The company-level structure should answer:

- where company-wide truth lives
- where product and project context lives
- where reusable standards live
- where public and internal knowledge is published from

It should not become a dumping ground for random notes.

## Design Rules

1. Top-level domains should change very rarely.
2. Second-level structure should be standardized and meaningful.
3. Deeper folders can expand per domain when needed.
4. Use metadata for visibility, ownership, and publishing rules.
5. Put implementation-coupled docs in project repositories, not in the central hub.
6. Prefer domain ownership at the folder level and knowledge views at the navigation level.

## Final Structure

```text
hub/
  00-governance/
    metadata-schema.md
    writing-style.md
    publishing-policy.md
    taxonomy.md
    review-lifecycle-policy.md
    templates/
    examples/

  01-company/
    strategy/
      vision.md
      principles.md
      roadmap.md
    business/
      sales/
      marketing/
      finance/
      legal/
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
      roadmap.md
      requirements/
      research/
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

  09-resources/
    external-docs/
    articles/
    tools/
    competitors/

  10-relationships/
    clients/
    partners/
    accounts/
    stakeholder-context/

  98-meta/
    assets/
    workflows/
    publishing/
    workspace-notes/

  90-archive/
  99-templates/
```

## What Each Top-Level Domain Is For

### `00-governance/`

Use for:

- the rules of the knowledge system itself
- metadata schemas
- style rules
- publishing rules
- lifecycle and review policy
- taxonomy and template standards

This is the operating system of the hub.

Without this domain, the hub becomes inconsistent very quickly.

### `01-company/`

Use for:

- company-wide strategy
- business function knowledge and operating models
- policies
- cross-functional operating processes
- principles that apply beyond one product or team

Best for:

- long-lived organizational truth

Do not use for:

- product-specific details
- repo-specific technical implementation docs

Recommended second-level split:

- `strategy/`
  - direction and long-term priorities
- `business/`
  - function-owned knowledge for sales, marketing, finance, legal
- `policies/`
  - rules and governance
- `processes/`
  - cross-functional workflows

### `02-products/`

Use for:

- long-lived product context
- user segments and use cases
- requirements and research
- product roadmap
- product-level releases
- links to repos and support materials

Best for:

- documenting the `why`, `who`, and `what` of a product

This is where business context and product context stay durable even when repositories change.

### `03-projects/`

Use for:

- cross-functional initiatives
- execution-focused work that may span several repos or teams
- milestones
- stakeholders
- project-level decisions
- involved repositories

Best for:

- temporary but important execution spaces

Projects end. Products often do not. That is why products and projects should stay separate.

### `04-engineering/`

Use for:

- company-wide engineering standards
- shared platform guidance
- shared patterns
- reusable runbooks
- common integration guidance

Best for:

- reusable technical knowledge that should not be duplicated in every repo

This is the cross-repository engineering brain.

### `05-operations/`

Use for:

- release management processes
- incident management process
- reliability standards
- continuity and disaster planning

Best for:

- company-wide operational practice

Repo-specific operations still belong in project repositories. This domain is for shared operational governance.

### `06-support/`

Use for:

- public knowledge base content
- internal support documentation
- troubleshooting flows
- FAQ collections

Best for:

- customer support and service operations
- published help content

This is often one of the most visible publishing areas.

### `07-security-risk/`

Use for:

- security controls
- security review guidance
- exceptions
- compliance evidence and standards

Best for:

- restricted or carefully governed documentation

This domain often needs stricter publishing rules and approval controls.

### `08-people-enablement/`

Use for:

- onboarding
- role guides
- training
- team ways-of-working

Best for:

- helping new people become effective faster
- scaling knowledge across team changes

### `09-resources/`

Use for:

- curated external references
- vendor or third-party documentation links
- useful articles and reports
- tool evaluations and comparison material
- competitor intelligence that should remain searchable

Best for:

- reference collections that support product, engineering, strategy, or operations

Important rule:

- this should be a curated library, not a dumping ground

If a resource changes company behavior, extract the learning into the owning domain instead of leaving only a link here.

### `10-relationships/`

Use for:

- client-facing context that is safe to keep in the hub
- partner knowledge
- account-specific implementation context
- stakeholder context for important long-lived relationships

Best for:

- B2B companies
- service businesses
- platform teams managing strategic integrations or enterprise accounts

Important rule:

- do not treat this as a CRM replacement
- highly sensitive commercial information should follow stricter access rules or stay in systems built for that purpose

### `98-meta/`

Use for:

- vault-level operational support files
- shared media reused across many company-level pages
- workspace notes about how the knowledge system is run
- publishing helpers and workflow notes

Best for:

- Obsidian-friendly workspace support
- cross-domain shared assets
- maintaining vault usability without mixing support files into content domains

Important rule:

- `98-meta/` supports the hub, but it is not itself the business content home
- do not store normal product, project, engineering, support, or company documents here

### `98-meta/assets/`

Use for:

- shared logos
- repeated screenshots
- reusable diagrams
- icons or visuals used across multiple company-level pages

Do not use for:

- page-specific screenshots that belong to a single document
- product- or project-specific assets that should stay near their owning content

### `90-archive/`

Use for:

- deprecated policies
- retired project spaces
- old standards
- superseded documents that still need historical trace

Do not leave old content mixed with active guidance.

### `99-templates/`

Use for:

- page templates
- domain templates
- product templates
- project templates
- project-repo docs templates

This is the factory for consistency.

## Detailed Use Cases By Domain

### Strategy vs Product vs Project

This distinction prevents the most common documentation confusion.

Use `01-company/strategy/` for:

- company vision
- multi-year priorities
- organization-wide principles

Use `01-company/business/` for:

- sales playbooks
- pricing and packaging logic
- marketing positioning
- campaign process
- finance operating guidance
- commercial rules
- legal templates or policy references that are not purely compliance controls

Use `02-products/` for:

- product context
- users
- requirements
- product roadmap

Use `03-projects/` for:

- specific delivery initiatives
- execution tracking
- short-to-medium-term milestones

Analogy:

- company = the business map
- product = the permanent business line
- project = the current mission

### Meta And Assets vs Content Domains

This distinction matters if the company wants to work comfortably in Obsidian.

Use `98-meta/` for:

- workspace helpers
- shared supporting files
- reusable assets

Use content domains for:

- actual knowledge
- canonical documentation
- business, product, project, support, and engineering content

Rule:

- `98-meta/` should improve editing and publishing workflows
- it should not become an alternative content hierarchy

### Business Functions vs Product Context

This is important for long-term clarity.

Use `01-company/business/sales/` for:

- universal sales process
- qualification rules
- pricing framework
- proposal standards
- enterprise sales playbooks

Use `01-company/business/marketing/` for:

- brand and messaging standards
- GTM process
- campaign frameworks
- channel strategy

Use `01-company/business/finance/` for:

- budgeting frameworks
- finance SOPs
- procurement process
- cost control guidance
- reporting logic

Use `02-products/<product-slug>/` for:

- product-specific positioning
- product roadmap
- user segments
- use cases
- release narratives

Rule:

- if the knowledge belongs to a business function regardless of product, keep it in `01-company/business/`
- if the knowledge belongs to one product, keep it in `02-products/`

### Knowledge Base As A View, Not A Root

Your earlier `Knowledge Base` idea is still useful, but it should be implemented as a navigation and discovery layer, not necessarily as one giant top-level folder.

Recommended model:

- engineering knowledge lives under `04-engineering/`
- support knowledge lives under `06-support/`
- onboarding knowledge lives under `08-people-enablement/`
- external references live under `09-resources/`
- client or partner knowledge lives under `10-relationships/`

Then the hub can generate a `Knowledge Base` view by:

- tags
- indexes
- owner pages
- topic pages
- search filters

This is more durable than storing all reusable intelligence under one mixed folder.

### Engineering Standards vs Repo Docs

Use `04-engineering/` for:

- standards that apply to many repositories
- shared platform practices
- common patterns

Use project repositories for:

- implementation-coupled technical docs
- service-specific architecture
- service-specific runbooks
- repo-local decisions

This separation is essential. Otherwise the hub becomes stale and duplicates repo docs.

### Support vs Public Product Docs

Use `06-support/public-kb/` for:

- help center content
- troubleshooting for users
- FAQ and guides intended for customers

Use `02-products/` for:

- product context, roadmap, requirements, and audience understanding

The product area explains the product. The support area helps users operate it.

### Resources vs Canonical Knowledge

Use `09-resources/` for:

- inputs from outside the company
- article notes
- tool references
- competitor references

Do not use it for:

- final company policy
- final engineering standards
- final product truth

Those should live in their owning domains after the resource has been interpreted.

### Relationships vs Product/Project Space

Use `10-relationships/` for:

- relationship-specific knowledge that spans time and workstreams
- implementation context tied to important clients or partners
- cross-functional context useful beyond one temporary project

Do not use it for:

- temporary delivery work
- generic account records better stored in CRM tools
- detailed repo-specific implementation docs

## Large-Scale Expansion Model

For a growing company, deeper nested structure is useful, but only under stable top-level domains.

Example expansion:

```text
04-engineering/
  standards/
    backend/
    frontend/
    platform/
    data/
    security/
  platform/
    ci-cd/
    observability/
    cloud/
    internal-developer-platform/
  patterns/
    auth/
    caching/
    messaging/
    tenancy/

06-support/
  public-kb/
    product-a/
    product-b/
  internal-kb/
    escalation/
    support-operations/
  troubleshooting/
    billing/
    auth/
    email/

01-company/
  business/
    sales/
      playbooks/
      pricing/
      proposals/
      qualification/
    marketing/
      positioning/
      campaigns/
      brand/
      channels/
    finance/
      budgeting/
      procurement/
      controls/
      reporting/
    legal/
      templates/
      reviews/
      agreements/

09-resources/
  external-docs/
    cloud/
    framework/
    vendor/
  articles/
    engineering/
    product/
    operations/
  tools/
    evaluations/
    standards/
  competitors/
    market-notes/
    product-comparisons/

10-relationships/
  clients/
    client-slug/
      _index.md
      context.md
      integrations.md
      constraints.md
  partners/
    partner-slug/
      _index.md
      contact-model.md
      integration-model.md

98-meta/
  assets/
    brand/
    common-diagrams/
    shared-screenshots/
  workflows/
    publishing.md
    sync-operations.md
  publishing/
    navigation-notes.md
    obsidian-usage.md
  workspace-notes/
    conventions.md
```

This is the right way to scale:

- stable top levels
- richer domain depth
- no uncontrolled sprawl at the root

## What Should Not Live In The Central Hub

Avoid placing these here as canonical content:

- repo-specific setup steps
- service-specific deployment procedures
- implementation details tightly coupled to code
- low-level API contract files as the primary source
- transient engineering scratch notes

Avoid putting these in the hub without stricter governance:

- secrets
- contractual data without access controls
- HR-sensitive people records
- detailed CRM data

Avoid using `98-meta/` for:

- ordinary business documents
- ordinary project documents
- engineering standards
- support knowledge

Those belong in project repositories and can be indexed or mirrored into the hub if needed.

## Publishing And Access Use Cases

The central hub is where visibility rules become practical.

Common outputs:

- `public-site`
  - support content
  - product usage documentation
  - selected release notes
- `internal-site`
  - policies
  - product context
  - projects
  - cross-functional process docs
- `engineering-site`
  - shared engineering standards
  - selected mirrored repo docs
  - shared runbooks and patterns

This is why the hub structure must be clean. It is not just for storage. It is also the publishing control plane.

## Recommended Ownership Model

Each top-level domain should have a steward:

- `00-governance/` -> documentation platform owner
- `01-company/` -> leadership, operations, or business-function owner
- `02-products/` -> product owner or PM group
- `03-projects/` -> project owner or program lead
- `04-engineering/` -> engineering leadership or platform team
- `05-operations/` -> operations or SRE owner
- `06-support/` -> support owner
- `07-security-risk/` -> security/compliance owner
- `08-people-enablement/` -> people ops or enablement owner
- `09-resources/` -> domain librarians or designated owners
- `10-relationships/` -> account/program/business owner
- `98-meta/` -> documentation platform or workspace owner

Without domain ownership, even a good structure will decay.

## Rules To Prevent Confusion

1. Do not add new top-level folders casually.
2. Put each document where its canonical owner lives.
3. Keep implementation-coupled docs in repositories.
4. Use products for long-lived product truth and projects for execution truth.
5. Use metadata for visibility and publishing, not folder names alone.
6. Archive retired content instead of deleting history.
7. Treat `Knowledge Base` as a generated view across domains, not necessarily as one folder.
8. Use `98-meta/` only for workspace support and shared assets, not as a parallel content tree.

## Final Recommendation

If the project-level structure is the workshop, the company-level structure is the library and control center.

A good team member should be able to guess the correct destination in seconds:

- company rules: `00-governance/`
- company direction: `01-company/`
- business functions: `01-company/business/`
- product truth: `02-products/`
- initiative execution: `03-projects/`
- shared engineering knowledge: `04-engineering/`
- operational governance: `05-operations/`
- support knowledge: `06-support/`
- security and compliance: `07-security-risk/`
- onboarding and training: `08-people-enablement/`
- curated external references: `09-resources/`
- clients, partners, and long-lived relationship context: `10-relationships/`
- workspace support and shared assets: `98-meta/`
