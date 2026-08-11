---
type: feature
nav_path: "Marketing → Discounts → Container codes → Parent terms & plan-gating"
route_name: discounts-codes_list
route_path: /admin/marketing-new/discounts/codes
aliases: ["Container code parent terms", "Container codes plan-gating", "Container codes uses counter", "Percent-value cap", "Container code delete cascade", "Наследени условия от контейнер", "Брояч на използвания"]
tags: [marketing, discounts, coupons, container, plan-gating, uses-counter]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Container codes — inherited terms, cap, plan-gating & uses counter

> Part of [[marketing-discounts-codes]]. See the hub for the list view, generator, redemption, and the JSON-API.

## Purpose

A generated Container code is a thin leaf row. Almost everything that governs how it behaves — the target, the customer-group restriction, the date window, the redemption cap — comes from the **parent Container discount**, not the code. This aspect documents what each code inherits, the percent-value cap enforced at generation, the `discount_coupon` plan-gating, the delete cascade, and the parent's recomputed `uses` counter.

## Where to find it

The parent Container discount is edited from the [[marketing-discounts]] table (its own discount-edit form). The generated codes hang off it and are listed at `/admin/marketing-new/discounts/codes` — see [[discounts-codes-list-view]].

## What the merchant can do here

- **Set the campaign terms once on the parent** (target, customer group, dates, redemption cap) and have every generated code inherit them.
- **Run successive batches at different values** under one parent (e.g., "1,000 codes at 10%, then 500 codes at 15%") — each code captures its own `type` + `value` at generation time.
- **Rely on the parent's `uses` counter** to track total redemptions across all of its codes.

## Settings & fields

The fields that matter live on the **parent** Container discount record. Each generated code row itself carries only:

| Field | What it holds |
|-------|---------------|
| `code` | The literal string the customer types. |
| `type` + `value` | Captured at generation time, so successive batches can differ. |
| `active` | Per-row toggle (see [[discounts-codes-list-view]]). |

## Business rules

### Codes inherit the parent Container's terms (and date window)

Each generated code is its own row, but the **business terms** come from the parent Container discount the codes are attached to: target, customer-group restriction, `date_start`, `date_end`, and the redemption count that rolls up to the parent's cap. When the customer enters a Container code at checkout, the platform redeems THIS row's `value` against the cart, then marks the row inactive (single-use — see [[discounts-codes-redemption]]). The parent continues to host more codes until they're all consumed.

### Percent-value cap — bounded by max Container type-value in store

When generating percent codes, the value is validated against the highest percentage any Container discount in the store has set on its parent record. This prevents the merchant from generating a 90%-off batch on a Container discount whose parent only allows 15% off, which would be inconsistent. The cap is enforced in the generator — see [[discounts-codes-generator]].

### Plan-gating — `discount_coupon`

Container codes are a **code-based discount**, so the parent Container counts against the `discount_coupon` **usage counter** (shared with single promo-code discounts) — the "used / limit" figure for code-based discounts. In the modern Discounts panel this counter does **not** hard-block creating the parent (only the Discount code (PRO) card is plan-gated at create — see [[marketing-discounts]] → Plan gates); the [[json-api-v2]] create path enforces the quota server-side. Once the parent exists, generating codes inside it has **no further per-code plan limit**.

### Bulk-delete cascade

Deleting a Container code from the list removes that code row directly. The parent Container discount is untouched. Historical order-discount rows that reference the deleted code remain in place for accounting. (The list-side delete mechanics are on [[discounts-codes-list-view]].)

### Uses counter — recompute, not increment

The `uses` counter on the **parent** Container discount is **recomputed from scratch** every time an associated order's status changes — not incremented per redemption. The recompute counts orders in the [[settings-statuses|counted statuses]] (default `paid` / `completed` / `fulfilled`). Practical effect:

- If a previously-counted order is **cancelled / refunded** later, the counter **automatically decrements** to reflect the new state — even if `max_uses` was previously reached, redemptions can become available again.
- Conversely, recovering a cancelled order back to a counted status re-counts it.

The sync runs with a 10-second delay after each order status change (queue: `order-events6`).

## Related

- [[marketing-discounts-codes]] — hub.
- [[discount]] — entity page for the parent Container discount.
- [[settings-statuses]] — the counted statuses the `uses` recompute reads.
- [[plan-gates]] — `discount_coupon` plan feature.

## Open questions

No outstanding questions.
