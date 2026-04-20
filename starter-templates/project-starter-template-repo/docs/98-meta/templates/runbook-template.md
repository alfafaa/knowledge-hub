---
title: Runbook Template
type: guide
status: draft
publish: false
---

# Runbook Template

Copy this into `docs/05-operations/runbooks/` for operational recovery, incident handling, or repeated operational tasks.

Recommended frontmatter for a real runbook:

```yaml
---
title: Recover Failed Payment Retry Queue
type: runbook
status: approved
owner: team-operations
publish: true
audience: engineering
visibility: internal
publish_targets:
  - engineering-site
---
```

## Purpose

What operational problem does this runbook solve?

## When To Use

Describe the trigger conditions.

## Preconditions

- required access
- required tools
- required environment knowledge

## Procedure

1. step 1
2. step 2
3. step 3

## Verification

How do you know the recovery or operation succeeded?

## Rollback Or Escalation

What should happen if the procedure fails?

## Related Links

Link dashboards, alerts, services, and design docs.
