---
type: feature
nav_path: "Apps → EuShipment"
route_name: apps.eushipment.overview
route_path: /admin/shipping/eushipment
aliases: ["EuShipment", "EU Shipment", "EuShipment EU", "no enable disable button", "app has no active toggle"]
tags: [apps, shipping, b2b, europe, omniship, aggregator]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 7
---
# EuShipment

## Purpose

**EuShipment** integration — a European B2B shipping aggregator focused on commercial / palletised shipments across the EU. Used by merchants moving larger goods (pallets, freight, B2B inventory) where standard parcel couriers aren't economic.

EuShipment is a **multi-carrier aggregator**: it doesn't deliver anything itself, it brokers shipments through whichever real couriers the merchant's EuShipment contract grants. Setup is two-level — the **parent app Settings** (one API key + a contract-driven courier picker), then each **installed courier** becomes its OWN shipping method with its own settings page. So at checkout the customer sees the specific aggregated couriers (DHL, DPD, GLS, etc.), each under its real brand, not a single "EuShipment" option.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> Activation here is **per courier**, not per app: each installed sub-courier has its own Enable / Disable button on its own settings page, see [[apps-eushipment-subcourier-settings]].

## Where to find it

Sidebar → Apps → install → **EuShipment** OR direct routes. Standard OmniShip sub-pages: Overview (`apps.eushipment.overview`), Settings (`apps.eushipment.settings`), Shipments, Shipments return, and the per-courier settings page (`apps.eushipment.external/:id`).

## What the merchant can do here

- Install / uninstall the integration (there is no app-level activate / deactivate — see the note above).
- Enter EuShipment credentials and install the contract-granted couriers — see [[apps-eushipment-credentials-couriers]].
- Configure each installed courier independently — see [[apps-eushipment-subcourier-settings]].
- Set per-courier, per-channel pricing — see [[apps-eushipment-pricing-modes]].
- View generated waybills / shipments and manage returns in the Shipments sub-pages.
- See real-time quotes at checkout once credentials are validated.

### What the merchant CANNOT do here

- Use the integration without an active courier contract + valid API credentials.
- Add couriers their EuShipment contract does not include.
- Generate waybills for destinations the courier does not serve.

## Settings & fields

EuShipment's configuration is split across three aspect pages; this hub only points to them:

- **Credentials + courier picker** — a single API-key field and the contract-driven sub-courier list. See [[apps-eushipment-credentials-couriers]].
- **Per-courier settings** — visualization, delivery channels, geo zones, payment providers, and the Additional Settings box (who-pays, default weight, return documents, fragile, fulfillment, plus contract-gated COD / insurance / open-package / Saturday switches). See [[apps-eushipment-subcourier-settings]].
- **Pricing modes** — the six per-channel rate models (three live-quote, three flat-rate) and the calculator modal. See [[apps-eushipment-pricing-modes]].

## Sub-pages (in this cluster)

This app is split into 3 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[apps-eushipment-credentials-couriers]] — the parent Settings page: the single `public_key` API key, validation against `/admin/api/eushipment/validate`, the per-merchant contract-dependent courier list, install-as-own-shipping-method behaviour, read-only capability flags, and the background sub-courier sync.
- [[apps-eushipment-subcourier-settings]] — the per-installed-courier settings page (`apps.eushipment.external/:id`): enable/disable, visualization, service-type channels, geo zones, payment-provider allow-list, and the full Additional Settings field reference incl. capability-gated switches.
- [[apps-eushipment-pricing-modes]] — the six pricing modes per channel (calculator / + fee / + free shipping / fixed-price / fixed-weight / price+weight), the calculator modal, quote currency, and the COD-only "courier disappears at checkout" scenario.

## Business rules

### Multi-carrier aggregator — couriers come from the contract

The list of installable couriers is per-merchant and contract-controlled; different merchants see different couriers. Each installed courier becomes its own shipping method with its own `external_id`, and the parent settings do NOT cascade to it. Full detail on [[apps-eushipment-credentials-couriers]].

### B2B / freight focus

Larger / palletised shipments where parcel couriers don't fit. Whether a shipment moves as parcel or pallet comes from the chosen underlying courier, not from EuShipment itself.

### External ID parsing on the order address-edit form

In [[orders-address-edit]] the integration string `eushipment_<id>` is parsed to extract a per-shipment external ID — visible in the address-edit form for tracking EuShipment's internal references.

### Same OmniShip pattern

Quote → waybill → tracking via [[orders-shipping-waybill]], with the EuShipment `external_id` carried through.

## Per-channel delivery pricing

EuShipment delivers to **address**, to **office** and to **locker** — each of its **3** delivery channels (to **address**, to **office** and to **locker**) is a separate rate card with its own enable toggle (`to_address` / `to_office` / `to_locker`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `calculator` — the real-time EuShipment quote; **no extra field** of its own.
- `calculator_fixed` — the EuShipment quote **plus a fixed fee** you enter in the **Parcel processing Fee** field (`fixed_price_<channel>`).
- `free` — the EuShipment quote, but **free above a threshold** you set in **Minimum Order Value for Free Delivery** (`free_shipping_total_<channel>`); below it the customer pays the quote.
- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

The calculator-based types also expose an optional **Fallback price** rate table, used only when the live quote can't return a price; the `fixed_*` types need no fallback (their table **is** the price). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[apps-sendcloud]] — sister European multi-carrier alternative for parcels.
- [[shipping]] — shipping landing.
- [[shipping-provider-mechanism]] — the shipping provider pattern each installed courier follows.
- [[orders-shipping-waybill]] — waybill flow with EuShipment external_id integration.
- [[orders-address-edit]] — special parsing of the `eushipment_<id>` integration string.

## Open questions

None.
