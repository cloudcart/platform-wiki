---
type: feature
nav_path: "Marketing → Discounts → Products → Save & replace flow"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Discount products save flow", "Discount products full replace", "product_to_discount row writes", "ProductUpdated event for discount", "ProductsSearchEnginesSync on discount save", "Запис на отстъпка — пълна замяна", "Edit на отстъпка изтрива варианти"]
tags: [marketing, discounts, fixed, products, save-flow, events, transaction, full-replace]
plan_gates: ["discount_fixed"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Discount products — save flow, full-replace semantics, events

> Part of [[marketing-discounts-products]]. See the hub for the list view, modal flow, fields, and business rules.

## Purpose

When the merchant saves the modal, toggles a row's status, or removes a product, the backend writes **per-variant rows** (not per-product) and re-evaluates downstream caches and search indices. This page documents the exact **order of operations** in the save transaction, the **full-replace semantics** that make "edit and save" silently drop variants not in the payload, and the **events fired** that propagate to the listing engine and the search index.

This matters most for "I edited my discount and now some variants are missing" tickets — the save flow is **designed** to replace the entire `(discount_id, product_id)` rowset on every Edit-mode save. The modal mitigates this by pre-filling all variants, but bulk-update paths (scripts, JSON-API v2 writes) must send every variant or accept the drop.

## Where to find it

The save flow is invoked by the merchant through the modal at `/admin/marketing-new/discounts/products/:id` — there is no separate UI for it. The list-page status toggle and remove actions run shorter variants of the same flow.

## What the merchant can do here

This page documents backend behaviour the merchant cannot directly invoke from a dedicated UI. The merchant triggers this flow by:

- **Saving the modal** in Add or Edit mode — see [[discounts-products-modal-flow]].
- **Toggling a row's Active state** (or bulk-toggling) — see [[discounts-products-list-view]].
- **Removing a row** (or bulk-deleting) — see [[discounts-products-list-view]].

## Settings & fields

### Save endpoint payload

The save endpoint accepts an array of entries: `{ product_id, variant_id, price, msrp? }` (price + MSRP in cents).

### Validation (runs before the transaction opens)

- `product_id`, `variant_id`, `price` are required integers; `price` is in cents.
- `price` must be at least 1 and strictly less than the variant's catalog price (*"Price must be at least 1 and less than <variant.price>"*).
- `variant_id` must not already exist on this discount (when adding a new product; not when updating an existing one).
- `product_id` must match the route's `product_id` (when updating).
- `msrp` (when the parent discount is in MSRP mode) is an integer in cents and follows the same price-validity check.

### Save transaction (single DB transaction)

1. **(Update only) Delete all existing rows** for this `(discount_id, product_id)` pair — full replace.
2. **For each entry in the submitted array, insert a row** with the precomputed `save` value (= `variant.price − price`, or `msrp − price` in MSRP mode) and `msrp_price` when applicable.
3. **Re-evaluate each affected product's default variant** (since the discount may have changed which variant is the cheapest).
4. **Fire `ProductUpdated`** so the listing engine rebuilds the product's grid row.
5. **Fire the search re-index** so the search index / search indices re-index the price.

### Status toggle endpoint

Accepts `{product_ids: [...], status: 'yes'|'no'}` and flips `active` on **every variant row** under the selected products. Both events (`ProductUpdated`, the search re-index) fire.

### Delete endpoint

Accepts `ids[product_ids][i]` query params and removes **every variant row** for each selected product. Both events fire.

## Business rules

### Per-variant rows under the hood (not per-product)

The save writes **one row per variant** to the `product_to_discount` table — not one row per product. The payload is an array of `{product_id, variant_id, price}` entries. "Common price" mode fills every entry's `price` with the same value; "Multiple price" lets the merchant enter different prices per variant.

### Save = full replace for the product

The update endpoint **deletes all existing rows** for this `(discount_id, product_id)` pair before re-inserting from the submitted array. So an "edit and save" is effectively a **full replace** — variants the merchant didn't include in the payload **disappear** from the discount. The modal mitigates this by always pre-filling all of the product's variants (even ones with no existing override) — but a script or external tool driving the endpoint directly could accidentally drop variants.

### `fixed_price >= variant.price` is silently dropped, not errored

When inserting per-variant rows, the save flow re-checks `fixed_price < variant.price`. Any entry where the fixed price is NOT cheaper than the variant's catalog price is **skipped** (no row inserted, no error message). The merchant sees the saved discount with FEWER variants than they entered — the invalid ones simply disappear. This compounds with the full-replace semantics: an Edit that re-submits a previously-valid price after a catalog-price drop can silently drop the row.

### Status toggle fans out to all variant rows

Toggling a single product's Active state (or bulk-toggling) flips the `active` column on **every variant row** for that product under this discount. Bulk-delete removes every variant row for each selected product.

### Per-variant date and discount_id inheritance

When inserting variant rows, missing `date_start`, `date_end`, `discount_id` are auto-filled from the parent discount before insert. Editing the parent discount's date range automatically updates every variant row's dates via the underlying model's update hook — the merchant doesn't have to re-save each product.

### Customer-group fan-out happens at the parent discount's save

When the parent Fixed discount has customer-group restrictions, the platform clones each variant row per group at the **parent's** save time. This page (and its save flow) does NOT expose customer groups — it inherits them. See [[discounts-products-business-rules]] for the rationale.

### Default Fixed discount (auto-created)

The platform has a concept of a **default Fixed discount** — a singleton Fixed discount marked with `for_products = yes` meta, auto-created on first need. Used as a fallback container for products discounted ad-hoc (e.g., via inline price edits on the product page). Most merchants never see this; it's an internal helper. See [[discounts-products-business-rules]].

### Events: `ProductUpdated` + the search re-index

Every save / toggle / delete fires both events for every affected product (chunked when bulk). `ProductUpdated` rebuilds the listing-engine grid row; the search re-index re-indexes the search index on the `searchable-import4` queue. The storefront reflects the change only after both have processed the affected products — see [[storefront-architecture]] + [[background-queue-inventory]].

### Webhook

Each save / toggle / delete also fires the `discount.updated` webhook event — see [[settings-hooks]]. Receivers must be idempotent because a single bulk-toggle on 30 products fires 30 events.

## Related

- [[marketing-discounts-products]] — hub.
- [[discounts-products-modal-flow]] — the UI entry point that triggers the save flow.
- [[discounts-products-list-view]] — the UI entry point for the toggle + delete endpoints.
- [[discounts-products-fields]] — the validation messages raised before the transaction opens.
- [[discounts-products-business-rules]] — the broader cross-cutting rules (type guard, picker source, MSRP-mode savings display).
- [[marketing-discounts-fixed]] — parent discount; customer-group fan-out and date inheritance live there.
- [[storefront-architecture]] — the search index re-index path triggered by the search re-index.
- [[background-queue-inventory]] — the `searchable-import4` queue that processes the re-index.
- [[settings-hooks]] — `discount.updated` webhook fires on each save / toggle / delete.

## Open questions

No outstanding questions.
