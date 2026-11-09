---
type: feature
nav_path: "Marketing → Discounts → Products → Save & replace flow"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id
aliases: ["Discount products save flow", "Discount products full replace", "product_to_discount row writes", "Запис на отстъпка — пълна замяна", "Edit на отстъпка изтрива варианти"]
tags: [marketing, discounts, fixed, products, save-flow, events, transaction, full-replace]
plan_gates: ["discount_fixed"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

# Discount products — save flow, full-replace semantics, events

> Part of [[marketing-discounts-products]]. See the hub for the list view, modal flow, fields, and business rules.

## Purpose

When the merchant saves the modal, toggles a row's status, or removes a product, the backend writes **per-variant rows** (not per-product) and re-evaluates downstream caches and search indices. This page documents the exact **order of operations** in the save transaction, the **full-replace semantics** that make "edit and save" silently drop variants not in the payload, and the **events fired** that propagate to the listing engine and the search index.

This matters most for "I edited my discount and now some variants are missing" tickets — every Edit-mode save removes all of the product's rows, on every discount, before writing back the submitted ones. The modal always sends every variant, but a script driving the endpoint directly must send every variant or accept the drop.

## Where to find it

The save flow is invoked by the merchant through the modal at `/admin/marketing/discounts/products/:id` — there is no separate UI for it. The list-page status toggle and remove actions run shorter variants of the same flow.

## What the merchant can do here

This page documents backend behaviour the merchant cannot directly invoke from a dedicated UI. The merchant triggers this flow by:

- **Saving the modal** in Add or Edit mode — see [[discounts-products-modal-flow]].
- **Toggling a row's Active state** (or bulk-toggling) — see [[discounts-products-list-view]].
- **Removing a row** (or bulk-deleting) — see [[discounts-products-list-view]].

## Settings & fields

### Save endpoint payload

The save endpoint accepts an array of entries: `{ product_id, variant_id, price }` (price in cents).

### Validation (runs before the transaction opens)

- `product_id`, `variant_id`, `price` are required integers; `price` is in cents.
- `price` must be at least 1 and no higher than the variant's catalog price (*"Price must be at least 1 and less than <variant.price>"*). A price equal to the catalog price is accepted.
- `variant_id` must not already exist on this discount (when adding a new product; not when updating an existing one).
- `product_id` must match the route's `product_id` (when updating).

### Save transaction (single DB transaction)

1. **(Update only) Delete all existing rows** for this `product_id`, on every discount — full replace.
2. **For each entry in the submitted array, insert a row** with the precomputed `save` value (= `variant.price − price`).
3. **Re-evaluate each affected product's default variant** (since the discount may have changed which variant is the cheapest).
4. **Fire the product-updated event** so the listing engine rebuilds the product's grid row.
5. **Fire the search-engine-sync event** so the search index / search indices re-index the price.

### Status toggle endpoint

Accepts `{product_ids: [...], status: 'yes'|'no'}` and flips `active` on **every variant row** under the selected products. Both events fire.

### Delete endpoint

Accepts `ids[product_ids][i]` query params and removes **every variant row** for each selected product. Both events fire.

## Business rules

### Per-variant rows under the hood (not per-product)

The save writes **one row per variant** to the `product_to_discount` table — not one row per product. The payload is an array of `{product_id, variant_id, price}` entries. "Common price" mode fills every entry's `price` with the same value; "Multiple price" lets the merchant enter different prices per variant.

### Save = full replace for the product

The update endpoint **deletes all existing rows** for this `product_id` on every discount, Fixed, Flat and Percent, before re-inserting from the submitted array, which writes back only the edited one. Flat and Percent rows return when the product is next saved or that discount is rebuilt. So an "edit and save" is effectively a **full replace** — variants the merchant didn't include in the payload **disappear** from the discount. The modal always sends every one of the product's variants — but a script or external tool driving the endpoint directly could accidentally drop variants.

### A price above the catalog price fails the whole save

A price above the variant's catalog price is rejected before the transaction opens: the whole save fails with the message above and nothing is written. A price equal to the catalog price is saved with `save = 0`.

### Status toggle fans out to all variant rows

Toggling a single product's Active state (or bulk-toggling) flips the `active` column on **every variant row** for that product under this discount. Bulk-delete removes every variant row for each selected product.

### Per-variant date and discount_id inheritance

When inserting variant rows, missing `date_start`, `date_end`, `discount_id` are auto-filled from the parent discount before insert. Editing the parent discount's date range automatically updates every variant row's dates via the underlying model's update hook — the merchant doesn't have to re-save each product.

### Customer groups are copied at this save

When the parent Fixed discount has customer-group restrictions, the platform clones each variant row per group when a product's prices are saved here. This page does NOT expose customer groups — it inherits them. Changing groups on an existing Fixed discount does not change products already attached until each is edited. See [[discounts-products-business-rules]].

### Default Fixed discount (auto-created)

The discount block on the product form writes into one auto-created Fixed discount, **Default Fixed Discount**, listed in the Discounts list. While it is inactive, prices entered there are saved but never applied. See [[discounts-products-business-rules]].

### Events: product-updated + search-engine-sync

Every save / toggle / delete fires both events for the affected products. product-updated rebuilds the listing-engine grid row; search-engine-sync re-indexes the search index. The storefront reflects the change only after both have processed the affected products — see [[storefront-architecture]] + [[background-queue-inventory]].

### Webhook

Saving, switching or removing products on a Fixed discount sends no webhook. `discount.updated` fires only when the discount record itself is saved — see [[settings-hooks]].

## Related

- [[marketing-discounts-products]] — hub.
- [[discounts-products-modal-flow]] — the UI entry point that triggers the save flow.
- [[discounts-products-list-view]] — the UI entry point for the toggle + delete endpoints.
- [[discounts-products-fields]] — the validation messages raised before the transaction opens.
- [[discounts-products-business-rules]] — the broader cross-cutting rules (type guard, picker source).
- [[marketing-discounts-fixed]] — parent discount; customer-group fan-out and date inheritance live there.
- [[storefront-architecture]] — the search index re-index path triggered by the search-engine-sync event.
- [[background-queue-inventory]] — the queue that processes the re-index.
- [[settings-hooks]] — webhook events; product changes here send none.

## Open questions

No outstanding questions.
