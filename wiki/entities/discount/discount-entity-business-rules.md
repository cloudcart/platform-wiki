---
type: entity
nav_path: "Entity → Discount → Business rules"
aliases: ["Discount business rules", "Discount validation", "Discount plan-gating", "Discount limits"]
tags: [marketing, discounts, entity, validation, plan-gates]
created: 2026-06-10
updated: 2026-11-04
source_count: 6
---

# Discount — Business rules

> Part of [[discount]]. See the hub for related aspects (fields, lifecycle, stacking, webhooks/API).

## Identity

The validation, plan-gating, restriction, and save-time normalisation rules the platform applies to a Discount row. The admin form, JSON-API v2 and GraphQL have separate validation; neither API runs the admin form's checks. Stacking-specific rules live separately on [[discount-entity-stacking-evaluation]].

## Aliases

- "Discount validation" — the per-field error messages surfaced to the merchant.
- "Plan-gating" — the per-type feature counters that determine availability.

## Key Attributes

### Countdown, Quantity and code limits

- **Countdown discount** — a second one can be saved. Checkout uses the first active one found, and tries no other.
- **Per-product Quantity discount** — a product can be in only one Quantity discount, active or not. Validation: *"Product is already in use"*.
- **Unique code** — every code is unique across all `discounts.code` per store.

### Plan-gating per type

The check runs on create only, and differs by path. See [[discount-stacking-plan-gating]].

| Plan feature | Counts | Used by |
|--------------|--------|---------|
| `discount_global` | No-code flat, percent and free-shipping discounts with `code_apply` off, which includes Countdown and Container discounts. Labels and banners do not count. | JSON-API v2 create. |
| `discount_fixed` | Fixed-type discounts. | JSON-API v2 and GraphQL create. |
| `discount_coupon` | Discounts holding their own code. Container and Code PRO discounts are not in it. | JSON-API v2 create. |
| `discount_quantity` | Quantity discounts. | GraphQL create. |
| `discount-code-pro` | Boolean enable. | Code PRO type availability. |
| `discount-code-pro-generator` | Numeric cap. | Max codes per bulk-generator run. |

In the admin form, a kind not enabled on the plan (`discount-<type>`) returns HTTP 403 *"This feature is not enabled for your plan. To access it, please upgrade your plan."* JSON-API v2 returns **402 Payment Required** over a quota. Usage counts discounts whether active or not; only deleting lowers it.

### Customer-group, region, and per-customer restrictions

A discount evaluates against the cart's customer (or guest group if no customer):

- `customer_groups[]` set → the cart's customer must be in one of those groups (else skipped).
- `geo_zone_id` set → the cart's shipping address must fall within the [[geo-zone]] (else skipped).
- `only_customer = 1` → enforced for codes at entry and for no-code Orders over and Countdown in totals.
- `maxused_user` set → the platform counts this customer's uses on orders in counted statuses. For logged-in customers on codes at entry and on no-code Orders over and Countdown.

### Force-save preserves discount on order edit

When `force_save = 1`, the discount stays attached to an order even if admin-side edits make the cart no longer meet the conditions (e.g., removing the qualifying product from an order with a shipping discount). Without `force_save`, the discount stays listed on the order, but stops being deducted while the conditions are not met. It is the merchant's own switch, *"Save the discount on your order"*, and can be off.

### Save-time field normalisation (on every create / edit)

Two normalisations run every time the Discount row is saved:

- **`code_prefix` defaults to 0** — when the merchant leaves the barcode-prefix flag null (the form omits it for non-barcode discount types), the hook sets it to `0`. This prevents a null value from breaking the storefront's barcode-scanner check.
- **`msrp` cleared for non-fixed types** — when the discount's `type` is anything other than `fixed`, the hook forces `msrp = 0`. The MSRP flag has meaning ONLY for fixed-price overrides; clearing it on `percent` / `shipping` / `quantity` / `countdown` discounts prevents the display layer from picking up a stale flag and showing a misleading "Now / Was" badge.

