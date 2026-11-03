---
type: entity
nav_path: "Entity → Variant → Key attributes"
aliases: ["Variant attributes", "Variant fields", "Variant record schema", "SKU fields", "Variant columns"]
tags: [entity, catalog, variants, attributes]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[variant]]. See the hub for the other aspects (lifecycle, relationships, business rules, side effects and API).

# Variant — Key attributes

## Identity

The full per-field schema for the [[variant|Variant]] record — every attribute the Variant stores, plus a precise list of what is NOT stored on the Variant despite appearing alongside it in the admin UI. This page is the reference the AI Assistant cites when a merchant asks *"Where is `compare_at_price` saved?"*, *"Does the Variant have its own active flag?"*, or *"What's the difference between `unit_id` and `base_unit_id`?"*.

The Product carries descriptive content (name, description, SEO, category, vendor) and the three master switches (`tracking`, `continue_selling`, `threshold` — see [[inventory-variant-model]]). The Variant carries inventory + money + per-SKU overrides.

## Aliases

- **Variant fields** / **Variant columns** — the per-record attribute set.
- **SKU fields** — informal merchant phrasing (SKU + price + quantity + barcode + weight all belong to the Variant).

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| `sku` | Stock-Keeping Unit code | Merchant-defined identifier for inventory + accounting. Must be unique within the store (the platform blocks duplicate SKUs on save — see [[variant-entity-business-rules]]). Empty is allowed for non-tracked products. |
| `barcode` | Barcode / EAN / UPC | Optional. Used by scanner workflows (POS, warehouse). No uniqueness constraint. |
| `price` | Selling price in cents | The price the customer pays for this Variant. Integer cents (1000 = 10 BGN). |
| `compare_at_price` / `msrp` | Strike-through price in cents | Optional. When set and greater than `price`, the storefront renders a "from X / now Y" layout. NOT in the canonical Variant fillable columns — persisted via the discount system (a `compare_at_price` is implemented as a price discount linked to the Variant). The merchant edits it in the Variants tab; the platform persists it as a discount record. |
| `cost_price` | Cost price in cents | Optional. Internal margin tracking — never shown on the storefront. Settable via CSV import (when the column is included) and readable/writable via the JSON-API v2 / GraphQL API; surfaced in admin margin / accounting reports only. (There is no product-catalogue CSV export screen — see [[apps-xml-feed]] / [[apps-google-sheets]].) |
| `quantity` | Stock on hand | Integer count. Combined with [[product|Product]]-level `tracking` and `continue_selling` to determine buyability. See [[inventory-variant-model]] for the per-Variant model. |
| `weight` | Variant weight | In the store's [[product|unit system]] (`metric` / `imperial`). Drives shipping calculation. |
| `width`, `height`, `length` | Dimensions | Optional. Used by shipping calculators that need volumetric weight. |
| `image_id` | FK to a Variant-specific image | Optional. When set, switches the storefront gallery to this image when the customer picks this Variant. Falls back to the Product's primary image. |
| `v1`, `v2`, `v3` | Denormalised option labels | Stores the human-readable option text for up to 3 parameters (e.g., `v1 = "Red"`, `v2 = "M"`). Cached on the Variant for fast search and listing. |
| `p1`, `p2`, `p3` | Parameter option IDs | FK-style references to the actual [[product-option|Parameter Option]] records — the canonical identity of which "Red" / "M" this Variant is. Up to 3, matching the product-level cap of 3 parameters. |
| `status_id` | FK → [[product-status]] (in-stock) | Per-Variant override of the Product's in-stock status label (e.g., "Ships in 2 days" for this size only). Optional — falls back to Product. |
| `out_of_stock_id` | FK → [[product-status]] (out-of-stock) | Per-Variant override of out-of-stock label + button text. Optional — falls back to Product. |
| `minimum` | Minimum order quantity for this Variant | Optional override of the Product's `minimum`. Defaults to **1** if set to 0 or negative on save (the platform silently bumps it back to 1 — see [[variant-entity-business-rules]]). |
| `threshold` | Low-stock alert threshold | Per-Variant threshold (e.g., re-order point). When `quantity` drops to / below this, [[settings-cart]] low-stock notifications fire. |
| `unit_id` | FK to measurement unit | Sold-by unit (piece, kg, m², etc.) for THIS Variant. Most products have a single unit per Product; the Variant-level unit is used for products sold in mixed-unit bundles. |
| `sort_order` | Display order among Variants | Lower = earlier in the picker. Tie-break is insertion order. |
| `delivery_price` | Per-Variant shipping surcharge in cents | Optional. When set, this amount is added to the line's shipping cost at checkout (e.g., bulky-item surcharge). Different from the base courier fee. |
| `unit_value`, `unit_text`, `base_unit_value`, `base_unit_id`, `unit_type` | Sold-by-measure metadata | When the Variant is sold by measurement (kg, m², L), the platform stores the **base unit** (e.g., 1 kg) plus the **sold unit** (e.g., 250 g). The storefront shows the unit price (price per base unit) for transparency. Auto-defaults: `base_unit_id = unit_id` and `base_unit_value = 1` when the merchant doesn't set them (see [[variant-entity-business-rules]]). |

