---
type: feature
nav_path: "Apps → Sendcloud"
route_name: apps.sendcloud.overview
route_path: /admin/shipping/sendcloud
aliases: ["Sendcloud", "Send cloud", "Shipping aggregator", "Multi-carrier shipping", "no enable disable button", "app has no active toggle"]
tags: [apps, shipping, aggregator, multi-carrier, europe, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 7
---
# Sendcloud (shipping aggregator)

## Purpose

**Sendcloud** is a **shipping aggregator** (not a single courier) that lets the merchant reach MULTIPLE European couriers (DHL, DPD, UPS, PostNL, GLS, Colissimo, Bpost, etc.) through ONE Sendcloud account + contract. Instead of negotiating with each courier separately, the merchant gets one bill from Sendcloud (which negotiates aggregated rates) and picks any courier at shipment time. Ideal for cross-border merchants without enough volume to contract couriers directly.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> Activation here is **per courier**, not per app: each installed courier has its own Enable / Disable button in the top-right toolbar of its own settings page (`/admin/shipping/sendcloud/external/:id`).

## Where to find it

Sidebar → Apps → install → **Sendcloud**. Standard OmniShip sub-pages: parent Settings (`apps.sendcloud.settings`), per-courier settings (`apps.sendcloud.external/:id`), Shipments, Shipments return.

## What the merchant can do here

- Install / uninstall the integration (there is no app-level activate / deactivate — see the note above).
- Connect Sendcloud credentials on the Settings page.
- Install each available courier individually as its own shipping option.
- See real-time quotes at checkout once connected.
- View generated waybills in the Shipments sub-page; manage returns in Shipments return.

### What the merchant CANNOT do here
- Use the integration without an active courier contract + valid Sendcloud connection.
- Type the API keys directly — they arrive only via the Sendcloud-hosted Connect flow.
- Control which couriers appear in the list (driven by the Sendcloud contract).
- Generate waybills for destinations the chosen courier does not serve.

## Settings & fields

### Parent Settings page — Connect to Sendcloud

The merchant does NOT paste credentials. Clicking **Connect** redirects to `panel.sendcloud.sc/shops/cloudcart/connect/...`, where Sendcloud authorises CloudCart and posts the credentials back. After connecting, the page shows two read-only display fields — **Public key** (`public_key`) and **Secret key** (`secret_key`) — both always disabled (the merchant cannot type them). The platform also stores an `integration_id` received in the same callback, but it is never displayed or editable. Before connecting, a yellow info box reads "Once you connect to SendCloud, your public and private key will be automatically populated." A red **Disconnect** button clears the keys and drops the connection.

### Available couriers — per-merchant, CONTRACT-DEPENDENT

Once connected, the platform queries Sendcloud and syncs the couriers available to THIS merchant based on their Sendcloud contract. Different merchants see different couriers. The list (loaded from `/admin/api/sendcloud/couriers`) appears as a Shipping methods table; each row is one sub-courier with an **Install** button (or, once installed, a link to its detail page + a **Settings** button to the per-courier page). Empty state: "Currently no couriers installed".

### Per-courier installation

Each courier installs separately. Installing one (POST `/admin/api/sendcloud/install-shipping`, toast "Installation successful"):

1. Creates a separate shipping provider in CloudCart with its own identifier.
2. Adds the courier to the merchant's Suppliers list.
3. Replaces Install with a **Settings** button opening the per-courier page (`apps.sendcloud.external`).
4. Makes the courier its own checkout option (e.g., "DPD Standard", "DHL Express", "PostNL Service Point").

### Per-courier settings (one shipping provider each)

The parent page holds NO per-courier fields — only the Connect card + the courier picker. Each installed courier's External page exposes the standard shipping-provider settings independently (values do NOT cascade from the parent):

- **Visualization** — name + logo upload + show-in-store toggle.
- **Pickup (Sender address)** — `sender_id` picker sourced from `/admin/api/sendcloud/sender-addresses`.
- **Return address** — return-address fields (`return_address.from_name`, etc.).
- **Company / Service** — one service card per supported channel (see "Office / service-point support" below).
- **Geo Zones** — geo-zone allow-list. **Payment providers** — payment-method allow-list.
- **Additional Settings** — two boxes:
  - `general_settings`: **Default weight** (`default_weight`, kg) + **width/length/height** (`default_width`, `default_length`, `default_height`, all mm).
  - `parcel_and_waybill_settings`: **Enable cash on delivery** (`cod`) switch + **Insurance** (`insurance`) switch.

Status toggle (Enable / Disable) sits in the top-right toolbar; the submit bar POSTs to `/admin/api/sendcloud/settings/:id`.

### Pricing models per installed courier

A pricing-mode picker (the same 6 modes as the rest of the OmniShip family, mirroring EuShipment) is available per courier, with rate rows, allowed services, countries and categories:

- **calculator** — live API quote from Sendcloud (aggregated prices).
- **calculator_fixed** — live quote + fixed processing fee added by the merchant.
- **free** — quote zeroed for the customer (merchant absorbs cost).
- **fixed_price** — flat tier per order subtotal.
- **fixed_weight** — flat tier per package weight.
- **price_and_weight** — combined matrix.

## Business rules

### Aggregator model (verified)

Sendcloud sits BETWEEN CloudCart and the underlying courier. On a quote request, Sendcloud returns options from multiple couriers at Sendcloud-negotiated pricing; at waybill time the merchant picks one and Sendcloud routes the request to that courier. All courier costs land on ONE Sendcloud invoice per period. The integration shows no margin or rate breakdown — detail and per-country courier availability live in Sendcloud's own portal, as does pickup scheduling.

### Each carrier is a separate shipping option (verified)

After connecting, the platform pulls the merchant's active Sendcloud contracts (DPD, DHL, UPS, PostNL, GLS, etc.) and the merchant installs each as its own shipping provider, visible to customers individually at checkout.

### Office / service-point support per carrier (verified)

By default this integration is door-to-door — supported delivery channels are `['address']`. But for carriers whose code is listed in Sendcloud's `service_point_carriers` global setting (e.g., PostNL, DHL ServicePoint), the External page also exposes an `office` service card, giving the same pickup-point picker as direct couriers. Carriers without service-point support remain address-only.

### No country restriction (verified)

The fallback allowed-countries list is empty — Sendcloud covers many EU markets and the quote API determines what is quotable.

### COD with cap (verified)

COD becomes available when the courier's `cod` setting is on AND the order is within the COD cap (10000 BGN for BGN stores).

### Waybill PDF on demand (verified)

Sendcloud returns waybill PDFs directly. Clicking **Print waybill** on an order fetches the PDF on demand. Same OmniShip quote → waybill → tracking flow — see [[orders-shipping-waybill]].

## Per-channel delivery pricing

SendCloud delivers to **address** — the single **address** channel is a separate rate card with its own enable toggle (`to_address`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time SendCloud quote; **no extra field** of its own.
- `calculator_fixed` — the SendCloud quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the SendCloud quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[settings-shipping]] — standard shipping-provider settings each installed courier inherits.
- [[shipping-provider-mechanism]] — how a shipping provider produces quotes + waybills.
- [[orders-shipping-waybill]] — waybill flow.

## Open questions
