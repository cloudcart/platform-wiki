---
type: feature
nav_path: "Marketing → Discounts → Container codes → Parent terms & plan-gating"
route_name: discounts-codes_list
route_path: /admin/marketing/discounts/codes, /admin/marketing/discounts/create/container
aliases: ["Container code parent terms", "Container codes plan-gating", "Container codes uses counter", "Percent-value cap", "Container code delete cascade", "Наследени условия от контейнер", "Брояч на използвания"]
tags: [marketing, discounts, coupons, container, plan-gating, uses-counter]
plan_gates: ["discount-container", "discount_global"]
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

# Container codes — Container terms, value limit, plan-gating & uses counter

> Part of [[marketing-discounts-codes]]. See the hub for the list view, generator, redemption, and the JSON-API.

## Purpose

A generated Container code is a thin row attached to no Container discount. What governs how it behaves — the target, the region, the date window, the customer-group restriction (verify) — comes from the **Container discount that wins at checkout**, not the code. This aspect documents what a code carries, how the winning Container is chosen, its value limit, plan-gating, deleting codes, and the Container's recounted `uses` counter.

## Where to find it

A Container discount is edited from the [[marketing-discounts]] table (its own discount-edit form). The generated codes are one store-wide list at `/admin/marketing/discounts/codes` — see [[discounts-codes-list-view]].

## What the merchant can do here

- **Set the terms on a Container discount** (target, customer group (verify), region, dates). They apply to any code when that Container wins at checkout.
- **Run successive batches at different percents** (e.g., "1,000 codes at 10%, then 500 codes at 15%") — each code keeps its own `type` + `value`.
- **Read a Container's `uses` counter** to see how many orders used it.

## Settings & fields

The fields that matter live on the **Container** discount record. Each generated code row itself carries only:

| Field | What it holds |
|-------|---------------|
| `code` | The literal string the customer types. |
| `type` + `value` | Captured at generation time, so successive batches can differ. |
| `active` | Per-row toggle (see [[discounts-codes-list-view]]). |

## Business rules

### Codes take their terms from the winning Container

Container codes are one store-wide pool attached to no Container. At checkout all active Containers for the customer's region try the entered codes; the highest total wins, and its target, dates and region apply. The winning Container's customer-group restriction also applies (verify). A code applies only if it fits what remains of that Container's value. An order does not use a code up: it stays reusable until turned off or deleted (see [[discounts-codes-redemption]]).

### Value limit — the Container's value caps the total

Generating codes does not compare the value with any Container. The limit applies at checkout: a Container's value is the maximum total, and codes add up while they fit. That cap is the Container's own **Discount value** field (a percentage) in the **General settings** box of its edit form (English labels; the Bulgarian ones come from the admin's translations); there is no separate cap field. A code larger than what remains is ignored with no error, so a 90% code on a 15% Container gives nothing from that Container.

### Plan-gating

In the admin form, creating a Container checks whether that kind is enabled on the plan (`discount-container`); if not, the response is 403 *"This feature is not enabled for your plan. To access it, please upgrade your plan."* Through [[json-api-v2]], creating a Container compares usage with `discount_global` and returns 402 Payment Required. The `discount_coupon` counter counts only discounts holding their own code, so a Container does not use it. Generating codes has **no plan limit**.

### Deleting codes

Deleting a Container code from the list removes that code row directly. No Container discount changes. Historical order-discount rows that reference the deleted code remain in place for accounting. (The list-side delete mechanics are on [[discounts-codes-list-view]].)

### Uses counter — recompute, not increment

The `uses` counter on each Container discount is **recomputed from scratch** every time an associated order's status changes — not incremented per redemption. The recompute counts orders in the [[settings-statuses|counted statuses]] (default `paid` / `completed` / `fulfilled`). Practical effect:

- If a previously-counted order is **cancelled / refunded** later, the counter **automatically decrements** to reflect the new state.
- Conversely, recovering a cancelled order back to a counted status re-counts it.

The count is redone at each order status change and once more about 10 seconds later.

## Related

- [[marketing-discounts-codes]] — hub.
- [[discount]] — entity page for the Container discount.
- [[settings-statuses]] — the counted statuses the `uses` recompute reads.
- [[plan-gates]] — how plan features are checked.

## Open questions

No outstanding questions.
