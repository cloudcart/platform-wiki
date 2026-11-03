---
type: feature
nav_path: "Products → Properties → Values (per property)"
route_name: category-property-values
route_path: /admin/products/property
aliases: ["Property values", "Property options", "Option values", "Property → Values"]
tags: [products, properties, values, options, taxonomy]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[products-property]]. See the hub for the other aspects (list view, wizard, categories, merge, business rules, programmatic access).

# Properties — values sub-page

## Purpose

The per-property sub-page that manages the discrete option values (Red, Blue, Cotton, 16GB, etc.) for a Checkbox-type property. Each value carries its own metadata — image, description, SEO — that surfaces on the storefront's filter sidebar and (on some themes) on a dedicated value landing page.

Range-type properties have no discrete values (the slider auto-computes min/max from product data at runtime), so the sub-page is meaningful only for Checkbox-type properties.

## Where to find it

Sidebar → Products → **Properties** → click the **Values** count for the row of the relevant property. The page opens from [[products-property-list-view]].

## What the merchant can do here

- See all option values for the property.
- **Drag-and-drop** to reorder values — controls the order on the storefront filter.
- Click **+ Add property value** to open the **Create / Edit value modal** (`xl`-sized — see field table below).
- Click an existing value name to open the same modal pre-loaded for editing.
- Open the **Merge values** modal — see [[products-property-merge]] for the dedicated aspect.
- **Bulk-delete** with confirmation.
- **Filter / search** within values.

## Settings & fields

### Create / Edit value modal

`xl`-sized popup. Two cards.

| Section | Field | Notes |
|---|---|---|
| **General settings** | **Name** | Required free text — the value as customers see it (e.g., "Red", "Cotton", "16GB"). Max **191 characters** (server-side, same cap as the property name). |
| General settings | **Description** | Optional rich-text editor. Shown on the dedicated value landing page on some storefronts. |
| General settings | **Category Property Image** | Optional single image (e.g., colour swatch). When an existing image is removed, the modal POSTs `/admin/api/core/properties/image/{id}` to clear it. Dimensions / max-thumb-size are governed by the parent property's `width`, `height`, `max_thumb_size` fields — see [[products-property-business-rules]]. |
| **Advanced settings** (collapsible) | **SEO title** | Optional. |
| Advanced settings | **SEO description** | Optional. |
| Advanced settings | **URL handle** | Optional URL slug for the value's storefront page. Managed via the shared `CcSeoConfiguration` block with a category-property URL prefix. |

### Range-type properties

Range-type properties have no option values — the merchant does NOT use this sub-page to define a range. The slider's min/max is auto-computed at runtime from the actual products' Range values. The merchant sets only the **Range decimal places** field on the property record itself; see [[products-property-wizard]].

If a Range property somehow has option values (e.g., legacy data, or because it was created via [[products-property-api|JSON-API v2]] as `select`/`radio` before re-classification), the Values sub-page still lists them but they don't drive the storefront filter.

## Business rules

- **Value name length cap: 191 characters** (server-side validated).
- **Value images dimensions are merchant-controlled at the parent-property level.** The `width`, `height`, and `max_thumb_size` fields are set on the property record, not per value. So all value-images for a single property share the same dimension rules. The merchant picks the dimensions that fit the storefront design — there is no platform default size. This **answers the recommended-image-size question** — the merchant SETS the dimensions; the platform enforces them.
- **Detaching a category does NOT cascade-delete per-product values that reference values defined here.** Orphan values remain in storage and reappear if the category is re-attached — see [[products-property-categories]].
- **Drag-reorder controls storefront order.** The sort order of values is the order in which they appear under the property on the storefront filter sidebar.
- **Saving a value triggers a storefront search-engine re-sync** for products tagged with the value — see [[products-property-api]] for side-effect detail.
- **Value merge consolidates values irreversibly** — see [[products-property-merge]] for the dedicated mechanics (cross-property merge, deduplication, ES re-sync, transactional behaviour).
- **The storefront product detail page joins on the product's PRIMARY category only.** A product in three categories (Electronics → Phones → Smartphones) only shows the values whose parent property is attached to the product's **primary `category_id`** in the Specifications table. Important for multi-category property strategies — see [[products-property-business-rules]].

### Permission

Requires the `products` permission section.

## Related

- [[products-property]] — hub.
- [[products-property-list-view]] — entry point (Values count cell).
- [[products-property-merge]] — the Merge values modal opens from this page.
- [[products-property-wizard]] — step 3 creates option values; this sub-page edits them.
- [[products-property-business-rules]] — full business-rule catalogue (image dimensions per property, orphan values, primary-category JOIN).
- [[products-property-api]] — JSON-API v2 surface for values (`api-property-options`).
- [[products-products]] — products carry per-product values into their editor.
- [[settings-files]] — value images stored here.

## Open questions

None.
