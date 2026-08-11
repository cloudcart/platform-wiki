---
type: feature
nav_path: "Marketing → Discounts → Products → Storefront display"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Fixed discount storefront", "was / now rendering", "Save X EUR label", "Variant-grid build"]
tags: [marketing, discounts, fixed, storefront, rendering]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (product modal, validation rules, row writes, plan gates, API access).

# Fixed discount — storefront display & variant-grid build

## Purpose

This aspect documents **what the customer sees** once a Fixed-discount price is live: the read path against `product_to_discount`, the "was / now" + "Save X EUR" rendering in standard vs MSRP mode, the variant-grid build the admin modal uses to populate its form, and the auto-deactivation feedback loop's user-visible outcome. For what the merchant entered, see [[fixed-discount-product-modal]]; for what got persisted, see [[fixed-discount-row-writes]].

## Where to find it

The storefront rendering happens automatically on every product card, category listing, and product-detail page where an active `product_to_discount` row matches the current customer-group + active date window. There is no merchant-side admin screen for the read-path — the merchant verifies behaviour by visiting the storefront or inspecting the saved rows via the JSON-API v2 path in [[fixed-discount-api-access]]. The variant-grid build documented here runs when the admin modal at `/admin/marketing-new/discounts/products/:id` opens for an existing Fixed-discount + product pair.

## What the merchant can do here

- Verify the "was / now" + "Save X EUR" rendering on the storefront matches the prices saved in the admin modal.
- Predict the headline difference between standard mode and MSRP mode, and decide whether the bigger headline is worth the framing trade-off.
- Diagnose "I raised my catalog price and the campaign price is still gone" — see the auto-deactivation feedback loop below.
- Understand why a product with two overlapping Fixed discounts shows the cheaper of the two.

## Settings & fields

This aspect introduces no new merchant-editable fields. The displayed prices come from the `product_to_discount` row's `price` (fixed price), `msrp_price` (in MSRP mode), and `save` (denormalized delta) — see [[fixed-discount-row-writes]]. The variant-grid build merges the following from existing product data:

| Source | What it provides | Used for |
|---|---|---|
| Variant identity (`id`, `quantity`, `sku`, `barcode`) | Identity columns. | Per-row keying. |
| Catalog `price` / `price_input` / `price_formatted` | "Price in store" (read-only). | Validation cap + "was". |
| Property / value pairs (`p1_id`, `p1`, `v1_id`, `v1`, …) up to `total_variants` | Attribute labels. | "Red / XL" row label. |
| Existing `product_to_discount` row (if any) | `discount_price`, `discount_price_input`, `discount_price_formatted`, `msrp_price`. | Pre-fill on Edit. |

## Business rules

### Variant-grid build for the modal

When the modal opens for an existing Fixed discount + product pair, the form builds one row per variant by merging the four **Settings & fields** sources above (the same merger [[fixed-discount-product-modal]] documents at the UI layer). Two behaviours go beyond a plain merge:

- **Pre-fill default for a new variant** (no existing `product_to_discount` row): if other variants already have discounts, the form pre-fills this variant's catalog price as the default discount price (so the merchant doesn't accidentally save 0); otherwise it stays zero / null.
- **Initial mode** comes from grouping variants by their `(discount_price, msrp_price)` pair — all share one pair → `single` (Common price) mode, otherwise `multiple` (Multiple price).

### Storefront read path

For each variant on display, the storefront looks up the active per-variant `product_to_discount` row (`active = 1`, matching customer-group or null, within the parent discount's active date window). If found, it renders the row's `price` (fixed price) and `save` (precomputed delta), plus the struck-through `msrp_price` (MSRP mode) or the catalog price (standard mode); if not found, the catalog price is shown unchanged.

The lookup orders by `price ASC` and picks first — producing the *"customer always gets the cheapest"* behaviour when multiple active Fixed discounts target the same variant (see the cross-discount-uniqueness note in [[fixed-discount-validation-rules]]).

### "was / now" rendering — standard vs MSRP mode

The struck-through "was" price depends on the parent discount's `msrp` flag:

| Mode | "was" price shown | "now" price shown | "Save X EUR" computed against |
|---|---|---|---|
| Standard (`msrp = 0`) | The variant's catalog price | `fixed_price` | Catalog price |
| MSRP (`msrp = 1`) | `msrp_price` from the row | `fixed_price` | MSRP |

The storefront uses the precomputed `save` column directly — no per-render computation (see [[fixed-discount-row-writes]] for how `save` is denormalized).

#### MSRP mode framing — bigger headline, smaller real saving

The "Save X EUR" label in MSRP mode compares against the merchant-entered `msrp_price`, NOT against the actual catalog price the storefront previously displayed. Worked example: catalog 800, MSRP 1,000, fixed price 700 → the customer sees ~~1,000~~ → **700**, "Save 300 EUR", but the true saving versus yesterday's catalog price (800) is only 100 EUR. MSRP framing yields the bigger headline; for honesty, leave MSRP mode off. The legacy form is the only place to set MSRP — the modern modal does not expose it (see [[fixed-discount-validation-rules]]).

### Auto-deactivation feedback loop

When the merchant updates a product's catalog price (Products → edit), the platform re-evaluates each fixed-discount row tied to the product:

| Catalog change | Row state after re-evaluation | Customer sees |
|---|---|---|
| Drops to ≤ fixed price | `active = 0` | Catalog price (no "was / now") |
| Rises above fixed price (after a drop) | Stays `active = 0` until a manual save | Catalog price (no "was / now") |
| Rises above fixed price (no prior drop) | Stays `active = 1`, `save` re-computed | Updated "Save X EUR" |

The row staying deactivated after a recovery is the most common Fixed-discount support ticket: *"I raised my catalog price and the campaign price isn't showing again."* The merchant must re-save the row to re-activate it — see [[fixed-discount-row-writes]].

### Cache invalidation chain

Each Fixed-discount save (or auto-deactivation) fires a **product-updated event** (invalidates the product-detail + category page fragments) and a **search-engine-sync event** (search indices update so filters / sort by effective price reflect the discount). The customer sees the new price only after the cache invalidates + search-index re-indexes; on high-traffic stores the storefront can lag the admin save by seconds — see [[storefront-architecture]] and [[background-queue-inventory]].

### Banner / sticker overlay

A Fixed discount can carry a banner / sticker via the parent Discount's `banner` field — the storefront overlays this on the product card in addition to the "was / now" pricing. The banner feature is documented at [[products-banners-labels]].

### Cart-rules see the fixed price as the "after discounts" line amount

When [[apps-cart-rules]] evaluates triggers against an in-cart line item, the per-line "after discounts" amount it sees is the fixed-discount price, NOT the catalog price. So a rule like "spend over X gets free shipping" compares its threshold against the fixed-discounted total.

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-row-writes]] — the `product_to_discount` rows this read path consumes; the auto-deactivation pipeline.
- [[fixed-discount-validation-rules]] — MSRP-mode validation; cross-discount overlap → "cheapest wins" lookup.
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
