---
type: feature
nav_path: "Marketing → Discounts → Products"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Fixed discount products", "Fixed-price products", "Per-product price override", "Фиксирана отстъпка"]
tags: [marketing, discounts, fixed, per-product-price]
plan_gates: ["discount_fixed", "total_discounts"]
created: 2026-05-23
updated: 2026-06-10
source_count: 5
---

# Fixed-discount products (per-product price override)

## Purpose

The **Fixed-discount products** page is the per-product management surface for a **Fixed-type discount** — the discount that sets a specific *target price* on a product (or per-variant) rather than a percent-off / amount-off calculation. Fixed discounts answer the merchant's question: *"I want this smartphone, normally 2,500 EUR, to sell for exactly 1,999 EUR during the campaign — and I want the 'was 2,500 / now 1,999' formatting to show on the listing."*

Unlike Global / Promo / Container discounts (which subtract a value at cart-evaluation time), a Fixed discount **stamps a per-variant price** that becomes the effective catalog price. The platform writes a row to `product_to_discount` per product variant — the storefront reads that row when rendering category pages and product detail pages, displaying "from <original> / now <fixed>" formatting automatically.

The merchant uses this page to:

- See every product currently attached to the Fixed discount (with their variant pricing).
- Add products (via the product picker workflow on the parent Discount form, then drill in here to set prices).
- Edit a product's fixed prices — choose between **Single price for all variants** (e.g., flat 999 EUR whatever the size) or **Different price for each variant** (e.g., S=899, M=999, L=1099).
- Optionally set the **MSRP (Manufacturer's Suggested Retail Price)** as the struck-through "was" price — useful when the merchant's catalog price already reflects an everyday discount and they want to show a deeper apparent saving (legacy form only — see [[fixed-discount-validation-rules]]).
- Toggle a product's discount on or off (per product, not per variant).
- Bulk-toggle and bulk-delete products from the Fixed discount's attachment list.

## Where to find it

From the [[marketing-discounts]] list, click "Products" on any **Fixed** discount row. The breadcrumb reads "Marketing → Discounts → Products". The route is `discounts-products` at `/admin/marketing-new/discounts/products/:id` (component `MarketingDiscountsProductsPage` — the SAME page documented in [[marketing-discounts-products]], since per-product price assignment is the shared mechanism for Fixed-type discounts). The rows shown are the products attached to this Fixed discount.

The per-product price-edit form opens as a modal (`DiscountsProductModal`) over this page; it loads/saves via the discount-products API at `/admin/api/core/discounts/products/{id}`.

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[fixed-discount-product-modal]] — list-view columns, the `DiscountsProductModal` flow, **Common price** (`single`) vs **Multiple price** (`multiple`) modes, parent-discount create form, what the merchant cannot do here.
- [[fixed-discount-validation-rules]] — `fixed_price ≤ variant.price` enforcement; the legacy form silent-skip vs modern API `save = 0` divergence; **MSRP mode** with `msrp_price > fixed_price`; per-variant uniqueness within a single Fixed discount (and the absence of cross-discount uniqueness); `date_end = today` is allowed.
- [[fixed-discount-row-writes]] — the per-variant `product_to_discount` row layout; customer-group fan-out (one row per group per variant); the denormalized `save` field; the replace-then-recreate save transaction; per-variant date inheritance; auto-deactivation on catalog-price drop.
- [[fixed-discount-plan-gates]] — `discount_fixed` numeric + access gate; `total_discounts` aggregate ceiling; HTTP 403 *"Not supported by plan"* on cap; the 10-minute activation cooldown (applies to Fixed); `marketing.discounts` permission.
- [[fixed-discount-api-access]] — JSON-API v2 dual-resource model (`/api/v2/discounts` + `/api/v2/product-to-discount`); GraphQL `Discount` mutations; identical side-effect pipeline regardless of source; the API-path divergence on `fixed_price = variant.price`; no audit-log row.
- [[fixed-discount-storefront-display]] — variant-grid build for the modal; the storefront read path against `product_to_discount`; "was / now" + "Save X EUR" rendering in standard vs MSRP mode; the auto-deactivation feedback loop.

