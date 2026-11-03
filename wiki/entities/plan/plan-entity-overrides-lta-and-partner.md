---
type: entity
nav_path: "Entity → Plan → LTA + partner overrides"
aliases: ["LTA contract override", "Long-term agreement plan", "Partner network plan", "UniCredit plan", "Reseller plan", "Profile dropdown plan link"]
tags: [entity, billing, plans, contracts, partner, lta]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 0
---

> Part of [[plan]]. See the hub for the other aspects (catalog structure, billing cycles, feature restrictions, lifecycle, free-plan expiry + demo).

# Plan — LTA + partner overrides

## Identity

Two override layers that sit ABOVE the standard [[plan-entity-catalog-structure|catalog]] / [[plan-entity-feature-restrictions|feature restrictions]] for specific merchant segments:

1. **Long-term agreement (LTA) contracts** — a contract with CloudCart holds a plan and often apps, feature packs and one-off services. Each item becomes one of the store's subscriptions, on a monthly cycle at an instalment price, for the contract term.
2. **Partner-network catalog** — when the merchant's site is bound to a reseller (e.g., UniCredit), the catalog is filtered to partner-only plans (type `unicredit` or similar reseller code) and the standard *Choose plan* link in the profile dropdown is hidden.

This page also captures the merchant-facing visibility rules for the *Choose plan* link itself (owner-gated, hidden from non-owner staff, hidden from partner merchants).

## Aliases

- **LTA contract** / **Long-term agreement** — bespoke contract managed via [[contracts]].
- **LTA override** — the contract's billing (monthly cycle, instalment price) in place of each item's own.
- **Partner network** / **Reseller plan** — plans of type `unicredit` (or another partner code) visible only to merchants of that reseller.
- **`reseller_id`** — the Site-level field pointing the merchant at a partner; `reseller_id = 157` is UniCredit.

## Key Attributes

The LTA and partner overrides do NOT live on the Plan record itself — they live elsewhere:

| Source | What it stores | Notes |
|--------|----------------|-------|
| **Plan `type`** | `default` / `unicredit` / per-partner reseller code | Drives the catalog filter on [[plans]]. See [[plan-entity-catalog-structure]] for the type field; this page documents its partner-network use. |
| **Site `reseller_id`** | FK pointing to a partner | When set, the catalog filters to plans of the matching `type`. UniCredit sites carry `reseller_id = 157`. |
| **Contract record** | Items, term (`ends_at`), sale price, monthly price, automatic renewal | Owned by [[contracts]]. Its items are ordinary subscriptions of the store. |

## Business rules

### Partner-network catalog overrides default

When the merchant's site has a partner reseller (e.g., `reseller_id = 157` = UniCredit), the catalog shows ONLY plans of type `unicredit` (the partner-only set). The *Choose plan* link in the profile dropdown is also hidden — partner merchants negotiate plans through the partner relationship, not by browsing the catalog.

Default-catalog plans are completely invisible to a partner merchant. A UniCredit merchant cannot accidentally see (or purchase) a Standard or Pro plan from the default catalog — the filter is applied site-wide on [[plans]].

### LTA contracts override the Plan

If the merchant has an active long-term agreement contract, [[plans]] redirects to the contract details page; the merchant manages their plan via the contract instead. The store's limits come from the plan and add-ons the contract holds, read the same way as on any store ([[plan-gates-lta-contracts]]).

### The end of an LTA contract

A contract with automatic renewal is extended by another term. One without it completes once `ends_at` has passed and every cycle inside the term is paid: plans, apps and feature packs return to their own billing cycle and list price from the first cycle after the term, one-off services are not billed again, and the store's status follows its plan. With a cycle inside the term unpaid, the contract is not completed; renewal keeps retrying and the expiry sweep handles giving up. Full rules, including the penalty invoice: [[contracts]].

### Plan visibility in the profile dropdown is owner-gated

The link to [[plans]] in the profile dropdown is hidden from non-owner staff. Only the store owner sees the *Choose plan* sub-item. Staff with restricted roles see only the current-plan badge in the dropdown. Partner-network merchants don't see the link at all (per the partner-catalog rule above).

Combined with the partner rule: the *Choose plan* link is visible only to (a) the store owner AND (b) on a non-partner site. Everyone else sees the badge only.

### Partner merchants negotiate, they don't self-serve

A partner merchant who wants to change plans contacts their partner (e.g., UniCredit) — not CloudCart directly. The partner co-ordinates the change through CloudCart staff. The merchant never sees [[plans-purchase]] in the partner case; the upgrade is managed externally.

### LTA + partner are independent layers

A merchant can be on an LTA AND be a partner merchant — the contract applies regardless of the partner status. The partner-catalog rule only governs what the merchant *sees* in [[plans]] (and whether the *Choose plan* link appears); the LTA governs what is billed. They compose without conflict.

### The contract drives billing during its term

The contract overwrites each of its subscriptions with a monthly cycle and its instalment price, and those drive the renewal charge and invoice lines. When the contract completes, is cancelled or expires, each item gets its own cycle and list price back, so a later renewal does not bill the instalment. The plan's mapping stays recorded on the [[site|Site]] throughout.

## Where it appears

- [[plans]] — filtered to partner plans for partner sites; redirected to the contract page when an LTA is active.
- [[contracts]] — the LTA management screen for merchants with active long-term agreements.
- Profile dropdown → *Choose plan* link — hidden from non-owners; hidden from partner merchants.
- [[plan-gates-lta-contracts]] — what a contract means for plan gates.

## Related

- [[plan]] — hub.
- [[plan-entity-catalog-structure]] — the Plan `type` field that drives partner filtering.
- [[plan-entity-feature-restrictions]] — what the LTA contract overrides (the same restriction shapes).
- [[contracts]] — LTA management feature.
- [[plans]] — catalog screen (the filter target).
- [[site]] — carries `reseller_id` + active plan-mapping.
- [[plan-gates-lta-contracts]] — what a contract means for plan gates.

## Open Questions

- Whether sites with multiple historical `reseller_id` values can switch back to the default catalog automatically when the partner relationship ends (verify).
