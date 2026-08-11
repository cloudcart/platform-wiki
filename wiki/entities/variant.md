---
type: entity
nav_path: "Entity → Variant"
aliases: ["Variant", "Product variant", "SKU", "Variation", "Combination", "Вариант", "Вариация", "Артикул"]
tags: [entity, catalog, products, variants]
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---
# Variant

## Identity

A **Variant** is a specific sellable SKU under a [[product|Product]] — the concrete combination of parameter options the customer actually adds to a cart and pays for. For a T-shirt product with parameters "Color" and "Size", each pairing — "Red, M", "Red, L", "Blue, M" — is a separate Variant with its own SKU, barcode, price, quantity, weight, dimensions, and image. The Product carries the descriptive content (name, description, SEO, category, vendor); the Variant carries the inventory and money. Even a "simple" product with no merchant-defined parameters has exactly **one** backing Variant under the hood — that's where its SKU and quantity live.

Variants are the unit Operations, Inventory, Imports, Discounts, and Orders all reference. Order line items point to a specific Variant ID; the [[discount|Discount]] of type `fixed` targets a specific Variant; stock alerts and back-in-stock waitlists fire per Variant. See [[variants-model]] for how Product + Parameter + Option + Variant compose, and [[products-variants-options]] for the merchant-facing parameter management screen.

The Variant entity is a multi-faceted record. The AI Assistant should drill into the aspect that matches the question, not read every page.

## Aliases

- **Variant** — the canonical merchant-facing term in the admin UI, imports, and exports.
- **Product variant** — used when distinguishing from non-product variants (rare).
- **SKU** — informal merchant phrasing; each Variant has exactly one SKU value, so merchants often call the Variant itself "the SKU".
- **Variation** / **Combination** — used in some import / app contexts.
- **Артикул** / **Вариант** / **Вариация** — Bulgarian terms used interchangeably.

## Key Attributes

The Variant is split across **five well-scoped aspects**:

- [[variant-entity-attributes]] — the full per-field schema (`sku`, `barcode`, `price`, `compare_at_price`, `cost_price`, `quantity`, `weight`, dimensions, `image_id`, the cached `v1` / `v2` / `v3` denormalised labels, the canonical `p1` / `p2` / `p3` Parameter Option references, `status_id` / `out_of_stock_id` overrides, `minimum`, `threshold`, `unit_id`, `sort_order`, `delivery_price`, sold-by-measure metadata, hidden `v*_norm` columns); plus what is NOT a Variant column (no `active` flag, no own timestamps, `tracking` and `continue_selling` inherited from parent Product, default-variant pointer on the Product).
- [[variant-entity-lifecycle]] — the six states (Created, In stock, Out of stock, Oversellable, Always in stock, Deleted); how a Variant gets created (single backing Variant on simple products, auto-generation when the merchant adds a new option); how it gets deleted (cascade from Parameter Option removal); the no-per-Variant-active-flag rule and the workarounds (delete the Option or set `quantity = 0` with `tracking + no-continue-selling`).
- [[variant-entity-relationships]] — required parent [[product|Product]]; 0–3 [[product-option|Parameter Options]] via `p1` / `p2` / `p3`; optional Variant-specific image; referenced by [[order|Order]] line items, Cart line items, `fixed` [[discount|Discount]] type, back-in-stock waitlist subscribers, smart-collection rule evaluation, search-engine index entries, imports / exports.
- [[variant-entity-business-rules]] — SKU + barcode live on the Variant (not the Product); the Variant is THE sellable unit; 3-parameter hard cap; one default Variant per Product; `v1`/`v2`/`v3` denormalised labels cascade-rename on Parameter Option rename; per-Variant `quantity` (Product `quantity` is a SUM); no per-Variant timestamps; price-range computation; Variant images are optional fallbacks; SKU uniqueness store-wide (admin returns 422, bulk CSV import silently skips); `compare_at_price` / `msrp` per-Variant; restock-notification trigger; deleting a Parameter Option does NOT block on historical orders; `cost_price` visibility; `fixed` discount targeting; save-time defaults (`minimum` floor, `base_unit_id` / `base_unit_value` defaults); cascade cleanup of `ImageVariant` and external-meta-data rows on delete.
- [[variant-entity-side-effects-and-api]] — JSON-API v2 access via [[api-variants]] (always under a parent product, no standalone create); same side effects on both paths (parent `date_modified` tick, the search re-index, `updateProductsDefaultVariant`, SKU uniqueness 422); the one difference from the admin path (JSON-API does NOT clamp `quantity ≥ 0`); the 500-variants-per-product and 3-Parameter-Option-per-Variant caps enforce on both paths; deletion semantics via either path (order-line `variant_id` set NULL but snapshots remain).

## Why it matters to the merchant

The Variant record is the **money-and-stock layer** of the catalogue. Five high-impact behaviours the merchant should understand:

- **SKU, barcode, price, and quantity are per-Variant — never on the Product.** Even a "simple" product has one backing Variant. See [[variant-entity-business-rules]].
- **Deleting a Parameter Option deletes its Variants.** Historical orders that reference those Variants keep snapshotted SKU + label text, but `variant_id` is set to NULL. See [[variant-entity-lifecycle]] + [[variant-entity-business-rules]].
- **`compare_at_price` and `cost_price` are per-Variant.** Edit on the Variants tab — older layouts only show the Product-level field. See [[variant-entity-business-rules]].
- **SKU uniqueness is store-wide; the bulk CSV path silently skips duplicates** while the admin / JSON-API paths return a hard validation error. See [[variant-entity-business-rules]] + [[variant-entity-side-effects-and-api]].
- **There is no per-Variant `active` flag.** To hide a single combination, the merchant deletes the Parameter Option or sets `quantity = 0` with `tracking = yes` + `continue_selling = no`. See [[variant-entity-lifecycle]].

## Where it appears

- [[products-variants-options]] — Variant parameter and option management; the screen where the merchant defines which Variants exist.
- [[products-inventory]] — per-Variant inventory tracking (the master inventory grid).
- [[products-products]] — Product list shows the SUM of Variant quantities; the per-Product detail page exposes the Variants tab.
- [[orders-details]] — order line items reference Variants (the line shows the Variant's SKU + denormalised labels).
- [[orders-ordered-products]] — per-Variant order line item view.
- [[marketing-discounts-fixed]] — `fixed` discount type picks a specific Variant.
- [[products-missing-product]] — back-in-stock waitlist; per-Variant.
- [[customers-details-products]] — customer's purchased-Variant history.

## Related

### Related entities

- [[product]] — required parent. Carries the descriptive content; the Variant carries the inventory and price.
- [[product-option]] — Parameter Option (Red, Large, Cotton). A Variant references up to 3 Parameter Options.
- [[order]] — orders contain Variant line items.
- [[discount]] — `fixed` discount type overrides a specific Variant's price.
- [[product-status]] — custom in-stock / out-of-stock labels can be overridden per-Variant.
- [[file-asset]] — Variant-specific image storage.

### Cross-cutting concepts

- [[variants-model]] — how Product + Parameter + Option + Variant compose into the SKU matrix.
- [[inventory-tracking]] — stock decrement timing, oversell rules, low-stock thresholds — all evaluated per Variant.
- [[inventory-variant-model]] — the Variant-as-unit-of-stock rule + the three master switches on the parent Product.
- [[checkout-flow]] — how a cart line resolves to a specific Variant at checkout.

## Open Questions

No outstanding questions — all items resolved or distributed to sub-pages.
