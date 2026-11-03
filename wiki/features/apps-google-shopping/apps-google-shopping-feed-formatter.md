---
type: feature
nav_path: "Apps → Google Shopping → Feed formatter"
route_name: apps.google_shopping
route_path: /admin/apps/google_shopping
aliases: ["Google Shopping feed formatter", "GMC payload builder", "Google Shopping product payload", "Variant offer mapping", "item_group_id"]
tags: [apps, google, shopping, feed, payload, formatter]
plan_gates: ["google_shopping"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Google Shopping → Feed formatter (per-variant offer payload)

> Part of [[apps-google-shopping]]. See the hub for the other aspects (settings, attributes, products, status, auto-sync, batch upload).

## Purpose

The **feed formatter** turns each CloudCart Variant into the Google Merchant Center (GMC) offer payload sent to the Shopping Content API — encoding variant grouping, sale-price effective dates, unit pricing, condition + adult flags, dimensions in cm, weights in grams, custom labels, and expiration dates.

The merchant cannot edit the formatter, but knowing what it sends explains why specific GMC disapprovals appear on [[apps-google-shopping-products]] and which CloudCart fields feed which Google attributes.

## Where to find it

The formatter has no merchant-facing screen. The outputs are visible indirectly via [[apps-google-shopping-products]] (per-product approval status) and via the Google Merchant Center web UI (the merchant's view in their GMC account).

## What the merchant can do here

The merchant influences the formatter's output by:

- Editing product / variant fields in [[products-products]] (name, description, price, barcode → GTIN, weight, dimensions, images).
- Configuring the attribute mappings on [[apps-google-shopping-attributes]] (Color, Size, Material, Pattern source resolution).
- Setting the store-wide defaults on [[apps-google-shopping-settings]] (`google_default.condition`, `google_default.adult`, `default_weight`, `default_width`, `default_height`, `default_depth`).
- Picking included destinations and `size_system` per batch upload via [[apps-google-shopping-batch-upload]].

### What the merchant CANNOT change

- One Google offer per Variant; all Variants of a parent share its `item_group_id`.
- Unit conversions (mm → cm; weight always grams).
- The `custom_label_0 = "CloudCart"` tag on every item (`custom_label_1..4` are not exposed).
- The auto-generated `checkout_link_template` custom attribute.

## Settings & fields

### Per-Variant offer payload

Each Variant becomes one Google offer with these fields:

| Google field | CloudCart source |
|---|---|
| `offerId` | The Variant's ID (one offer per Variant). |
| `itemGroupId` | Parent Product ID — all Variants of the same parent share this group. |
| `title` | Product name. |
| `description` | Product description. |
| `imageLink` | First image (sorted by `sort_order`). |
| `additionalImageLinks` | Remaining images. |
| `price` | Variant price (store currency). |
| `salePrice` | Variant `detailed_discount` value when present. |
| `sale_price_effective_date` | ISO range `YYYY-MM-DDT00:00:00Z/YYYY-MM-DDT23:59:59Z` from the discount's start + end dates. |
| `availability` | Mapped from CloudCart status via the `google_status` mapping in [[apps-google-shopping-settings]]. If a variant's status matches none of the configured mappings, it falls back to a stock check: `in_stock` when the variant meets its minimum-orderable quantity OR the product has `continue_selling = yes` (see [[inventory-oversell]]), otherwise `out_of_stock`. |
| `quantity` | Variant `quantity`. |
| `condition` | `google_default.condition` (default `"new"`). |
| `adult` | `google_default.adult` (default `"no"`). |
| `gtin` | Variant `barcode` when present. Variants without a barcode get no GTIN — which can trigger Google's "Missing GTIN" disapproval for products that need it. |
| `brand` | Product vendor name. |
| `productWeight` | Variant weight OR app-level `default_weight` fallback. Always sent in **grams**. |
| `productLength` / `productWidth` / `productHeight` | Variant dimensions OR app-level fallbacks. Stored in mm, auto-converted to **cm** (`/10`). |
| `expirationDate` | Product `active_to` when set (campaign / seasonal expiry). Google auto-deletes the listing after this date. |
| `customLabel0` | Hard-coded `"CloudCart"` — used for Google Ads segmentation. |
| `customAttribute checkout_link_template` | Auto-generated `{site_url}/checkout-link/{variant_id}` — used by Buy on Google / direct checkout flows. |
| `is_bundle` | `"yes"` when the CloudCart product type is `bundle`, else default. |
| `sizeSystem` | The per-batch `size_system` setting (one of 11: EU, US, UK, FR, DE, IT, JP, AU, BR, CN, MEX). |
| `includedDestinations` | The `include_destination` array from Settings (Free listings, Shopping ads, Surfaces across Google, Dynamic remarketing). |
| `unitPricingBaseMeasure` + `unitPricingMeasure` | Only when the Grocery Store app is installed AND the variant has a unit with a Google-supported short name. |

### Attribute setters

Only eight Google attributes have dedicated handling:

- **Direct**: `age_group`, `gender`, `size_type`, `size_system`.
- **Smart-resolution** (`color`, `material`, `pattern`, `size`): pulled from either the matching variant parameter OR a category property, depending on the source chosen in the mapping on [[apps-google-shopping-attributes]].

Any other attribute the merchant maps — even though it appears in the dropdown — is NOT applied to the feed.

### Sale price auto-population

When a Variant has a `detailed_discount`, its discounted price is sent as `sale_price`, and the discount's start + end dates as `sale_price_effective_date` (ISO). The merchant does NOT configure sale fields separately — they flow from the standard CloudCart discount system.

### Tax + shipping defaults

Tax and shipping defaults are store-wide, set on [[apps-google-shopping-settings]] (`default_tax`). Per-product overrides are NOT exposed.

## Business rules

### Variant offer model

Each Variant is sent as its own Google offer (`offerId = variant_id`), all sharing the parent's `itemGroupId`, so Google's storefront shows them as variants of one product (size/color picker), not separate products. Single-variant products send one offer with the parent product's ID as both offer and group.

### `size_system` is per-batch, not per-product

The Size system attribute is set **per upload batch** via the modal on [[apps-google-shopping-batch-upload]] (`size_system` setting) and applies to every offer in that batch — no per-product override. Merchants selling US-sized and EU-sized apparel from one store must pick one, or split into separate sites.

### Image upload — no client-side validation

The formatter sends whatever image URL the variant has (sorted by `sort_order`) with **no validation of dimensions, background, or size** before upload. If Google rejects the image, it surfaces as a per-product disapproval on [[apps-google-shopping-products]]; the merchant fixes the image in [[products-products]] and re-syncs.

### Target country + language come from store settings

The feed uses the store's **primary language**, **operation country**, and **currency** from store-level settings. It does NOT support one feed targeting multiple countries; merchants selling in several countries use separate CloudCart sites (one per country) with separate Merchant Center IDs.

### Custom label semantics

`custom_label_0` is always `"CloudCart"` — useful for Google Ads segmentation (target ads to CloudCart products vs other catalog sources). The other labels (`custom_label_1..4`) are NOT exposed; merchants wanting more segmentation use Google Ads campaign-level segmentation instead.

### Expiration date side-effect

Setting `active_to` on a product (typically a seasonal / campaign field) implicitly tells Google to auto-delete the listing after that date. Merchants who use `active_to` for storefront visibility purposes should be aware it also affects GMC.

### Unit pricing requires the Grocery Store app

`unitPricingBaseMeasure` + `unitPricingMeasure` are sent only when the [[apps-grocery-store-settings|Grocery Store]] app is installed AND the variant's unit has a Google-supported short name (`oz`, `lb`, `mg`, `g`, `kg`, `floz`, `pt`, `qt`, `gal`, `ml`, `cl`, `l`, `cbm`, `in`, `ft`, `yd`, `cm`, `m`, `sqft`, `sqm`, `ct`). Otherwise the unit defaults to `ct = 1` (each) with no unit-pricing attributes.

### Status values Google reports back

GMC returns one of nine status values per offer, surfaced on [[apps-google-shopping-products]]: `Processing`, `Under Review`, `Approved`, `Approved (Limited)`, `Disapproved`, `Pending`, `Expired`, `Pending Review After Appeal`, `Not Showing`.

## Related

- [[apps-google-shopping]] — hub.
- [[apps-google-shopping-settings]] — store-wide defaults + status mapping the formatter consumes.
- [[apps-google-shopping-attributes]] — attribute mappings the formatter resolves.
- [[apps-google-shopping-products]] — where disapprovals from the formatter's payload surface.
- [[apps-google-shopping-batch-upload]] — upload path that calls the formatter.
- [[apps-google-shopping-auto-sync]] — event path that calls the formatter for incremental updates.
- [[products-products]] — source of product / variant fields.
- [[products-variants-options]] — variant parameter sources for `color` / `size`.
- [[products-vendors]] — brand source.
- [[apps-grocery-store-settings]] — unlocks unit pricing in the formatter.

## Open questions

- Are `custom_label_1..4` reserved by CloudCart for future use, or simply not implemented? `(verify)`
- Does the formatter send `gender` / `age_group` for products without those mapped, or omit the field entirely? `(verify)`
