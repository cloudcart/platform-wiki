---
type: feature
nav_path: "Marketing → Discounts → Products → Storefront display"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id
aliases: ["Fixed discount storefront", "was / now rendering", "Save X EUR label", "Variant-grid build"]
tags: [marketing, discounts, fixed, storefront, rendering]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (product modal, validation rules, row writes, plan gates, API access).

# Fixed discount — storefront display & variant-grid build

## Purpose

This aspect documents **what the customer sees** once a Fixed-discount price is live: the read path against `product_to_discount`, the "was / now" + "Save X EUR" rendering, the variant-grid build the admin modal uses to populate its form, and the auto-deactivation feedback loop's user-visible outcome. For what the merchant entered, see [[fixed-discount-product-modal]]; for what got persisted, see [[fixed-discount-row-writes]].

## Where to find it

The storefront rendering happens automatically on every product card, category listing, and product-detail page where an active `product_to_discount` row matches the current customer-group + active date window. There is no merchant-side admin screen for the read-path — the merchant verifies behaviour by visiting the storefront or inspecting the saved rows via the JSON-API v2 path in [[fixed-discount-api-access]]. The variant-grid build documented here runs when the admin modal at `/admin/marketing/discounts/products/:id` opens for an existing Fixed-discount + product pair.

## What the merchant can do here

- Verify the "was / now" + "Save X EUR" rendering on the storefront matches the prices saved in the admin modal.
- Diagnose "I raised my catalog price and the campaign price is still gone" — see the auto-deactivation feedback loop below.
- Understand why a product with two overlapping Fixed discounts shows the cheaper of the two.

## Settings & fields

This aspect introduces no new merchant-editable fields. The displayed prices come from the `product_to_discount` row's `price` (fixed price) and `save` (denormalized delta) — see [[fixed-discount-row-writes]]. The variant-grid build merges the following from existing product data:

| Source | What it provides | Used for |
|---|---|---|
| Variant identity (`id`, `quantity`, `sku`, `barcode`) | Identity columns. | Per-row keying. |
| Catalog `price` / `price_input` / `price_formatted` | "Price in store" (read-only). | Validation cap + "was". |
| Property / value pairs (`p1_id`, `p1`, `v1_id`, `v1`, …) up to `total_variants` | Attribute labels. | "Red / XL" row label. |
| Existing `product_to_discount` row (if any) | `discount_price`, `discount_price_input`, `discount_price_formatted`. | Pre-fill on Edit. |

## Business rules

### Variant-grid build for the modal

When the modal opens for an existing Fixed discount + product pair, the form builds one row per variant by merging the four **Settings & fields** sources above (the same merger [[fixed-discount-product-modal]] documents at the UI layer). Two behaviours go beyond a plain merge:

- **A variant with no existing row** opens with an empty **New price**. It must be filled before saving: a blank price fails the save.
- **Initial mode** comes from grouping variants by their `discount_price` — all share one → `single` (Common price) mode, otherwise `multiple` (Multiple price).

### Storefront read path

For each variant on display, the storefront looks up the active per-variant `product_to_discount` row (`active = 1`, matching customer-group or null, within the parent discount's active date window). If found, it renders the row's `price` (fixed price) and `save` (precomputed delta), plus the struck-through catalog price; if not found, the catalog price is shown unchanged.

The lookup orders by `price ASC` and picks first — producing the *"customer always gets the cheapest"* behaviour when several active rows match the same variant, whether Fixed or no-code Flat or Percent (see the cross-discount-uniqueness note in [[fixed-discount-validation-rules]]).

### "was / now" rendering

The struck-through "was" price is the variant's catalog price, the "now" price is `fixed_price`, and "Save X EUR" is computed against the catalog price. Listings use the stored `save` value (see [[fixed-discount-row-writes]]); the variant price block calculates the saving from the current catalog price.

### Auto-deactivation feedback loop

When the merchant updates a product's catalog price (Products → edit), the platform re-evaluates each fixed-discount row tied to the product:

| Catalog change | Row state after re-evaluation | Customer sees |
|---|---|---|
| Drops to ≤ fixed price | `active = 0` | Catalog price (no "was / now") |
| Rises above fixed price (after a drop) | Stays `active = 0` until re-saved or switched back on | Catalog price (no "was / now") |
| Rises above fixed price (no prior drop) | Stays `active = 1`, `save` re-computed | Updated "Save X EUR" |

The row staying deactivated after a recovery is the most common Fixed-discount support ticket: *"I raised my catalog price and the campaign price isn't showing again."* The merchant must re-save the row or switch it back on — see [[fixed-discount-row-writes]].

### Cache invalidation chain

Each Fixed-discount save (or auto-deactivation) fires a **product-updated event** (invalidates the product-detail + category page fragments) and a **search-engine-sync event** (search indices update so filters / sort by effective price reflect the discount). The customer sees the new price only after the cache invalidates + search-index re-indexes; on high-traffic stores the storefront can lag the admin save by seconds — see [[storefront-architecture]] and [[background-queue-inventory]].

### Banner / sticker overlay

A Fixed discount can carry a banner / sticker via the parent Discount's `banner` field — the storefront overlays this on the product card in addition to the "was / now" pricing. The banner feature is documented at [[products-banners-labels]].

### Cart-rules see the fixed price as the "after discounts" line amount

When [[apps-cart-rules]] evaluates triggers against an in-cart line item, the per-line "after discounts" amount it sees is the fixed-discount price, NOT the catalog price. So a rule like "spend over X gets free shipping" compares its threshold against the fixed-discounted total.

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-row-writes]] — the `product_to_discount` rows this read path consumes; the auto-deactivation pipeline.
- [[fixed-discount-validation-rules]] — cross-discount overlap → "cheapest wins" lookup.
- [[fixed-discount-product-modal]] — the merchant-side form whose variant-grid is documented here.
- [[fixed-discount-api-access]] — the API surfaces that produce the same storefront-visible state.
- [[storefront-architecture]] — the ES read-side that backs the storefront's effective-price lookups.
- [[background-queue-inventory]] — the search-engine-sync queue chain.
- [[discounts-storefront-display]] — cross-cutting storefront rendering of any discount type (Fixed is one input).
- [[products-banners-labels]] — banner / sticker feature a Fixed discount can carry.
- [[apps-cart-rules]] — Cart Rules see the fixed price as the per-line "after discounts" amount.
- [[analytics-top-order-product-discounts]] — analytics dashboard surfacing top product-level discount usage.

## Open questions

No outstanding questions.
