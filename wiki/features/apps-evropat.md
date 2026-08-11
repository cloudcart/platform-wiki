---
type: feature
nav_path: "Apps → Evropat"
route_name: apps.evropat.overview
route_path: /admin/shipping/evropat
aliases: ["Evropat", "Evropat courier"]
tags: [apps, shipping, courier, bulgaria, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 5
---
# Evropat

## Purpose

**Evropat** courier integration. Single-key API authentication.

## Where to find it

Sidebar → Apps → install → **Evropat** OR direct routes. Standard OmniShip sub-pages.

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials in the Settings sub-page.
- View generated waybills / shipments in the Shipments sub-page.
- Manage returns in the Shipments return sub-page.
- See real-time quotes at checkout once credentials are validated.

### What the merchant CANNOT do here
- Use the integration without an active courier contract + valid API credentials.
- Generate waybills for destinations the courier does not serve.

## Settings & fields

Single credential: **API key**.

## Business rules

Same simple key-only auth as [[apps-berry]]. Standard OmniShip flow.

## How it works (verified against backend)

### Coverage country
**Bulgaria.** The integration's fallback allowed-countries list is `['BG']`, and the courier's offices are populated through CloudCart's Bulgarian shipping office database.

### Calculator modes (storefront price options)
At checkout, the merchant can choose how delivery price is computed:
- **Evropat calculator** — real-time price quoted from Evropat's API.
- **Evropat calculator + processing fee** — courier quote plus a fixed merchant surcharge.
- **Evropat calculator + free shipping** — courier quote that the merchant covers; storefront shows free shipping.
- **Fixed value at price without Evropat calculator** — flat price per cart-value tier.
- **Fixed weight value without Evropat calculator** — flat price per weight tier.
- **Fixed value for price and weight without Evropat calculator** — combined flat rules.

### Settings the merchant configures
- **Sending method**: Send from office / Send from address.
- **Default package dimensions**: length, height, width in cm — used when products don't have measurements.
- **Verification with ID card** — optional age / identity check on delivery.
- **Notify the recipient via SMS / Viber** — toggle.
- **Fragile shipment** flag per waybill.
- **Back documents** — accompanying documents that need to come back signed.
- **Open before paying** — only available when the SENDER (merchant) pays for the shipment; if the recipient pays, the option is greyed out.

### Capabilities at checkout / order
Once credentials are validated, the storefront fetches real-time delivery quotes during checkout, and the merchant can generate waybills + Evropat-side tracking from each order.

## Per-channel delivery pricing

Evropat delivers to **address** and to **office** — each of its **2** delivery channels (to **address** and to **office**) is a separate rate card with its own enable toggle (`to_address` / `to_office`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time Evropat quote; **no extra field** of its own.
- `calculator_fixed` — the Evropat quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the Evropat quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.

## Sub-pages (modern Vue)

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.evropat.overview` | `/admin/shipping/evropat/` |
| Settings | `apps.evropat.settings` | `/admin/shipping/evropat/settings` |
| **Addresses** | `apps.evropat.addresses` | `/admin/shipping/evropat/addresses` |
| Shipments | `apps.evropat.shipments` | `/admin/shipping/evropat/shipments` |
| Shipments return | `apps.evropat.shipments-return` | `/admin/shipping/evropat/shipments-return` |

Like Econt, Evropat exposes an **Addresses** tab — sender address book. Only visible when credentials are validated.

## Settings tab — full layout (deep audit 2026-05-27)

### 1. Credentials box (custom `CourierCredentialsSection.vue`)
Single field:
- **API key** (`api_key`) — required. Placeholder: "Enter your API key".

On invalid: shows "API key is not valid" inline. Connect button until validated.

### 2. Name & logo (Visualization)

### 3. Sender data box — slide-down editor (`SenderDataSection.vue`)
- **Main address** (`address_id`) — async-search select against `/admin/api/evropat/addresses`. Required. Lists the addresses configured in the Addresses tab.

The merchant picks the PRIMARY sender address here; per-order overrides happen at waybill time.

Pickup keys: `address_id`.

### 4. Services / 5. Per-channel rate cards
Standard per-channel rate cards (address + office channels).

### 6. Geo zones / 7. Payment providers — standard.

### 8. Additional settings — two boxes (backend-driven)

#### Box 1 — `general_settings`
- **Payer of the courier service upon return** (`return_shipment`) — radio (sender / receiver / other).
- **Default weight for one item** (`default_weight`).
- **Default width / length / height** (mm).
- **Choose a content description** (`order_content`).

#### Box 2 — `parcel_and_waybill_settings`
- **Who pay the shipping cost** (`side`) — radio.
- **Enable cash on delivery** (`cd`) — switch.
- **Enable pos terminal payment for cash on delivery** (`allowPosTerminalPayment`) — switch; depends on `cd = 1`.
- **Payment of cash on delivery** (`cod_pay`) — select: `cash` (Cash) | `client_number` (By client number). Depends on `cd = 1`.
- **Client number** (`client_number`) — string; depends on `cod_pay = client_number`.
- **Insurance** (`insurance`) — switch.
- **Select a document that declares the value shipment value** (`insurance_document`) — select; depends on `insurance = 1`. Options: Invoice (only when store has invoicing enabled) / Receipt.
- **Money transfer** (`money_transfer`) — switch.
- **Verification with ID card** (`verification`) — switch.
- **View** (`allowShipmentCheck`) — switch (allow recipient to inspect package).
- **Notify the recipient via SMS / VIBER** (`notification`) — switch.
- **Fragile shipment** (`breakable`) — switch.
- **Back documents** (`returnReceipt`) — switch.
- **Accompanying documents** (`accompanyingDocuments`) — switch.

### 9. Submit-changes sticky footer.

## Addresses tab — full layout (`Addresses.vue` + `AddAddress.vue`)

Manages saved sender addresses (multi-warehouse / multi-pickup-point).

### List table
Columns: **Address name** (clickable, opens edit modal via `AddressName.vue`), **Primary Address** (Yes/No), **Actions** (trash).

The empty state (`#noResult` slot) renders the same **+ Add address** button.

### Add address modal (`AddAddress.vue`)
Triggered by **+ Add address** button. Right-side slide-in modal (size lg). Header: title + Cancel + Save.

Fields:
- **Address name** (`address.name`) — required.
- **Pickup** radio (`address.address.type`):
  - **Send from office**
  - **Send from address**
- **First and last name** (`address.address.name`) — required.
- **Company name** (`address.address.company`) — optional.
- **Phone number** (`address.address.phone`) — phone input, required.
- When pickup = office:
  - **Office** (`address.address.office`) — async-search select against `/admin/api/evropat/offices`. Required.
- When pickup = address:
  - **Select city** (`address.address.city`) — async-search select against `/admin/api/evropat/cities`. Required.
  - **Enter an address** (`address.address.address`) — text input. Required.

POST to Evropat's address endpoint on Save; success toast "Saved successfully".

## Shipments / Shipments return tabs
Shared `Shipments.vue` shipping table. Bulk-print → `PrintFormatSelectModal` (A4 / A6).

## Overview tab — standard.

## No Payments tab
Evropat's Vue router does NOT mount a Payments sub-page. The five mounted sub-pages are Overview, Settings, Addresses, Shipments, Shipments-return.

## Open questions

_None — all questions answered above._
