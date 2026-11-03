---
type: feature
nav_path: "Orders → Ordered Products → Export → CSV schema"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders_products
aliases: ["Ordered Products export columns", "Products by orders CSV columns", "Aggregated product export schema", "Supplier export columns", "Order products column list"]
tags: [orders, products, export, csv, schema, columns, suppliers]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-ordered-products-export]]. See the hub for related aspects (trigger / 2FA, sync vs async, filter scope, delivery, permissions / plan).

# Ordered Products export — CSV schema

## Purpose

Documents the **fixed column set** of the aggregated product-pivot CSV — the 10 base columns, the 3 additional columns the Suppliers app appends, the one-row-per-variant layout, the supplier-column rename, quantity normalisation, the order-ID separator, and header / currency formatting. The merchant cannot customise the schema from the UI; for a custom column set they transform the exported CSV in their own tools.

## Where to find it

The CSV is produced by both the synchronous and asynchronous paths described in [[ordered-products-export-sync-vs-async]]. The schema below applies to both — the only differences are encoding choices on the async output (covered in [[ordered-products-export-delivery]]).

## What the merchant can do here

- Read the produced file in Excel / Google Sheets / Numbers — headers are translated to the admin UI language.
- Re-shape or aggregate columns in their own tooling after export (the schema is fixed at write time).

The merchant CANNOT add / remove / re-order columns from the export UI, choose XLSX / XML output, or collapse the per-variant rows into one row per product.

## Settings & fields

### Base column set (10 columns)

| Column | What it shows |
|--------|---------------|
| **Order IDs** | Semicolon-separated list of order IDs containing this product. |
| **Product name** | Product display name. |
| **Variants** | Variant parameter values (e.g., `Color: Red; Size: M`). |
| **Options** | Product option values selected by the customer (e.g., custom text). |
| **SKU** | Product SKU. |
| **Barcode** | Product barcode. |
| **Single product price** | Per-unit price at order time. |
| **Discounted price** | Per-unit price after applied discounts. |
| **Product quantity** | Aggregated SUM of quantities across matching orders. |
| **Total** | Line total (quantity × price). |

### Suppliers-app columns (3 appended → 13 total)

When the **Suppliers** app is installed, three columns are appended:

| Column | What it shows |
|--------|---------------|
| **Supplier** (or **Suppliers info**) | Supplier name(s) — header varies by whether the merchant filtered by a specific supplier. |
| **Supplier product identifier** | The supplier-side SKU (when configured per product). |
| **Price from supplier** | The supplier's wholesale price for the product. |

## Business rules

### One row per variant × options

The CSV mirrors the pivot's per-variant rows. Each row captures BOTH the product's variant info (size / colour / etc.) AND the customer's option selections (custom text, file-upload metadata — files themselves are not embedded). Two rows differ if either the variant OR the options differ. For product-level aggregation the merchant aggregates in their downstream tool.

### Suppliers app changes the column count

The CSV column count differs based on whether the Suppliers app is installed: **10 columns without the app, 13 with it** (the 3 supplier columns appended). Merchants integrating the CSV into external tools that expect a fixed column count must be aware of this schema-shift. See [[apps]].

### Supplier column rename based on filter

The supplier column header changes by whether the merchant filtered by a specific supplier:

- Filtered by one supplier → header is **"Supplier"**.
- Not filtered (showing all) → header is **"Suppliers info"** (products may have multiple suppliers).

### Order IDs semicolon-separated (not comma)

The order-ID list uses `;` as separator (e.g., `101; 103; 108`) — NOT comma — to avoid confusion with CSV field separators. Downstream systems should parse on `;` for that column.

### Quantity normalisation

The `Product quantity` column applies the platform's quantity-normalisation helper to the aggregated SUM, handling unit-based products (1, 2, 3) vs weight / measure-based products (1.5 kg, 2.75 m) — the merchant sees the appropriate numeric form per product type.

### Headers translated, currency per order

Column headers translate based on `site('language_cp')` (admin UI language). Monetary fields (price, total) use each underlying **order's** currency, so multi-currency stores get mixed-currency rows — same as the pivot's display rendering. This mirrors [[orders-export-csv-schema]].

## Related

- [[orders-ordered-products-export]] — hub.
- [[ordered-products-export-sync-vs-async]] — the two paths that both produce this same schema.
- [[ordered-products-export-filter-scope]] — the supplier filter that drives the column rename.
- [[orders-export-csv-schema]] — the per-order export schema (contrast: one row per line item, 46+ columns).
- [[apps]] — the Suppliers app that appends the 3 supplier columns.
- [[products-property]] — properties / options that populate the Variants / Options columns.
- [[product]] — entity page.

## Open questions

None.
