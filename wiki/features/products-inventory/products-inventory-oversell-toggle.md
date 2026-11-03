---
type: feature
nav_path: "Products → Inventory → Oversell toggle"
route_name: products_inventory
route_path: /admin/products/inventory
aliases: ["Continue selling when sold out", "Stop selling when sold out", "Oversell toggle", "Backorder toggle", "Продажба при изчерпана наличност"]
tags: [products, inventory, oversell, continue-selling, bulk]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
> Part of [[products-inventory]]. See the hub for the other aspects (table, quantity editing, price editing, side effects).

# Inventory — the oversell toggle

## Purpose

Two bulk actions on the Inventory screen let the merchant flip the **"continue selling when sold out"** flag for a group of products at once: **Continue selling when sold out** turns it ON, **Stop selling when sold out** turns it OFF. The flag decides whether a product stays buyable once its stock hits 0 — the merchant's tool for backorders, pre-orders, and replenishable goods.

This page covers the screen-level toggle behaviour and its validation gate. The full platform-wide oversell mechanics (clamping, "owed" units) live on [[inventory-oversell]].

## Where to find it

Sidebar → Products → **Inventory** (`/admin/products/inventory`) → select rows → bulk actions **Continue selling when sold out** / **Stop selling when sold out**.

## What the merchant can do here

| Action | What it does |
|--------|--------------|
| **Continue selling when sold out** | For selected rows, sets the `continue_selling` flag ON. When stock reaches 0, the product remains buyable and goes into oversold. |
| **Stop selling when sold out** | For selected rows, sets the flag OFF. Stock at 0 → the product disappears from the storefront or shows "Out of stock". |

## Settings & fields

The toggle is the `continue_selling` flag on the parent **Product** (not per-Variant). The bulk action acts on the parent product of each selected row, so all Variants of that product share the resulting value. There is no per-field configuration beyond ON / OFF.

## Business rules

### The flag lives on the product, not the Variant

`continue_selling` is a per-**Product** switch — flipping it affects every Variant of that product equally. Selecting one Variant row and turning the flag ON turns it ON for all siblings of the same product.

### ON = stays buyable at zero stock

When ON, the product remains buyable even when its quantity reaches 0 (the storefront doesn't gray out the product or show "Out of stock"). Useful for:

- Products with replenishable stock (the merchant knows more inventory is coming soon).
- Pre-orders where the merchant accepts orders before stock arrives.

When OFF (default), the product becomes unavailable at zero stock — customers see "Out of stock" and cannot add to cart. The product returns to availability when the merchant restocks.

### Negative inventory does NOT arise from this screen

Turning the flag ON does **not** let the merchant pre-create a backorder gap from the Inventory grid: the quantity editor clamps at 0 (see [[products-inventory-quantity-editing]]). On the order-decrement path the platform also clamps the Variant `quantity` at 0 regardless of the flag — the Variant count never goes negative. The merchant tracks "how many we owe" via the count of outstanding paid orders against a 0-stock Variant, not a negative number. See [[inventory-oversell]] for the full clamping mechanics.

### Continue-selling validation gate (untracked products rejected)

`continue_selling` cannot be turned ON for a product whose `tracking = no` — the backend rejects with `cannot_continue_selling_untracked_product`. Because the bulk toggle acts on the parent product, it only succeeds if **every** selected Variant's parent product is `tracking = yes`. A bulk request that sweeps across untracked products surfaces this validation error. (Untracked products are also invisible on the [[products-inventory-table]] grid, so this mostly bites API callers — see [[inventory-variant-model]] for the `tracking` master switch.)

## Related

- [[products-inventory]] — hub.
- [[inventory-oversell]] — the platform-wide oversell model, clamp-at-0, and "owed" units tracking.
- [[inventory-variant-model]] — the `tracking` master switch the validation gate checks.
- [[products-products]] — the product editor where `continue_selling` and `tracking` also live.
- [[product]] — entity carrying the `continue_selling` flag.

## Open questions

None.
