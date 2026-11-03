---
type: entity
nav_path: "Entity → Discount → Business rules"
aliases: ["Discount business rules", "Discount validation", "Discount plan-gating", "Discount limits"]
tags: [marketing, discounts, entity, validation, plan-gates]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

# Discount — Business rules

> Part of [[discount]]. See the hub for related aspects (fields, lifecycle, stacking, webhooks/API).

## Identity

The validation, plan-gating, restriction, and save-time normalisation rules the platform applies to a Discount row — independent of how it was created (admin UI or JSON-API v2). Stacking-specific rules live separately on [[discount-entity-stacking-evaluation]].

## Aliases

- "Discount validation" — the per-field error messages surfaced to the merchant.
- "Plan-gating" — the per-type feature counters that determine availability.

## Key Attributes

### One-per-store-instance limits

- **Countdown discount** — only ONE can exist per store. Trying to create a second returns: *"Countdown discount already exists"*.
- **Per-product Quantity discount** — only ONE active quantity discount can target any given product. Validation: *"A volume discount with this product already exists"*.
- **Fixed-discount parent + child category conflict** — a Fixed discount cannot target a category AND its sub-category simultaneously: *"Parent and Child product categories, can not be included"*.
- **Unique code** — every code is unique across all `discounts.code` per store.

### Plan-gating per type

Each type counts against a separate plan-feature counter — the merchant's package determines how many of each type they can have:

| Plan feature | Counts | Used by |
|--------------|--------|---------|
| `discount_global` | Discounts without a code (Global / Countdown / no-code shipping). | Always-on discounts. |
| `discount_fixed` | Fixed-type discounts. | Per-product price overrides. |
| `discount_coupon` | All discounts with a code. | Promo / Container / Code PRO. |
| `discount_quantity` | Quantity discounts. | Tiered product discounts. |
| `discount-code-pro` | Boolean enable. | Code PRO type availability. |
| `discount-code-pro-generator` | Numeric cap. | Max codes per bulk-generator run. |

When the plan doesn't permit, the create endpoint returns *"Not supported by plan"* with the list of plans where it IS supported.

### `discount_global` plan-gate also blocks Banners and Labels

The `discount_global` plan-feature counts ALL codeless discounts in the store — including pure-visual banner / label rows that don't actually reduce price ([[products-banners-labels]]). A merchant on a plan with `discount_global = 5` who has 3 banners and 2 labels has hit the cap and cannot create a new Global percent-off campaign without archiving a visual row first. (verify)

### Customer-group, region, and per-customer restrictions

A discount evaluates against the cart's customer (or guest group if no customer):

- `customer_groups[]` set → the cart's customer must be in one of those groups (else skipped).
- `geo_zone_id` set → the cart's shipping address must fall within the [[geo-zone]] (else skipped).
- `only_customer = 1` → guests cannot use the discount at all.
- `maxused_user` set → the platform counts how many orders from THIS customer (in counted statuses) have used the discount; if `>= maxused_user`, the code is rejected.

### Force-save preserves discount on order edit

When `force_save = 1`, the discount stays attached to an order even if admin-side edits make the cart no longer meet the conditions (e.g., removing the qualifying product from an order with a shipping discount). Without `force_save`, the discount detaches automatically. Required for `shipping` and `order_over` discounts.

### Save-time field normalisation (on every create / edit)

Two normalisations run every time the Discount row is saved:

- **`code_prefix` defaults to 0** — when the merchant leaves the barcode-prefix flag null (the form omits it for non-barcode discount types), the hook sets it to `0`. This prevents a null value from breaking the storefront's barcode-scanner check.
- **`msrp` cleared for non-fixed types** — when the discount's `type` is anything other than `fixed`, the hook forces `msrp = 0`. The MSRP flag has meaning ONLY for fixed-price overrides; clearing it on `percent` / `shipping` / `quantity` / `countdown` discounts prevents the display layer from picking up a stale flag and showing a misleading "Now / Was" badge.

