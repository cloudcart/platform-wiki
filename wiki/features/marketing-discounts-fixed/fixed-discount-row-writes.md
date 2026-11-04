---
type: feature
nav_path: "Marketing → Discounts → Products → Row writes"
route_name: discounts-products
route_path: /admin/marketing/discounts/products/:id
aliases: ["product_to_discount rows", "Fixed discount row writes", "Per-variant attachment", "Customer-group fan-out", "save denormalization"]
tags: [marketing, discounts, fixed, persistence, side-effects]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (product modal, validation, plan gates, API access, storefront display).

# Fixed discount — `product_to_discount` row writes

## Purpose

This aspect documents **what gets persisted** when a Fixed-discount price is saved: the `product_to_discount` row layout, customer-group fan-out (one row per group per variant), the denormalized `save` column, the replace-then-recreate save transaction and its event chain, per-variant date inheritance, and the auto-deactivation when the catalog price drops.

For what the merchant types into the form, see [[fixed-discount-product-modal]]. For what gets rejected pre-save, see [[fixed-discount-validation-rules]].

## Where to find it

The row-write pipeline runs automatically whenever a Fixed-discount price is saved, toggled, or deleted from the Fixed-discount products page (`/admin/marketing/discounts/products/:id`). There is no "row inspection" UI — the rows are visible only via the JSON-API v2 `product-to-discount` resource (see [[fixed-discount-api-access]]) or as their storefront side effects (see [[fixed-discount-storefront-display]]).

## What the merchant can do here

The merchant doesn't operate this pipeline directly — it is the **side effect** of using the [[fixed-discount-product-modal]]. Understanding it lets the merchant:

- Predict how many `product_to_discount` rows a save creates (variants × customer groups).
- Understand why a "no-op" `save = 0` row appeared (see [[fixed-discount-validation-rules]]).
- Understand why a previously-active row deactivated itself after a catalog-price edit.
- Plan the customer-group fan-out cost before assigning many groups to a high-variant-count discount.

## Settings & fields

This aspect introduces no new merchant-facing fields. It documents the **stored** shape of `product_to_discount` rows (set indirectly via [[fixed-discount-product-modal]]):

| Stored column | Source | Notes |
|---|---|---|
| `product_id` | Parent product (selected in the modal). | One per product attached to the discount. |
| `variant_id` | One entry per variant in the submitted save. | One row per variant — never per product. |
| `discount_id` | Parent Fixed discount. | Auto-filled at save. |
| `price` | `fixed_price` from the form, in integer cents. | The fixed price the storefront renders. |
| `save` | Precomputed: `variant.price − fixed_price`. | Denormalized at write time. |
| `customer_group_id` | Parent discount's `customer_groups` set (fan-out clones per group); `null` otherwise. | One row per group per variant. |
| `active` | Defaults to active on save; flipped by the inline / bulk toggle. | Also switched off by the auto-deactivation feedback loop and when the discount expires. |
| `date_start` / `date_end` | Inherited from parent if blank. | Re-inherited on parent date-range edits. |

## Business rules

### Per-variant attachment via `product_to_discount`

Saving a fixed price **writes one `product_to_discount` row per variant** — never per product (columns in **Settings & fields** above). These rows are what the storefront queries when rendering product cards (see [[fixed-discount-storefront-display]]); disabling or deleting a row immediately reverts the storefront to the catalog price.

### Customer-group expansion (one row per group per variant)

When the parent Fixed discount has customer groups assigned, the per-variant row is **cloned per group** — three groups + two variants → 6 rows (2 × 3). With no group restriction the row has `customer_group_id = null` and applies to everyone, so the storefront can query `product_to_discount` at render-time without re-filtering by group. Groups are copied when a product's prices are saved: changing groups on an existing Fixed discount does not change products already attached until each is edited. See [[customers-custom-groups]].

### `save` is denormalized at write time

The `save` column is **precomputed at save time** as the savings in integer cents: `variant.price − fixed_price`. Listings use it for the "Save X EUR" label.

