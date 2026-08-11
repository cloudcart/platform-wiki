---
type: feature
nav_path: "Apps → Sameday"
route_name: apps.sameday.overview
route_path: /admin/shipping/sameday
aliases: ["Sameday", "Sameday Courier", "Sameday Romania", "Sameday EasyBox"]
tags: [apps, shipping, courier, romania, bulgaria, locker, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 4
---
# Sameday (Romanian / Bulgarian courier)

## Purpose

**Sameday** integration — Romania's dominant courier service, also serving Bulgaria. Sameday offers three delivery channels: **traditional courier delivery** (to home / office), **office pickup**, AND **EasyBox lockers** (self-service pickup network). The app provides real-time quotes, waybill generation, sender configuration, and EasyBox locker selection at checkout. It is the most flexible of the Romanian couriers ([[apps-cargus]] is address-only; [[apps-boxnow]] is locker-only).

For Romanian merchants this is typically the primary courier; Bulgarian merchants use it as an alternative to Econt / Speedy / Boxnow.

## Where to find it

Sidebar → Apps → install → **Sameday** OR direct routes. Sameday exposes FOUR sub-pages — note there is **no Payments tab** (different from Econt / DPD); pair-with-payment-provider configuration lives only inside Settings.

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.sameday.overview` | `/admin/shipping/sameday/` |
| Settings | `apps.sameday.settings` | `/admin/shipping/sameday/settings` |
| Shipments | `apps.sameday.shipments` | `/admin/shipping/sameday/shipments` |
| Shipments return | `apps.sameday.shipments-return` | `/admin/shipping/sameday/shipments-return` |

Shipments and Shipments-return share one screen; bulk-print offers A4/A6 format select.

## What the merchant can do here

- Enter Sameday API credentials and pick the country instance (Settings).
- Enable one or more delivery channels: **To address**, **To EasyBox locker**, **To office**.
- Configure package defaults, COD, insurance, and return-waybill behaviour.
- Generate outbound and return waybills; bulk-print labels.

**What the merchant CANNOT do here:**
- Use a single Sameday account across multiple countries simultaneously — each country (RO, BG) needs its own credentials/contract; configure one country per install.
- Select a country other than Bulgaria or Romania — Hungary and other Sameday markets are not exposed.
- Generate waybills outside Sameday's served countries.

## Settings & fields

### Credentials box (`CourierCredentialsSection.vue`)
- **Username** (`username`) — Sameday API username; required.
- **Password** (`password`) — masked; required.
- **Country** (`country`) — select with TWO options: `Bulgaria (bg)` | `Romania (ro)`.

Username + password OBTAIN a bearer token from Sameday on first sign-in; the token is cached with an expiry and refreshed automatically — the merchant never manages it. A "Connect" button shows until validated; invalid credentials surface inline "Invalid credentials" on all three fields. The country picker drives the API endpoint, the service-tier list, the locker network (RO has the largest EasyBox network), and the quote currency (RON for RO, BGN for BG).

### Services / rate cards
The standard Services tags box is conditionally HIDDEN for Sameday — service tiers are managed per-channel inside the calculator instead. Each channel (address / office / locker) has its own rate card opened via the pencil. A Sameday-specific extra, **Type of services** (`allowed_methods_{channel}`), is a multi-tag select against `/admin/api/sameday/services?type={channel}` that picks which service tiers (e.g., NextDay / SameDay / 2H Express) offer that channel. Free-shipping service follow-ups (city / intercity) are available.

Geo zones and Payment providers boxes are standard. Name & logo (Visualization) is standard. Sameday's Vue defines no custom sender editor — the sender is chosen via `default_address` below.

### Additional settings — Box 1 (`general_settings`)
- **Default weight for one item** (`default_weight`) — required (100g default per item when unspecified).
- **Default width / length / height** (mm) — 10cm × 10cm × 10cm default per item.
- **Submit product sizes** (`item_sizes`) — switch. When OFF, all items ship as ONE package with default dimensions; when ON, each cart item ships as a separate package with its own dimensions, so Sameday calculates volumetric weight per package.
- **Choose a sender address** (`default_address`) — select; only populated while a session is active, lists sender addresses returned by Sameday's API.
- **Package Type** (`package_type`) — Package / Small Package / Big Package (numeric IDs 0/1/2).
- **Default number of packages to deliver to an address** (`package_address`) — number; depends on `item_sizes = 0`.
- **Default number of packets to deliver to a locker** (`package_locker`) — number; depends on `item_sizes = 0`.
- **Choose a content description** (`content`) — Product name / SKU / barcode / Order number (Sameday adds "Order number", not present on other couriers).

### Additional settings — Box 2 (`parcel_and_waybill_settings`)
- **Enable cash on delivery** (`cd`) — switch.
- **Insurance** (`insurance`) — switch.
- **Open before payment** (`open_before_test`) — switch; help-text: *"This option can only be used for delivery to an address."*
- **Create return waybill** (`return_waybill`) — switch. The four fields below all depend on `return_waybill = 1`:
  - **Add cash on delivery to return waybill** (`return_waybill_cod`) — switch.
  - **Add insurance to return waybill** (`return_waybill_insurance`) — switch.
  - **Select return service** (`return_waybill_service`) — select against `/admin/api/sameday/services`.
  - **How many days return waybill is valid** (`return_waybill_days`) — number, 1–365.

Defaults out of the box: sender pays; address channel on; Sameday-calculator (real-time API quote) pricing.

## Business rules

- **EasyBox is Sameday's locker network.** Dominant in Romania. When enabled, customers pick a specific locker at checkout — same UX as [[apps-boxnow]], but as ONE of multiple Sameday options rather than locker-only.
- **"Open before paying" requires sender-pays.** Per the help text: *"The option Open before paying can only be used if the payer of the shipment is the SENDER."* On receiver-pays COD it is silently disabled regardless of the toggle.
- **COD supported per country**, synced via [[orders-sync-cod]]. The platform caps COD at 10000 BGN per order **only when the store currency is the literal `BGN`** (legacy; or the merchant's lower COD-max). For any other currency — including `EUR` (the new Bulgarian norm) and RON — there is no platform-side cap; Sameday's server-side limits apply.
- **Currency follows the recipient address.** Quotes and waybill amounts (subtotal, COD, item prices) convert from store currency to the destination-country currency: RO → RON, BG → BGN. The merchant doesn't pick it. When the customer switches payment method (e.g. COD → online), shipping recalculates and Sameday's COD fee disappears.
- **Cross-border RO↔BG** is handled under contract — the platform calls Sameday's quote API with the destination country; if covered, a quote returns, otherwise the merchant uses another courier.
- **Sandbox mode by default.** The integration runs against Sameday's sandbox API (test-mode is set permanently true in the codebase). There is **no merchant-facing toggle** to switch to production; that requires a code-level change. A separate debug-waybill mode returns a mock waybill without committing to Sameday — useful for testing before going live. *(verify whether production cutover is still code-gated)*
- **Side effects** follow the common OmniShip pattern — see [[shipping-provider-mechanism]].

## Per-channel delivery pricing

Sameday delivers to **address**, to **office** and to **locker** — each of its **3** delivery channels (to **address**, to **office** and to **locker**) is a separate rate card with its own enable toggle (`to_address` / `to_office` / `to_locker`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Sameday quote; **no extra field** of its own.
- `calculator_fixed` — the Sameday quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the Sameday quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote. It also adds **Free Delivery Service within the City** and **Intercity** selects that pick which Sameday service fulfils the free leg.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-cargus]] — sister Romanian courier (often installed alongside; address-only).
- [[apps-boxnow]] — sister locker provider (locker-only; Sameday EasyBox is one option among many).
- [[shipping]] — shipping providers landing.
- [[orders-shipping-waybill]] — waybill generation flow.
- [[orders-sync-cod]] — COD payment sync.
- [[settings-payment-providers]] — COD configuration.
- [[shipping-provider-mechanism]] — common shipping (OmniShip) pattern.

## Open questions

_None — pending the production-mode `(verify)` noted under Business rules._
