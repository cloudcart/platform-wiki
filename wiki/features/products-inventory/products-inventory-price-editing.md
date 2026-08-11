---
type: feature
nav_path: "Products → Inventory → Price editing"
route_name: products_inventory
route_path: /admin/products/inventory
aliases: ["Inventory price editing", "Change price modal", "Bulk price change", "Промяна на цена от наличности"]
tags: [products, inventory, price, bulk]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
> Part of [[products-inventory]]. See the hub for the other aspects (table, quantity editing, oversell toggle, side effects).

# Inventory — price editing

## Purpose

The Inventory screen doubles as a fast **price-editing** surface. The merchant can change the per-Variant price one row at a time (click the Price cell) or across many selected SKUs at once (Change price bulk action) — handy for a seasonal markup or a quick markdown without opening each product editor.

## Where to find it

Sidebar → Products → **Inventory** (`/admin/products/inventory`).

- **Per-row**: click the **Price** cell on any row.
- **Bulk**: select rows → **Change price** bulk action.

## What the merchant can do here

- Edit a single Variant's price inline via the Price modal.
- Apply one new price to all selected Variants via the Change price bulk action.
- Edit the special / sale price where the product carries one (per-row Price modal).

## Settings & fields

### Per-row Price modal (ProductInventoryTablePriceModal)

Clicking the **Price** cell on any row OR the **Change price** bulk action opens the Price modal. Description text: *"This action will change you product/s price"*. A single Price currency input (min 0).

- Per-row, the modal can also expose the **special / sale price** (if the product has one) and other price-related fields the variant carries.
- Save commits to the selected ids via a single PATCH and refetches the table; toast *"Price updated successfully"* on success.
- Closing the modal without saving discards the change.

## Business rules

### One price applies to ALL selected SKUs (bulk)

The Change price bulk action sets the SAME new price on every selected Variant. There is no per-Variant differentiation in the bulk path — for individual prices the merchant edits each row's Price cell.

### Price is stored in minor units internally

The Price modal stores the per-Variant `price` as an integer in minor units (cents / stotinki) — the merchant types `12.34` and the platform stores `1234`. The displayed price in admin and storefront is the formatted version. A per-Variant price **overrides** the product's base price; clearing it makes the Variant fall back to the base price (see [[variants-model]]).

### After a price save, the default Variant may flip

After every bulk price-save, the platform re-runs the default-Variant selection for each affected product. The default Variant is the one with the **lowest `price`** (ties broken by Variant ID — oldest wins). So lowering one Variant's price below all siblings can promote it to the default Variant shown on the storefront category card.

### Side effects on save

A price save fires the same downstream chain as a quantity save — search re-index, storefront cache flush, `product.updated` webhook. See [[products-inventory-side-effects]] for the full list.

## Related

- [[products-inventory]] — hub.
- [[products-products]] — product editor; per-Variant price and special price also live there.
- [[variants-model]] — per-Variant price override vs base price; default-Variant selection.
- [[variant]] — entity carrying the per-SKU `price`.

## Open questions

None.
