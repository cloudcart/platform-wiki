---
type: concept
nav_path: "Concept → Shipping provider mechanism → Configuration"
aliases: ["Shipping provider configuration", "Carrier credentials", "Sender address book", "Allowed delivery channels", "Configure shipping carrier", "Конфигурация на куриер", "API данни на куриер", "Адрес на изпращач"]
tags: [shipping, couriers, providers, integrations, configuration, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider-mechanism]]. See the hub for the other aspects (pricing models, pickup points, waybill, COD, geo routing, status tracking).

# Shipping provider mechanism — Configuration

## Definition

**Configuration** is the carrier-onboarding half of the shipping provider mechanism: the merchant installs the carrier's app, enters the credentials the carrier issued, fills in the sender address book (where packages are picked up from), selects which delivery channels to expose at checkout, and toggles any optional pallet / insurance / signature services. Once configured, the carrier appears as a shipping method at storefront checkout and is ready to quote live prices.

Every shipping carrier — Econt, Speedy, BoxNow, DHL, DPD, GLS, Cargus, Sameday, Fan Courier, ACS, etc. — follows the same five-step onboarding lifecycle. The carrier-specific quirks (Econt's pallet rules, BoxNow's locker-only channel, DHL's international account codes) are configured *inside* this shared pattern.

## Scope

Covered:

- Install + credential shape per carrier.
- Sender address book (single vs. multi-warehouse).
- Allowed delivery channels (to address / to office / to locker).
- Optional pallet / insurance / signature toggles.
- Active / Inactive without uninstall.
- Where the merchant edits each piece.

Not covered:

- Pricing model the carrier uses — see [[shipping-provider-mech-pricing-models]].
- Cash on delivery setup — see [[shipping-provider-mech-cod]].
- Per-carrier specifics (Econt's `key_word`, Speedy site IDs, BoxNow API key) — see each carrier's app page.
- Database-row attributes — see [[shipping-provider-attributes]].

## Contrasts

- **Install vs. activate**: installing the app loads the configuration screens; activating (Active = yes) is what surfaces it at checkout. Inactive carriers retain their credentials but are hidden — useful for seasonal carriers or during testing.
- **Credentials vs. sender address book**: credentials authenticate the merchant *to* the carrier's API. The sender address book describes the *physical pickup origin* the carrier should drive to when collecting packages. Both are required; one without the other yields silent quote failures.
- **Carrier-API credentials vs. COD agreement**: API credentials let the merchant call the carrier's quote / waybill endpoints. The COD agreement (a separate contract with the carrier's bank) lets the carrier collect cash on behalf of the merchant. They're configured separately — see [[shipping-provider-mech-cod]].

## Where it applies

### The five-step onboarding flow

1. **Installing the app** from the [[apps]] catalog (filtered to category 4) or from [[settings-shipping]]'s "Browse shipping integrations" modal — same effect either way.
2. **Entering API credentials** the carrier provided. The credential shape varies:
   - **Username + Password** — Econt (the merchant's Econt account login), Speedy (Speedy username + Speedy password).
   - **Client ID + Client Secret** — DHL, DPD, GLS.
   - **API key / API token** — BoxNow, some Romanian carriers.
3. **Testing the connection** — most apps validate credentials by calling the carrier's API on save. Invalid credentials return a carrier-specific error inline on the field. (verify — exact validation behaviour per carrier.)
4. **Configuring the sender address book** — pickup addresses from which the carrier collects packages. The merchant typically has ONE default sender address (their warehouse / office); multi-warehouse merchants can store multiple and pick one per order. The address format is carrier-specific:
   - Econt requires `key_word` (auto-fills firm + city / office / quarter / street from Econt's address registry).
   - Speedy requires Speedy site / street IDs.
   - DHL / DPD / GLS use standard country + city + postcode + street fields.
5. **Selecting allowed delivery channels** — most Bulgarian / Romanian carriers expose three options the merchant can individually enable / disable: to address, to office / branch, to locker.

### Optional services

- **Pallet shipment** — Econt exposes a Pallet Shipment toggle with dimensions + category / weight rules. Other carriers may expose a similar toggle (verify).
- **Insurance** — most carriers expose an insurance toggle and an insured-amount field on the per-order waybill flow.
- **Signature required / fragile / hazardous** — additional flags that ride along on the waybill API call. See [[shipping-provider-mech-waybill]].

### Active / Inactive toggle

Like payment providers, shipping carriers can be **Active / Inactive** without uninstalling (toggle in [[settings-shipping]]) — inactive methods are hidden from checkout but their configuration is preserved. This is the safe way to temporarily disable a carrier (e.g., during a credentials rotation) without losing the sender address book and delivery channel selections.

### Where the merchant edits each piece

- Credentials + sender address book + allowed channels + optional services: the carrier's individual app page (e.g., [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]]).
- Active / Inactive toggle: [[settings-shipping]] (also available inside the app page).
- Default shipping method shown first at checkout: [[settings-cart]] (NOT settings-shipping).
- Package dimensions feeding carrier weight / volumetric calculations: [[settings-boxes]].
- Operation country (filters which carrier apps are *available* in the Browse integrations modal): [[settings-general]].

## Related

- [[shipping-provider-mechanism]] — hub.
- [[settings-shipping]] — shipping-methods hub; Active/Inactive toggle lives here.
- [[shipping-provider]] — sister entity for the per-row data shape.
- [[shipping-provider-lifecycle]] — install / activate / soft-delete state machine on the entity side.
- [[shipping-provider-attributes]] — the actual columns stored per configured carrier.
- [[apps]] — apps catalog (category 4 = shipping).
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-boxnow]] / [[apps-cargus]] / [[apps-sameday]] / [[apps-dhl]] / [[apps-dpdbulgaria-speedy]] / [[apps-dpdromania]] / [[apps-fancourier]] / [[apps-gls]] / [[apps-acscourier]] / [[apps-albanian-courier]] — per-carrier configuration pages.
- [[settings-cart]] — default carrier + auto-select toggle.
- [[settings-boxes]] — package dimensions.
- [[settings-general]] — operation country filter for the catalog.
- [[payment-provider-mechanism]] — sister concept for payment integrations (same configure → activate pattern).

## Open Questions

- ⏸️ Exact validation behaviour on credential save varies across carriers — some validate by calling a no-op endpoint, others accept the credentials and fail later on first quote. (verify per carrier on the individual app pages.)
