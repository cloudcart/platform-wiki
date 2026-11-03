---
type: feature
nav_path: "Orders → + Add order → Draft state"
route_name: admin.orders.add
route_path: /admin/orders/add
aliases: ["Add order draft state", "Manual order draft", "is_draft is_admin", "Manual order notifications suppressed", "Manual order GeoIP capture", "Manual order locale currency frozen", "Auto shipping provider on manual order"]
tags: [orders, manual, smarty, draft, geoip, notifications]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders-add]]. See the hub for the other aspects (wizard, customer, delivery methods, address handling, validation, no-API rationale).

# Add order — initial draft state

## Purpose

A successful step-1 save on the **+ Add order** panel creates an order in a very specific **draft state** — invisible to the customer, silent on notifications, decrementing no stock, and with a number of side-effects auto-applied (admin GeoIP, locale freeze, tax resolution, auto-attached shipping provider for pickup modes). This page documents exactly what the order looks like the moment after step 1 completes and before the merchant clicks **Create order** in step 2.

## Where to find it

This state is set on the backend during the POST to `/admin/orders/add/save` (the endpoint behind the **Save** / **Next** button — see [[orders-add-validation-save]]). The merchant doesn't configure any of these flags directly; they're hard-coded at save time.

## What the merchant can do here

The merchant cannot configure the draft-state flags through any UI — they're set by the save endpoint as part of step 1. What the merchant can do is **observe** the draft order in [[orders]] (filtered by "Created by admin") and continue editing it on [[orders-details]] in `?preview=true` mode (step 2 of the wizard — see [[orders-add-wizard]]).

## Settings & fields

### Draft order initial values (verified, hard-coded)

| Field | Initial value | Purpose |
|---|---|---|
| `status` | `pending` | Default status of any new order. |
| `status_fulfillment` | `not_fulfilled` | Nothing has shipped. |
| `abandoned` | `0` | Not abandoned (manual order, not a cart). |
| `notify_customer` | `0` | Notifications OFF — no emails. See [[orders-notify-customer]]. |
| Meta `is_draft` | `true` | Marks this as a draft order. Hides from default list views. |
| Meta `is_admin` | `true` | Counts toward [[orders]] filter "Created by admin". |

### Order context fields auto-populated

| Field | Source | Notes |
|---|---|---|
| `customer_id`, `customer_group_id`, `customer_email`, `customer_first_name`, `customer_last_name` | From the selected customer / fallback chain | See [[orders-add-customer]]. |
| `shop_id` | From Stores app selection (when present) | See [[orders-add-delivery-methods]]. |
| `customer_geoip` | MaxMind GeoIP on **admin's** IP | City, state, country, ISO code, timezone, lat/lon. Empty if GeoIP cannot resolve. |
| `customer_ip` | Admin's IP (integer-formatted) | This is why manual orders sometimes show the staff member's office IP in the [[orders-details]] sidebar's IP info card. |
| Locale, currency, unit system | Store defaults at creation time | Frozen on the order — see "Locale + currency frozen" below. |

## Business rules

### Notifications suppressed during draft (verified)

The created order is hard-coded with `notify_customer = 0`. The customer receives **ZERO emails** during the draft phase. The flag is flipped to `1` (notify enabled) only when the merchant clicks **Create order** in step 2 (for offline-payment providers) — see [[orders-notify-customer]]. So the manual-order workflow is silent by default; the customer is only notified when the merchant explicitly commits the draft.

### Stock NOT reserved at draft creation (verified)

Only the bare order shell is created at this step; **no product line items are added**. Stock is decremented only when products are added later through the order-details page's product-add flow ([[orders-products]]) AND only at the configured status transition (per `order_status_for_quantity_decrease` on [[settings-cart]]). So creating a draft does **not** lock inventory away from other customers.

The full timing rules for stock movement are documented on [[inventory-decrement-timing]].

### Customer geolocation auto-captured (admin's IP, not customer's)

On creation the platform looks up the admin's IP via the MaxMind GeoIP service and writes `customer_geoip` (city, state, country, ISO code, timezone, lat/lon) to the order. This is the **ADMIN's** geolocation, NOT the customer's — useful for tracking which physical store / region a manual order was created from. If GeoIP cannot resolve (local IP, MaxMind throttle), the field is left empty.

The platform also stores the admin's IP as an integer-formatted `customer_ip` on the order — which is why a manual order's IP info card sometimes shows the office IP rather than the customer's.

### Locale + currency + unit system frozen from store defaults

When the corresponding fields are empty (typical for a fresh draft), the platform populates locale, currency, and unit system from the store's defaults at draft-creation time. This **freezes** the order's currency at creation — even if the merchant later changes the store's default currency, this order keeps its original one.

The freeze is the same one that applies to storefront-checkout orders; manual orders are not special-cased on this point.

### Auto-attached shipping provider for pickup modes (verified)

For pickup orders (office / locker / marketplace), the platform automatically attaches the matching shipping provider record to the draft on step-1 save. The merchant doesn't pick a courier separately — it's inferred from the office prefix (e.g., `econt-1234` → Econt) or store selection.

For address delivery, **no shipping provider is attached** at this step; the merchant configures shipping later on [[orders-details]] in step 2. See [[orders-add-delivery-methods]].

### Order `side` flag from shipping provider

The order's meta `side` (payer side: sender vs receiver) is auto-set from the attached shipping provider's default config. For address delivery with no provider attached yet, the default is `PAYER_RECEIVER`.

### Tax auto-resolution

After creating the order shell and address, the platform looks up the matching VAT rate based on the address's country (and any geo-zone overrides). If a tax rule matches, it's applied to the order AND `vat_included` is set to `yes` / `no` based on the tax rule's price-inclusive flag.

### Side effects beyond the order record

- **Saved-address creation** for pickup modes — a new entry is appended to the customer's saved-addresses list. See [[orders-add-address-handling]].
- **No** customer record is created at draft save (the customer must exist before step 1).
- **No** webhook fires at draft creation `(verify)`.

## Related

- [[orders-add]] — hub.
- [[orders-add-wizard]] — what happens after the draft state is set (step 2 in `?preview=true`).
- [[orders-add-validation-save]] — what triggers the save and how rollback protects the draft state.
- [[orders-add-delivery-methods]] — which delivery types auto-attach a shipping provider.
- [[orders-add-customer]] — customer fallback chain feeding the draft's customer fields.
- [[orders-details]] — where the merchant clears the draft flag via **Create order** (offline payments only — see [[orders-add-wizard]]).
- [[orders-notify-customer]] — the `notify_customer` flag and when it flips.
- [[orders-products]] — the product-add flow in step 2 that actually creates line items.
- [[inventory-decrement-timing]] — when the eventually-added products decrement stock.
- [[settings-cart]] — `order_status_for_quantity_decrease` setting governing stock timing.
- [[orders]] — "Created by admin" filter that surfaces drafts.

## Open questions

- Whether the admin-only `order.created` webhook fires for the draft itself, or only when the merchant clicks **Create order** in step 2 (verify).
