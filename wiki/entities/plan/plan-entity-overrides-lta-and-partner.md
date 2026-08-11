---
type: entity
nav_path: "Entity → Plan → LTA + partner overrides"
aliases: ["LTA contract override", "Long-term agreement plan", "Partner network plan", "UniCredit plan", "Reseller plan", "Profile dropdown plan link"]
tags: [entity, billing, plans, contracts, partner, lta]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[plan]]. See the hub for the other aspects (catalog structure, billing cycles, feature restrictions, lifecycle, free-plan expiry + demo).

# Plan — LTA + partner overrides

## Identity

Two override layers that sit ABOVE the standard [[plan-entity-catalog-structure|catalog]] / [[plan-entity-feature-restrictions|feature restrictions]] for specific merchant segments:

1. **Long-term agreement (LTA) contracts** — when a merchant signs a contract with CloudCart, the contract's negotiated feature values supersede the underlying Plan's values for the contract duration. The contract is the source of truth; the Plan is the fallback.
2. **Partner-network catalog** — when the merchant's site is bound to a reseller (e.g., UniCredit), the catalog is filtered to partner-only plans (type `unicredit` or similar reseller code) and the standard *Choose plan* link in the profile dropdown is hidden.

This page also captures the merchant-facing visibility rules for the *Choose plan* link itself (owner-gated, hidden from non-owner staff, hidden from partner merchants).

## Aliases

- **LTA contract** / **Long-term agreement** — bespoke contract managed via [[contracts]].
- **LTA override** — the contract's feature values that supersede the Plan's.
- **Partner network** / **Reseller plan** — plans of type `unicredit` (or another partner code) visible only to merchants of that reseller.
- **`reseller_id`** — the Site-level field pointing the merchant at a partner; `reseller_id = 157` is UniCredit.

## Key Attributes

The LTA and partner overrides do NOT live on the Plan record itself — they live elsewhere:

| Source | What it stores | Notes |
|--------|----------------|-------|
| **Plan `type`** | `default` / `unicredit` / per-partner reseller code | Drives the catalog filter on [[plans]]. See [[plan-entity-catalog-structure]] for the type field; this page documents its partner-network use. |
| **Site `reseller_id`** | FK pointing to a partner | When set, the catalog filters to plans of the matching `type`. UniCredit sites carry `reseller_id = 157`. |
| **Contract record** | LTA-negotiated feature values + duration | Owned by [[contracts]]. Stores its OWN feature restriction values that override the underlying Plan's for the contract's `ends_at` window. |

## Business rules

### Partner-network catalog overrides default

When the merchant's site has a partner reseller (e.g., `reseller_id = 157` = UniCredit), the catalog shows ONLY plans of type `unicredit` (the partner-only set). The *Choose plan* link in the profile dropdown is also hidden — partner merchants negotiate plans through the partner relationship, not by browsing the catalog.

Default-catalog plans are completely invisible to a partner merchant. A UniCredit merchant cannot accidentally see (or purchase) a Standard or Pro plan from the default catalog — the filter is applied site-wide on [[plans]].

### LTA contracts override the Plan

If the merchant has an active long-term agreement contract, [[plans]] redirects to the contract details page; the merchant manages their plan via the contract instead. The contract's feature values override the underlying Plan's values for the contract's duration. When the LTA expires, gates fall back to the underlying Plan's values.

The Plan record itself is unchanged during an LTA — the gate engine reads contract values first, then falls back to Plan values for any feature the contract doesn't explicitly override. This means LTAs can be "partial" (only override a handful of features) — the rest of the Plan still applies as-is.

### LTA contract end has no grace window

When an LTA (Long-Term Agreement) contract reaches `ends_at`, the override drops at that exact timestamp — gates immediately fall back to the underlying Plan's values, with no grace window. CloudCart staff typically extend or renew the contract in advance to avoid the cliff.

This is the only "sharp edge" timestamp in the Plan lifecycle — every other transition (renewal, cancel, expire on retries, free-plan inactivity) has either retries, a graduated warning sequence, or a stays-usable-until-cycle-end grace. The LTA cliff is by design — the contract is a legal instrument with a defined end date, and the gating must honour it exactly.

### Plan visibility in the profile dropdown is owner-gated

The link to [[plans]] in the profile dropdown is hidden from non-owner staff. Only the store owner sees the *Choose plan* sub-item. Staff with restricted roles see only the current-plan badge in the dropdown. Partner-network merchants don't see the link at all (per the partner-catalog rule above).

Combined with the partner rule: the *Choose plan* link is visible only to (a) the store owner AND (b) on a non-partner site. Everyone else sees the badge only.

### Partner merchants negotiate, they don't self-serve

A partner merchant who wants to change plans contacts their partner (e.g., UniCredit) — not CloudCart directly. The partner co-ordinates the change through CloudCart staff. The merchant never sees [[plans-purchase]] in the partner case; the upgrade is managed externally.

### LTA + partner are independent layers

A merchant can be on an LTA AND be a partner merchant — the LTA's feature overrides apply regardless of the partner status. The partner-catalog rule only governs what the merchant *sees* in [[plans]] (and whether the *Choose plan* link appears); the LTA governs what the gates resolve to. They compose without conflict.

### Underlying Plan still drives invoicing during an LTA

The contract's feature values override gate decisions, but the underlying Plan still drives the cycle anniversary, renewal charge, and invoice line items (LTA payments are typically annual upfront, but the underlying plan-mapping is still what the system records on the [[site|Site]]). When the LTA expires and the merchant doesn't renew, the underlying Plan resumes as the source of truth without any explicit migration.

## Where it appears

- [[plans]] — filtered to partner plans for partner sites; redirected to the contract page when an LTA is active.
- [[contracts]] — the LTA management screen for merchants with active long-term agreements.
- Profile dropdown → *Choose plan* link — hidden from non-owners; hidden from partner merchants.
- [[plan-gates]] — the gate-engine consults contract values first, then falls back to Plan values.

## Related

- [[plan]] — hub.
- [[plan-entity-catalog-structure]] — the Plan `type` field that drives partner filtering.
- [[plan-entity-feature-restrictions]] — what the LTA contract overrides (the same restriction shapes).
- [[contracts]] — LTA management feature.
- [[plans]] — catalog screen (the filter target).
- [[site]] — carries `reseller_id` + active plan-mapping.
- [[plan-gates]] — gate-engine resolution order (contract → Plan).

## Open Questions

- Whether LTA contract `ends_at` extensions retroactively apply if processed AFTER the cliff (i.e., the merchant briefly hit Plan-fallback before the extension landed) — verify.
- Whether sites with multiple historical `reseller_id` values can switch back to the default catalog automatically when the partner relationship ends (verify).
