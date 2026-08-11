---
type: feature
nav_path: "Marketing → Discounts → Products → Row writes"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["product_to_discount rows", "Fixed discount row writes", "Per-variant attachment", "Customer-group fan-out", "save denormalization"]
tags: [marketing, discounts, fixed, persistence, side-effects]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-fixed]]. See the hub for the other aspects (product modal, validation, plan gates, API access, storefront display).

# Fixed discount — `product_to_discount` row writes

## Purpose

This aspect documents **what gets persisted** when a Fixed-discount price is saved: the `product_to_discount` row layout, customer-group fan-out (one row per group per variant), the denormalized `save` column, the replace-then-recreate save transaction and its event chain, per-variant date inheritance, and the auto-deactivation when the catalog price drops.

For what the merchant types into the form, see [[fixed-discount-product-modal]]. For what gets rejected pre-save, see [[fixed-discount-validation-rules]].

## Where to find it

The row-write pipeline runs automatically whenever a Fixed-discount price is saved, toggled, or deleted from the Fixed-discount products page (`/admin/marketing-new/discounts/products/:id`). There is no "row inspection" UI — the rows are visible only via the JSON-API v2 `product-to-discount` resource (see [[fixed-discount-api-access]]) or as their storefront side effects (see [[fixed-discount-storefront-display]]).

## What the merchant can do here

The merchant doesn't operate this pipeline directly — it is the **side effect** of using the [[fixed-discount-product-modal]]. Understanding it lets the merchant:

- Predict how many `product_to_discount` rows a save creates (variants × customer groups).
- Understand why a "no-op" `save = 0` row appeared (legacy form vs modern API divergence — see [[fixed-discount-validation-rules]]).
- Understand why a previously-active row deactivated itself after a catalog-price edit.
- Plan the customer-group fan-out cost before assigning many groups to a high-variant-count discount.

## Settings & fields

This aspect introduces no new merchant-facing fields. It documents the **stored** shape of `product_to_discount` rows (set indirectly via [[fixed-discount-product-modal]]):

| Stored column | Source | Notes |
|---|---|---|
| `product_id` | Parent product (selected in the modal). | One per product attached to the discount. |
| `variant_id` | Per-variant in the submitted `prices[]`. | One row per variant — never per product. |
| `discount_id` | Parent Fixed discount. | Auto-filled at save. |
| `price` | `fixed_price` from the form, in integer cents. | The fixed price the storefront renders. |
| `save` | Precomputed: `variant.price − fixed_price` (standard) or `msrp_price − fixed_price` (MSRP mode). | Denormalized at write time. |
| `msrp_price` | Form input (MSRP mode only). | Strikethrough "was" price. |
| `customer_group_id` | Parent discount's `customer_groups` set (fan-out clones per group); `null` otherwise. | One row per group per variant. |
| `active` | Defaults to active on save; flipped by the inline / bulk toggle. | Subject to auto-deactivation feedback loop. |
| `date_start` / `date_end` | Inherited from parent if blank. | Re-inherited on parent date-range edits. |

## Business rules

### Per-variant attachment via `product_to_discount`

Saving a fixed price **writes one `product_to_discount` row per variant** — never per product (columns in **Settings & fields** above). These rows are what the storefront queries when rendering product cards (see [[fixed-discount-storefront-display]]); disabling or deleting a row immediately reverts the storefront to the catalog price.

### Customer-group expansion (one row per group per variant)

When the parent Fixed discount has customer groups assigned, the per-variant row is **cloned per group** — three groups + two variants → 6 rows (2 × 3). With no group restriction the row has `customer_group_id = null` and applies to everyone, so the storefront can query `product_to_discount` at render-time without re-filtering by group. See [[customers-custom-groups]].

> **⚙️ Backend — CloudCart staff only (internal; not a merchant-facing answer).**
> The fan-out happens in the platform code: it reads the parent's `customer_groups` IDs and falls back to `[null]` when none are set, then for each group it clones the `ProductToDiscount` row, sets `customer_group_id`, and persists via the platform code. That second method also back-fills `type`, `date_start`, `date_end`, and `discount_id` from the parent discount when the cloned row leaves them blank — which is why per-variant rows inherit the parent's date window.

### `save` is denormalized at write time

The `save` column is **precomputed at save time** as the savings in integer cents — either `variant.price − fixed_price` (standard) or `msrp_price − fixed_price` (MSRP mode). The storefront uses it directly for the "Save X EUR" label.

**Important consequence in MSRP mode:** the label compares against MSRP, NOT the previously-shown catalog price. With catalog 800, MSRP 1,000, fixed 700 it shows "Save 300 EUR" — but the true saving versus yesterday's price is 100 EUR. Merchants who want honesty should leave MSRP mode off. See [[fixed-discount-storefront-display]].

### Save flow — full transaction, replace-then-recreate

The save flow runs as one atomic transaction (rolls back entirely on any error):

