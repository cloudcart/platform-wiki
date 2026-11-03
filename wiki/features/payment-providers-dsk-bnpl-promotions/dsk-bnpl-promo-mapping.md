---
type: feature
nav_path: "Payment Providers → DSK BNPL → Promotions → Product mapping"
route_name: apps.dsk_bnpl.promotions
route_path: /admin/payment-providers/dsk_bnpl/promotions
aliases: ["DSK BNPL promotion mapping", "DSK promotion ID mapping", "Add discount DSK BNPL", "DSK BNPL leasing schemes preview", "Свързване на продукт с DSK промоция"]
tags: [paymentproviders, payment-providers, dsk-bnpl, bnpl, promotions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---
> Part of [[payment-providers-dsk-bnpl-promotions]]. See the hub for the other aspects (the `promo_html` storefront banner, and bulk export / import).

# DSK BNPL — Promotion product mapping

## Purpose

This aspect covers the core of the Promotions tab: **mapping a CloudCart product to a DSK promotion ID** so that DSK returns its promotional loan terms (lower rate or interest-free) for that product instead of the default catalog terms. It documents the promotions table, the Add / Edit modal, the live leasing-schemes preview with per-variant filtering, the checkout override, and the bundle auto-rewrite rule.

## Where to find it

Sidebar → **Payment Providers** → **DSK BNPL** → **Promotions** tab. The page shows a paginated table of promotion rows (one per product, with name + image). Clicking **+ Add discount** opens the editor modal; clicking an existing row opens it for editing.

## What the merchant can do here

- See the full list of products currently mapped to a DSK promotion ID (paginated, with product name + image).
- Click **Add discount** to map a CloudCart product to a DSK promotion ID with start/end dates and optional scheme-variant filters.
- Click a row to edit its DSK promotion ID, allowed scheme variants, or start/end dates.
- Delete a row to remove the mapping (the product reverts to its CloudCart product ID against DSK's default catalog terms).
- Preview the live installment table via **Leasing schemes**, and tick which pricing variants survive into the saved mapping.

## The Add / Edit Promotion modal — three cards

Clicking **+ Add discount** (the label is literally "Add discount", not "Add promotion") opens a right-side slide-out modal with **Cancel** + **Save** in the header. Its body has **three stacked cards** that drive one flat promotion row:

### Card 1 — "Promotion to be applied to:"

| Field | What it does | Validation / notes |
|-------|--------------|--------------------|
| **Product picker** (live search) | A single-product picker that searches CloudCart's catalog by name/SKU as the merchant types. Hidden / archived products are selectable. | Required. Field-level error binds to `product`. Bundle products are auto-rewritten on save to the first child product (see Bundles below). |

Helper text below: *"Determine which products the discount will be applied to."*

### Card 2 — "Date range"

| Field | What it does | Validation / notes |
|-------|--------------|--------------------|
| **Start date** | Date picker (formatted per the store's `format.date` setting). | Optional. Sent as `start_date`. Field-level error binds to `start_date`. |
| **End date** | Date picker. | Disabled when **No expiration** is checked. Sent as `end_date`. Field-level error binds to `end_date`. |
| **No expiration** | Checkbox. | Default ON for new rows. When ON, the form sends `no_expire=on` instead of an `end_date` and the promotion is open-ended. Auto-unchecks when the merchant picks an end date manually. |

Helper text below: *"Specify the start date and the end date of the discount, or set no expiration."* The date columns are saved but not enforced by the storefront — see [[dsk-bnpl-promo-bulk]] for the gating caveat.

### Card 3 — "Interest free leasing"

| Field | What it does | Validation / notes |
|-------|--------------|--------------------|
| **Enter DSK promotion ID** (text input) | The promotion identifier issued by DSK Bank for this product on their side. | Required. Field-level error binds to `dsk_promotion_id`. Trimmed of whitespace and stored on the row as `dsk_promotion_id`. |
| **Leasing schemes** button | Fetches and renders a live preview of what the customer will see at checkout. Disabled until both Product and DSK promotion ID are filled. | The merchant must click the button each time — for DSK BNPL the preview does NOT auto-refresh when Product or DSK promotion ID changes; re-click after any change. |

### Leasing schemes preview table (appears after clicking the button)

When the preview returns successfully, a **fourth card** appears with one or more pricing schemes — each shows its name (`PricingSchemeName`) and a variant table with these columns:

| Column | Source field |
|--------|--------------|
| **Number of deposits** | `PricingSchemeName` (typically encodes month count) |
| **Monthly payment** | `InstallmentAmountFormatted` |
| **% NIR** | `NIRFormatted` — yearly nominal interest rate |
| **% APR** | `APRFormatted` — annual cost of credit |
| **Total amount** | `TotalRepaymentAmountFormatted` |

For DSK BNPL (and Fibank BNPL) the preview table is **selectable** — each row has a checkbox. The merchant ticks which `PricingVariantId` rows survive into the saved `variants` array; un-ticked variants are NOT shown to the customer at checkout. If after filtering no variants remain in a scheme, the whole scheme is dropped.

If the preview returns an error (typically because DSK has no promotion configured for that ID), an inline red box shows DSK's message verbatim — the merchant can still save the row, but the customer sees DSK's default catalog terms until DSK configures the promotion.

## Settings & fields

### Promotion row fields (table view + Add modal)

A saved row holds **Product**, **DSK promotion ID**, **Start date**, and **End date** (entered in the three modal cards above), plus the **variant filter** — set by ticking rows in the leasing-schemes preview:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Variants** (from the preview tick-list) | Optional list of DSK pricing-variant IDs (`PricingVariantId`) — only these appear in the customer's pricing table for this product. | Empty (all variants allowed) | If non-empty, every returned variant whose `PricingVariantId` isn't in this list is dropped. If NO variants remain after filtering, the whole scheme is dropped (the customer sees no DSK BNPL plans for that product). |

## Business rules

### How the promotion override flows through

When the storefront pricing module runs, each product is matched to its promotion row. If a row exists, its `dsk_promotion_id` is sent to DSK as the goods ID (instead of the CloudCart product ID) and the row's `variants` array filters the returned schemes; products with no row use the CloudCart product ID.

This means **DSK's promotional terms only show on the customer's checkout when both the merchant has added the mapping AND DSK Bank has actually configured the promotion on their side for that ID.** If DSK hasn't configured it, the API returns the default catalog terms — the mapping by itself doesn't create a promotion.

### Bundles — auto-rewriting to the first bundle child's product ID

If the merchant picks a product that is itself a **bundle**, the saved row is rewritten to the first child product in that bundle, because DSK's pricing API needs a real product ID rather than the CloudCart "bundle" concept. The merchant doesn't see this happening; the saved row shows the rewritten product, not the original bundle.

### Plan-gating

This aspect inherits the same plan-gating as the parent DSK BNPL provider, which is **none** — every CloudCart plan can use it.

## Related

- [[payment-providers-dsk-bnpl-promotions]] — hub.
- [[payment-providers-dsk-bnpl]] — parent hub for DSK BNPL.
- [[payment-providers-dsk-bnpl-settings]] — Store Unique ID + public key + minimum order value.
- [[payment-providers-fibank-bnpl-promotions]] — equivalent Promotions screen for the Fibank BNPL provider (same shape, different bank).
- [[product]] — the entity each promotion row maps to.

## Open questions

_None._
