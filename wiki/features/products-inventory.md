---
type: feature
nav_path: "Products → Inventory"
route_name: products_inventory
route_path: /admin/products/inventory
aliases: ["Inventory", "Stock management", "Quantity management", "Наличности", "Склад", "Количества"]
tags: [products, inventory, stock, quantity]
plan_gates: ["products", "multi_variants", "digital_products", "hidden_products"]
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---
# Inventory

## Purpose

A focused screen for **stock management at scale** — the merchant sees every product and variant SKU in one table, with the current quantity, price, and identifiers (SKU, barcode) per row. Unlike [[products-products]] which is centred on managing the product as a whole, Inventory is centred on the **per-variant quantity and price** so the merchant can quickly bulk-update stock levels (e.g., after a delivery), bulk-change prices (e.g., for a seasonal markup), or flip the "continue selling when out of stock" toggle for a group of SKUs.

The merchant can edit quantities **inline per row** (set a new value OR add to existing) and the row shows a live preview of the resulting quantity until the merchant clicks Save. For broader changes, the merchant selects multiple rows and uses bulk Update quantities or Change price modals.

This hub is the navigation pivot for the Inventory screen. Each operational aspect lives in its own sub-page below; drill into the one that matches the question rather than reading all of them.

## Where to find it

Sidebar → Products → **Inventory**.

The page's breadcrumb reads "Products → Inventory". The route is `/admin/products/inventory`. The header icon is the list-ul icon.

This page requires the products / inventory permission section. Moderators without it cannot access the Inventory sidebar entry. The same permission tree's category restrictions (from [[settings-staff]]) apply — a moderator restricted to certain categories sees only inventory rows for products in those categories.

## What the merchant can do here

- **See and find SKUs** — every product / variant on one paginated table with sorting and filters (Quantity, Manufacturer, Category, SKU, Barcode). See [[products-inventory-table]].
- **Edit quantities** — per-row Set / Add inline editor with live preview, plus a bulk Update-quantities modal. See [[products-inventory-quantity-editing]].
- **Edit prices** — per-row Price modal and a Change-price bulk action. See [[products-inventory-price-editing]].
- **Flip the oversell toggle** — bulk "Continue selling when sold out" / "Stop selling when sold out". See [[products-inventory-oversell-toggle]].

What the merchant **cannot** do here: create products, manage variant DEFINITIONS, edit images / descriptions / SEO, add a brand-new SKU to a product, or view stock-movement history. Those live on [[products-products]], [[products-variants-options]], and the [[products-change-log]] modal respectively.

## Settings & fields

The detailed field tables (list columns, the per-row editor, both modals, filter operators) are documented per aspect:

- List columns + filters → [[products-inventory-table]].
- Per-row quantity editor + bulk-quantity modal → [[products-inventory-quantity-editing]].
- Per-row / bulk Price modal → [[products-inventory-price-editing]].
- Bulk selling-toggle controls → [[products-inventory-oversell-toggle]].

## Business rules

The Inventory screen sits on top of the platform-wide [[inventory-tracking]] model — the [[variant|Variant]] is the unit of stock, the master switches (`tracking`, `continue_selling`, `threshold`) live on the parent [[product|Product]], and `order_status_for_quantity_decrease` on [[settings-cart]] governs WHEN orders decrement stock. Screen-specific rules:

- **Only TRACKED products appear** — the grid hard-filters `tracking = yes` AND non-NULL quantity; untracked / unlimited SKUs are invisible. See [[products-inventory-table]].
- **All edits clamp at 0** — the inline / bulk quantity editor cannot drive a Variant negative; only the order-decrement path moves stock, and that clamps at 0 too. See [[products-inventory-quantity-editing]] and [[inventory-oversell]].
- **Every save ripples downstream** — search re-index, storefront cache flush, `product.updated` webhook; but NOT the low-stock email. See [[products-inventory-side-effects]].

## Sub-pages (in this cluster)

- [[products-inventory-table]] — the SKU list: columns, sorting, the five filters, the tracked-only query, and what the screen does NOT manage.
- [[products-inventory-quantity-editing]] — per-row Set / Add editor with live preview, the bulk Update-quantities modal, clamp-at-0 rule, and the 50M cap.
- [[products-inventory-price-editing]] — per-row Price cell + Change-price bulk action, minor-units storage, special price, and the default-variant flip after a price save.
- [[products-inventory-oversell-toggle]] — bulk Continue / Stop selling actions, the untracked-product validation gate, and how negative inventory does (and doesn't) arise.
- [[products-inventory-side-effects]] — what fires on save (search, cache, webhook), the suppressed low-stock email, JSON-API v2 parity + the no-clamp difference, and the plan gates governing which SKUs appear.

## Related

- [[products]] — parent hub.
- [[products-products]] — full product editor; quantity can also be edited from there per-variant.
- [[products-variants-options]] — variant parameters; their option values create the SKUs that Inventory tracks.
- [[products-change-log]] — the audit trail for stock changes (no history on this screen).
- [[inventory-tracking]] — the platform-wide stock model this screen sits on.
- [[settings-cart]] — `product_threshold` for low-stock notifications; `order_status_for_quantity_decrease` for when stock decrements.
- [[settings-staff]] — moderator permission + category restrictions that scope this page.
- [[product]] — entity page.
- [[variant]] — entity page.

## Open questions

None.
