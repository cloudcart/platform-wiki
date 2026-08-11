---
type: feature
nav_path: "Apps → Glovo"
route_name: apps.glovo.overview
route_path: /admin/shipping/glovo
aliases: ["Glovo", "Glovo delivery", "On-demand delivery"]
tags: [apps, shipping, on-demand, last-mile, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-26
source_count: 8
---
# Glovo (on-demand delivery)

## Purpose

**Glovo** integration — last-mile / on-demand delivery via Glovo's couriers. Different from traditional couriers: Glovo delivers within HOURS (not days). Used by merchants offering same-day or instant delivery — typically restaurants, grocery stores, pharmacies, urgent retail.

The Glovo integration is **per-location**: instead of one set of credentials for the whole store, the merchant configures Glovo separately for EACH physical location (from the Stores app). Each location has its own Glovo API Key + Secret Key, its own pricelist (per-km tariff), and its own working hours.

## Where to find it

Sidebar → Apps → install → **Glovo** OR direct routes. Standard OmniShip sub-pages.

## Prerequisites

🚨 Glovo requires TWO other apps to be installed/configured first:

1. **Stores app** must be installed — Glovo orders are dispatched per physical location (each location = one Glovo store).
2. **Google Maps API key** must be configured ([[settings-general]] section) — used to geocode addresses + calculate distance.

If either is missing, the Glovo settings page shows an inline warning and is non-functional until fixed.

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure Glovo credentials per location (one API Key + Secret per Stores-app location).
- Set per-location pricelist (tariff per-km bracket).
- Configure order-execution mode (auto on new order vs. manual fulfillment).
- View generated waybills / shipments in the Shipments sub-page.

### What the merchant CANNOT do here
- Use Glovo without the Stores app + Google Maps API key.
- Use Glovo for destinations outside the 100-distance-unit radius of any configured store.
- Use Glovo when all in-range stores are closed at the moment of checkout.

## Settings & fields

### Per-location credentials

Each Glovo store (configured under the Stores app) has its own credentials, entered separately:

| Field | Notes |
|-------|-------|
| **Public API Key** (`public_key`) | Public API key for THIS specific Glovo store. |
| **Secret API Key** (`private_key`) | Private API secret for THIS specific Glovo store. |

The merchant adds a location, then opens its Glovo configuration panel (Connect Account modal) and enters that location's keys. Repeat per Glovo store.

### Per-location pricelist

For each store, the merchant defines a per-km pricelist: distance brackets (`from` / `to` km) each mapped to a price. Example: 0-5km = 4.99, 5-10km = 7.99, 10-100km = 9.99. The platform looks up the matching bracket based on the customer's distance from the store at checkout.

### Parent app Additional Settings box (apply to all Glovo stores)

| Field | Effect |
|-------|--------|
| **API Version** (`api_version`) | Select: `v1 (Legacy)` / `v2 (New)` — required. |
| **Enable cash on delivery** (`cd`) | Switch. |
| **Default weight for one item** (`default_weight`) | Number, required. |
| **Order Execution** (`execution_order`) | Select: `On new order` (auto-dispatch to Glovo immediately) OR `Manual order execution` (merchant processes first) — required. |
| **Shipment type** (`contentType`) | Select: `FOOD` / `FOOD WL` / `GENERIC PARCEL`. |
| **Type of vehicle** (`type_vehicle`) | Select: `Any vehicle` / `Car` / `Big car`. |

There is NO "Execution method" toggle, NO "Nearest delivery location" option, and NO "Default Location" dropdown — those concepts are not in the merchant UI. There is also NO global credentials card (credentials are per-location) and NO GeoZones card (Glovo skips the global GeoZones section). The platform automatically picks the closest open Glovo store within 100 distance-units of the customer at quote time.

### Pricing model (storefront price)

Three pricing types only — `calculator`, `calculator_fixed`, `free`. No fixed-price-only or weight-only modes. This matches Glovo's per-distance nature:

- **Fixed price for delivery per km** — uses the per-km pricelist for the matching store.
- **Fixed price per km + processing fee** — per-km pricelist plus a flat merchant surcharge.
- **Fixed price per km + free shipping** — per-km pricelist BUT zeroed for the customer (merchant absorbs).

### Per-location modals (Stores table)

The Stores sub-page lists every Glovo-enabled location. Each row shows the title + address plus configuration-error badges ("No shop address entered", "No shop work time entered", "No location price list entered", "No credentials is entered") and an Active/Inactive toggle that is **blocked while any error exists** — a location that loses required configuration auto-deactivates. Three action buttons per row open side-modals:

- **Connect Account modal** ("Connect with Glovo! ON DEMAND") — the per-location Public API Key + Secret API Key fields (see credentials table above). Saving clears the "No credentials is entered" badge.
- **Price List modal** — the per-km distance rows (`from` km / `to` km / `price`). Validation: "Field is required", "You have not entered delivery prices for all selected distances", and an overlap check `{from_one} is in range {from_second} and {to_one} for row {row}`.
- **Location Details modal** — store display name + URL handle (slug at `/store/<handle>`), full address fields, per-day **Working Hours** (active toggle + open/close pickers, used to gate availability at checkout), Email + Phone contacts (format-validated), and SEO title/description that cascade into the storefront.

## Business rules

### Hourly delivery vs daily

Glovo's value: same-day / within-hours delivery. Limited to specific cities where Glovo operates. Quote → waybill → tracking follows the standard OmniShip pattern via [[orders-shipping-waybill]].

### Address-only

Supported delivery channel is `['address']` — Glovo is door-to-door only (no locker / office channels).

### Auto-routes to closest in-range open store

At quote time the platform measures the distance from the customer's address to every configured Glovo store, filters to those within the **100-distance-unit cap** that are **currently open**, and exposes the closest one as the quote. This answers the range question: if the customer is outside every location's radius — or every in-range store is closed at that moment — Glovo simply does not appear at checkout. Availability therefore depends on **real-time store hours** (configured per-location in the Stores app), not just geography. There is no merchant-facing toggle controlling this routing.

### COD supported with cap

COD is offered when the merchant's COD switch is on AND the order is within the COD cap (10000 BGN for BGN stores).

### Closed-store / invalid-credentials handling

When the platform tries to dispatch but the chosen store is closed at that moment, the order history gets a `glovo_store_is_closed` message and dispatch is skipped. If the store's credentials are invalid, the history gets `glovo_invlid_credentials` and dispatch is skipped. The merchant must intervene manually in both cases.

### Tracking URL fallback

The waybill response uses Glovo's tracking URL by default; when the backend `tracking` setting equals `cloudcart`, the response uses CloudCart's `/tracking/{waybill_id}` page instead. This setting is NOT exposed in the merchant Settings UI — it is a backend-only value.

## Per-channel delivery pricing

Glovo delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Glovo quote; **no extra field** of its own.
- `calculator_fixed` — the Glovo quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the Glovo quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price. **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-stores]] — Stores app (REQUIRED prerequisite).
- [[settings-general]] — Google Maps API key setting (REQUIRED prerequisite).
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[shipping-provider-mechanism]] — common shipping pattern.

## Open questions

_None — all questions answered above._
