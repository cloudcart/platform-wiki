---
type: feature
nav_path: "Products → Inventory → Quantity editing"
route_name: products_inventory
route_path: /admin/products/inventory
aliases: ["Inventory quantity editing", "Set add quantity", "Bulk update quantities", "Update quantities modal", "Промяна на количества"]
tags: [products, inventory, stock, quantity, bulk]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[products-inventory]]. See the hub for the other aspects (table, price editing, oversell toggle, side effects).

# Inventory — quantity editing

## Purpose

The quantity-editing modules let the merchant change stock levels either **one row at a time** (inline per-row editor) or **across many selected SKUs at once** (the bulk Update-quantities modal). Both modules share the same **Set / Add** mechanic and a **live preview** of the resulting quantity, so the merchant can verify before committing.

This is the screen merchants use after a delivery ("add 20 to each restocked SKU") or a write-down ("set damaged batch to 0").

## Where to find it

Sidebar → Products → **Inventory** (`/admin/products/inventory`).

- **Per-row editor**: the Update-quantity control on each table row.
- **Bulk modal**: select rows → **Update quantities** bulk action.

## What the merchant can do here

- **Set** a row's quantity to a typed value (replace the current number).
- **Add** a delta to a row's quantity (increment, or decrement with a negative number).
- **Preview** the resulting quantity before saving.
- **Bulk Update quantities** — apply ONE Set / Add operation to all selected SKUs at once.

## Settings & fields

### Per-row quantity editor

Each row has an inline quantity-update module with two modes:

- **Set** mode — replace the current quantity with the typed value (e.g., "set to 50").
- **Add** mode — add the typed value to the current quantity (e.g., current 12, add 5 → 17). A negative value decrements.

The chosen value is held in a **temporary preview state** until the merchant clicks Save. The preview is per-row, so editing several rows shows individual previews before any of them are committed. Hitting Save commits the change immediately to that row and clears the preview.

### Bulk-quantity modal (ProductInventoryBulkQuantityModal)

Opens via the Update quantities bulk action. The modal has:

- **Quantity input** with an inline **Set / Add toggle** (same module as the per-row editor).
- A help-text row reading *"{N} variants will be changed:"* where N is the count of selected SKUs.
- A scrollable preview list of every selected variant (product thumbnail + name + current quantity + **live preview** of the resulting quantity as the merchant types). The preview re-runs on every change to either the toggle or the input value.
- Cancel + Save buttons. Save dispatches one API call with the action (`add` / `set`) + quantity + ids, refetches the table, and clears the bulk-quantity state.

## Business rules

### One value applies to ALL selected SKUs identically

The Update quantities bulk modal applies ONE value to ALL selected rows. Selecting 50 T-shirt variants and choosing "Add 10" adds 10 to **each** variant's stock independently — it does not split 10 across them. Likewise "Set quantity to 50" puts 50 on every selected variant even if one currently has 5 and another has 200.

For non-uniform updates (a different quantity per variant), the merchant uses the per-row inline editor instead.

### Set / Add is clamped at 0 on this screen

The per-row and bulk Update-quantities action clamps the resulting quantity to **at least 0** — even in Add mode with a negative value. Submitting "Add -100" to a Variant currently at 5 produces 0, not -95. The `Set` mode also clamps negative inputs to 0.

**This means the Inventory screen cannot put a Variant into negative inventory directly**, even when "Continue selling when sold out" is ON for that product (see [[products-inventory-oversell-toggle]]). Negative inventory does not arise here at all — and on the order-decrement path the platform also clamps at 0; the merchant tracks "owed" units via outstanding paid orders, not a negative count (see [[inventory-oversell]]).

### Quantity hard cap of 50,000,000

Quantity is constrained to `<= 50,000,000` per Variant at the product-save layer. The Inventory page's inline editor doesn't enforce the cap itself, but the bulk product-save validation does. Above-cap values trigger `quantity_max_50000000`.

### What a quantity save does NOT do

Bulk Update-quantities through this screen updates the Variant `quantity` directly and does **not** trigger the `product_quantity_low` / `product_out_of_stock` admin emails — those fire only on the order-decrement code paths. So a bulk restock or write-down does not flood the merchant with low-stock emails. The full list of what a save does and doesn't fire is on [[products-inventory-side-effects]].

## Related

- [[products-inventory]] — hub.
- [[products-products]] — product editor; per-Variant quantity can also be edited there.
- [[inventory-oversell]] — the clamp-at-0 rule on the order path and how "owed" units are tracked.
- [[inventory-variant-model]] — the Variant-as-unit-of-stock model; `quantity = NULL` (unlimited) semantics.
- [[variant]] — entity carrying the per-SKU `quantity`.

## Open questions

None.