## What the merchant can do here

Top-level entry points (full detail lives on the aspect pages):

| Action | Aspect page |
|---|---|
| List / filter / sort attached products; bulk toggle / delete | [[fixed-discount-product-modal]] |
| Add a product, pick pricing mode, enter per-variant prices | [[fixed-discount-product-modal]] |
| Understand why a price was rejected at save | [[fixed-discount-validation-rules]] |
| Understand what got written to `product_to_discount` | [[fixed-discount-row-writes]] |
| Hit *"Not supported by plan"* or the cooldown toast | [[fixed-discount-plan-gates]] |
| Drive Fixed discounts from an external integration | [[fixed-discount-api-access]] |
| Diagnose "the storefront still shows old price" | [[fixed-discount-storefront-display]] |

## Settings & fields

The full field-by-field tables live on the aspect pages. Top-level controls reachable from this page: **list columns** — Product Name, Price, Active (inline toggle), row remove (see [[fixed-discount-product-modal]]); **per-product edit modal** — `price_type` (`single` / `multiple`) + `prices[]` array per variant with `variant_id` + `price` (catalog, read-only) + `fixed_price` (+ `msrp_price` in legacy MSRP mode); **endpoints** — list / save / toggle / remove via `/admin/api/core/discounts/products/{id}`. See [[fixed-discount-api-access]] for the full table.

## Business rules

Summary (drill into the aspect page for the verified detail):

- **Per-variant attachment via `product_to_discount`** — one row per variant (NOT per product); customer-group fan-out clones the row per group. See [[fixed-discount-row-writes]].
- **`fixed_price ≤ variant.price`** — equality passes validation; legacy form silently skips, modern API writes a `save = 0` row. See [[fixed-discount-validation-rules]].
- **MSRP mode** (`msrp = 1`) — separate "was" price; `msrp_price > fixed_price` enforced. Legacy form only — modern Vue modal does NOT expose this. See [[fixed-discount-validation-rules]].
- **Plan gating** — `discount_fixed` quota counted at the **discount level**, not the product level (unlimited products per discount). See [[fixed-discount-plan-gates]].
- **10-minute activation cooldown** — *"You've already activated this discount. Please wait:minutes minutes…"*. See [[fixed-discount-plan-gates]].
- **Auto-deactivation on catalog price drop** — catalog ≤ fixed → row deactivates automatically. See [[fixed-discount-row-writes]].
- **No cross-discount uniqueness** — two Fixed discounts CAN both target the same variant; storefront picks the cheapest. See [[fixed-discount-validation-rules]].

## Related

- [[marketing-discounts]] — parent hub; the Fixed discount type lives there.
- [[marketing-discounts-products]] — shared per-product price assignment page (same component).
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] — sibling no-code discount types.
- [[marketing-discounts-codes]] / [[marketing-discounts-code-pro]] — code-based discount types.
- [[marketing-discounts-quantity]] / [[marketing-discounts-countdown]] — other discount-type siblings.
- [[discount]] — entity page for the parent Fixed discount record.
- [[discount-stacking]] — per-type cooldown table + multi-discount evaluation rules.
- [[discounts-eligibility]] — how customer groups / geo zones / date windows scope eligibility.
- [[discounts-storefront-display]] — cross-cutting storefront rendering of any discount type.
- [[products-products]] — products attached to the Fixed discount.
- [[customers-custom-groups]] — customer groups under the parent Fixed discount drive per-group row fan-out.
- [[settings-hooks]] — `discount.created` / `discount.updated` webhooks fire on each save here.
- [[apps-cart-rules]] — Cart Rules see Fixed-discount prices as the per-line "after discounts" amount.
- [[analytics-top-order-product-discounts]] — analytics dashboard surfacing top product-level discount usage.
- [[products-banners-labels]] — separate visual-label / sticker feature (a Fixed discount can carry a banner via the parent Discount's `banner` field).

## Open questions

No outstanding questions at the hub level. Aspect pages may carry their own open items.
