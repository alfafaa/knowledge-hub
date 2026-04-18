---
id: billing-payment-recovery-runbook
title: Payment Recovery Runbook
type: runbook
audience: engineering
visibility: internal
status: approved
owner: team-billing
publish: true
publish_targets:
  - engineering-site
last_reviewed: 2026-04-04
review_cycle_days: 90
summary: Operational steps for payment recovery failures.
---

# Payment Recovery Runbook

## Trigger

Use this runbook when repeated payment attempts fail for a live customer account and recovery automation has stopped progressing.

## Checks

1. Confirm the latest failure event in the billing ledger.
2. Confirm whether a retry job is still scheduled.
3. Confirm whether the payment gateway returned a hard or soft failure.

## Recovery Steps

1. Check the affected account in the billing admin view.
2. Verify that the latest charge event matches the gateway status.
3. If the failure is retryable, requeue the recovery job once.
4. If the failure is non-retryable, mark the account for support follow-up.
5. Add an incident note with the account id, event id, and action taken.

## Escalate When

- the ledger and payment gateway disagree
- retry jobs are stuck repeatedly
- multiple accounts show the same failure pattern

## Post-Incident

- update the support note with the final outcome
- link any broader incident ticket
- propose a pattern or alert improvement if this was manual-heavy