### Hidden v1/v2/v3 normalised columns

In addition to the cached label columns (`v1`, `v2`, `v3`), the Variant also stores hidden `v1_norm`, `v2_norm`, `v3_norm` normalised lookup keys — used internally for fast deduplication and search join performance. The merchant never sees these directly; they are auto-maintained when the merchant renames a Parameter Option.

## What is NOT on the Variant row

These attributes appear alongside the Variant in the admin UI but live elsewhere:

| Attribute | Where it actually lives | Why |
|-----------|-------------------------|-----|
| `tracking` / `continue_selling` | Parent [[product|Product]] | These master switches apply to every Variant of the product equally. Editing on the Product cascades to every Variant immediately, with no per-Variant override. See [[inventory-variant-model]]. |
| Default-variant pointer | Product's `default_variant_id` column | The "default variant" is **not** a flag on the Variant row — the Product points to whichever Variant should be pre-selected on the storefront. Changing the default rewrites the Product, not the Variants. |
| Per-Variant visibility / "active" flag | Does not exist | The Variant table has **no `active` column**. To hide a single Variant from the storefront picker, the merchant must either delete the Parameter Option (which removes the Variant) or set `quantity = 0` with the parent Product's `tracking = yes` and `continue_selling = no` (greys it out in the picker). See [[variant-entity-lifecycle]]. |
| `created_at` / `updated_at` | Does not exist on the Variant | Change tracking happens at the Product level. The Product's `date_modified` ticks on every Variant save. See [[variant-entity-business-rules]]. |
| Parameter list | Parent Product (`p1` / `p2` / `p3` slots) | The Product defines WHICH parameters exist (up to 3); the Variant references WHICH options it picks for each. |

## Where it appears

- [[products-variants-options]] — variant parameter and option management.
- [[products-inventory]] — per-Variant inventory grid; bulk Update Quantities + Set / Add modes.
- [[products-products]] — Product list shows SUM of Variant quantities; the Variants tab on the product editor is where per-Variant fields are edited.
- [[apps-csv-import]] / [[apps-xml-sync]] — bulk-import paths that write per-Variant rows; CSV accepts per-Variant `compare_at_price` as a column.

## Related

- [[variant]] — hub.
- [[product]] — parent record; carries `tracking`, `continue_selling`, `threshold`, `default_variant_id`.
- [[product-option]] — Parameter Option (Red, Large, Cotton); referenced via `p1` / `p2` / `p3`.
- [[product-status]] — custom in-stock / out-of-stock status records referenced by `status_id` / `out_of_stock_id`.
- [[variants-model]] — Parameter / Option / Variant structural model.
- [[inventory-variant-model]] — per-Variant `quantity` model + the three master switches on the parent Product.

## Open Questions

None.
