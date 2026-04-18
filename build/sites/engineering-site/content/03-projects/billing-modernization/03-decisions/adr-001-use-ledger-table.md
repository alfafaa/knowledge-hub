---
id: billing-adr-001-ledger-table
title: Use Ledger Table For Charge Events
type: adr
audience: engineering
visibility: internal
status: approved
owner: team-billing
publish: true
publish_targets:
  - engineering-site
last_reviewed: 2026-04-04
review_cycle_days: 365
summary: Capture billing events in a ledger model.
---

# ADR-001 Use Ledger Table For Charge Events

## Status

Accepted

## Context

The billing service needs a durable record of charge attempts, retries, reversals, and recovery actions.

A mutable `payments` row makes current-state queries simple, but it weakens traceability and makes post-incident reconstruction harder.

## Decision

We will store billing activity in an append-only ledger table and derive operational state from those events.

## Consequences

Positive:

- event history remains auditable
- reconciliation can be replayed
- recovery workflows become easier to reason about

Trade-offs:

- read models need derivation logic
- simple current-state queries require projection tables or views
- developers must think in events instead of mutable rows

## Follow-up

- add projection rules for account billing state
- define idempotency rules for recovery workers
- document retention and archival policy for ledger events
