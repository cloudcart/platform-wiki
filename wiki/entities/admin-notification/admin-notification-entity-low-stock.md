---
type: entity
nav_path: "Entity → Admin Notification → Low-stock & out-of-stock"
aliases: ["product_quantity_low notification", "product_out_of_stock notification", "Low-stock email", "Out-of-stock email", "Low-stock threshold", "Per-product threshold override", "product_threshold setting", "Известие за изчерпващ запас"]
tags: [entity, notifications, inventory, low-stock, out-of-stock]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[admin-notification]]. See the hub for the other aspects (types, master switch, recipient, delivery, alert channel).

# Admin Notification — Low-stock & out-of-stock alerts

## Identity

Two of the 14 toggleable Admin Notification types are driven by [[inventory-tracking|inventory tracking]]: **`product_quantity_low`** (a [[variant|Variant]]'s stock crosses a configured low-stock threshold) and **`product_out_of_stock`** (a Variant's stock falls to zero). Both fire at the moment an order line decrements stock (NOT on manual stock edits or bulk imports — see [[inventory-restock]] and [[products-change-log]] for those audit trails), and both honour the standard suppression model (master switch + per-type toggle — see [[admin-notification-entity-master-switch]]).

The two types differ from the rest of the 14 toggleable categories in that they support a **per-product threshold override** on top of the store-wide default. Low-stock alerting can therefore be tuned per-product without rewriting the global setting.

## Aliases

- **`product_quantity_low`** — the toggleable type for low-stock alerts; `mail_product_quantity_low` setting key.
- **`product_out_of_stock`** — the toggleable type for out-of-stock alerts; `mail_product_out_of_stock` setting key.
- **`product_threshold`** — the store-wide low-stock threshold setting on [[settings-cart]].
- **Per-product threshold** — the override field on the product editor (the `threshold` attribute on the [[product|Product]]; see [[inventory-variant-model]]).
- **Low-stock alert** / **Известие за изчерпващ запас** — informal merchant-facing phrasing.
- **Out-of-stock alert** / **Известие за изчерпан запас** — informal phrasing for the zero-stock case.

## Key Attributes

### Two notification types — `product_quantity_low` and `product_out_of_stock`

| Type | `mail_<label>` setting | Triggered when |
|------|------------------------|----------------|
| **`product_quantity_low`** | `mail_product_quantity_low` | A Variant's resulting `quantity` after stock-decrement is at or below the applicable threshold (store-wide default OR per-product override). |
| **`product_out_of_stock`** | `mail_product_out_of_stock` | A Variant's resulting `quantity` after stock-decrement reaches zero. |

Both default to ON when the setting row is missing. Both are gated by the master switch (see [[admin-notification-entity-master-switch]]).

### Two-level threshold — store-wide default with per-product override

The low-stock check fires using a two-level threshold:

| Level | Setting | Where configured |
|-------|---------|------------------|
| **Store-wide default** | `product_threshold` | [[settings-cart]] → "Order and product quantities" box. Applies to every Variant of every Product by default. |
| **Per-product override** | `threshold` attribute on the Product | Product editor → product-level field. Overrides the store-wide default for THIS product's Variants only. |

Resolution rule: if the per-product `threshold` is set (non-blank, non-zero), it wins; otherwise the store-wide `product_threshold` applies. Per-product threshold validation:

- Blank → falls back to store-wide default.
- `0` → REJECTED with *"threshold has invalid value"* (the platform treats `0` as missing, but the API requires the field to be either blank or a positive integer).
- Set on a Product where `tracking = no` → REJECTED with *"product cannot have threshold if not tracked"* (untracked products never decrement stock, so a threshold is meaningless).

See [[inventory-variant-model]] for the full per-product / per-Variant validation matrix.

### Per-variant triggering granularity

The check fires at the moment an order line decrements stock — comparing the resulting Variant `quantity` against the applicable threshold. Triggering granularity is **per-Variant**, not per-Product:

- A Product with 5 Variants where only ONE drops below threshold triggers **one notification** for that single Variant.
- A Product with 5 Variants where THREE drop below threshold in the same order triggers **three notifications** (one per affected Variant).
- A Variant that drops to zero triggers BOTH `product_quantity_low` (if zero crosses the threshold) AND `product_out_of_stock` — both types fire independently.

