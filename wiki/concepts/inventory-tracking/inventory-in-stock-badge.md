---
type: concept
nav_path: "Concept → Inventory tracking → In-stock badge + low-stock alerts"
aliases: ["In-stock badge logic", "Out-of-stock badge logic", "Notify me when in stock", "Low-stock email", "product_quantity_low", "product_out_of_stock", "Storefront stock display", "Minimum order quantity"]
tags: [catalog, inventory, stock, storefront, notifications, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[inventory-tracking]]. See the hub for the other aspects (variant model, decrement timing, restock, oversell, bundle stock, multi-warehouse, debugging playbook).

# Inventory — in-stock badge + low-stock alerts

## Definition

This aspect covers two related storefront / notification surfaces driven by Variant `quantity`:

1. **The in-stock badge** — what the storefront shows for each Variant: "In stock" / "Out of stock" / "Notify me when in stock" / a custom label.
2. **The low-stock + out-of-stock admin email alerts** — the `product_quantity_low` and `product_out_of_stock` notifications sent to the merchant when a Variant drops below the threshold or hits zero.

Both depend on the three master switches from [[inventory-variant-model]] (`tracking`, `continue_selling`, `threshold`) plus the storefront's per-Variant `quantity`. The storefront's in-stock check also considers `minimum` (minimum order quantity) — a Variant with positive stock can still be unsellable if stock < minimum.

## Scope

Covered:

- The 3-rule in-stock decision per Variant.
- Multi-Variant card aggregation on category / search results.
- The two related alert notifications + their gating.
- The threshold inclusivity rule (`>=` triggers the email).
- The `minimum` order quantity rule that blocks Add-to-cart even when stock is positive.
- `quantity = NULL` (unlimited stock) behaviour.

Not covered here:

- The master switches themselves — see [[inventory-variant-model]].
- Bundle in-stock derivation — see [[inventory-bundle-stock]].
- Back-in-stock subscriber queue — see [[products-missing-product]].
- Custom in-stock / out-of-stock label management — see [[products-statuses]].

## Contrasts

