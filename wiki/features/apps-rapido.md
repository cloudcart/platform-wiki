---
type: feature
nav_path: "Apps → Rapido"
route_name: apps.rapido.overview
route_path: /admin/shipping/rapido
aliases: ["Rapido", "Rapido courier", "Rapido BG", "Rapido deprecated"]
tags: [apps, shipping, courier, bulgaria, romania, omniship, deprecated]
plan_gates: []
status: DEPRECATED
created: 2026-05-22
updated: 2026-06-11
source_count: 1
---
# Rapido (DEPRECATED — use DPD Bulgaria instead)

> **⚠️ This integration is DEPRECATED.** CloudCart has retired Rapido as a recommended courier integration. **New merchants should use [[apps-dpdbulgaria-speedy]] (DPD Bulgaria) instead** for Bulgarian courier needs. Existing merchants with active Rapido configurations may continue to use it, but the integration is no longer maintained or marketed; switch to DPD Bulgaria at next contract renewal.
>
> Together with [[apps-dpdbulgaria-speedy|Speedy]], Rapido has been superseded as part of CloudCart's consolidation around DPD Bulgaria as the canonical Bulgarian courier. The underlying integration remains in place so existing installations don't break, but no new investment is going into Rapido. The historical documentation below is kept for AI Assistant context when answering questions from merchants who still have a Rapido configuration on their store.

## Purpose

**Rapido** WAS a regional courier serving **Bulgaria (BG)** and **Romania (RO)**. The CloudCart integration provided real-time delivery quotes, waybill generation, and tracking, offered alongside Econt / DPD Bulgaria etc. as an additional carrier option. Today the recommended path is [[apps-dpdbulgaria-speedy]] for Bulgarian shipping; Romanian needs are better served by [[apps-dpdromania]], [[apps-cargus]], [[apps-fancourier]], or [[apps-sameday]].

The merchant historically integrated Rapido by entering Rapido API credentials provided by their Rapido contact (or by creating an account through Rapido directly).

## Where to find it

Sidebar → Apps → install → **Rapido**. Standard OmniShip sub-pages (settings, per-order waybill). The settings screen is a legacy template — there is no modern Vue port; refer to [[apps-dpdbulgaria-speedy]] for the modern equivalent UI patterns (per-channel modal, additional-settings boxes, address picker).

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials + sender address (state / city / postcode / office / phone) in the Settings sub-page.
- Pick allowed delivery channels (to address, to office).
- Generate waybills + print PDF labels per order.
- See real-time quotes at checkout once credentials are validated.

### What the merchant CANNOT do here
- Use Rapido without a registered courier contract + valid API credentials.
- Generate waybills outside Bulgaria / Romania.
- Generate a waybill without a valid sender post code (the API requires it).

## Settings & fields

### Credentials

| Field | Notes |
|-------|-------|
| **Username** | Rapido API username (provided by Rapido). |
| **Password** | Rapido API password. |

### Sender address (required at install)

Standard OmniShip sender-address fields:

| Field | Notes |
|-------|-------|
| **State / Region** | Sender state / region. |
| **City** | Sender city. Picked from Rapido's live registry (synced in the background) — the dropdown shows three city-type prefixes: `ГР.` (city), `К.К.` (resort), `С.` (village), e.g. *"ГР. Sofia (1000)"*. |
| **Postcode** | Sender post code. **Required** — the API rejects waybills without it (error: *"Post code is required. Please, edit the shipping address."*). |
| **Office** | Optional pickup office (Rapido office network). |
| **Sender phone** | Sender contact phone. |
| **Sender name** | Sender / merchant name. |

### Allowed delivery channels

| Channel | What customer sees |
|--------|---------------------|
| **To address** | Home / office delivery. |
| **To office** | Pickup from a Rapido office (customer selects a specific office at checkout; it is stored on the cart and printed on the waybill). |

The merchant enables one or both. There is no locker channel.

### Pricing modes (storefront)

- **Rapido calculator** — real-time API quote.
- **Rapido calculator + handling fee** — quote plus a fixed merchant surcharge.
- **Rapido calculator + free shipping** — quote zeroed for the customer (merchant absorbs).
- **Fixed shipping rate calculated by the amount at the checkout** — flat price per cart-value tier.
- **Fixed shipping rate calculated by the weight of the products** — flat price per weight tier.
- **Fixed amount for shipping by cart total and weight of the products** — combined matrix.

### Additional shipment options

| Option | Notes |
|--------|-------|
| **Fragile** | Marks the shipment fragile (Rapido may charge a fragile surcharge). |
| **Insurance** | Declares an insurance value for the shipment. |
| **Money transfer** | Rapido's money-transfer service (separate from COD). |
| **Return documents** | Request signed delivery documents back from the recipient. |
| **Option before payment** | Customer inspects parcel before paying (when sender pays the shipment). |

### Payer side

The merchant picks **Sender** or **Recipient** as the default payer; the per-order waybill form allows override.

## Business rules

Standard OmniShip pattern (quote → waybill → tracking via [[orders-shipping-waybill]], PDF label printing supported) with Rapido-specific quirks:

- **Coverage countries.** Quotes are generated only when the receiver address is in **Bulgaria (BG)** or **Romania (RO)**.
- **Currency conversion to BGN.** Rapido's API expects amounts in BGN. When the store currency is NOT BGN, the platform converts amounts (subtotal, COD, insurance, item prices) to BGN at API-call time using the internal FX rate. The order's stored currency stays the original; conversion is only for the API request.
- **COD with cap + recalculate on payment change.** COD is enabled when the merchant's COD setting is on AND the order is within the COD cap (10000 BGN for BGN stores; non-BGN stores have no platform cap, so Rapido's server-side limits apply). When the customer switches payment method (online ↔ COD), shipping recalculates so the COD surcharge appears / disappears.
- **Insurance with cap.** Insurance is available when the merchant's insurance setting is on AND the order is within the same 10000 BGN cap (reused as the insurance ceiling).
- **Postcode required for waybill.** Rapido rejects waybills without a sender post code; the merchant must complete the postcode field in the address before generating a waybill.
- **Reference data is auto-synced.** Cities, countries, offices, streets, and post codes refresh automatically in the background as Rapido updates its registry — the merchant doesn't manage these lists manually.

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-dpdbulgaria-speedy]] — alternative Bulgarian couriers.
- [[apps-cargus]] / [[apps-fancourier]] / [[apps-dpdromania]] / [[apps-sameday]] — alternative Romanian couriers.
- [[shipping-provider-mechanism]] — common shipping pattern.

## Open questions

_None — all questions answered above._
