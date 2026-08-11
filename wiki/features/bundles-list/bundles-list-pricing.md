---
type: feature
nav_path: "Products → Bundles → Pricing"
route_name: bundles-edit.new
route_path: /admin/products/bundles-new/edit/:id
aliases: ["Bundle pricing", "Bundle price mode", "Fixed price bundle", "Percent discount bundle", "Bundle savings"]
tags: [apps, administration, products, bundles, pricing]
plan_gates: ["bundles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Bundles — pricing modes

> Part of [[bundles-list]]. See the hub for the other aspects (creation, stock, plan gates).

## Purpose

This aspect covers **how a bundle is priced**: the two mutually-exclusive pricing modes (fixed price vs percentage discount), the validation rule that blocks fixed pricing when components carry variant pricing, the auto-derived `individual_price` total, and the savings shown to the customer.

## Where to find it

The pricing controls are on the bundle Add/Edit form (route `bundles-edit.new`, path `/admin/products/bundles-new/edit/:id`) — see [[bundles-list-creation]] for the rest of the form.

## What the merchant can do here

The merchant picks one of two pricing modes via the bundle's single `variant.type`:

- **`price` mode (fixed price)** — type a fixed bundle price. The bundle sells at exactly that price regardless of constituent price changes. If per-item `individual_price` overrides are enabled, the bundle price auto-calculates as the sum of overridden prices (see below).
- **`percent` mode (percentage discount)** — set a discount percent (e.g. `10%`). The bundle price = sum of each constituent's `price_from / price_to` × quantity, MINUS the percent. The bundle becomes a **price range** (`price_from` ≠ `price_to`) when any constituent has variant pricing.

## Settings & fields

- `variant.type` — `price` or `percent` (the pricing mode).
- The fixed amount (in `price` mode) or the discount percent (in `percent` mode).
- Per-item `individual_price` + `individual_price_enabled` — the per-row override that feeds the auto-derived total (the field itself is documented on [[bundles-list-creation]]).

## Business rules

### Fixed price is BLOCKED when components have variant pricing

Validation rule: if `variant.type = price` AND any component product has variant pricing (`price_from != price_to`), the save fails with *"Fixed price is not allowed when the bundle contains products with variants"*. Merchants who want to bundle products-with-variants MUST use `percent` mode. This is the single most common pricing-mode support question.

### Auto-derived `individual_price` flag

When the merchant enables a per-item `individual_price` on ANY component, the platform automatically computes the bundle price as the SUM of `(overridden price OR original price_from) × qty` for each item, and writes it to the bundle's variant. The merchant does not type the total — it is calculated.

When `variant.type = percent`, the platform sets `individual_price = 1` automatically (the bundle is treated as "individually priced" because the discount is applied per item).

### Savings shown on the storefront

The bundle's price is typically less than the sum of the constituent prices — that discount is the merchant's tool to promote the bundle. The storefront shows both the bundle price and the "savings vs individual" calculation, so the customer sees how much the bundle saves them.

### Relationship to per-item quantity

The auto-derived total multiplies each item's overridden/original price by that item's `qty`. Per-item `qty` is only effective when `individual_qty_enabled` is toggled ON for the row — otherwise it counts as 1. The qty mechanics live on [[bundles-list-creation]].

## Related

- [[bundles-list]] — hub.
- [[bundle]] — the bundle entity (`variant.type`, `individual_price`).
- [[products-products]] — constituent products carry the `price_from`/`price_to` that drive `percent` mode.
- [[variants-model]] — why a component with variant pricing forces `percent` mode.
- [[marketing-discounts]] — alternative promotional pricing without a bundle.

## Open questions

None.