### Save flow — full transaction, replace-then-recreate

The save flow runs as one atomic transaction (rolls back entirely on any error):

1. In the admin modal, an edit first deletes that **product's** `product_to_discount` rows on **every discount** — Fixed, no-code Flat and no-code Percent alike. Only the edited discount's rows are written back; Flat and Percent rows return when the product is next saved or that discount is rebuilt. Adding a product (not editing) deletes nothing, so two Fixed discounts can hold the same product until one of them is edited. See [[fixed-discount-validation-rules]].
2. For each variant in the submitted prices, compute `fixed_price` and insert the row. Customer-group fan-out applies (clone per group, else one row with `customer_group_id = null`); `date_start` / `date_end` and `discount_id` are filled from the parent when blank. A fixed price **greater than** the variant's catalog price is **rejected with a validation error** (*"Price must be at least 1 and less than &lt;price&gt;"*) and the whole save fails; a price **equal** to the catalog price is accepted and stored as a `save = 0` row.
3. Re-evaluate the product's "default" variant (typically the cheapest), since the discount may have changed it.
4. Fire the product-updated and search-engine-sync events (effects below).

### Per-variant date inheritance from parent

When a per-variant row's `date_start` / `date_end` aren't explicitly set, they're **inherited from the parent Fixed discount** — so a row's effective expiry is the parent's by default. Editing the parent's date range updates every existing variant row's range (only when `date_start` / `date_end` change).

### Toggle and delete cascade events

Single-toggle (the row Active switch) and bulk-toggle flip the `active` column on every variant row for the product; bulk-delete removes the rows. All three fire product-updated + search-engine-sync events.

### Auto-deactivation on catalog price drop

When the merchant updates a product's catalog price elsewhere (Products → edit), the platform re-evaluates each fixed-discount row tied to the product:

- If the new catalog price ≤ the row's fixed price, the row is **deactivated** (`active = 0`).
- If the catalog price is now greater than the fixed price, the row's `save` field is re-computed (delta against the new catalog).

This keeps fixed-prices honest relative to the moving catalog price without manual intervention. Once deactivated, a row stays deactivated until it is re-saved or switched back on — even if the catalog price later rises back above the fixed price. Merchants who edit catalog prices often while a Fixed discount is live should verify the rows after the edit — see [[fixed-discount-storefront-display]] for the storefront fallback when no active row is found.

### Expiry switches product rows off

When a Fixed discount expires, its products switch off too. After extending and reactivating it, switch the products back on or re-save them.

### Fixed discounts are themselves the per-product attachments

Code discounts and Orders-over discounts write no `product_to_discount` rows; no-code Flat and Percent discounts on products write them when saved. Fixed discounts ARE the per-variant attachment rows — they are written by the product save itself, with no separate background pass.

### Side-effect summary

| Event fired | When | Downstream effect |
|---|---|---|
| product-updated | After save / toggle / delete | Listing engine rebuilds the product's grid row; storefront page-cache invalidates. |
| search-engine-sync | After save / toggle / delete | Search indices re-index the product's effective price. |
| `discount.created` webhook | On parent discount create | See [[settings-hooks]]. |
| `discount.updated` webhook | On parent discount update only; product saves, toggles and deletes here send none | See [[settings-hooks]]. |

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-product-modal]] — where the merchant enters the prices that produce these rows.
- [[fixed-discount-validation-rules]] — pre-save validation, incl. the equality edge case that produces `save = 0` rows.
- [[fixed-discount-storefront-display]] — how these rows are read at render time + the auto-deactivation feedback loop.
- [[fixed-discount-api-access]] — JSON-API v2 + GraphQL surfaces that trigger the same row-write pipeline.
- [[customers-custom-groups]] — customer groups drive the per-group fan-out.
- [[settings-hooks]] — `discount.created` / `discount.updated` webhook destinations.
- [[products-products]] — catalog price changes here trigger the auto-deactivation pipeline.
- [[discount]] — entity page for the parent Fixed discount record.

## Open questions

No outstanding questions.
