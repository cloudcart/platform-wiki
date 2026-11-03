---
type: feature
nav_path: "Products → Inventory → Table"
route_name: products_inventory
route_path: /admin/products/inventory
aliases: ["Inventory table", "Inventory list", "Stock list", "SKU list", "Списък с наличности"]
tags: [products, inventory, stock, list, filters]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[products-inventory]]. See the hub for the other aspects (quantity editing, price editing, oversell toggle, side effects).

# Inventory — the SKU table

## Purpose

The Inventory table is the **list view** of the screen — every sellable product / variant SKU on one paginated table, so the merchant can locate the rows they want before editing. Each row shows the **Product** (name + thumbnail), **Identifiers** (SKU + barcode), **Price**, **Quantity**, and the inline Update-quantity controls. For products with variants, each variant is its own row (e.g., "T-Shirt — Red — Large"); a product without variants shows as a single row.

This page documents finding and scoping SKUs — the columns, sorting, and filters. The editing modules that live on each row are documented separately (see [[products-inventory-quantity-editing]] and [[products-inventory-price-editing]]).

## Where to find it

Sidebar → Products → **Inventory** (`/admin/products/inventory`). The table is the body of that page. No separate route.

## What the merchant can do here

- See every tracked SKU on one paginated table.
- **Sort** by Product name, Item ID (default — newest first), or Quantity.
- **Filter** the table down to the SKUs of interest (see the filter operators below).
- **Bulk-select** rows to feed the bulk actions (quantity, price, selling-toggle — documented in the sibling aspects).
- Click a Product cell to jump to that product's edit page.

What the merchant **cannot** do from the table:

- Create new products (use [[products-products]]).
- Manage variant DEFINITIONS — the parameters and values themselves (use [[products-variants-options]]).
- Edit images, descriptions, SEO — those live on the product editor.
- View stock-movement history per SKU. This table shows only the current quantity, not how it got there — for the audit trail use the [[products-change-log]] modal.
- Add a brand-new SKU to an existing product (the variant matrix is managed on the product editor).

## Settings & fields

### List columns

| Column | Notes |
|--------|-------|
| **Product** | Product name + thumbnail. Click navigates to the product's edit page. For products with variants, each variant is its own row. |
| **Identifiers** | SKU and barcode shown together. Each is searchable via filter. |
| **Price** | Click to open the Price modal — see [[products-inventory-price-editing]]. |
| **Quantity** | Current stock count. Sortable. Live-preview area shows the new value while editing. |
| **Update quantity** | Per-row inline editor with Set / Add toggle and Save button — see [[products-inventory-quantity-editing]]. |

### Filters

| Filter | Operators / source |
|--------|--------------------|
| **Quantity** | Numeric: Exactly / Not equal to / More than / Less than. |
| **Manufacturer / Vendor** | Multi-select from [[products-vendors]] with Includes / Does not include. |
| **Category** | Multi-select from [[products-categories]] with Includes / Does not include. |
| **SKU** | Text contains. |
| **Barcode** | Text contains. |

## Business rules

### Inventory table only shows TRACKED products

The Inventory grid query hard-filters `tracking = yes` AND `quantity IS NOT NULL`. So an untracked product (`tracking = no`) or a Variant with a NULL quantity (treated as unlimited stock — see [[inventory-variant-model]]) is **invisible** on this screen. Merchants who can't find a digital-goods or untracked product here should NOT panic — switching to the product editor and turning tracking on will surface it.

### Filter for low-stock candidates

The Quantity filter with "Less than" is the typical "show me what's running low" query:

- Filter: `Quantity less than <merchant's low-stock threshold>` (often 5 or 10).
- The table shows only SKUs at or below that level → the merchant can prioritise restocking.

Combine with the Category or Vendor filter to scope to a department or supplier.

### Permission scoping applies to the rows shown

A moderator restricted to certain categories (via [[settings-staff]]) sees only inventory rows for products in those categories — the table is filtered to their permission scope before any filter the merchant applies.

## Related

- [[products-inventory]] — hub.
- [[products-products]] — full product editor (create products, edit images / SEO, manage the variant matrix).
- [[products-variants-options]] — variant parameters; their option values create the SKUs this table lists.
- [[products-vendors]] — vendor filter source.
- [[products-categories]] — category filter source.
- [[products-change-log]] — the audit trail for stock changes (not shown on this table).
- [[settings-staff]] — moderator permission + category restrictions.

## Open questions

None.
