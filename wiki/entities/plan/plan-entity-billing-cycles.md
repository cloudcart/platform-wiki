---
type: entity
nav_path: "Entity → Plan → Billing cycles + pricing"
aliases: ["Plan billing cycles", "Plan pricing", "Plan price-detail variants", "Plan currency", "Plan soft-disable", "Monthly yearly 2-year"]
tags: [entity, billing, plans, pricing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[plan]]. See the hub for the other aspects (catalog structure, feature restrictions, lifecycle, free-plan expiry + demo, LTA + partner overrides).

# Plan — Billing cycles + pricing

## Identity

The per-cycle pricing layer of a [[plan|Plan]] — every plan exposes one or more **price-detail variants** (monthly / yearly / 2-year), each with its own price, currency, and active flag. The merchant chooses the cycle on [[plans-purchase]]; the same Plan can offer different combinations of cycles (e.g., a plan available only yearly, or with monthly + yearly but no 2-year).

This page documents the variants themselves, their currency rules, and the soft-disable mechanism CloudCart uses to retire a plan without deleting its catalog record.

## Aliases

- **Billing cycle** — monthly / yearly / 2-year.
- **Price-detail variant** — the per-cycle price record (one variant per (plan × cycle) combination).
- **Currency** — the invoicing currency, bound to the issuer company.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Billing cycle** | Monthly / yearly / 2-year | Per-Plan choice — a Plan may publish any subset of cycles. Each cycle is a separate price-detail variant. |
| **Price** | Per-variant amount | Set per cycle. The cheapest variant per Plan drives the sort order on [[plans]] (see [[plan-entity-catalog-structure]]). |
| **Currency** | Per-variant currency code | Driven by the issuer company's invoicing currency — BGN for BG, EUR for DE, etc. A BG merchant cannot view EUR prices for the BG plan; only the issuer's currency renders. |
| **Active flag** | yes / no per variant | Per-variant published flag. CloudCart soft-disables a plan by deactivating ALL its variants (the plan record stays but it disappears from the catalog). |

A Plan must have **at least one ACTIVE detail variant** to appear in the [[plans]] catalog — this is the mechanism CloudCart uses to retire a plan without deleting the underlying record (existing subscribers continue uninterrupted).

## Business rules

### Soft-disable via deactivating all price variants

To retire a plan from the public catalog while keeping existing subscribers on it, CloudCart deactivates every price-detail variant. The plan record + all its plan-feature restrictions stay intact; the plan simply stops appearing on [[plans]]. Existing subscribers continue on the plan until they switch — there is no auto-migration. New sign-ups can't pick it.

This is different from `Active in catalog = no` (see [[plan-entity-catalog-structure]]), which also hides the plan but is a separate flag.

### Currency is bound to the issuer company

Each price-detail variant's currency is the issuer's invoicing currency — BGN for BG plans, EUR for DE plans, etc. There is **no admin-side currency switcher** on [[plans]]. Each plan card shows the issuer-company's invoicing currency only. A BG merchant cannot view EUR prices for a BG plan; only BGN renders. CloudCart staff create separate plan records per issuer-company when both currencies are needed.

### The cheapest active variant drives sort order

Plans are sorted on [[plans]] by the **lowest** billing-cycle price ascending. A plan with monthly = 50 BGN and yearly = 480 BGN sorts on 50 (the cheapest cycle, not the cheapest per-month-equivalent). This is why long-cycle-only plans tend to land higher in the list — their cheapest cycle is by definition a larger absolute number than a monthly-available competitor.

### Cycle choice is per-purchase, not per-Plan

The merchant chooses the billing cycle at purchase time on [[plans-purchase]]. The same Plan can be bought on different cycles by different merchants — the active subscription record carries the chosen cycle. Switching cycles requires a new purchase (replacing the existing subscription); the same plan, different cycle, is a new subscription record.

### Renewal charges fire on the cycle anniversary

At each `next_billing_date` (one cycle after purchase / last renewal), the saved card on [[billing-cards]] is charged. Cycle-end behaviour is handled by [[subscription-lifecycle]] — this page documents only the variant structure, not the renewal mechanics.

## Where it appears

- [[plans]] — each plan card shows the cheapest active cycle's price as the headline; hovering / expanding reveals the other cycles.
- [[plans-purchase]] — the merchant picks the cycle here. The chosen cycle's price becomes the subscription's recurring charge.
- [[subscriptions-detail]] — the merchant's plan subscription shows the chosen cycle and the next renewal date.
- [[billing-cards]] — the saved card used for renewal charges on the cycle anniversary.

## Related

- [[plan]] — hub.
- [[plans]] — catalog screen.
- [[plans-purchase]] — purchase flow + cycle picker.
- [[subscription-lifecycle]] — renewal mechanics around the cycle anniversary.
- [[billing-cards]] — saved card for renewal charges.
- [[details-billing]] — invoicing details applied to the renewal invoice.

## Open Questions

- Whether per-variant `active = no` removes the cycle from [[plans-purchase]] (the picker) immediately or whether already-set subscriptions on that cycle continue to renew on the deactivated variant (verify).
