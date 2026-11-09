---
type: feature
nav_path: "Orders → Order details → Discount → Add → Existing-discount eligibility"
route_name: admin.orders.discount.add
route_path: /admin/orders/action/discount/:order_id/add
aliases: ["Existing discount eligibility", "Discount picker filter", "Which discounts appear in the order discount dropdown", "order_over threshold filter", "Discount target type filter"]
tags: [orders, discount, eligibility, filtering]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[orders-discount-add]]. See the hub for the other aspects (form fields, manual discounts, delete, recalculation, API).

# Order-level discount — existing-discount eligibility

## Purpose

The **filter that decides which existing [[marketing-discounts]] appear** in the Add Discount form's "Choose target" dropdown ([[orders-discount-add-form]]). The picker is narrow, but it does not run every check the storefront runs (see Business rules).

## Where to find it

The filter runs server-side when [[orders-details]] → **Add Discount** → **Existing discount** is selected. The merchant never sees the filter directly — only its result (the narrowed dropdown, or the *"There are no discounts available."* alert when nothing qualifies).

## What the merchant can do here

- Choose only from the **pre-qualified** discount list. There is no "show all" override in this UI.
- When a needed discount is missing from the list, the merchant either uses a [[orders-discount-add-manual|manual discount]], a per-line discount ([[orders-products]]), or activates the discount in [[marketing-discounts]] and relies on customer reorder.

## Settings & fields

The list of available existing discounts is built by excluding any discount that fails ANY of these checks:

1. **Customer-group match** — the discount must target this customer's group OR have `customer_group_id = null` (applies to all groups). See [[customer-group]].
2. **Type exclusion** — `type = banner`, `label` or `code-pro` discounts are excluded.
3. **`is_container` 0 or empty** — container discounts (parent of multiple sub-discounts) are excluded.
4. **`order_over` threshold** — the discount's minimum-order-total must be ≤ the order's `price_subtotal`.
5. **Target-type whitelist** — only target types `all`, `order_over`, and `shipping` are allowed (see below).
6. **Code-less exclusion** — a discount with NO code AND a target type that is NOT `order_over` is hidden (see below).

Inactive, expired and used-up discounts are also left out.

## Business rules

### Only three target types appear

The "Choose discount target" dropdown shows ONLY discounts whose target type is one of:

- **all** (*For every product in the cart*) — a percent comes off each line. A flat amount comes off every line in full, once per line, whatever the quantity, and a line can go below zero. Lines holding a product discount are skipped when `code_apply` is off. See [[discount-stacking-amount-by-target]].
- **order_over** (*Orders over*) — one amount off the order, shown as a row in the totals, while the subtotal is strictly above the threshold.
- **shipping** — shipping-cost discount.

Other types — product-targeted, category-targeted, vendor-targeted, selection-targeted, category-vendor — are EXCLUDED even if eligible by every other criterion. A discount limited to a specific product category therefore cannot be applied as an order-level discount via this UI; the merchant uses a per-line discount ([[orders-products]]) instead.

### Code-less, non-order-over discounts are hidden

A subtler exclusion: if an existing discount has NO code AND its target type is NOT `order_over`, it is hidden from the dropdown. So code-less discounts targeting `all` or `shipping` are excluded. The rationale is that code-less discounts auto-apply at checkout already — manually attaching them here would double-apply.

### When the subtotal drops below the threshold

The `order_over` threshold is checked again on every recalculation. If a discount required "Order over 100" and the merchant later removes products until the order falls to 80, the discount stays listed on the order (see [[orders-discount-add-delete]] to remove it), but its amount stops being deducted. The amount keeps being deducted only if **Save the discount in the order** is on for that discount.

### Orders created in the admin get no automatic order-level discount

An order created in the admin ([[orders-add]]), like any order being edited, takes its order-level discounts only from what is stored on the order. No-code **Orders over** discounts and [[apps-cart-rules|Cart Rules]] apply automatically only in the storefront cart and checkout, so a manual order above the threshold gets neither. To give one, add the discount here: a no-code Orders over discount is listed once the order's subtotal reaches its threshold. A Cart Rule cannot be added to an order; use a manual discount instead.

### The picker is not the storefront's check

The picker checks subtotal, customer group, type, and target type. It does not check region, registered-customers-only, per-customer limits or `code_apply`, which the storefront checks when a code is entered. A discount at exactly its threshold is listed and can be added, then deducts nothing unless **Save the discount in the order** is on. See [[discount-stacking]] for the storefront's rules.

## Related

- [[orders-discount-add]] — hub.
- [[orders-discount-add-form]] — the dropdown this filter populates.
- [[marketing-discounts]] — the discount rules being filtered.
- [[customer-group]] — customer-group match check.
- [[discount-stacking]] — the storefront's rules.
- [[discount]] — entity page (target types, `order_over`, `is_container`).

## Open questions

None.
