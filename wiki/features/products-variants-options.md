---
type: feature
nav_path: "Products → Variants"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Variants", "Variant parameters", "Product variants", "Options", "Product Parameters", "Variant attributes", "Parameter definitions", "Parameter taxonomy", "Варианти", "Опции", "Параметри"]
tags: [products, variants, options, sku, hub]
plan_gates: ["multi_variants", "variants.listing"]
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---

# Variants

## Purpose

**Products → Variants** is where the merchant defines the **variant parameters** that split a product into separate SKUs — the customisation dimensions customers see as "pick a size" / "pick a colour" on the storefront product page. A T-shirt with Size and Colour as variant parameters becomes 4 size × 5 colour = 20 SKUs, each with its own inventory, barcode, and price.

This page is the **hub** for the variants admin surface. The screen has grown large enough — list table, 2-step wizard, 6 option types with per-type validation, per-parameter Values sub-page with Merge action, a paid plan-gated "separate product in listing" toggle, hard data-model caps, and the parallel JSON-API v2 surface — to warrant a split into focused aspects. Use the catalogue below to drill into the relevant slice.

**Variants are different from properties.** Variants create separate stock units; each combination is a separate SKU with its own quantity tracked independently. They're **purchase-determining** — the customer must pick before adding to cart. Properties ([[products-property]]) are descriptive specifications. They don't create SKUs and don't gate the add-to-cart action. Choose carefully: a T-shirt size goes here (it's a SKU); a laptop's "has wifi" goes to properties (it's informational).

## Where to find it

Sidebar → Products → **Variants**. Route `/admin/products/variants`. Breadcrumb: "Products → Variants". Header icon: sliders.

## Sub-pages (in this cluster)

The Administrator-facing surface is split into 8 aspect pages. Drill into the aspect that matches the question — don't read the whole cluster end-to-end.

- [[products-variants-list-table]] — the default paginated table; columns (Name / Values / Products / Active / Sort priority); drag-reorder; bulk actions; Active-toggle semantics.
- [[products-variants-wizard]] — the **+ Add variant** 2-step modal (Step 1: settings; Step 2: values) + the single-screen Edit modal for existing parameters.
- [[products-variants-types]] — catalogue of the 6 option types (Select / Radio / Image sample / Color sample / 2D schema / Numeric alpha) + per-type value validation patterns.
- [[products-variants-values]] — the per-parameter Values sub-page: create-or-edit modal, the **"Enable Drag and drop sorting"** toggle that must be on before drag-reorder works, delete protection.
- [[products-variants-merge]] — the **Merge values** operation: consolidate values store-wide (survivor + values-to-merge), reassign variants, **rewrite past orders**, cross-parameter merge; permanent and deletes the merged values.
- [[products-variants-listing-toggle]] — the paid "Show each variant as a separate product in listing" toggle, the `variants.listing` gate, the 24-hour throttle, and the storefront listing-rebuild effect.
- [[products-variants-data-model]] — hard caps (3 parameters per product, 500 SKUs per product), cross-parameter limits, type-locked-once-in-use, delete protection, sort-priority auto-increment, fillable + `diff` tracking.
- [[products-variants-api]] — the JSON-API v2 surface (`/api/v2/variant-parameters`, `/api/v2/variant-options`, `/api/v2/variants`), same validation + same side effects, no webhooks on parameter / value CRUD.

## What the merchant can do here

This is a navigation hub — concrete actions live on the aspect pages. At a glance:

- Manage the store-wide variant parameter catalogue (list + wizard + edit + delete).
- Manage option values per parameter (add, edit, reorder, merge, delete).
- Pick the customer-facing UI shape per parameter (one of 6 option types).
- Opt into the paid per-variant listing feature (`variants.listing`).
- Bulk-create / update via [[apps-csv-import]] or the JSON-API v2 endpoints.

## Settings & fields

The full field catalogue lives on the aspect pages. Top-level summary:

| Surface | Aspect page | Key fields / controls |
|---|---|---|
| List columns | [[products-variants-list-table]] | Name, Values count, Products count, Active, Sort priority |
| Wizard Step 1 | [[products-variants-wizard]] | Name, Option type, advanced toggles |
| Wizard Step 2 | [[products-variants-wizard]] | Per-type value-input fields |
| Values modal | [[products-variants-values]] | Name + (image / hex / 2D coords) depending on parameter type |
| Merge values | [[products-variants-values]] | Primary value + Values to merge |
| Listing toggle | [[products-variants-listing-toggle]] | `variants.listing` toggle + variant-name-in-title toggle |

## Business rules

The full rule set lives on the aspect pages. The four cross-cutting rules that touch most aspect pages:

- **Max 3 variant parameters per product** + **max 500 variant combinations per product**. Hard data-model caps. See [[products-variants-data-model]].
- **Parameter type is locked once products use it.** The merchant must recreate to switch types. See [[products-variants-data-model]] + [[products-variants-wizard]].
- **Merge values is irreversible** AND rewrites past order-lines too — use it when retroactively cleaning up the catalogue. Parameter rename does NOT cascade to order history. See [[products-variants-values]].
- **The `variants.listing` toggle is 24-hour throttled** independently of the plan gate, because it triggers a storefront listing rebuild. See [[products-variants-listing-toggle]].

## Plan gates

This feature is gated by two plan-feature keys (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `multi_variants` | Boolean | Whether variants are available at all on the merchant's plan. The `/admin/products/parameters` (legacy) and `/admin/products/variants` URLs are access-gated — when the feature is locked, navigating here redirects to the per-feature upsell. The wizard cannot be opened, and the product editor's Variants section is hidden. |
| `variants.listing` | Boolean | The "Show each variant as a separate product in listing" paid toggle. See [[products-variants-listing-toggle]] for the 24-hour throttle and storefront rebuild effect. |

## Related

- [[products]] — parent hub.
- [[products-products]] — the actual variant-to-product matrix lives on each product's Edit page.
- [[products-property]] — descriptive specifications (no SKU split); compare-and-contrast with variants.
- [[products-categories]] — variants are store-wide (NOT category-scoped); compare with properties which ARE category-scoped.
- [[products-inventory]] — stock is tracked per variant SKU; the inventory view aggregates by product but lets the merchant drill into per-variant quantities.
- [[products-change-log]] — surfaces per-variant `diff` history (audit trail for changes).
- [[settings-files]] — Image-sample value images stored here.
- [[apps-csv-import]] — bulk-create variants + values via CSV.
- [[apps-listing-engine]] — companion app that reacts to the `variants.listing` toggle.
- [[variants-model]] — the broader Parameter / Option / Variant conceptual model.
- [[variant]] — entity page.
- [[product]] — entity page.
- [[json-api-v2]] — auth, rate-limit, and the side-effects principle for the API path.

- [[variants-index-new]]
## Open questions

- Exact mechanism of the value-text rename cascade onto live variants — `(verify)`. Tracked on [[products-variants-values]] + [[products-variants-data-model]].
