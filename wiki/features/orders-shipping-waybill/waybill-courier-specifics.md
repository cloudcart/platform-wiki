---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → Courier specifics"
route_name: admin.internal.waybill
route_path: /admin/orders/action/shipping/:order_id/waybill
aliases: ["Per-courier waybill", "Courier waybill form", "Econt waybill", "Speedy waybill", "DPD waybill", "BoxNow waybill"]
tags: [orders, shipping, waybill, courier, econt, speedy, dpd, boxnow, sameday, omniship]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (generate flow, payer side, print PDF, remove/void, generic modal, API path).

# Waybill — per-courier specifics

## Purpose

Each courier integration (Econt, Speedy, DPD-BG, DPD-RO, BoxNow, Sameday, GLS, Cargus, DHL, Berry, Cargus, AlbanianCourier, Ntclogistics, Tcscourier, Fancourier, EuShipment, ElsLogistic, Sendcloud, Dexpress, Evropat, Frisbo, Rapido, Elslogistic) owns its own waybill form, served from `apps/{courier}/...`. Fields vary substantially. The platform's OmniShip layer normalises the surface, but the per-courier UX differs.

## Where to find it

When the order's shipping provider exposes its own `apps.<courier>.waybill` route, the Generate waybill button on [[orders-details]] opens the COURIER'S form, not the generic modal. Routing rule documented on [[waybill-generic-modal]].

## What the merchant can do here

Common field categories across couriers (NOT exhaustive — see each courier app's docs):

| Category | Typical fields (per-courier) |
|----------|------------------------------|
| **Recipient** | Name, address, phone (from order's shipping address; Econt auto-merges billing-company data — see below). |
| **Pickup** | Specific pickup point (Econt offices, BoxNow lockers, Speedy depots). Autocomplete from the courier's office API. |
| **Package** | Weight, dimensions, number of packages. Derived from products + chosen [[settings-boxes]]. |
| **Service** | Service tier (standard / express / next-day / overnight / drop-off / pickup). Courier-specific. |
| **Insurance** | Declared value in store currency. Pre-filled with the order's shippable-products total. |
| **COD** | Cash-on-delivery amount. Pre-filled with order's invoice total when payment is COD; 0 otherwise. |
| **Payer side** | Sender / Recipient / Other. See [[waybill-payer-side]] for the per-courier allowed list. |
| **Notes** | Free-text note to the courier. |
| **Document/receipt** | Whether customer needs to sign on receipt, return signed document, etc. |

## Settings & fields

### Cross-courier billing-merge — EXCLUSIVE to Econt

ONLY Econt's controller merges billing-address company data (company name, VAT, MOL, BULSTAT) into the waybill's receiver address. DPD Bulgaria's controller has a milder `client_name` parameter that splits an admin-entered name into first/last — it does NOT pull from billing. Speedy, BoxNow, Sameday, GLS, Cargus, DPD Romania, and all other couriers do NOT auto-merge billing-company data; the waybill uses the shipping address as-is.

If a Bulgarian merchant needs a company-tagged waybill for B2B customers, they must use Econt — other couriers require manually populating the company in the order's shipping address.

### Sameday — sets sender company from site setting

Sameday's controller uses `setting('company_name')` to populate the waybill's `company_name` field. So Sameday waybills show the platform-level "Company name" (from [[settings-general]]) as the sender's organisation name. Other couriers infer it from the configured sender-address profile.

### Econt — terminology

Econt uses **"Bill of lading" (товарителница)** terminology. When the merchant clicks Generate waybill, the platform calls Econt's bill-of-lading API. Econt assigns a tracking number; the platform stores it. See [[apps-econt]].

### BoxNow — locker-only

BoxNow ships exclusively to lockers. The waybill form requires picking a locker ID; address-only shipping is not supported. See [[apps-boxnow]].

### Speedy — international restrictions

Shipping INTERNATIONAL (any destination country other than Bulgaria) removes Receiver-pays entirely — only the sender can pay shipping. A Bulgarian merchant shipping to e.g., Greece via Speedy must pay shipping themselves; cannot pass to recipient. See [[waybill-payer-side]] for the full filter rules.

### DPD-BG — supports all three payer sides

DPD Bulgaria is one of the few couriers that supports Sender, Receiver, AND Other (Third Party) on the waybill. Most other couriers support only Sender + Receiver. See [[waybill-payer-side]].

### Per-courier `getWaybillSides` summary

| Courier | Native order in `getWaybillSides` |
|---------|-------------------------------------|
| **Econt** | Receiver → Sender → Other |
| **Speedy** | Receiver → Sender |
| **DPD Bulgaria** | Sender, Receiver, Other (all three) |
| **DPD Romania** | depends per manager override |
| **Cargus / Berry / DPD-style** | Sender → Receiver |
| **BoxNow (lockers)** | Sender → Other |
| **AlbanianCourier / Rapido / Elslogistic** | Sender → Receiver |
| **GLS, DHL Express, Ntclogistics, Tcscourier, Fancourier, EuShipment, Sendcloud** | each has its own override — typically Sender + Receiver |

## Business rules

### OmniShip abstraction layer

The platform's OmniShip layer normalises courier-specific behaviours behind a common interface:
- Check if a specific provider is installed + configured.
- List providers with active COD sync.
- Each provider's manager exposes support-type, allowed waybill sides, default payer side, and insurance formatting.

So the merchant sees a roughly consistent UI across couriers, but the underlying API calls vary substantially.

### Pickup-type-aware change-provider flow

When the merchant changes shipping provider on an order (pre-waybill), the platform inspects the current shipping address's office/locker state and the new provider's supported types — then redirects to one of:

- **office** flow — order has office_id and new provider supports `SUPPORT_OFFICE`.
- **locker** flow — order has office_id with office_type=1 and new provider supports `SUPPORT_LOCKERS`.
- **address** flow — new provider is external + supports `SUPPORT_ADDRESS` and current address doesn't match.
- **marketplace** flow — new provider has `SUPPORT_MARKETPLACE`.
- Otherwise — instant change without sidebar form.

So picking a new provider may bounce the merchant into a different sidebar (office selector for Econt, locker picker for BoxNow) before the order is updated.

### Tax recalc when changing shipping provider

When the merchant changes provider (pre-waybill), the platform:
1. Deletes any existing `shipping_provider`-scoped taxes on the order.
2. Fetches all taxes for the billing zone where `shipping_provider = newProviderId`.
3. Re-creates the matching tax rows.
4. Recalculates shipping quote + order totals.

So changing provider can shift the order's total via TAX changes alone — even if shipping cost is unchanged.

### Marketplace-pickup providers — divert from waybill

Providers with `SUPPORT_MARKETPLACE` (Amazon FBA, Frisbo) divert the Change Provider action to `apps.{app_key}.changePickup` or `apps.shipping.changePickup`. The merchant doesn't generate a waybill on the platform — the marketplace handles dispatch.

## Related

- [[orders-shipping-waybill]] — hub.
- [[apps-econt]] / [[apps-boxnow]] / [[apps-sameday]] / [[apps-gls]] / [[apps-dhl]] / [[apps-cargus]] / [[apps-dexpress]] / [[apps-eushipment]] / [[apps-elslogistic]] / [[apps-evropat]] / [[apps-albanian-courier]] / [[apps-frisbo-settings]] / [[apps-pick-and-pack]] — courier app pages.
- [[settings-general]] — `company_name` setting (Sameday uses this).
- [[settings-boxes]] — package dimensions used to pre-fill.
- [[shipping]] — shipping provider configuration.

## Open questions

None.
