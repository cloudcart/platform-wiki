---
type: feature
nav_path: "Apps → Suppliers → Supplier Products"
route_name: apps.suppliers_products.settings
route_path: /admin/apps/suppliers/supplier_products/:id
aliases: ["Supplier Products", "Per-supplier product list", "Supplier-product mapping"]
tags: [apps, administration, suppliers, supplier-products, mapping]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Suppliers → Supplier Products

## Purpose

The **Supplier Products** view shows the **per-supplier product mapping** — for each supplier the merchant works with, which CloudCart products they supply, with what per-link data (cost, supplier-SKU, lead time, MOQ).

Used by merchants to:
- Audit which suppliers supply which products.
- Compare per-product cost across suppliers (price-comparison view).
- Bulk-edit supplier mappings.
- Identify the cheapest supplier per product (highlighted).

For the full Suppliers feature set, see [[apps-suppliers]].

## Where to find it

Sidebar → Apps → Suppliers → **Supplier Products view** (per supplier). Route: `/admin/apps/suppliers/supplier_products/:id` (route name `apps.suppliers_products.settings`) — the `:id` is the supplier id; this view is opened from a specific supplier row in the Suppliers list, not as a flat cross-supplier tab.

## What the merchant can do here

### Supplier-Products data table

| Column | Notes |
|---|---|
| **Product** | CloudCart product name + thumbnail. |
| **Supplier** | The supplier this row maps to. |
| **Supplier SKU** | The supplier's internal SKU (may differ from CloudCart's). |
| **Cost** | Per-supplier cost price. |
| **Lead time** | Days from order placement to supplier dispatch. |
| **MOQ** | Minimum order quantity. |
| **Cheapest flag** | Visual indicator when this supplier offers the lowest price for the product. |
| **Actions** | Edit, Delete, View supplier. |

### Filter / search

- By supplier.
- By product.
- By cost range.
- Search by SKU / name.

### Bulk-edit mappings

Multi-select rows + bulk actions:
- Bulk-update lead times.
- Bulk-update costs (e.g., supplier announces 10% increase across the board).
- Bulk-delete mappings.

### Add new mapping

**+ Add supplier-product** → opens a modal:
1. Pick a CloudCart product.
2. Pick a supplier.
3. Fill in per-link data (cost, supplier SKU, lead time, MOQ).
4. Save.

### What the merchant CANNOT do here
- Edit the underlying product — jump to [[products-products]].
- Edit the underlying supplier — jump to the supplier detail page (legacy URL).
- Delete a supplier from this view (only the mapping).

## Settings & fields

### Per-mapping data

| Field | Notes |
|---|---|
| **product_id** | CloudCart product. |
| **supplier_id** | The supplier. |
| **supplier_sku** | Supplier's internal product code. |
| **cost** | Per-supplier wholesale price. |
| **currency** | Cost currency (when different from store currency). |
| **lead_time_days** | Days from order to dispatch. |
| **moq** | Minimum order quantity. |
| **notes** | Free-text notes. |

### Cheapest-supplier highlight

For each product, the system identifies the supplier offering the LOWEST `cost` and visually highlights that row. Useful for purchase-order decisions.

## Business rules

### Many-to-many relationship

A single product can have MULTIPLE supplier mappings. A single supplier supplies MULTIPLE products. The Supplier Products table flattens this many-to-many for browsing.

### Cost comparison drives purchase orders

When the merchant generates POs from order demand (see [[orders-supplier-products]] aggregation), the platform uses the cheapest-supplier mapping to recommend which supplier to source from.

### Side effects on save
- New / updated mapping persisted.
- Cheapest-supplier flag recalculated for the product.
- Affects [[orders-supplier-products]] aggregation view.

### Permission
Standard apps permission scope.

## Related

- [[apps-suppliers]] — Suppliers hub.
- [[apps-suppliers-overview]] — overview page.
- [[orders-supplier-products]] — cross-order supplier aggregation (uses these mappings).
- [[products-products]] — products listed in this mapping.

## How it works (verified against backend)

### Stored fields are minimal

Each row in `supplier_products` is just `(supplier_id, product_id, variant_id, price, price_type, in_stock, identifier)`. There is **no** `lead_time`, **no** `MOQ`, **no** currency override, **no** notes column, **no** quantity tiers — the only price is a single integer per (supplier × variant). The "Lead time / MOQ / Notes / Currency" columns described in earlier drafts of this page are aspirational; they are not in the shipped model.

### Filter / sort options

The list-grid filters exposed by `FilterSupplierProducts` are:

- **Free-text query** across `identifier` (the supplier's SKU) and the linked product name.
- Sort is by `id` only.

The supplier-list grid (`FilterSuppliers`) has richer filters:

- Free-text query across `name`, `email`, `phone`.
- `has_products` boolean (suppliers with / without products attached).
- `product` (in / not-in a chosen product list).
- `product_id` exact match.
- Sort by `name`, `id`, or `products_count`.

There is no "cost range" filter and no "cheapest supplier" filter on this view.

### Cost editing is per (supplier × variant)

Clicking **Change settings** on a product opens a modal that:

- Lets the merchant pick between **Common price** (one cost for every variant) and **Multiple prices** (per-variant inputs).
- For each variant: cost + supplier identifier (SKU). Costs are stored as integer cents via the platform code.
- Adds the in-stock flag (set to 1 by default when the row is created).

### No CSV import for bulk price updates

The Suppliers app provides a CSV **export** (the platform's standard export, format `Supplier → identifier → price` per the `csv_export_suppliers` translation). There is no CSV-import endpoint for bulk updating costs; bulk changes are done one product at a time through the **Change settings** modal.

### Cheapest supplier is computed elsewhere

The "Supplier with cheapest price" indicator (translation `products_by_order_suppliers_info`) appears on the cross-order [[orders-supplier-products]] aggregation view, not on this per-supplier list. There is no "highlight cheapest" badge in this table.

### No historical cost tracking

The `supplier_products` row has no `created_at` / `updated_at` (`$timestamps = false`) and no audit log table. Updating a supplier price overwrites the previous value in place — the merchant cannot see what last month's cost was.

### No quantity-tier pricing

Cost is one value per (supplier × variant). There is no per-quantity-band cost table (no "100+ units = lower per-unit price"). The merchant who needs tier pricing maintains it outside CloudCart.

### No supplier-API integration in this app

There is no automated cost-pull endpoint inside Suppliers. Supplier feeds come through separate apps ([[apps-xml-sync]] / [[apps-xml-import]]) — those write to product prices/stocks, not to `supplier_products`.

### No drop-shipping order-routing

Saving a supplier-product mapping does not register the supplier for drop-shipping automation. The platform does not auto-create POs or send order notifications to a supplier when an order is placed.

### Delete is per (supplier × product)

The **Delete** action on this list deletes all rows in `supplier_products` for the (supplier_id, product_id) pair (all variants at once). It does not delete the supplier and does not delete the underlying product.

## Open questions