### When the check fires (and when it doesn't)

The threshold check runs at **stock-decrement time** — that is, when an [[order|Order]] reaches the status configured by `order_status_for_quantity_decrease` on [[settings-cart]] (see [[inventory-decrement-timing]]):

| Stock change source | Low-stock alert fires? |
|---------------------|------------------------|
| Order decrement (at `paid` or `pending` per setting) | YES |
| Order cancel / refund / void → stock returns (see [[inventory-restock]]) | NO (re-credit doesn't fire alert) |
| Manual admin edit on [[products-inventory]] | NO (verify) |
| Bulk import via [[apps-csv-import]] / [[apps-xml-sync]] | NO (bulk imports bypass the alert) |
| JSON-API v2 write to `variant.quantity` | (verify) |

Bulk imports bypassing the alert is intentional: a CSV that drops 1,000 Variants below threshold would otherwise produce 1,000 emails in one batch. The merchant is expected to review stock state via [[products-inventory]] after a bulk import.

### Interaction with `continue_selling` / oversell

Both alerts fire **regardless** of the [[product|Product]]'s `continue_selling` flag (see [[inventory-oversell]]) — the alert is informational, not gating. With `continue_selling = yes`, the Variant remains sellable after the alert; with `continue_selling = no`, the storefront blocks Add-to-cart for that Variant going forward.

### Practical guidance — turning off low-stock alerts for a specific Product

The merchant has three options to silence low-stock alerts for one Product without affecting the rest of the store:

1. **Set per-product threshold to a very low value** (e.g., 1) — alerts fire only when stock is almost exhausted.
2. **Set per-product `tracking = no`** — the Product is treated as always-in-stock, no threshold applies; this also disables the out-of-stock alert.
3. **Disable `mail_product_quantity_low` globally** on [[settings-admin-notifications]] — affects ALL products, not selective.

There is no per-Product opt-out of the low-stock notification specifically.

### Recipient and delivery

Both `product_quantity_low` and `product_out_of_stock` route to the standard `site_email` (see [[admin-notification-entity-recipient]]) and dispatch through the asynchronous `admin_notify` queue (see [[admin-notification-entity-delivery]]). They do NOT use the `mapping`-based grouping — each Variant trigger creates its own alert row.

## Where it appears

- [[settings-admin-notifications]] — `mail_product_quantity_low` + `mail_product_out_of_stock` toggles.
- [[settings-cart]] → "Order and product quantities" — `product_threshold` store-wide default.
- Product editor on [[products-products]] — per-product `threshold` override field.
- [[products-inventory]] — Variant-level stock management screen (where the merchant inspects stock state after an alert).
- [[products-missing-product]] — back-in-stock subscribers; a Variant that crossed to zero typically also has wishlist demand to satisfy.

## Related

- [[admin-notification]] — hub.
- [[admin-notification-entity-types]] — the two product-driven types in the 17-type catalogue.
- [[admin-notification-entity-master-switch]] — master + per-type gating that suppresses these.
- [[admin-notification-entity-delivery]] — async queue delivery these types use.
- [[inventory-tracking]] — concept hub for stock tracking.
- [[inventory-variant-model]] — per-product `threshold` validation rules.
- [[inventory-decrement-timing]] — when stock decrements (which is when the alert fires).
- [[inventory-restock]] — stock-return rules (re-credits do NOT fire alerts).
- [[inventory-in-stock-badge]] — storefront in-stock / out-of-stock badge logic that pairs with these alerts.
- [[settings-cart]] — `product_threshold` configuration.
- [[products-products]] — per-product `threshold` + `tracking` + `continue_selling` switches.
- [[products-inventory]] — Variant-level stock management.
- [[apps-csv-import]] / [[apps-xml-sync]] — bulk imports that bypass the alert.

## Open Questions

- Whether manual stock edits on [[products-inventory]] trigger the low-stock check, or only order decrements (verify).
- Whether JSON-API v2 writes to `variant.quantity` trigger the alert (verify).
- Whether `product_out_of_stock` and `product_quantity_low` can both fire from the SAME decrement event when stock crosses from above-threshold straight to zero (typical answer: YES, both fire; verify).
