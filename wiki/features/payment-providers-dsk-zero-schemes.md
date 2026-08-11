---
type: feature
nav_path: "Payment Providers → DSK Zero → Schemes"
route_name: apps.dsk_zero.schemes
route_path: /admin/payment-providers/dsk_zero/schemes
aliases: ["DSK Zero Schemes", "DSK 0% schemes", "DSK installment schemes", "Схеми ДСК Зеро", "ДСК 0% схеми"]
tags: [paymentproviders, payment-providers, dsk-zero, bnpl, schemes, zero-interest]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 1
---
# Schemes

## Purpose

The Schemes tab is the heart of the DSK Zero integration — the merchant defines here exactly which products can be bought interest-free, and over how many months. Each **scheme** is a pair of a month count + a list of products that qualify for that scheme. The merchant typically creates several schemes (e.g., 6 months for one product tier, 12 months for another, 18 months for a third). A product can appear in multiple schemes, in which case the storefront shows all matching plans for that product.

## Where to find it

Sidebar → **Payment Providers** → **DSK Zero** → **Schemes** tab.

## What the merchant can do here

- See the list of existing schemes, sorted by months ascending — each row shows the scheme's month count + the number of products attached.
- Click **Add Schema** to open the form panel and create a new scheme.
- Click any row to edit a scheme — change the month count or edit the product list.
- Click delete on a row to remove a single scheme.
- Select multiple schemes via the bulk checkbox and click **Delete selected** to bulk-remove.
- Export the full scheme list to Excel (`cloudcart-dsk-promo.xls`) via the **Export** button.
- Import schemes in bulk from an Excel file via the **Import** button.

## Settings & fields

Clicking **Add Schema** (or any row, to edit) opens a right-side slide-out modal with **Cancel** + **Save** buttons. Save is disabled while a save is in flight. When editing, the modal opens pre-filled with the scheme's current month count and products. The body has two fields:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Number of months** (number input) | Number of monthly 0%-interest installments offered to the customer for this scheme. | None | Required. Positive integer. Must be **unique** across the merchant's schemes — you cannot create two schemes both labelled "6 months". Bulgarian attribute label "брой месеци". Errors bind to the `months` field. |
| **Discount target - Product/s** (multi-select picker, AJAX search) | List of products that qualify for this scheme. The customer must have ONLY these products (or a subset) in their cart for the scheme to apply. Hidden / archived products are selectable. | Empty | Required. Multi-select tag picker over the store's catalog; must reference existing products. Bulgarian attribute label "конкретни продукти". Errors bind to the `products` field. |

On Save the modal closes and the table re-fetches. If the merchant tries to create a duplicate month-count scheme, the save returns a validation error on the `months` field and the modal stays open with the error rendered inline.

## Business rules

### Cart-matching at checkout

A scheme is shown to the customer only when **every** product in the cart is included in that scheme's product list. If even one cart item is missing from the list, the scheme is dropped. Schemes with an empty product list are skipped entirely.

### Multi-scheme cart error

If the merchant has any schemes defined AND the customer's cart has more than one product AND no single scheme covers all items, the system raises:

> "Има продукти от различни лизингови схеми. Моля, направете отделни поръчки"
> *"There are products from different leasing schemes. Please make separate orders."*

The merchant can't disable this — it's enforced by the pricing layer whenever a multi-product cart spans multiple schemes. The customer must split the order into separate orders.

### Pricing the customer sees per scheme

For a qualifying scheme of N months at price P, the customer sees:

- Monthly installment: P / N (rounded to 2 decimals)
- NIR 0%, APR 0%, total repayment P (no markup)
- **Down payment is always 0 BGN** — the merchant cannot configure a down payment for DSK Zero; the customer pays nothing at checkout and starts the monthly cycle one month later. (With 0% interest a down payment would not change the customer-facing split anyway.)

The pricing scheme name the customer sees is "{N} months" (localised).

### Months must be unique

A uniqueness check blocks two schemes with the same month count. To have two different product groups eligible for the same number of months, the merchant must merge them into one scheme — there's no way to split.

### Bundles

Unlike DSK BNPL, DSK Zero does NOT auto-rewrite bundle products to their bundle children. The merchant should add the parent bundle product directly to the scheme's product list if they want the bundle to be eligible.

### Bulk import / export format

Export downloads an Excel file (`cloudcart-dsk-promo.xls`) with one row per scheme — month count + a serialised list of product IDs. Import accepts the same shape and upserts schemes. This file is **intentionally separate** from the DSK BNPL Promotions export (`cloudcart-dsk-bnpl-promo.xls`), which carries different columns (per-product DSK promotion mappings); the two files are not interchangeable, so a merchant managing both providers maintains two separate spreadsheets.

### Plan-gating

Inherits the zora-only gating of the parent DSK Zero provider — non-zora stores don't see this tab. There is no CloudCart-plan gate on top of that.

## Related

- [[payment-providers-dsk-zero]] — parent hub for DSK Zero.
- [[payment-providers-dsk-zero-settings]] — agreement / merchant ID + email contact.
- [[payment-providers-dsk-bnpl-promotions]] — equivalent "per-product loan terms" screen for DSK BNPL, but a totally different model (DSK BNPL uses DSK's promotion IDs; DSK Zero uses local schemes only).
- [[product]] — products referenced by each scheme.
- [[payment-providers]] — top-level Payment Providers area.

## Open questions

(none)
