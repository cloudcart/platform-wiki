---
type: feature
nav_path: "Products → Properties → List view"
route_name: category-property-list
route_path: /admin/products/property
aliases: ["Property list", "Properties table", "Properties grid"]
tags: [products, properties, filters, list, taxonomy]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-property]]. See the hub for the other aspects (wizard, categories, values, merge, business rules, programmatic access).

# Properties — list view

## Purpose

The default tab of [[products-property]] — a paginated table of every property defined for the store. From here the merchant finds existing properties, toggles their storefront visibility, re-orders them on the storefront filter sidebar, and reaches the per-property sub-pages (Categories, Values) by clicking the relevant count cell.

## Where to find it

Sidebar → Products → **Properties**. The list is the default view at `/admin/products/property`.

## What the merchant can do here

- See all properties at a glance.
- **Toggle "Use as filter"** inline — surfaces / hides the property on the storefront category filter sidebar (see [[products-property-business-rules]] for the Active vs Use-as-filter matrix).
- **Toggle "Active"** inline — soft-disables the property everywhere (editor + storefront).
- **Drag-and-drop rows** to re-order properties — controls the order of properties on the storefront filter sidebar AND on the product editor's category-properties section.
- **Sort** by any column. **Search** by name.
- Click the **Products** count to jump to [[products-products]] pre-filtered to products using this property.
- Click the **Categories** count to open the per-property Categories sub-page — see [[products-property-categories]].
- Click the **Values** count to open the per-property Values sub-page — see [[products-property-values]].
- Click **+ Add property** to open the [[products-property-wizard|3-step wizard]].
- **Bulk actions** (multi-select):
  - **Activate** — sets `active = ON` for selected rows.
  - **Deactivate** — sets `active = OFF`.
  - **Delete** — with confirmation; partially blocked when rows are in use (see [[products-property-business-rules]] delete-protection).

## Settings & fields

### List columns

| Column | Field key | Notes |
|--------|-----------|-------|
| **Property name** | `name` | Sortable. Click opens the Edit property modal (same shape as wizard step 1 — see [[products-property-wizard]]). |
| **Products** | `products_count` | Sortable. Click navigates to [[products-products]] filtered by this property. |
| **Categories** | `categories_count` | Sortable. Click opens [[products-property-categories]] for this property. |
| **Values** | `options_count` | Sortable. Click opens [[products-property-values]] for this property. |
| **Use as filter** | `is_visible` | Inline toggle. When ON, the property appears on the storefront category-page filter sidebar. |
| **Active** | `active` | Inline toggle. When OFF, the property is hidden everywhere. |
| **Sort priority** | `sort` | Sortable + draggable. Lower = higher in the filter sidebar. |
| **(actions)** | — | Per-row Delete button. |

### Bulk-action toggles vs delete

Activate / Deactivate / Use-as-filter toggles are **unrestricted by usage** — they can be flipped freely on properties in active use (the property is simply hidden; per-product values are preserved). Delete is the only action blocked when products still reference the property. See [[products-property-business-rules]] for the delete-protection rule and the error-message format.

## Business rules

- **Drag-drop reorder drives two surfaces** — the property list reorder controls both the storefront category filter sidebar AND the product editor's category-properties section. The merchant typically puts the most important properties (Brand, Color, RAM, CPU) at the top.
- **Soft-disable preserves data** — flipping Active = OFF or Use-as-filter = OFF hides the property; per-product values remain in storage and reappear when re-enabled.
- **Saving / toggling triggers a storefront search-engine re-sync** — the storefront filter behaviour reflects the new state immediately. See [[products-property-api]] for the side-effect details (shared with admin saves).

### Permission

This view requires the `products` permission section. Moderators without it cannot see the Properties sidebar entry.

## Related

- [[products-property]] — hub.
- [[products-property-wizard]] — opens from **+ Add property**.
- [[products-property-categories]] — opens from the Categories cell.
- [[products-property-values]] — opens from the Values cell.
- [[products-property-business-rules]] — Active vs Use-as-filter matrix, delete-protection, sort-priority effect.
- [[products-products]] — opens pre-filtered when the merchant clicks a Products count.
- [[products-categories]] — properties are attached to categories.

## Open questions

None.
