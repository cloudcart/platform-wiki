---
type: feature
nav_path: "Products → Variants → List"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Variants list", "Variant parameters list", "Variants table", "Списък с варианти"]
tags: [products, variants, list]
plan_gates: ["multi_variants"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Variants — list table

> Part of [[products-variants-options]]. See the hub for the other aspects (wizard, types, values, listing toggle, data model, API).

## Purpose

The default landing screen under **Products → Variants** — a paginated table of every variant parameter defined store-wide (Colour, Size, Material, etc.). The Administrator inventories, reorders, deactivates, and bulk-removes parameters here, then drills into each row to manage its option values on the per-parameter Values sub-page (see [[products-variants-values]]).

## Where to find it

Sidebar → Products → **Variants**. Breadcrumb: "Products → Variants". Route `/admin/products/variants`. Header icon: sliders.

## What the merchant can do here

- See all variant parameters in a paginated table — Name, Values count (linked), Products count (linked), Active toggle, Sort priority, per-row Delete.
- **Drag-and-drop rows** to reorder — but **only after clicking the "Enable Drag and drop sorting" button** first (until it is on, rows are static and dragging does nothing — not a bug; same mechanism as [[products-variants-values]]). Controls the order in which variant pickers appear on the product editor and the storefront product page.
- Sort by name, values count, products count, or sort priority.
- **Toggle Active** per row — disables the parameter (stops appearing on product editors and the storefront).
- Click **+ Add variant** to open the 2-step creation wizard — see [[products-variants-wizard]].
- Click a parameter row's name to open the single-screen Edit modal — same fields as wizard Step 1, no Step 2.
- Click the Values count on a row to drill into the per-parameter Values sub-page (see [[products-variants-values]]).
- Click the Products count to jump to [[products-products]] filtered by products using this parameter.
- **Bulk actions** with row checkboxes:
  - **Active** — sets selected rows to active=ON.
  - **Inactive** — sets selected rows to active=OFF.
  - **Delete** — with confirmation; protected when parameters are in use (see [[products-variants-data-model]]).

## Settings & fields

### List columns

| Column | Notes |
|--------|-------|
| **Name** | The parameter name. Sortable. Click opens Edit modal. |
| **Values** (`options_count`) | Sortable. Click opens the per-parameter Values sub-page. |
| **Products** (`products_count`) | Sortable. Click opens [[products-products]] filtered by products using this parameter. |
| **Active** (`visible`) | Toggle. When OFF, the parameter is hidden everywhere — editor + storefront picker + filter. |
| **Sort priority** (`sort`) | Sortable + draggable. Controls the order on the product editor's variants section and on the storefront variant pickers. |
| **(actions)** | Per-row Delete button. |

## Business rules

### Sort priority drives both editor and storefront order

The Sort priority column controls TWO surfaces:

1. The order of variant pickers on the **product editor's Variants section** (which the merchant fills in first).
2. The order of variant pickers on the **storefront product detail page** (which customers interact with).

Merchants typically order them by importance/dependency (Colour before Size, because the customer needs to pick colour first to see size availability per colour).

### Active toggle disables completely (does NOT detach)

Setting a parameter to Active = OFF hides it everywhere — the product editor doesn't show it, the storefront pickers don't show it. Products that already use this parameter **keep** their variant assignments stored; customers just can't see / pick the variant any more (so they effectively see a "broken" product without variant options unless the merchant edits the products to remove the dependency).

The safer alternative when a parameter becomes stale: detach it from products via [[products-products]] bulk actions first, then deactivate or delete the parameter.

### Sort priority auto-assigns on create

When the merchant creates a new variant parameter via the wizard ([[products-variants-wizard]]), its sort priority defaults to `max(sort) + 1` — appended to the end of the parameter list. The merchant can then drag-and-drop to reorder.

### Delete protection when in use

Deleting a parameter that's still used by any product fails with an in-use error. The merchant must detach products first OR delete the products before the parameter can be removed. See [[products-variants-data-model]] for the full data-model rules.

### Permission

This page requires the products / variants permission section. Moderators without it cannot see the Variants sidebar entry.

### Side effects on save

- **Search re-index** — adding / activating a variant parameter triggers a storefront search engine resync so customers can filter / see the new variants.
- **Storefront cache invalidation** — variant pickers, product listings, and category-page caches are flushed.

## Related

- [[products-variants-options]] — hub.
- [[products-variants-wizard]] — the **+ Add variant** flow this list links to.
- [[products-variants-values]] — the per-parameter Values sub-page reached by clicking the Values count.
- [[products-variants-data-model]] — hard caps (max 3 parameters per product, 500 SKUs) + delete protection mechanics.
- [[products-products]] — products list filtered via Products-count click.
- [[products-property]] — sister screen for descriptive (non-SKU) specifications.
- [[products]] — parent hub.

## Open questions

None.