### Date-window propagation to fixed variants

When a `fixed` discount is edited and either `date_start` or `date_end` changes, the new dates propagate in one bulk UPDATE to every linked fixed-discount-variant row. This keeps the variant-level "active window" in sync with the parent — a merchant who shortens a 7-day Promo to 24 hours doesn't have to also manually update each of the 50 variants tied to the discount. Runs only on `type = fixed` (no-op on other types since they don't carry per-variant rows).

### Container codes — one store-wide pool

A Container discount (`flat` or `percent` with `is_container = 1`) takes its value from [[discount-code|Container codes]]. The codes are one store-wide pool attached to no Container, each string unique in the pool, and an order does not use a code up: it stays reusable until turned off or deleted.

### Container code application

All active Containers for the customer's region try the codes in the cart's `discount_container_code` array; the highest total wins. A code applies only if it fits what remains of that Container's value. Codes that do not fit stay in the array, unapplied. See [[discount-stacking-cart-code-slots]].

### Cart code mutual exclusion (stand-alone XOR Container)

The cart entity has two columns: `discount_code` (single string) and `discount_container_code` (array). Setting one **clears** the other — there is no third state. Stand-alone codes (Promo / Code PRO) live in `discount_code`; bulk-generated Container codes accumulate in `discount_container_code`. See [[discount-entity-stacking-evaluation]] for the full stacking implications.

### Code PRO — per-code conditions

Each PRO code is its own row with its OWN `type`, `type_value`, target, conditions, customer-group restriction, region, max-uses, and date window. One campaign can have many codes with different terms (VIP customers at 25% off, newsletter subscribers at 10% off, etc.).

### Barcode-as-code mode

When `code_prefix = 1` AND `code_format` is `ean13` / `ean8`, the code is treated as a barcode. Storefront barcode-scanner integrations match the scanned value against either the full code (`barcode_prefix = 0`) or as a prefix (`barcode_prefix = 1`). Both modes validate against EAN checksum rules. Used by physical-retail merchants.

### Deleting a discount

A discount used in a smart collection or an XML import / sync task cannot be deleted from the list: *"This discount cannot be deleted because it is still used in: ..."*. Deleting a Code PRO discount removes its codes (verify). Container codes belong to no Container, so they stay in the pool. Historical per-order audit rows are preserved (the order's stored discount snapshot is independent of the live Discount row).

### Code lookup is case-insensitive

The cart's code-validation flow does a case-insensitive match on the code plus an explicit case-insensitive equality check afterwards — the second check guards against edge-case false positives, so `SUMMER20`, `summer20`, and `Summer20` all resolve to the same discount.

### Amount limits

- `flat` and `order_over`: no maximum amount.
- `percent`: limited to **100%** in the admin form only. Neither API limits it. JSON-API stores values as sent, so percent is percent × 100 (1000 means 10%).


## Where it appears

- [[marketing-discounts]] — surfaces validation errors and the plan response (HTTP 403).
- [[plan-gates]] — the cross-cutting plan-feature catalogue.
- [[settings-hooks]] — `discount.*` webhooks fire after these rules pass.
- [[api-discounts]] — JSON-API v2 has its own validation — see [[discount-entity-webhooks-api]].

## Related

- [[discount]] — hub.
- [[discount-entity-fields]] — the fields these rules validate.
- [[discount-entity-lifecycle]] — delete behaviour.
- [[discount-entity-stacking-evaluation]] — stacking-specific rules (`code_apply`, `apply_regular_price`, where Cart Rules sit).
- [[discount-code]] — Container and Code PRO code rows.
- [[customer-group]] / [[geo-zone]] — restriction targets.
- [[plan-gates]] — per-type plan-feature catalogue.
- [[products-banners-labels]] — pure-visual rows, not counted against `discount_global`.

## Open Questions

- ⏸️ **Bulk-export of Container codes format** — column order, encoding for codes containing `#` / `.` characters, header row presence — need verification on a live export.
