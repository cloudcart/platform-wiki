---
type: feature
nav_path: "Payment Providers → Fibank BNPL → Promotions"
route_name: apps.fibank_bnpl.promotions
route_path: /admin/payment-providers/fibank_bnpl/promotions
aliases: ["Fibank BNPL Promotions", "Fibank promotions", "Fibank promotion ID", "Промоции Fibank BNPL", "Фибанк БНПЛ промоции"]
tags: [paymentproviders, payment-providers, fibank-bnpl, bnpl, promotions]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Promotions

## Purpose

Fibank can put specific products on a **promotional loan scheme** — e.g., "0% interest for 6 months on TV X", "free 12 months on washing machine Y" — and assigns each such product a **Fibank promotion ID** in their bank-side system. By default CloudCart sends the cart's product category IDs (Fibank's API is category-based) to Fibank's calculation API; this Promotions tab lets the merchant override that for specific products, telling CloudCart "when this CloudCart product is in the cart, send Fibank's promotion ID instead." The result is that Fibank returns the promotional loan terms (lower rate or interest-free) for that product instead of the default category terms.

This screen is the **architectural twin of [[payment-providers-dsk-bnpl-promotions|DSK BNPL Promotions]]** — same model shape (per-product mapping + start/end dates + variant filter), same import/export Excel format, same bundle auto-rewriting. The only difference is which bank's promotion IDs are stored.

## Where to find it

Sidebar → **Payment Providers** → **Fibank BNPL** → **Promotions** tab. Route `/admin/payment-providers/fibank_bnpl/promotions`. The page renders a table of promotion rows (one per product).

## What the merchant can do here

- See the full list of products currently mapped to a Fibank promotion ID (paginated, with product name + image).
- Click **Add discount** (the literal button label) to map a CloudCart product to a Fibank promotion ID with start/end dates and optional scheme-variant filters.
- Click a row to edit its Fibank promotion ID, allowed scheme variants, or start/end dates; click delete to remove the mapping (the product reverts to its CloudCart category ID against Fibank's default terms).
- **Export** all mappings to an Excel file (`cloudcart-fibank-bnpl-promo.xls`); **Import** mappings in bulk from the same shape.
- Edit the **Promo text area** rich-text snippet (stored as `promo_html`) in the card below the table; it has its own **Save** button (`POST /promotion/html/save`) and renders on the storefront product page.

## The Add / Edit Promotion modal — three cards

Clicking **Add discount** (the literal button label — Fibank reuses the shared payment-provider promotion editor) opens a right-side slide-out modal at size `xl`, with **Cancel** + **Save** in the header. Three stacked cards:

- **Card 1 — "Promotion to be applied to:"** — the **Product picker** (AJAX single-product search over the catalog at `/admin/api/core/products/search`, hidden/archived selectable). Helper text: *"Determine which products the discount will be applied to."*
- **Card 2 — "Date range"** — **Start date**, **End date**, and a **No expiration** checkbox (default ON; sends `no_expire=on` instead of an end date, auto-unchecks if an end date is picked; End date is disabled while it is checked).
- **Card 3 — "Interest free leasing"** — the **Enter Fibank product category IDs** text input (required; error binds to `fibank_promotion_id`) plus the **Leasing schemes** button.

See **Settings & fields** below for what each field stores and validates.

The **Leasing schemes** button calls `GET /admin/api/payment_providers/fibank_bnpl/pricing/{product_id}/{fibank_promotion_id}?json=1` and previews the customer's pricing table. It is disabled until both Product and the Fibank ID are populated, and the merchant must click it each time — for Fibank BNPL the preview does NOT auto-refire when Product or the Fibank ID changes (only the `bnp` provider auto-refires).

### Leasing schemes preview table

Same shape as the DSK BNPL preview (see [[payment-providers-dsk-bnpl-promotions#leasing-schemes-preview-table-appears-after-clicking-the-button|DSK BNPL Promotions → preview table]]) — one card per scheme, each with a variants table whose columns are: **Number of deposits**, **Monthly payment**, **% NIR**, **% APR**, **Total amount**. Ticking variant rows constrains the saved `variants` array; un-ticked variants are dropped from the customer's pricing module for this product. On error, an inline red box renders Fibank's message verbatim.

## Settings & fields

### Promotion row fields (table view + Add modal)

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Product** | The CloudCart product the merchant is mapping. | None | Required. If the product is part of a **bundle**, CloudCart rewrites the mapping to the first bundle component's product ID on save. |
| **Fibank product category IDs** | The promotion identifier issued by Fibank, sent to their API in place of the product's category ID when the product is in the cart. UI label is plural (*"Enter Fibank product category IDs"*) because Fibank's API field is `product_category_ids`, though the merchant typically enters one ID. | None | Required. Trimmed on save. Stored as `fibank_promotion_id`. |
| **Variants** (from the preview tick-list) | Optional list of Fibank pricing-variant IDs to filter to. | Empty (all allowed) | If non-empty, any variant whose `PricingVariantId` isn't in the list is dropped; if none remain, the whole scheme is dropped. |
| **Start date** | First date the promotion is active. | NULL (no start gate) | Date picker. |
| **End date** | Last date the promotion is active. | NULL (open-ended via *No expiration*) | Date picker; disabled when *No expiration* is checked. |

## Business rules

### How the promotion override flows through

When the storefront pricing module runs, for each cart product it uses the product's `fibank_promotion_id` as the goods ID (plus the row's `variants` as filters) if a promotion row exists; otherwise it sends the CloudCart product ID as `product_category_ids` (Fibank's API is category-based). It then calls Fibank for all schemes, filters each scheme's variants by the collected filter, and drops any scheme left with zero variants.

This means **Fibank's promotional terms only show at checkout when both the merchant has added the mapping AND Fibank has configured the promotion on their side for that ID.** If Fibank hasn't configured it, the API returns default terms — the mapping by itself doesn't create a promotion.

### Bundles — auto-rewriting

If the merchant picks a bundle product, the saved row is rewritten to the first child product in that bundle. Fibank's API doesn't understand bundles; CloudCart silently re-maps.

### Start / End date gating

The dates are stored but the storefront does NOT currently consult them when calculating prices — same caveat as the [[payment-providers-dsk-bnpl-promotions|DSK BNPL Promotions]] tab. For strict date gating, the merchant should add/remove the mapping at the right time.

### Plan-gating

Inherits the parent Fibank BNPL provider's plan-gating — **none**.

## Related

- [[payment-providers-fibank-bnpl]] — parent hub for Fibank BNPL.
- [[payment-providers-fibank-bnpl-settings]] — Store Unique ID + minimum order value.
- [[payment-providers-dsk-bnpl-promotions]] — DSK BNPL equivalent (same shape, different bank, different default-ID semantics: DSK is product-ID-based, Fibank is category-ID-based by default).
- [[product]] — the entity each promotion row maps to.
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

_None._

## Verified — what is sent to Fibank as `product_category_ids`

Verified against backend: the Fibank API field `product_category_ids` is filled with the per-product `fibank_promotion_id` the merchant configured here, not the CloudCart product ID. If the column is left blank, the platform falls back to the platform-side category ID for that product.
