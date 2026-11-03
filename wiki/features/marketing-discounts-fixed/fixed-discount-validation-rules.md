---
type: feature
nav_path: "Marketing → Discounts → Products → Validation rules"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id
aliases: ["Fixed discount validation", "fixed_price ≤ catalog", "Fixed discount uniqueness"]
tags: [marketing, discounts, fixed, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects.

# Fixed discount — validation rules

## Purpose

This aspect documents **every rejection** a merchant can hit when saving a Fixed-discount price — at the parent form, the per-variant modal, and the modern JSON-API path. It also covers the **equality edge case** at `fixed_price = variant.price`, per-variant uniqueness within a single discount (and the absence of cross-discount uniqueness), and the `date_end = today` boundary.

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
| Duplicate variant within the same discount | `variant_id` | *"Variant already exists in discount."* |
| `date_end` past-day check | `date_end` | *"End date cannot be less than now"* — fires only for dates already past. |

Plan-gate and activation-cooldown rejections are not covered here — see [[fixed-discount-plan-gates]].

## Business rules

### `fixed_price ≤ variant.price` — equality is special

A Fixed discount must not exceed the variant's catalog price — `fixed_price > variant.price` is rejected at validation. The modal rejects with *"Price must be at least 1 and less than &lt;catalog price&gt;"*, and a rejected price **fails the whole save** (it is not silently dropped).

**Equality (`fixed_price = variant.price`) passes validation** — the validator compares "strictly greater than". The row is written with `save = 0`, and the storefront then shows a "0 EUR saving" tag: a no-op discount taking a per-product attachment slot.

To avoid the `save = 0` row, always set the fixed price **strictly below** catalog. For "no discount on this variant", omit the variant from the submitted `prices[]` array rather than submitting it at catalog price; after an API save, check the resulting `product_to_discount` rows for any `save = 0` rows that indicate accidental equality.

When the catalog price later drops to or below the fixed price, the platform automatically **deactivates the row** — see [[fixed-discount-row-writes]] for the auto-deactivation feedback loop.

### Per-variant uniqueness within a single Fixed discount

Within a single Fixed discount, each variant ID can appear **at most once** in the submitted `prices[]` array — the validator rejects duplicates with a validation error pointing at the duplicated variant.

### A product effectively lives in ONE Fixed discount (the save deletes by product)

There is **no save-time validation error** blocking two Fixed discounts from initially targeting the same product. But the modern save flow makes coexistence impractical: editing a product on any Fixed discount **deletes that product's per-variant rows by `product_id` — across every Fixed discount** (not just the current one — see [[fixed-discount-row-writes]]), then re-creates rows only for the discount being saved. So in practice a product belongs to **one** Fixed discount at a time: attaching or editing it on a second discount detaches it from the first.

(Older wiki phrasing claimed a hard "one Fixed discount per product" uniqueness *error* — *"You can`t use same products in this type of discount."* — that string exists in the translation file but is **never triggered**; the effective single-discount-per-product behaviour comes from the product-keyed delete, not from a validation rule.) For the storefront lookup when a row is present, see [[fixed-discount-storefront-display]].

### `date_end = today` — accepted (not rejected as "in the past")

The save validator compares `date_end` against the **end of the current day** in store timezone using a strict less-than check, so a `date_end` equal to today IS accepted (it represents end-of-day today). The rejection message *"End date cannot be less than now"* fires only for dates that already passed, not for today.

A merchant CAN save a Fixed discount with `date_end = today`; the per-variant rows stay valid through 23:59 today in store timezone. Auto-disable (the UTC sweep) won't pick it up until up to ~27 hours later — see [[background-queue-inventory]] for the daily expiry process.

### Save outcome by submitted price

| Submitted condition | Outcome |
|---|---|
| `fixed_price < variant.price` | Row inserted |
| `fixed_price = variant.price` | Row inserted with `save = 0` |
| `fixed_price > variant.price` | Rejected at validation |
| Duplicate `variant_id` in `prices[]` | Rejected at validation |

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-product-modal]] — where the merchant enters the prices that these validators check.
- [[fixed-discount-row-writes]] — what lands in `product_to_discount` after a successful save (including the `save = 0` edge case).
- [[fixed-discount-storefront-display]] — the "Save X EUR" label and the storefront price lookup.
- [[fixed-discount-api-access]] — the API surface that produces `save = 0` rows when `fixed_price = variant.price` is submitted.
- [[background-queue-inventory]] — the daily expiry sweep that respects the `date_end = today` boundary.
- [[discount]] — entity page for the parent Fixed discount.

## Open questions

- The modern API's lack of the silent-skip guard on `fixed_price = variant.price` — verify whether this is intentional (so integrators can see all submitted rows) or a known divergence to be patched (verify).