- **In-stock badge vs sellable check** — most badges only reflect whether Add-to-cart is enabled. But CloudCart's `enable_sell` flag also factors in `minimum` — a Variant with positive `quantity` below `minimum` shows out-of-stock + greyed Add-to-cart even though stock is technically present.
- **Threshold inclusive (`>=`) vs strict (`>`)** — the low-stock alert fires when `threshold >= quantity AND quantity > 0`. So setting threshold = 5 fires alerts at quantity 5, 4, 3, 2, 1 — but NOT at 0 (that's a separate `product_out_of_stock` alert).
- **`quantity = NULL` vs `quantity = 0`** — NULL means unlimited; the storefront treats it as always in-stock regardless of `tracking`. `quantity = 0` is a real "out of stock" state (sellable only if `continue_selling = yes`).

## Where it applies

### The in-stock decision (per Variant)

The storefront decides what to render for each Variant per these three rules:

1. **If `tracking = no`** (master OFF) → **ALWAYS in stock**. The storefront shows the merchant's in-stock label (defaults to "In stock", customisable per Variant via `status_id` foreign key to [[product-status]]). The Variant's `quantity` is irrelevant.
2. **If `tracking = yes` AND (`quantity > 0` OR `continue_selling = yes` OR `quantity IS NULL`)** → **in stock**. Storefront uses the in-stock label.
3. **If `tracking = yes` AND `quantity <= 0` AND `continue_selling = no`** → **out of stock**. Storefront uses the out-of-stock label (defaults to "Out of stock", customisable per Variant via `out_of_stock_id` to [[product-status]]). The "Notify me when in stock" button appears here if the product's status enables it — see [[products-missing-product]].

So a Variant with `quantity = 0` and `continue_selling = yes` shows in-stock. A Variant with `quantity = 5` and `tracking = no` also shows in-stock (the count is ignored). The `quantity` field itself never goes negative — the platform clamps on every decrement per [[inventory-oversell]].

### Multi-Variant card aggregation

For multi-Variant products on category pages / search results, the storefront aggregates per-Variant in-stock states into a single card-level state:

- **At least one Variant in-stock** → the card shows in-stock. The Variant picker on the product detail page greys out the unavailable Variant options.
- **All Variants out-of-stock** → the card shows out-of-stock. The picker is greyed entirely.

### `minimum` order quantity blocks Add-to-cart even when stock > 0

The `enable_sell` flag on each Variant is computed live as:

- `tracking = no` → `enable_sell = true` (always sellable).
- `tracking = yes` AND `continue_selling = yes` → `enable_sell = true` (oversell active).
- `tracking = yes` AND `quantity IS NULL` → `enable_sell = true` (NULL = unlimited).
- Otherwise → `enable_sell = (quantity >= minimum)`.

**Practical consequence**: a Variant with `quantity = 3` and `minimum = 5` (minimum order quantity) is **unsellable** — the storefront greys out Add-to-cart even though there are 3 units in stock. The out-of-stock label appears in this scenario despite the positive count. The merchant has to either raise quantity above the minimum or lower the minimum.

### The low-stock email — `product_quantity_low`

When a Variant's `quantity` drops below the configured threshold (per-product `threshold` overrides the store-wide `product_threshold` from [[settings-cart]]), the platform queues the `product_quantity_low` admin email. Three gates must ALL be ON for the email to actually send:

1. **The Variant drops to or below the threshold** AND `quantity > 0` (at exactly 0, the `product_out_of_stock` template fires instead). The threshold check is **inclusive** — `threshold = 5` fires at quantities 5, 4, 3, 2, 1.
2. **`mail_product_quantity_low = yes`** (per-notification toggle on [[settings-admin-notifications]]).
3. **`administrator_email_notifications = yes`** (master switch on [[settings-admin-notifications]]).

Recipient: the store's `site_email` from [[settings-general]], or a per-notification override on [[settings-admin-notifications]].

### The out-of-stock email — `product_out_of_stock`

A separate template fires when `quantity` lands exactly at `0`. Gated similarly by `mail_product_out_of_stock` toggle + the master switch. Don't confuse with the low-stock template — they're different emails for different thresholds.

### When the alert fires — order-decrement code path only

The low-stock + out-of-stock checks fire on **order placement / decrement** specifically, NOT on every Variant save. So:

- **Bulk imports** ([[apps-csv-import]] / [[apps-xml-sync]] / ERP imports) update `Variant.quantity` directly without firing the alert. The merchant does NOT receive a flood of emails on bulk imports. (CSV / XML import write directly via `updateColumns`, which bypasses the order pipeline.)
- **Manual edits** in the product editor or on [[products-inventory]] also do NOT fire the alert.
- **Order-edit on [[orders-details]]** — increasing a line quantity on an existing order DOES trigger the threshold check (via `quantityIncrementDecrementProductEdit`). So this is the only admin-side path that can fire low-stock alerts.

### Threshold validation rejects `0`

The `threshold` field on the product editor rejects `0` directly — the `intval` cast of `0` is treated as "missing", returning *"threshold has invalid value"*. To effectively disable low-stock alerts for a product, either leave the per-product threshold blank (falls back to store-wide `product_threshold`) or turn off `mail_product_quantity_low` globally on [[settings-admin-notifications]].

The threshold field is also rejected when `tracking = no` is set — *"product cannot have threshold if not tracked"*.

## Related

- [[inventory-tracking]] — hub.
- [[inventory-variant-model]] — the three master switches that drive the badge logic.
- [[inventory-oversell]] — `continue_selling` keeps a 0-stock Variant showing in-stock.
- [[inventory-bundle-stock]] — bundle card aggregation (different rules — see that page).
- [[product-status]] — custom in-stock / out-of-stock label catalogue.
- [[products-statuses]] — merchant manages custom status labels here.
- [[products-missing-product]] — back-in-stock subscriber queue triggered by the "Notify me" button on out-of-stock Variants.
- [[settings-cart]] — store-wide `product_threshold`.
- [[settings-admin-notifications]] — `mail_product_quantity_low` + `mail_product_out_of_stock` toggles + `administrator_email_notifications` master.
- [[settings-general]] — `site_email` as default low-stock recipient.
- [[orders-details]] — order-edit quantity changes trigger the threshold check.
- [[apps-csv-import]] / [[apps-xml-sync]] — bulk paths that bypass the alert.

## Open Questions

None.
