---
type: feature
nav_path: "Products → Options → Add / Edit → Applicable products"
route_name: apps.product_options.edit.new
route_path: /admin/products/options-new/:type/:id?
aliases: ["Product option assignment", "Option mapping", "Applicable products for option", "Приложими продукти"]
tags: [apps, products, options, customisation]
plan_gates: ["product_options"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-options-overview]]. See the hub for the other aspects (types, pricing, order handling).

# Product Options — assignment scope

## Purpose

Decides **which storefront products show an option**. An option is dormant until it is assigned to a scope. The assignment is configured in the **Appearance / Applicable products** card of the Add / Edit option form: the merchant picks a scope type and then selects the matching targets.

## Where to find it

Sidebar → Products → **Options** → **+ Create new option** (or edit) → **Appearance / Applicable products** card → **Choose a type** dropdown + the target picker below it.

## What the merchant can do here

- Choose one of four assignment scopes for the option.
- Pick the specific products, category, vendor, or smart collection the option applies to.

## Settings & fields

| Field | Type | Notes |
|-------|------|-------|
| **Choose a type** (`mapping`) | Dropdown — Select (none) / **Specific product/s** / **Product category** / **Manufacturer** / **Smart collection** | Required to activate the option on the storefront. |
| **Mapping-target picker** | Multi-tag picker against the matching autocomplete endpoint | Endpoints: `/admin/api/core/products/search` (product), `/admin/api/core/product-categories/search` (category), `/admin/api/core/vendors/search` (vendor), `/admin/api/core/collections/search` (selection). Changing the mapping type clears the previously-selected targets. |

## Business rules

### Four assignment scopes

The option is attached to exactly one scope:

- **product** — attach to specific product(s); only those products show the option on their storefront page.
- **category** — every product in the chosen category inherits the option.
- **vendor** — every product from the chosen vendor / manufacturer inherits the option.
- **selection** — every product in a [[products-smart-collections|smart collection]] inherits the option.

### Mapping is required and validated

When saving, **Mapping** is required and must be one of `product` / `category` / `vendor` / `selection`. The matching target field (e.g. `product[]` when mapping = product) is required once that mapping is chosen. Changing the mapping type clears any previously-selected targets.

### Empty target = saved but dormant

When the target list is empty (e.g. a vendor with no products), the option is saved but stays **inactive** on the storefront until products start matching the scope. Combined with the per-option **Active** toggle from the Options list, both must resolve to "on + matching products" for the option to render.

### Storefront sort priority

The order options appear on the storefront product page is the **Sort priority** set by drag-reorder on the Options list ([[products-options-overview]]) — assignment scope decides *which* products show the option, sort priority decides *the order* within a product.

## Related

- [[products-options-overview]] — hub.
- [[products-options-types]] — the option's input type.
- [[products-smart-collections]] — the `selection` scope target.
- [[products-products]] — products that inherit assigned options.
- [[product-option]] — the underlying option entity.

## Open questions

None.