### Date-window propagation to fixed variants

When a `fixed` discount is edited and either `date_start` or `date_end` changes, the new dates propagate in one bulk UPDATE to every linked fixed-discount-variant row. This keeps the variant-level "active window" in sync with the parent — a merchant who shortens a 7-day Promo to 24 hours doesn't have to also manually update each of the 50 variants tied to the discount. Runs only on `type = fixed` (no-op on other types since they don't carry per-variant rows).

### Container codes — child of a parent discount

A Container discount (`flat` or `percent` with `is_container = 1`) holds many child [[discount-code|DiscountCode]] codes — typically generated in bulk via the codes-list sub-page. Each child code is consumed once. The redemption mechanism is the same as a regular promo code, but the row lives in the child code-table rather than the parent `discounts` table.

### Container code application — sequential consumption with `total_value` cap

When a Container discount applies, the platform consumes Container code rows from the cart's `discount_container_code` array sequentially: each code's `value` is added to a running `type_value` total until either all codes are consumed or the running total reaches the parent's `total_value` cap. Codes beyond the cap remain unconsumed and stay in the cart's array (so the customer's other codes don't simply disappear — they remain for the next eligible cart). This supports multiple Container codes per cart.

### Cart code mutual exclusion (stand-alone XOR Container)

The cart entity has two columns: `discount_code` (single string) and `discount_container_code` (array). Setting one **clears** the other — there is no third state. Stand-alone codes (Promo / Code PRO) live in `discount_code`; bulk-generated Container codes accumulate in `discount_container_code`. See [[discount-entity-stacking-evaluation]] for the full stacking implications.

### Code PRO — per-code conditions

Each PRO child is its own row with its OWN `type`, `type_value`, target, conditions, customer-group restriction, region, max-uses, and date window. A single parent can have many children with different terms (VIP customers at 25% off, newsletter subscribers at 10% off, etc.).

### Barcode-as-code mode

When `code_prefix = 1` AND `code_format` is `ean13` / `ean8`, the code is treated as a barcode. Storefront barcode-scanner integrations match the scanned value against either the full code (`barcode_prefix = 0`) or as a prefix (`barcode_prefix = 1`). Both modes validate against EAN checksum rules. Used by physical-retail merchants.

### Deleting a Container / Code PRO parent cascades to children

Removing a Container or Code PRO parent **cascades** to its child code rows. Historical per-order audit rows are preserved (the order's stored discount snapshot is independent of the live Discount row).

### Code lookup is case-insensitive

The cart's code-validation flow does a case-insensitive match on the code plus an explicit case-insensitive equality check afterwards — the second check guards against edge-case false positives, so `SUMMER20`, `summer20`, and `Summer20` all resolve to the same discount.

### Currency / amount caps

- `flat` amounts: max **100,000 cents** (1,000 BGN per discount).
- `percent`: max **100%**.

## Where it appears

- [[marketing-discounts]] — surfaces validation errors and plan-overflow modals (HTTP 402).
- [[plan-gates]] — the cross-cutting plan-feature catalogue.
- [[settings-hooks]] — `discount.*` webhooks fire after these rules pass.
- [[api-discounts]] — JSON-API v2 enforces the same rules — see [[discount-entity-webhooks-api]].

## Related

- [[discount]] — hub.
- [[discount-entity-fields]] — the fields these rules validate.
- [[discount-entity-lifecycle]] — soft-delete + cascade behaviour.
- [[discount-entity-stacking-evaluation]] — stacking-specific rules (`code_apply`, `apply_regular_price`, Discounts-before-Cart-Rules).
- [[discount-code]] — Container child code row.
- [[customer-group]] / [[geo-zone]] — restriction targets.
- [[plan-gates]] — per-type plan-feature catalogue.
- [[products-banners-labels]] — pure-visual rows that count against `discount_global`.

## Open Questions

- ⏸️ **Bulk-export of Container codes format** — column order, encoding for codes containing `#` / `.` characters, header row presence — need verification on a live export.
