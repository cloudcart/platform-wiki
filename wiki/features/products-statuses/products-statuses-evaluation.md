---
type: feature
nav_path: "Products → Product statuses"
route_name: product-statuses-index
route_path: /admin/products/statuses
aliases: ["Product status evaluation", "Which status applies", "Status priority", "Manual status override", "out_of_stock_id", "Bundle status bypass"]
tags: [products, statuses, stock, customer-facing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Product statuses — how a status is chosen

## Purpose

This aspect explains **which** status a customer actually sees when several could apply: the per-variant evaluation, the manual `status_id` / `out_of_stock_id` overrides set on the product, the priority order among Conditional rules, the "one badge per product" rule, and the bundle bypass.

> Part of [[products-statuses]]. See the hub for the related aspects (list tables, modal, operators/actions, side-effects).

## Where to find it

The rules below are defined on the Product statuses screen (Sidebar → Products → **Product statuses**) but they take effect on the **storefront** — the product card and product detail page. The per-product manual overrides are set on the [[products-products]] Edit page.

## What the merchant can do here

- Order Conditional rules by priority on the list (see [[products-statuses-list-tables]]) so the right one wins.
- Set a manual in-stock and out-of-stock status per product on the product editor to override the global rules for that one product.

## Settings & fields

### Two manual status pickers on the product editor

The product editor (per [[products-products]]) has TWO manual status pickers that store onto the product record:

- **"Status when in stock"** → `status_id`.
- **"Status when out of stock"** → `out_of_stock_id`.

These let the merchant override BOTH the in-stock and out-of-stock outcomes independently for that specific product, without changing the global Conditional rule list.

## Business rules

### Evaluation is per-VARIANT, not per-product

The status badge displays on the storefront product card / detail. On a **listing view** (no variant selected yet), the platform evaluates the rule against the product's **default variant**. On the **product detail page** (after the customer picks a variant), the badge re-evaluates against the SELECTED variant's quantity — so a multi-variant product can show different statuses depending on which colour/size is active. The aggregate "is anything in stock" question only matters when no variant is selected. To indicate per-variant unavailability separately, the theme greys out / marks unavailable variants in the picker.

### Manual override precedence (with caveats)

When the merchant has manually set a status on the product (the Non-conditional bottom-table slot), it wins over Conditional rules in two cases:

- The variant has positive stock (≥ minimum), OR
- The product has tracking OFF or "Continue selling" ON.

If the variant is below minimum AND tracking is on AND continue-selling is off, the manual `status_id` is OVERRIDDEN by either `out_of_stock_id` (the separate manual out-of-stock pick on the product) or the first Conditional rule that matches as an out-of-stock type. The full ranked precedence chain is documented in [[product-status-evaluation-precedence]].

### Priority order matters among Conditional rules

Two Conditional statuses can both match the same product (e.g., "Lower than 5" AND "Lower than or equal to 5" both match a product with 3 in stock). The platform picks the **first matching rule by sort order**. The merchant should put the most specific rules first; the Sorting conflict indicator on the list flags overlaps — see [[products-statuses-list-tables]].

### One status applies per product at a time

A product displays only ONE status badge. The Conditional system picks one by priority; a Non-conditional override set on the product takes precedence over Conditional rules when it applies.

### Status sync is real-time

When an order changes stock (decrement on checkout, increment on cancellation), the product's status is re-evaluated immediately. The customer browsing the storefront sees the new status on the next page load — no merchant action needed. The decrement timing itself is governed by `order_status_for_quantity_decrease` on [[settings-cart]].

### Bundles bypass this system entirely

Per [[bundles-list]], bundle products do NOT evaluate the Conditional status rules. Their status is forced: *In Stock* if selling is enabled, *Out of Stock* otherwise. Custom statuses do not apply to bundle products.

## Related

- [[products-statuses]] — hub.
- [[products-statuses-list-tables]] — priority ordering + conflict indicator for Conditional rules.
- [[products-statuses-operators-actions]] — the operators matched here against variant stock.
- [[product-status-evaluation-precedence]] — the data-model 5-level precedence chain.
- [[products-products]] — the product editor with the two manual status pickers.
- [[bundles-list]] — bundle products that bypass the status system.
- [[settings-cart]] — `order_status_for_quantity_decrease` controls when stock decrements and statuses flip.

## Open questions

None.
