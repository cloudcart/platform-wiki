---
type: feature
nav_path: "Products → Variants → Data-model rules"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Variant data model", "Variant limits", "3 parameters per product", "500 variants per product", "Variant fields", "Variant SKU matrix limits", "Лимити на варианти"]
tags: [products, variants, limits, data-model]
plan_gates: ["multi_variants"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Variants — data-model rules + hard caps

> Part of [[products-variants-options]]. See the hub for the other aspects (list table, wizard, types, values, listing toggle, API).

## Purpose

The structural rules and hard caps the platform enforces on variant parameters, variant values, and the per-product SKU matrix. The merchant sees them as validation errors or as toggles that go grey ("type locked", "delete blocked", "limit reached"). This page is the cross-reference for *why* a save was rejected.

## Where to find it

The rules apply on **every** parameter / value mutation reachable from **Products → Variants** (the list table, the wizard, the Edit modal, the per-parameter Values sub-page) and on the JSON-API v2 equivalents — see [[products-variants-api]].

## What the merchant can do here

This is a reference page — the merchant doesn't click anything specifically here. The caps surface as:

- "Maximum N variant parameters reached" — when adding a 4th parameter to a product.
- "Maximum 500 variants per product reached" — when the SKU multiplication exceeds the cap.
- "Parameter type cannot be changed because products are using it" — on the Edit modal Type field.
- "Cannot delete: parameter is used by products" — on parameter delete.
- "Cannot delete: value is used by variants" — on value delete.
- The 24-hour throttle on the listing toggle — see [[products-variants-listing-toggle]].

## Settings & fields

### Variant record — 19 fields (verified)

The per-SKU variant record stores:

| Field | Purpose |
|---|---|
| `item_id` | Parent product ID |
| `v1`, `v2`, `v3` | Text values for the 3 parameter slots (denormalised) |
| `v1_id`, `v2_id`, `v3_id` | FK to ParameterOption (the canonical option ID) |
| `quantity` | Stock for this SKU |
| `sku` | Unique SKU code |
| `barcode` | EAN / UPC |
| `price` | Variant-specific price (overrides product base price) |
| `delivery_price` | Variant-specific shipping cost |
| `weight` | Variant weight (for shipping calc) |
| `unit_id` | Unit-of-measure (kg / g / L / ml / etc.) |
| `unit_value` | Unit quantity (e.g., 500g means `unit_value=500` + `unit_id=g`) |
| `unit_text` | Display text override |
| `minimum` | Minimum order qty for this variant |
| `base_unit_value` | Base unit quantity (for per-unit pricing display) |
| `base_unit_id` | Base unit ID |
| `unit_type` | Unit-of-measure category |

Both text VALUE (`v1` = "Red") AND option_id (`v1_id` = 42) are stored. The text version is denormalised for fast lookup; the id is for join integrity.

### Parameter name validation

- **Name** required, max 150 characters, **unique across the store**.
- **Type** required, must be one of: `select`, `radio`, `image`, `color`, `2d`, `numeric_alpha`. Full type catalogue: see [[products-variants-types]].

## Business rules

### MAXIMUM 3 PARAMETERS PER PRODUCT (hard cap)

Variant records store only `v1`, `v2`, `v3` (+ `v1_id`, `v2_id`, `v3_id`). **A single product CANNOT have more than 3 variant parameters** — the data model has no 4th slot.

So when the wiki says "5 parameters × 10 values = 100,000 SKUs" as worry — actually impossible: max 3 parameters × N values per parameter.

**Practical SKU cap = parameter1_values × parameter2_values × parameter3_values.** E.g., 10 sizes × 5 colors × 3 materials = 150 SKUs for a 3-parameter product.

### Hard cap of 500 variants per product

A single product can have at most **500 variant combinations**. Beyond this, the save fails. So a 3-parameter product where 10 sizes × 10 colors × 6 materials = 600 SKUs would be rejected — the merchant must reduce one dimension.

### Cross-parameter limits on the same product

Within a single product's variant matrix:

- **At most 1 `numeric_alpha` parameter per product.**
- **At most 2 `2d` parameters per product.**
- **If `numeric_alpha` is present, at most 1 `2d` parameter** on the same product (combined check).

Store-wide creation is unrestricted; the limits apply only when assigning parameters to a single product. See [[products-variants-types]] for the full per-type validation.

### Variant parameter type is locked after create

Like properties, the variant parameter's type cannot be changed once products start using it. The Edit modal in [[products-variants-wizard]] shows the Type radio but server-side validation rejects the change. The merchant must delete and recreate to switch types.

### Cross-parameter exclusion via quantity 0

There is **no** "this combination doesn't exist" flag. If a product has Color + Size, but "Red Large" isn't physically available, the merchant sets the Red+Large variant's `quantity` to 0 and turns off "Continue selling when sold out" (see [[inventory-oversell]]). Customers see it as out-of-stock; the variant remains visible in the picker.

### Variants don't track created_at / updated_at

The variant record itself does not store timestamps, so the merchant cannot see when a specific variant SKU was added from the variant data alone. The parent product's timestamps and any [[products-change-log|Change log]] entries are the proxy for "when did this variant appear".

### Diff tracking on update

When a variant is updated, the platform captures the dirty (changed) fields into a `diff` object stored alongside the update. This is the per-variant change-history mechanism — used for audit / analytics. Surfaced to the merchant via [[products-change-log]].

### Fillable protection during save

Any incoming attribute NOT on the fillable list is dropped before save — prevents mass-assignment of fields that should be guarded (e.g., `id`).

### Delete protection — must detach products first

- Deleting a parameter that's currently used by any product fails with "parameter used by products". The merchant must first remove the parameter from all products that use it (via the product editor or via bulk-edit) before deletion succeeds.
- Same logic applies to deleting an individual value: if any variant uses that value, the deletion fails. The merchant can reassign products to other values or use the Merge action ([[products-variants-values]]) to consolidate values.

### Variants are store-wide (NOT category-scoped)

A "Size" parameter affects every product that uses it across all categories. Compare with properties ([[products-property]]), which ARE category-scoped.

### Side effects on save

- **Search re-index** — adding / activating a variant parameter triggers a storefront search engine resync.
- **Storefront cache invalidation** — variant pickers, product listings, and category-page caches are flushed.
- **No merchant webhook for parameter / value CRUD** — these changes don't fire `product.created` / `product.updated`; they're treated as catalog-metadata. Subscribed receivers won't be notified until a product using the parameter is itself saved.

## Related

- [[products-variants-options]] — hub.
- [[products-variants-types]] — the 6 types whose limits are enforced here.
- [[products-variants-wizard]] — Edit modal that enforces the type-locked rule.
- [[products-variants-values]] — value delete protection + merge to work around it.
- [[products-variants-list-table]] — list-screen Delete that respects the in-use protection.
- [[products-variants-api]] — same caps apply on the JSON-API v2 path.
- [[variant]] — entity page.
- [[product]] — entity page.
- [[inventory-oversell]] — quantity-0 + continue-selling pattern for "combination doesn't exist".
- [[products-change-log]] — where per-variant `diff` history surfaces for the merchant.
- [[variants-model]] — the broader conceptual model (Parameter / Option / Variant hierarchy).

## Open questions

- Exact rename-cascade mechanism when a value's text is changed (denorm refresh vs read-side join) — `(verify)`.
