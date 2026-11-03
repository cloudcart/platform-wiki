---
type: entity
nav_path: "Entity → Shipping Provider → Attributes"
aliases: ["Shipping provider attributes", "Shipping provider fields", "Courier configuration fields", "Provider credentials", "Sender address book", "Delivery channel toggles"]
tags: [entity, shipping, couriers, providers, attributes, credentials, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider]]. See the hub for the other aspects (lifecycle, pricing models, checkout filters, COD, delivery channels & waybill).

# Shipping Provider — Key attributes

## Identity

Each installed Shipping Provider stores a configuration record with credentials, sender data, channel toggles, and operational flags. These fields are what the merchant edits on the provider's settings page (e.g., [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-cargus]]) — they decide whether the provider's methods appear at checkout, with which sender, against which COD account, and through which delivery channels.

## Aliases

- **Shipping provider fields** / **Courier configuration fields** — the umbrella for everything below.
- **Provider credentials** — the API auth subset.
- **Sender address book** — the pickup-address subset.
- **Delivery-channel toggles** — the `to_address` / `to_office` / `to_locker` subset.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Provider code** (internal key) | Stable identifier (`econt`, `speedy`, `boxnow`, `cargus`, `dpd-bulgaria`, `gls`, etc.) | Used internally to pick the right integration; never edited by the merchant. |
| **Storefront name** | Customer-facing label at checkout | Editable per provider — e.g., the merchant can rename "Econt" to "Express delivery". Each shipping method (per delivery channel) can have its own label. |
| **Logo** | Provider-logo image | Defaults to the courier's logo; merchant can upload a custom override for Custom methods. |
| **Active** | yes / no | Master on/off toggle on [[settings-shipping]]. When `no`, the provider's methods are hidden at checkout; when `yes`, they appear (subject to other scoping). Toggling persists immediately. |
| **Credentials (per-provider)** | API username + password / client ID + secret / API key | Shape varies: Econt + Speedy use username + password; DHL / DPD / GLS use client ID + client secret; BoxNow and some Romanian carriers use an API key. Saved during the carrier's onboarding form. |
| **Sender address book** | Pickup addresses from which the courier collects parcels | Most merchants store ONE default sender (warehouse / office); multi-warehouse merchants can store multiple and pick per order. Format is carrier-specific — Econt requires `key_word` (auto-fills city / office / quarter / street); Speedy uses Speedy site / street IDs; DHL / DPD / GLS use standard country + city + postcode + street. |
| **Allowed delivery channels** | `to_address` / `to_office` / `to_locker` toggles | Most Bulgarian / Romanian carriers expose three options the merchant individually enables / disables. BoxNow is locker-only — only "to locker" is offered. See [[shipping-provider-delivery-channels-waybill]] for full channel semantics. |
| **COD agreement number** | Carrier-side cash-on-delivery contract ID (e.g., Econt's `cod_account`) | Required for COD to work end-to-end. Econt and Speedy verify the configured COD account against the merchant's registered carrier-side clients before each quote; outdated configs are silently dropped. See [[shipping-provider-cod]]. |
| **COD-sync toggle** | yes / no | *"Automatically set order status to paid when we get information from shipping provider with Cash on delivery"* — when ON, the carrier reports the COD-collected event and CloudCart flips the order's payment to `completed` automatically. |
| **Pallet rules** (Econt only) | Pallet Shipment toggle + categories / minimum weight | When ON, carts matching the rules ship as pallets at pallet rates. Other carriers do not expose pallet rules in the same form. |
| **Insurance toggle** | yes / no + amount logic | Optional; the carrier insures the parcel up to the cart's subtotal. |
| **Additional services** | Signature-required, fragile-handling, etc. | Per-carrier; merchant enables the ones the courier supports. |
| **Office / locker cache window** | Server-side cached list of carrier pickup points | Econt's list is cached for 1 day; similar pattern across other carriers. When a courier updates its registry, merchants see the new locations within the cache window without doing anything. |
| **Pricing model** | `integration` (live API) / `price` (custom rate rows) / `weight` (custom rate rows) / `price_and_weight` / `marketplace` | See [[shipping-provider-pricing-models]] for the three patterns. |

### Save-time field normalization

Whenever the Shipping Provider row is persisted, the platform normalizes four fields in one write before the database commit:

- **Target inferred from `geo_zone_id`** — if `target` is empty but a `geo_zone_id` is supplied, `target` is set to `regions`. If `target` is empty AND (no zone OR `type = marketplace`), `target` defaults to `restofworld`. This guarantees every row has a well-defined targeting scope.
- **Zone wipe for rest-of-world** — when `target = restofworld`, any `geo_zone_id` value is forcibly cleared to NULL.
- **Insurance rate stored as cents** — the entered `insurance` value is run through an integer-price normalisation (e.g. `1.50` → `150`). The runtime adds insurance as a per-order surcharge using the stored integer.
- **Marketplaces field normalized to array** — for `type = marketplace`, a comma-separated string input is split into an array (`['amazon','ebay']`); for non-marketplace types the field is wiped to NULL. So the merchant can paste a list and the engine consumes it as a clean array.

## Where it appears

- [[settings-shipping]] — the central hub: every installed shipping method as a row with these fields editable.
- Per-carrier app pages — one page per courier with its credentials + sender + channel form:
  - **Bulgarian carriers**: [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-dpdbulgaria-speedy]].
  - **Romanian carriers**: [[apps-cargus]], [[apps-sameday]], [[apps-dpdromania]], [[apps-fancourier]].
  - **International**: [[apps-dhl]], [[apps-dhlexpress]], [[apps-gls]].
- [[settings-boxes]] — package dimensions used by carrier-integration weight / volumetric calculations against these credentials.

## Related

- [[shipping-provider]] — hub.
- [[settings-shipping]] — where the fields are edited.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-boxnow]] / [[apps-cargus]] — per-carrier forms exposing these fields.
- [[settings-boxes]] — package-dimension defaults fed into integrations.
- [[geo-zone]] — `geo_zone_id` field for Custom-method targeting (see [[shipping-provider-checkout-filters]]).

## Open Questions

- The exact insurance-cap formula per carrier `(verify)`.
