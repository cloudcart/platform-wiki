---
type: feature
nav_path: "Apps → GLS"
route_name: apps.gls.overview
route_path: /admin/shipping/gls
aliases: ["GLS", "General Logistics Systems", "GLS Europe", "GLS courier"]
tags: [apps, shipping, courier, europe, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-26
source_count: 4
---
# GLS (European courier)

## Purpose

**GLS (General Logistics Systems)** integration — a pan-European parcel network. CloudCart's GLS app handles real-time quotes, waybill generation, GLS ParcelShop pickup-point selection, and cross-border shipments. GLS's strength is **international parcel delivery** between European countries — useful for merchants who ship across the EU.

Each merchant configures GLS for ONE country (their contract country) but can ship FROM that country to ANY European GLS-served destination.

## Where to find it

Sidebar → Apps → install → **GLS**, or direct routes. GLS exposes only TWO sub-pages — the leanest router among the shipping providers:

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.gls.overview` | `/admin/shipping/gls/` |
| Settings | `apps.gls.settings` | `/admin/shipping/gls/settings` |

No Payments, Shipments, or Shipments-return tab — sender / fulfilment work happens in the shared [[orders]] + Shipments screens, not under the GLS app.

## What the merchant can do here

Configure credentials + country endpoint, set the sender address, define rate cards, and toggle GLS add-on services (see Settings & fields). Allowed delivery methods:

- **To address** — home / office delivery (the only supported channel).
- **To ParcelShop** — GLS's pickup-point network (small shops, gas stations); customer picks one at checkout.

What the merchant **cannot** do here: use GLS without a registered courier contract; generate waybills outside GLS-served countries; bypass Test mode if credentials are sandbox-tier.

## Settings & fields

### Credentials box (`CourierCredentialsSection.vue`)

FIVE fields — the most complex among the simple-credential couriers. All five are `credentials-keys` (read-only display after Save until the pencil re-opens them); a failure shows "Invalid credentials" on every field.

| Field (key) | Notes |
|-------|-------|
| **GLS Username** (`username`) | basic auth; required. |
| **GLS Password** (`password`) | masked (type=password); required. |
| **GLS Client ID** (`client_id`) | GLS account ID; required. |
| **Select country** (`endpoint_id`) | searchable select, required — picks the country-specific GLS API endpoint. See list below. |
| **Mode** (`test_mode`) | select: `test` \| `production`. First-class persisted credential — the merchant explicitly sets it. |

The `endpoint_id` is a number 1–7, each mapping to a GLS country office. Offices differ in pricing, service tiers, surcharges, and add-ons:

1. Croatia (HR) · 2. Czechia (CZ) · 3. Hungary (HU) · 4. Romania (RO) · 5. Slovenia (SI) · 6. Slovakia (SK) · 7. Serbia (RS)

### Sender data box — slide-down editor (`SenderDataSection.vue`)

TEN fields (all part of `pickup-keys.settingsKeys`), in two groups split by an `<hr>`:

**Address:** `sender_country` (required, can't be cleared), `sender_city`, `sender_zip_code`, `sender_street`, `sender_street_number` (all required), `sender_addition_info` (optional).

**Contact:** `sender_name` (sender / company name), `sender_contact_name`, `sender_phone` (phone input), `sender_email` — all required except phone.

### Rate cards

GLS supports the **address** channel only — a single card. Pricing types are limited to `fixed_price`, `fixed_weight`, `price_and_weight` — NO calculator-based / live quoting on this endpoint. The merchant must define their own price-per-weight table. GLS exposes no multi-service tags (services list is empty).

### Additional settings — `parcel_and_waybill_settings` (one box, backend-driven)

Switches: **Enable cash on delivery** (`cd`), **24-hour guaranteed delivery** (`24h`), **Insurance** (`ins`), **Declared parcel value** (`dpv`), **Delivery after recipient verification / signature** (`aos`), **Recipient phone notification** (`cs1`), **Recipient notification and delivery choice** (`fds`), **Recipient SMS notification and delivery choice** (`fss`), **Pickup from sender's address** (`pss`), **CO₂ compensation** (`tgs`, GLS "ClimateProtect").

**Select print format** (`printer_layout`) — select with four options: **A4 2x2**, **A4 4x1**, **Thermo**, **Connect**. This drives GLS bulk label printing on the standard order-fulfilment flow.

Standard boxes also present: Name & logo (Visualization), Geo zones, Payment providers, and a submit-changes sticky footer.

## Business rules

### Cross-border deliveries are GLS's specialty

When the destination country differs from the merchant's, GLS routes internally — the platform passes the destination address to GLS's quote API, which returns cross-border pricing.

### Open international — no hardcoded country list

GLS is the only courier with an EMPTY `fallback_allowed_countries` list, reflecting its pan-European nature. The merchant's GLS contract determines which countries they can ship to/from. Supported delivery channels are `['address']` only (door-to-door), unlike DPD's three-channel support.

### COD supported

`supportsCashOnDelivery = true` when the `cd` setting is on AND the order is within the COD cap (10000 BGN for BGN stores; for other currencies GLS server-side limits apply). Synced via [[orders-sync-cod]]. Per the OmniShip family pattern, switching payment method on an order recalculates shipping when COD is supported.

### Test mode → sandbox URL

`test_mode` is a distinct boolean credential. Picking `Test` switches the API base URL from `api.mygls.<country>` to `api.test.mygls.<country>`; all quotes + waybills hit the sandbox, so no real shipping volume is generated. Pick `Production` to go live.

### One contract per install

The integration stores one credential set + one country endpoint. A merchant with multiple GLS contracts (e.g. Hungarian + Romanian) needs separate stores or manual credential switching — there is no per-shipment endpoint switching.

### Where waybills appear

Generated waybills appear in the global [[orders]] list filtered by shipping provider, not under the GLS app (no Shipments tab). Bulk label printing is driven by the `printer_layout` setting.

## Per-channel delivery pricing

GLS delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

Each `fixed_*` type's table **is** the price (there is no live calculator on GLS, so no fallback). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[apps-dpdbulgaria-speedy]] / [[apps-dpdromania]] — alternative European couriers.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] — Bulgaria-focused alternatives.
- [[orders-shipping-waybill]] — waybill flow.
- [[orders-sync-cod]] — COD sync.

## Open questions
