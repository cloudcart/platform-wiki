---
type: concept
nav_path: "Concept → Variants model → Pricing"
aliases: ["Variant pricing", "Per-Variant price", "Price override", "price_from price_to", "Default Variant pricing", "Variant discount", "Цена на вариант"]
tags: [catalog, variants, parameters, options, concepts, pricing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[variants-model]]. See the hub for the other aspects (Parameter, Option, matrix generation, inventory link, image mapping, known issues).

# Variants model — Pricing

## Definition

Each [[variant|Variant]] carries its **own** `price` that **overrides** the parent [[product|Product]]'s base price. If the Variant's `price` is unset, the Variant inherits the base price. On top of that, the platform supports per-Variant fixed-amount discounts (a separate `discount_price` field on the Variant record), per-Variant `delivery_price` shipping cost overrides, and per-Variant unit-of-measure pricing (e.g., "5 BGN per 100 g" computed from `base_unit_value` + `base_unit_id`).

The parent Product also carries two **denormalised** fields recomputed on every Variant price save:

- `price_from` — min(Variant.price across this product's Variants).
- `price_to` — max(Variant.price across this product's Variants).

These are the "from / to" range the storefront shows on category cards when the customer hasn't picked a Variant yet. The `default_variant_id` — the Variant shown in the listing card's price box by default — is also auto-recomputed on price save: lowest price wins, ties broken by Variant ID (oldest / first-created wins). The merchant cannot pick it manually; to force a Variant to be the default, price it lower than all siblings (and raising the cheapest sibling's price can demote it). See [[variants-matrix-generation]] for the auto-recomputation chain.

Both `price` and `discount_price` are capped at 1,000,000,000 minor units — effectively unlimited for normal goods, but a guard against import-data overflow.

## Scope

Covered here:

- Per-Variant `price` override of the parent product base price.
- Per-Variant `discount_price` (fixed-amount discount stored on the Variant).
- Per-Variant `delivery_price` shipping cost override.
- Per-Variant unit-of-measure pricing (`base_unit_value` / `base_unit_id` / `unit_type`) and the auto-fill behaviour.
- The 1,000,000,000 minor-units cap on `price` and `discount_price`.
- `price_from` / `price_to` denormalisation on the parent product.
- `default_variant_id` auto-recomputation (lowest price, ties by ID).
- How storefront discount rules target specific Variants.
- Bulk-editing Variant prices from the product editor matrix.

Not covered here:

- The full matrix layout / 3-Parameter cap / 500-Variant cap — see [[variants-matrix-generation]].
- Cart-level / order-level discount stacking — see [[marketing-discounts]] + [[discount-stacking]].
- Multi-currency conversion — see [[multi-currency]].
- Quantity-tier discounts that scale per-Variant — see [[marketing-discounts-quantity]].
- Cart-level Product Options price modifiers — see [[products-options-overview]].

## Contrasts

- **Variant `price` vs Product base price** — the Variant `price` overrides the parent product's base price when set. Unset Variant `price` inherits the base price. The base price is still useful as the default and as the fallback on simple (single-Variant) products.
- **Variant `discount_price` vs cart-level Discount rules** — `discount_price` is a fixed amount stored on the Variant record itself (the "old price strikethrough" pattern). Cart-level Discount rules from [[marketing-discounts]] are runtime rules that fire on conditions (cart total, customer group, coupon code) and are NOT stored on the Variant.
- **Variant `price` vs Product Options price modifier** — Variant `price` is a per-SKU override; [[products-options-overview|Product Options]] price modifiers (additive / multiplicative / per-quantity) apply to the SAME SKU based on customer-input customisations at the cart line. Both can stack on the same order line.

## Where it applies

Per-Variant pricing surfaces on:

- The Variants matrix on [[products-products]] — the merchant edits per-Variant `price`, `discount_price`, `delivery_price`, `weight`, `minimum` directly in the grid. Bulk-edit by selecting rows.
- [[products-inventory]] — drill into per-Variant `quantity`; some price fields visible on the row.
- The storefront product detail page — Variant price shown when the customer picks Options; `price_from` / `price_to` shown before any pick. Discounted Variants show the strikethrough price + the discounted price.
- The storefront category page — each card shows the `default_variant_id`'s price (or `price_from` if the variant-aware listing mode is off).
- [[marketing-discounts]] — Discount rules can target specific Variants (Variant ID, SKU, or Parameter-Option combination); they combine with `discount_price` / per-Variant `price` per the [[discount-stacking]] precedence.
- [[marketing-discounts-quantity]] — quantity-tier discounts work on per-Variant stock (e.g. a 5-for-4 deal on a specific Colour-Size evaluates against that Variant's cart quantity).

### Unit-of-measure pricing and auto-fill

The unit-of-measure fields drive the storefront's "X BGN per unit" display:

| Field | Purpose |
|-------|---------|
| `unit_id` | The Variant's unit (kg, g, L, ml, etc.). |
| `unit_value` | Amount in that unit — e.g., 500 for a "500 g" Variant. |
| `unit_text` | Optional free-text override of the unit name. |
| `base_unit_id` | Base unit for the per-unit price — copied from `unit_id` if left empty. |
| `base_unit_value` | Amount in the base unit — set to `1` if left empty. |
| `unit_type` | Display-type hint for the per-unit price. |

Auto-fill on save: if `unit_id` is set but `base_unit_id` is empty it copies `unit_id`; if `unit_id == base_unit_id` and `base_unit_value` is empty it sets `base_unit_value = 1`. Result: a "500 g" Variant priced at 25 BGN displays "5 BGN per 100 g" automatically — the merchant never computes the per-unit price.

### Bulk-managing Variant prices

Bulk price management across a product's Variants is done in the Variants matrix on [[products-products]] — the merchant edits prices in the grid and selects rows for bulk-edit. There is no separate per-Variant bulk-price tool outside the matrix. For cross-product bulk updates (e.g. raise every Variant of a category by 10 %), use [[apps-csv-import]] CSV import with the price columns populated, or the Products-list bulk-edit tooling.

### What a price save triggers

Saving a Variant price (even a no-change save) re-indexes the parent product for storefront search, clears the cached product / category listings, and sends the `product.updated` webhook to receivers configured on [[settings-hooks]]. Receivers should be idempotent. Bulk updates de-duplicate by parent product — saving 50 Variants of one product fires these once, not 50 times.

## Related

- [[variants-model]] — hub.
- [[variants-matrix-generation]] — the 500-Variant cap, the v1/v2/v3 slot model, default_variant_id auto-recomputation.
- [[variants-inventory-link]] — per-Variant `quantity` (the stock side, distinct from price).
- [[product]] — Product entity carrying base price + denormalised `price_from` / `price_to` / `default_variant_id`.
- [[variant]] — Variant entity carrying `price` / `discount_price` / `delivery_price` / unit fields.
- [[products-products]] — product editor with the per-Variant pricing grid.
- [[products-inventory]] — per-Variant stock screen.
- [[marketing-discounts]] — cart-level Discount rules that can target Variants.
- [[marketing-discounts-quantity]] — quantity-tier discounts per Variant.
- [[discount-stacking]] — precedence between Variant `discount_price` and cart-level discounts.
- [[multi-currency]] — currency conversion of per-Variant prices.
- [[settings-hooks]] — `product.updated` webhook fires on every price save.

## Open Questions

None.
