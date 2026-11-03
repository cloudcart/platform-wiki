---
type: feature
nav_path: "Orders → Order details → Discount → Add"
route_name: admin.orders.discount.add
route_path: /admin/orders/action/discount/:order_id/add
aliases: ["Add order discount", "Order-level discount", "Manual discount", "Apply discount to order", "Order discount management", "Добавяне на отстъпка към поръчка"]
tags: [orders, discount, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---
# Order-level discount (add / delete)

## Purpose

The flow for **applying or removing an ORDER-LEVEL discount** on a specific placed order. Distinct from per-line discounts ([[orders-products]]) — order-level discounts affect the order's subtotal, not specific line items.

Two paths to a discount:

1. **Existing discount** — pick from the merchant's defined [[marketing-discounts]] (rules already created by the merchant). The platform pre-filters to discounts that match the order's customer group + `order_over` threshold + are not banner / label / container types — see [[orders-discount-add-existing-eligibility]].
2. **Manual discount** — type a one-off discount with flat amount OR percentage, applied right now to this order only. Doesn't show up in [[marketing-discounts]] reports — see [[orders-discount-add-manual]].

The merchant uses this when:
- The customer phoned to claim a missed promotion (merchant applies the existing discount manually).
- The merchant negotiated a courtesy discount (e.g., "10% off for the inconvenience" — manual).
- A discount was forgotten at checkout and needs to be added retroactively.

This page is the **hub** for the order-level discount cluster. Each aspect of the flow lives in its own sub-page; drill into the one that matches the question.

## Where to find it

From [[orders-details]] → **Discount action row** in the order summary: an **Add Discount** button when no order-level discount is applied, or a **Remove Discount** button when one IS applied.

Sub-routes:
- `admin.orders.discount.add` (GET / POST) — open form / save.
- `admin.orders.discount.delete` (GET) — remove the order-level discount.
- `admin.orders.modifications.delete` (GET) — remove discount-related modifications.

See [[orders-discount-add-form]] for the modal field inventory and [[orders-discount-add-delete]] for the removal flow.

## What the merchant can do here

- **Add an existing discount** — pick a pre-filtered campaign from [[marketing-discounts]]; its rules apply. See [[orders-discount-add-form]] + [[orders-discount-add-existing-eligibility]].
- **Add a manual discount** — type a one-off flat or percent value. See [[orders-discount-add-manual]].
- **Remove the order-level discount** — restores any consumed usage count on existing discounts. See [[orders-discount-add-delete]].
- **Remove discount-related modifications** — clean up orphan line-level modifications introduced by the discount. See [[orders-discount-add-delete]].

What the merchant **cannot** do here:
- Add a **second** order-level discount — the platform throws *"Order already has a discount"*; remove the existing one first (see Business rules below).
- Add a discount on an **archived** order — throws *"Cannot perform this operation on archived order"*.
- Apply a banner / label / container-type discount, a wrong-customer-group discount, or one whose `order_over` threshold exceeds the subtotal — all filtered out of the picker ([[orders-discount-add-existing-eligibility]]).
- Apply a product- / category- / vendor-targeted discount at order level — only `all` / `order_over` / `shipping` target types appear ([[orders-discount-add-existing-eligibility]]).

## Settings & fields

The Add Discount modal is one `ajaxForm` with a single primary dropdown (**Choose discount**: `existing` / `manual`) that progressively reveals the matching sub-form. Full field-by-field inventory — including the dynamic currency-vs-percent input mask, default type, and the request validator validation — is on [[orders-discount-add-form]].

The existing-discount picker is **pre-filtered** by the backend (customer group, `order_over`, type exclusions, target type, code-less exclusion). The complete filter list and the no-auto-detach behaviour are on [[orders-discount-add-existing-eligibility]]. Manual-discount field rules (flat-less-than-subtotal, percent clamping, fixed label) are on [[orders-discount-add-manual]].

## Sub-pages (in this cluster)

- [[orders-discount-add-form]] — the Add Discount modal: primary dropdown, existing / manual sub-forms, dynamic input mask, the request validator validation, panel-reload chain.
- [[orders-discount-add-existing-eligibility]] — the pre-filter that decides which existing [[marketing-discounts]] appear in the picker; the three allowed target types; threshold no-auto-detach.
- [[orders-discount-add-manual]] — one-off manual discounts: flat-less-than-subtotal rule, percent clamp / no-negative, default Percent type, fixed "Manual discount" label.
- [[orders-discount-add-delete]] — removing the order-level discount + delete-modifications; the browser confirm dialog; usage-count restore.
- [[orders-discount-add-recalculation]] — the add/delete recalculation cascade (re-price → totals → tax → shipping), side effects, `order.updated` webhook, history entries, uses-counter recount.
- [[orders-discount-add-api]] — why add/delete is admin-only; the read-only [[api-order-discount]] resource.

## Business rules

### One order-level discount at a time

The platform enforces ONE order-level discount per order. Before creating, it checks for any non-shipping order-level discount already present — if one exists, it throws *"Order already has a discount"*. To swap discounts, the merchant removes the existing one first, then adds the new one. (Shipping discounts may be exempted from this check when the order subtotal is below the shipping discount's `order_over` threshold, in which case the shipping discount isn't actually applied.)

This is distinct from per-line discounts ([[orders-products]]) — a single line can have multiple per-line discounts AND the order can carry its own order-level discount on top. See [[discount-stacking]].

### Archived orders blocked

Archived orders (`isArchived = true`) reject ALL three discount routes (`add`, `delete`, `delete-modifications`) with *"Cannot perform this operation on archived order"*. The merchant must unarchive first via [[orders-archive]].

### Existing-discount filters drive merchant choice

The existing-discount picker is intentionally narrow — it only shows discounts that would legitimately apply, so the merchant cannot accidentally mis-apply one. The full filter logic is on [[orders-discount-add-existing-eligibility]].

### Recalculation + audit

Adding or removing a discount recalculates subtotal, tax, and shipping in one transaction, fires `order.updated` per [[settings-hooks]], and writes a history entry capturing the acting admin. No customer notification is sent. Full mechanics on [[orders-discount-add-recalculation]].

## Related

- [[orders-details]] — parent page (Discount action row).
- [[orders-products]] — sister flow for PER-LINE discounts (different scope).
- [[orders-history]] — discount events appear here.
- [[marketing-discounts]] — definitions of existing discounts; uses-left counter affected by add/delete.
- [[customer-group]] — customer group filters which discounts are eligible.
- [[settings-taxes]] — tax recalculation triggered by discount change.
- [[orders-archive]] — archived orders can't be discount-edited.
- [[settings-hooks]] — `order.updated` webhook.
- [[api-order-discount]] — read-only JSON-API v2 resource.
- [[json-api-v2]] — API overview.
- [[discount-stacking]] — how this discount coexists with per-line + cart discounts.
- [[discount]] — entity page.
- [[order]] — entity page.

## Open questions

None.