1. Delete existing `product_to_discount` rows for this **`product_id`**. Note the modern (Vue) save keys this delete on the **product only — not** on `(discount_id, product_id)` — so it also removes that product's rows from **any other Fixed discount**. In practice a product lives in **one** Fixed discount at a time: editing it on one discount detaches it from the others. See [[fixed-discount-validation-rules]].
2. For each variant in the submitted prices, compute `fixed_price` (and `msrp_price` if MSRP mode is on) and insert the row. Customer-group fan-out applies (clone per group, else one row with `customer_group_id = null`); `date_start` / `date_end` and `discount_id` are filled from the parent when blank. In the modern path a fixed price **greater than** the variant's catalog price is **rejected with a validation error** (*"Price must be at least 1 and less than &lt;price&gt;"*) — the whole save fails, nothing is silently dropped; a price **equal** to the catalog price is accepted and stored as a `save = 0` row. (The legacy form instead silently skipped any `fixed_price >= variant.price` row.)
3. Re-evaluate the product's "default" variant (typically the cheapest), since the discount may have changed it.
4. Fire the product-updated and search-engine-sync events (effects below).

> **⚙️ Backend — CloudCart staff only (internal; not a merchant-facing answer).**
> The product-keyed delete is literally the platform code inside the platform code (the `admin.api.discounts.fixed.update` route, `POST products/{discount_id}/{product_id}`) — there is **no `discount_id` clause**, which is why editing a product on one Fixed discount wipes its rows everywhere. the platform code (the `POST products/{discount_id}` route) does **not** pre-delete — it only inserts — so two discounts can transiently both hold the same product until one is edited. The per-row price cap is the `validate_price` extension in the request validator (`$value < 1 || $value > variant.price` → error *"Price must be at least 1 and less than &lt;price&gt;"*), so equality passes and writes `save = 0`. The legacy `app/Http/Controllers/Sitecp/Discounts/the platform code` uses a strict `<` skip instead.

### Per-variant date inheritance from parent

When a per-variant row's `date_start` / `date_end` aren't explicitly set, they're **inherited from the parent Fixed discount** — so a row's effective expiry is the parent's by default. Editing the parent's date range updates every existing variant row's range (only when `date_start` / `date_end` change).

### Toggle and delete cascade events

Single-toggle (the row Active switch) and bulk-toggle flip the `active` column on every variant row for the product; bulk-delete removes the rows. All three fire product-updated + search-engine-sync events. Each toggle counts against the 10-minute activation cooldown — see [[fixed-discount-plan-gates]].

### Auto-deactivation on catalog price drop

When the merchant updates a product's catalog price elsewhere (Products → edit), the platform re-evaluates each fixed-discount row tied to the product:

- If the new catalog price ≤ the row's fixed price, the row is **deactivated** (`active = 0`).
- If the catalog price is now greater than the fixed price, the row's `save` field is re-computed (delta against the new catalog).

This keeps fixed-prices honest relative to the moving catalog price without manual intervention. Once deactivated, a row stays deactivated until a manual save re-activates it — even if the catalog price later rises back above the fixed price. Merchants who edit catalog prices often while a Fixed discount is live should verify the rows after the edit — see [[fixed-discount-storefront-display]] for the storefront fallback when no active row is found.

### Fixed discounts are themselves the per-product attachments

Unlike code-based or order-over discounts, which write `product_to_discount` rows in a separate regeneration step, Fixed discounts ARE the per-variant attachment rows — the regeneration is the **save flow itself**, with no separate background pass. The 10-minute activation cooldown still applies, but the cost is mostly in the listing-engine sync, not row creation.

### Side-effect summary

| Event fired | When | Downstream effect |
|---|---|---|
| product-updated | After save / toggle / delete | Listing engine rebuilds the product's grid row; storefront page-cache invalidates. |
| search-engine-sync | After save / toggle / delete | Search indices re-index the product's effective price. |
| `discount.created` webhook | On parent discount create | See [[settings-hooks]]. |
| `discount.updated` webhook | On parent discount update (incl. save-flow re-writes here) | See [[settings-hooks]]. |

## Related

- [[marketing-discounts-fixed]] — hub.
- [[fixed-discount-product-modal]] — where the merchant enters the prices that produce these rows.
- [[fixed-discount-validation-rules]] — pre-save validation, incl. the equality edge case that produces `save = 0` rows via the API.
- [[fixed-discount-storefront-display]] — how these rows are read at render time + the auto-deactivation feedback loop.
- [[fixed-discount-api-access]] — JSON-API v2 + GraphQL surfaces that trigger the same row-write pipeline.
- [[customers-custom-groups]] — customer groups drive the per-group fan-out.
- [[settings-hooks]] — `discount.created` / `discount.updated` webhook destinations.
- [[products-products]] — catalog price changes here trigger the auto-deactivation pipeline.
- [[discount]] — entity page for the parent Fixed discount record.

## Open questions

No outstanding questions.
