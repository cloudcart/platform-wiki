---
type: feature
nav_path: "Orders → Order details → Discount → Add → Existing-discount eligibility"
route_name: admin.orders.discount.add
route_path: /admin/orders/action/discount/:order_id/add
aliases: ["Existing discount eligibility", "Discount picker filter", "Which discounts appear in the order discount dropdown", "order_over threshold filter", "Discount target type filter"]
tags: [orders, discount, eligibility, filtering]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-discount-add]]. See the hub for the other aspects (form fields, manual discounts, delete, recalculation, API).

# Order-level discount — existing-discount eligibility

## Purpose

The **filter that decides which existing [[marketing-discounts]] appear** in the Add Discount form's "Choose target" dropdown ([[orders-discount-add-form]]). The picker is intentionally narrow: it only surfaces discounts that could legitimately apply to THIS order, so the merchant cannot accidentally mis-apply one.

## Where to find it

The filter runs server-side when [[orders-details]] → **Add Discount** → **Existing discount** is selected. The merchant never sees the filter directly — only its result (the narrowed dropdown, or the *"No discounts available"* alert when nothing qualifies).

## What the merchant can do here

- Choose only from the **pre-qualified** discount list. There is no "show all" override in this UI.
- When a needed discount is missing from the list, the merchant either uses a [[orders-discount-add-manual|manual discount]], a per-line discount ([[orders-products]]), or activates the discount in [[marketing-discounts]] and relies on customer reorder.

## Settings & fields

The list of available existing discounts is built by excluding any discount that fails ANY of these checks:

1. **Customer-group match** — the discount must target this customer's group OR have `customer_group_id = null` (applies to all groups). See [[customer-group]].
2. **Type exclusion** — `type = banner` or `type = label` discounts are excluded (they aren't real price discounts).
3. **`is_container = 0`** — container discounts (parent of multiple sub-discounts) are excluded.
4. **`order_over` threshold** — the discount's minimum-order-total must be ≤ the order's `price_subtotal`.
5. **Target-type whitelist** — only target types `all`, `order_over`, and `shipping` are allowed (see below).
6. **Code-less exclusion** — a discount with NO code AND a target type that is NOT `order_over` is hidden (see below).

So the merchant only sees discounts that could legitimately apply to this order.

## Business rules

### Only three target types appear

The "Choose discount target" dropdown shows ONLY discounts whose target type is one of:

- **all** — discount applies to the whole order regardless of which products.
- **order_over** — discount triggers when subtotal exceeds a threshold.
- **shipping** — shipping-cost discount.

Other types — product-targeted, category-targeted, vendor-targeted, selection-targeted, category-vendor — are EXCLUDED even if eligible by every other criterion. A discount limited to a specific product category therefore cannot be applied as an order-level discount via this UI; the merchant uses a per-line discount ([[orders-products]]) instead.

### Code-less, non-order-over discounts are hidden

A subtler exclusion: if an existing discount has NO code AND its target type is NOT `order_over`, it is hidden from the dropdown. So code-less discounts targeting `all` or `shipping` are excluded. The rationale is that code-less discounts auto-apply at checkout already — manually attaching them here would double-apply.

### Threshold does NOT auto-detach when subtotal drops

Once a discount is applied, the `order_over` threshold check is NOT re-evaluated when subsequent line changes shrink the subtotal. If a discount required "Order over 100" and the merchant later removes products until the order falls to 80, the discount STAYS attached — no auto-detach. The merchant must manually remove the discount (see [[orders-discount-add-delete]]) to enforce the threshold.

### Filter guides the merchant toward valid applications

Because the picker pre-filters by subtotal, customer group, type, and target type, the merchant cannot apply a discount the order doesn't qualify for. This is the same eligibility logic the storefront runs, surfaced as a back-office picker — see [[discount-stacking]] for how the same checks run on the storefront cart.

## Related

- [[orders-discount-add]] — hub.
- [[orders-discount-add-form]] — the dropdown this filter populates.
- [[marketing-discounts]] — the discount rules being filtered.
- [[customer-group]] — customer-group match check.
- [[discount-stacking]] — the same eligibility checks on the storefront cart.
- [[discount]] — entity page (target types, `order_over`, `is_container`).

## Open questions

None.
