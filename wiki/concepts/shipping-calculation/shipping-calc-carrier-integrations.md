---
type: concept
nav_path: "Concept → Shipping calculation → Carrier integrations"
aliases: ["Carrier shipping integrations", "Live carrier quote", "getQuotes API", "Econt quote", "Speedy quote", "BoxNow quote", "Cargus quote", "Live shipping quote", "Куриерска интеграция", "Жива оферта от куриер"]
tags: [shipping, carriers, integrations, omniship, multi-currency, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (rate models, geo gating, the checkout cascade, COD surcharge, discounts + Cart Rules, persistence).

# Shipping — carrier integrations

## Definition

**Carrier integrations** are shipping methods with `type = integration` whose quote comes from a **live API call to the carrier's `getQuotes` endpoint** at checkout-time — Econt, Speedy, BoxNow, Cargus, Sameday, Fan Courier, DHL, DHL Express, GLS, DPD, and so on. The merchant cannot edit per-row prices the way they can on a custom method ([[shipping-calc-rate-models]]); the carrier owns the price and the platform passes it through unchanged.

The integration is installed + configured via the carrier's dedicated app screen ([[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-cargus]], [[apps-sameday]], [[apps-dhl]], [[apps-dhlexpress]], etc.) — credentials, sender data, default-service options, pallet rules. Once installed AND configured, the carrier appears as a shipping method on [[settings-shipping]] alongside custom methods, where the merchant toggles it active / inactive, sets its `target` geo scope ([[shipping-calc-geo-gating]]), its allowed-payment-method allow-list, and its customer-group restrictions — the price arithmetic is delegated to the carrier.

An **installed-but-misconfigured** carrier integration (missing or invalid credentials) does NOT show at checkout — the carrier's API rejects the quote request and the platform silently skips that method, with no log entry; the carrier just disappears.

## Scope

Covered: the live `getQuotes` call at checkout-time; what the platform sends in the request (receiver address, package dimensions / weight, service options, COD amount, insurance amount); multi-currency FX conversion to the carrier's billing currency; the country-default carrier-recommendation filter on the [[settings-shipping]] "Browse integrations" modal; the per-carrier behaviours and failure modes (Speedy / Econt / BoxNow / Cargus channels, COD caps, weight caps, re-quote) detailed under "Where it applies" below.

Not covered here:

- The carrier's own app-configuration screens (credentials, sender data, pallet-rule editors) — see [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], etc.
- The custom-method rate-row path — see [[shipping-calc-rate-models]].
- COD surcharge mechanics in detail — see [[shipping-calc-cod-surcharge]].
- The structural shipping provider abstraction every carrier registers under — see [[shipping-provider-mechanism]].
- Waybill generation (the per-order action after the order is placed) — see [[orders-shipping-waybill]].

## Contrasts

- **Carrier integrations vs. custom methods** — integrations ask the carrier's API live and pass through; custom methods use merchant-editable rate-row tables ([[shipping-calc-rate-models]]). Both appear side-by-side at checkout.
- **Carrier's quoted price vs. discount layer** — the carrier's quote is what it is. To make it cheaper, the merchant uses [[marketing-discounts-shipping]] (zeros it) or [[apps-cart-rules]] (any modification). See [[shipping-calc-discounts-rules]].
- **Service-option choice at checkout vs. fixed-method selection** — carriers like Econt and Speedy return MULTIPLE service options per quote ("Next-day to address 6.50 BGN", "Same-day 12 BGN", "To Econtomat 4 BGN") — the customer picks one inside the method's row at checkout. BoxNow returns only the locker option; the customer doesn't see a sub-choice.

## Where it applies

### The `getQuotes` call

When a carrier-integration method survives the [[shipping-calc-geo-gating|geo gate]], the platform calls the carrier's `getQuotes` API with:

- The **receiver address** — country / city / post-code / street, with carrier-specific address resolution (Speedy to its site IDs, Econt to its city/office catalogue, BoxNow to the nearest active locker).
- The **package dimensions + weight** — derived from products (sum of `weight × quantity`) and the merchant's configured boxes on [[settings-boxes]] (smallest box that fits).
- **Service options** the customer has selected — `address` / `office` / `locker` for Speedy and Econt; locker-only for BoxNow.
- **COD amount**, if the customer's payment method is COD ([[shipping-calc-cod-surcharge]]).
- **Insurance amount**, when configured per-method or per-order.

The carrier responds with one or more service options, each with its own price. The customer's selected option is stored on the cart for the order ([[shipping-calc-persistence]]).

### Multi-currency FX conversion

For multi-currency stores, the platform converts COD / insurance / subtotal into the carrier's billing currency before the API call, using the latest Fixer.io-synced FX rate from the platform's internal rate table (see [[multi-currency]]):

- **Speedy** bills in **BGN** for BG operations, **RON** for RO operations.
- **Cargus** bills in **RON**.
- **Econt** bills in **BGN** for BG, **RON** for RO.
- **BoxNow** bills in the country's local currency (BGN / RON / EUR depending on operation).

### Country-default carrier-recommendation filter

The [[settings-shipping]] "Browse integrations" modal filters its list by the store's [[settings-general]] operation country. Bulgarian stores see Econt, Speedy, BoxNow BG, etc.; Romanian stores see Cargus, Sameday, Fan Courier, DPD Romania, etc. The merchant cannot override this filter from the modal — to access integrations for other countries, change the country in Settings → Store settings.

### Per-carrier behaviours

**Speedy** (BG / RO)

- Three **delivery channels**: `address` (to door), `office` (to Speedy office), `locker` (to APT / parcel locker). The customer picks one inside the Speedy row.
- **Insurance amount** is always converted to **EUR** — DPD Bulgaria (Speedy)'s billing currency — regardless of the store currency.
- **10,000 BGN COD cap** — legacy, only for stores on the `BGN` currency; a store on `EUR` (the new norm) gets no platform cap. Carts above this with COD selected get silently dropped (see [[shipping-calc-cod-surcharge]]).

**Econt** (BG / RO)

- **Pallet shipping** is triggered by category / weight thresholds when [[apps-econt]] has Pallet Shipment enabled. Carts matching the pallet rules quote at pallet rates instead of parcel rates.
- **10,000 BGN COD cap** — legacy, only for stores on the `BGN` currency; a store on `EUR` (the new norm) gets no platform cap.
- **Office-delivery weight cap of 1,000 kg** — above this, only address delivery is offered.

**BoxNow** (BG / RO / GR / CY / HR)

- **Locker-only**. "To address" is HIDDEN at checkout; only "To locker" is offered.
- The platform looks up the **nearest active locker** to the customer's address using BoxNow's locker catalogue.

**Cargus** (RO)

- Supports **home + office** delivery.
- Supports **COD**.
- **Automatic re-quote on payment-method switch** — when the customer changes from card to COD (or vice versa), the platform calls `getQuotes` again because the COD surcharge changes the quote.

### Failure modes

- **Invalid credentials** — the carrier rejects the quote request. The platform silently skips the method; the customer doesn't see it at checkout.
- **COD cap exceeded** — for BG carriers above 10,000 BGN, COD options are dropped; the customer must pay online.
- **Weight cap exceeded** — Econt's office-delivery 1,000 kg cap forces address-delivery only.
- **No locker in range** (BoxNow) — the method is silently dropped if no active locker covers the customer's address.

## Related

- [[shipping-calculation]] — hub.
- [[shipping-calc-rate-models]] — the custom-method alternative.
- [[shipping-calc-geo-gating]] — the gate that runs BEFORE `getQuotes`.
- [[shipping-calc-cod-surcharge]] — the COD-cap and re-quote rules in detail.
- [[shipping-calc-persistence]] — how the chosen carrier quote is saved on the cart and order.
- [[shipping-provider-mechanism]] — structural abstraction every carrier registers under.
- [[multi-currency]] — FX-rate sourcing for the carrier's billing currency.
- [[settings-shipping]] — "Browse integrations" modal.
- [[settings-boxes]] — package dimensions feeding volumetric quotes.
- [[settings-general]] — operation country driving the country-default filter.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-boxnow]] / [[apps-cargus]] / [[apps-sameday]] / [[apps-dhl]] / [[apps-dhlexpress]] — per-carrier configuration screens.
- [[orders-shipping-waybill]] — downstream waybill issuance for the carrier the customer picked.

## Open Questions

- (verify) **Per-product shipping surcharge.** There is no first-party "this product adds €5 to the shipping line" feature on carrier integrations. Merchants who need per-product surcharges typically use [[apps-cart-rules]] (adding a flat fee when a specific product is in cart) or build the surcharge into the product's price.
