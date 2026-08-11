---
type: feature
nav_path: "Payment Providers → DSK BNPL → Promotions → Bulk & endpoints"
route_name: apps.dsk_bnpl.promotions
route_path: /admin/payment-providers/dsk_bnpl/promotions
aliases: ["DSK BNPL promo export", "DSK BNPL promo import", "cloudcart-dsk-bnpl-promo.xls", "DSK BNPL promotion endpoints", "DSK BNPL promo date gating", "Импорт експорт DSK промоции"]
tags: [paymentproviders, payment-providers, dsk-bnpl, bnpl, promotions, import-export]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---
> Part of [[payment-providers-dsk-bnpl-promotions]]. See the hub for the other aspects (the product → DSK promotion ID mapping, and the `promo_html` storefront banner).

# DSK BNPL — Bulk export / import & endpoints

## Purpose

This aspect covers the operational mechanics of the Promotions tab that sit alongside the per-product mapping UI: the **Excel bulk export / import** path for the promotion rows, the start / end **date-gating caveat** (the columns are saved but not currently enforced), and the full **backend endpoint reference** for the tab.

## Where to find it

Sidebar → **Payment Providers** → **DSK BNPL** → **Promotions** tab. The **Export** and **Import** buttons sit on the promotions table toolbar. The route is `/admin/payment-providers/dsk_bnpl/promotions`; all backend endpoints live under `/admin/api/payment_providers/dsk_bnpl/`.

## What the merchant can do here

- Export all promotion mappings to an Excel file (`cloudcart-dsk-bnpl-promo.xls`) via the **Export** button.
- Import promotion mappings in bulk from an Excel file via the **Import** button.
- Edit a large number of mappings off-platform in the spreadsheet, then re-upload — the bulk path is faster than the inline UI for many rows.

## Settings & fields

The bulk file carries the same fields as a single promotion row (see [[dsk-bnpl-promo-mapping]] for the full field reference): the CloudCart product ID, the DSK promotion ID, the variant list, and the date range. There are no bulk-only fields — the Excel shape mirrors the row shape one-to-one.

## Business rules

### Bulk export / import format

`Export` builds an Excel workbook of every promotion row and downloads it as `cloudcart-dsk-bnpl-promo.xls`. The columns include the CloudCart product ID, the DSK promotion ID, the variant list, and the date range.

`Import` accepts an Excel upload at the same shape and upserts the rows. This is the merchant's bulk-edit path; for a few rows the inline UI is faster.

### Start / End date gating

The dates are stored as `datetime` and are intended to gate when the promotion is active — i.e., outside the date range the merchant probably wants the override to fall back to default catalog terms. **At the time of writing the storefront code does NOT enforce the date gate** — the date columns are saved but not consulted when the pricing module runs. If a merchant needs strict date gating they should delete or re-create the mapping at the right time.

### Permissions / endpoints

All Promotions endpoints live under `/admin/api/payment_providers/dsk_bnpl/`:

- `GET /promotions` — paginated list.
- `GET /promotion/edit/{promotionId}` — load one row for editing.
- `POST /promotion/save/{promotionId}` — save / create (requires `product` and `dsk_promotion_id`).
- `GET /promotion/delete/{promotionId}` — soft-removes the row.
- `POST /promotion/html/save` — saves the rich-text `promo_html` blob into the provider configuration (see [[dsk-bnpl-promo-html]]).
- `GET /export-promo` — Excel download.
- `POST /import-promo` — Excel upload.
- `GET /pricing/{productId?}/{dskPromotionId?}` — preview the calculated installment table for a given product / promotion ID (used by the form to show the merchant what the customer will see — see [[dsk-bnpl-promo-mapping]]).

### Plan-gating

This aspect inherits the same plan-gating as the parent DSK BNPL provider, which is **none** — every CloudCart plan can use it.

## Related

- [[payment-providers-dsk-bnpl-promotions]] — hub.
- [[payment-providers-dsk-bnpl]] — parent hub for DSK BNPL.
- [[payment-providers-fibank-bnpl-promotions]] — equivalent Promotions screen for the Fibank BNPL provider (same shape, different bank).
- [[product]] — the entity each promotion row maps to.

## Open questions

_None._
