---
type: feature
nav_path: "Marketing → Discounts → Shipping → Force-save"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Free shipping force_save", "Save the discount on your order", "Shipping discount admin edit", "force_save shipping"]
tags: [marketing, discounts, shipping, force-save, admin-edit]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (eligibility, value mechanics, stacking, other zero-paths, plan gates / API, examples).

# Shipping discount — force-save (admin-edit guard)

## Purpose

This page documents the **`force_save` toggle** ("Save the discount on your order") — the admin-edit guard that keeps a Free-shipping discount attached to an existing order even when an admin edit removes the conditions that originally qualified it.

It matters because shipping discounts and order-over discounts often live on orders that an admin needs to edit (add/remove a line item, change quantities). Without `force_save`, those edits would detach the free shipping and the customer would owe the difference.

## Where to find it

The **Save the discount on your order** toggle appears on the Create / Edit form at `/admin/marketing-new/discounts/create/global` (or `create/code`) whenever the merchant has set Discount type to **Free shipping**. The field is shown in both target modes (`all` and `order_over`) and is **required** for `type = shipping`. See [[marketing-discounts-shipping]] for the entry-surface flow.

## What the merchant can do here

- Toggle `force_save` ON (the form pre-checks it on creation for `type=shipping`).
- (Cannot) save a shipping discount without `force_save` — pre-validation guards against unsaved-force_save edits.

## Settings & fields

### Force-save toggle

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Save the discount on your order** | `force_save` | When ON, the free shipping stays attached to a previously-placed order even if an admin edit removes the qualifying products or drops the subtotal below `order_over`. | 1 / 0. **Required when type=shipping** — the form enforces it. |

This field is **required** for shipping discounts (cross-validated). The platform's rule: shipping discounts and order-over discounts often live on orders that an admin needs to edit; without `force_save`, those edits would detach the free shipping.

## Business rules

### Force-save on order edits — what stays vs what detaches

When an admin edits an existing order with a free-shipping discount applied:

- If `force_save = 1`: the free-shipping line stays on the order even if the new line-item set drops the subtotal below `order_over`, or removes a qualifying product, or changes the region. The customer's saved benefit is preserved.
- If `force_save = 0`: editing the order to violate the discount's conditions **detaches** the free shipping. The customer's order total recalculates with the shipping cost added back.

This is why the form pre-checks `force_save` on creation. Without it, every minor admin edit risks accidentally surcharging the customer.

### Force-save bypasses condition re-check at edit time

When `force_save = 1` and the discount is already attached to an existing order, the platform's discount-validation check **returns true immediately** if the call is in the `isOrder = true` context (i.e., we're recalculating an existing order, not a fresh cart). The original conditions are NOT re-checked.

This is what keeps free shipping attached even if an admin edits the order to break the conditions. The customer's saved benefit is preserved without the admin having to manually re-attach the discount.

### Scope — `force_save` only matters for EXISTING orders

`force_save` has **no effect at fresh-cart evaluation**. When a customer is building a new cart on the storefront, every cart-totals computation runs the full eligibility check (target, conditions, customer group, region, dates, uses). `force_save = 1` does NOT skip these checks for unrelated carts — only for the SAME order where the discount is already attached.

So a Free-shipping discount with `force_save = 1` and `order_over = 50 EUR` still requires a 50 EUR subtotal for a new cart; the 50 EUR check only stops applying once that same cart became an order with the discount stamped on it.

### Why `force_save` is required for shipping (not for Flat / Percent)

Flat and Percent discounts also expose `force_save`, but it's optional on those types. Shipping is the **only discount type that hard-requires** `force_save` because:

- Shipping discounts almost always live on order-over carts (the most common shape is "Free shipping over X EUR").
- Admin edits to an existing order frequently change the subtotal (add/remove line items).
- Without `force_save`, even a +1 quantity edit can drop the subtotal below `order_over` and trigger an unexpected shipping surcharge for the customer.
- The platform's order-edit flow does NOT show the merchant a confirmation dialog when a discount detaches; the change happens silently.

Making `force_save` required eliminates this footgun.

### Interaction with order recalculation pipelines

When an admin edits an order via [[orders-details]], the order recalculates. The platform's recalculation:

1. Reads the original discount attachments stored on the order.
2. For each attached discount, decides whether to re-validate or short-circuit:
   - `force_save = 1` + `type = shipping` → short-circuit; discount stays.
   - `force_save = 0` → re-validate; discount may detach.
3. Recomputes the cart totals with surviving discounts.

This pipeline runs every time the admin saves a change on the order — line-item edits, quantity changes, address changes, even payment-method changes that affect shipping quote. The `force_save` flag is what ensures the customer's free-shipping promise is not silently broken by routine admin work.

### What `force_save` does NOT do

- It does NOT preserve free shipping when the **status** changes to one that re-credits (cancel / refund / void). A cancelled order is detached from all discounts regardless of `force_save`.
- It does NOT block the merchant from manually removing the discount from the order via the admin UI — the toggle prevents *automatic* detachment from edit-driven re-validation only.
- It does NOT affect new carts placed against the same discount — only the specific orders that already had it stamped on at submit time.

## Related

- [[marketing-discounts-shipping]] — hub.
- [[shipping-discount-eligibility]] — the conditions whose re-check `force_save` bypasses.
- [[shipping-discount-stacking]] — selection rule #4 (`force_save = 1` short-circuits condition re-check).
- [[orders-details]] — the admin order-edit screen where `force_save` matters.

## Open questions

None.
