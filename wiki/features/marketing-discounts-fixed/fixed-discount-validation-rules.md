---
type: feature
nav_path: "Marketing → Discounts → Products → Validation rules"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id
aliases: ["Fixed discount validation", "fixed_price ≤ catalog", "Fixed discount uniqueness"]
tags: [marketing, discounts, fixed, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects.

# Fixed discount — validation rules

## Purpose

This aspect documents **every rejection** a merchant can hit when saving a Fixed-discount price in the admin — at the parent form and the per-variant modal. The APIs run separate checks (see [[fixed-discount-api-access]]). It also covers the **equality edge case** at `fixed_price = variant.price`, per-variant uniqueness within a single discount (and the absence of cross-discount uniqueness), and the end-date rule.

## Where to find it

Validation rejections surface on the same Fixed-discount products page documented in [[fixed-discount-product-modal]] — `/admin/marketing/discounts/products/:id`. Errors appear as inline toasts and per-field highlights inside the per-product price modal. Parent-discount-level rejections (date range) surface on the parent Fixed-discount create / edit form.

## What the merchant can do here

- See which submitted price was rejected and why (per-field error + the offending variant row highlighted), then adjust and re-submit without losing the rest of the form state.
- Spot a `save = 0` row (a row stored at equality with catalog price; see below).

## Settings & fields

The fields validated by these rules are documented field-by-field in [[fixed-discount-product-modal]]. This page describes the **rules** that apply to those fields; it introduces no new fields.

| Validator | Target field(s) | Rejection message |
|---|---|---|
| Fixed price above catalog | `*.price` | *"Price must be at least 1 and less than &lt;catalog price&gt;"* |
| Variant already on this discount, when adding | `variant_id` | *"Variant already exists in discount. Variant ID: &lt;id&gt;"* |
| End date before the start date | `date_end` | *"The end date must be after the start date"* |
| End date missing with **No expiration** off | `date_end` | *"The end date is required"* |

Plan-gate rejections are not covered here — see [[fixed-discount-plan-gates]].

## Business rules

### `fixed_price ≤ variant.price` — equality is special

A price from 0.01 up to and including the variant's catalog price is accepted in the admin; `fixed_price > variant.price` is rejected at validation. The modal rejects with *"Price must be at least 1 and less than &lt;catalog price&gt;"*, and a rejected price **fails the whole save**.

**Equality (`fixed_price = variant.price`) passes validation** — the validator compares "strictly greater than". The row is written with `save = 0`, and the storefront then shows a "0 EUR saving" tag (verify): a no-op discount taking a per-product attachment slot.

In the admin every variant needs a price; a blank one fails the save. Entering the catalog price gives a no-saving row, which switches off at the next product save.

When the catalog price later drops to or below the fixed price, the platform automatically **deactivates the row** — see [[fixed-discount-row-writes]] for the auto-deactivation feedback loop.

### Per-variant uniqueness within a single Fixed discount

When adding a product, a variant already on this discount is rejected with the message above. Duplicates inside one submission are not checked, and an edit runs no such check.

### A product can sit on two Fixed discounts until it is edited

There is **no save-time validation error** blocking two Fixed discounts from targeting the same product. Adding a product to a second Fixed discount keeps it on the first, and the customer gets the cheaper. Editing its prices on either removes it from the other: the save deletes the product's rows on every discount, then re-creates rows only for the discount being saved (see [[fixed-discount-row-writes]]). For the storefront lookup when a row is present, see [[fixed-discount-storefront-display]].

### End date — today and past dates save

The form refuses only an end date before the start date, and asks for one unless **No expiration** is on. Past dates and today save. With `date_end = today` the per-variant rows stay valid through 23:59 today in store timezone; a past end date simply does not apply. The hourly expiry sweep switches the discount off at the first run after 00:00 UTC on the day after its end date — see [[background-queue-inventory]].

### Save outcome by submitted price

| Submitted condition | Outcome |
|---|---|
| `fixed_price < variant.price` | Row inserted |
| `fixed_price = variant.price` | Row inserted with `save = 0` |
| `fixed_price > variant.price` | Rejected at validation |
| `fixed_price` below 0.01 or blank | Rejected at validation |
| Variant already on this discount, when adding | Rejected at validation |

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-product-modal]] — where the merchant enters the prices that these validators check.
- [[fixed-discount-row-writes]] — what lands in `product_to_discount` after a successful save (including the `save = 0` edge case).
- [[fixed-discount-storefront-display]] — the "Save X EUR" label and the storefront price lookup.
- [[fixed-discount-api-access]] — the API paths, which do not compare the price with the catalog price.
- [[background-queue-inventory]] — the hourly expiry sweep.
- [[discount]] — entity page for the parent Fixed discount.

## Open questions

No outstanding questions.
