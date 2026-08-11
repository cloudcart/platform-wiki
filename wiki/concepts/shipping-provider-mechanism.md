---
type: concept
nav_path: "Concept → Shipping provider mechanism"
route_name: ""
route_path: ""
aliases: ["Shipping provider mechanism", "Shipping provider pattern", "How shipping providers work", "Courier integration model", "Common shipping pattern", "Shipping integration lifecycle", "Courier provider mechanism", "Куриерски доставчици", "Шаблон на куриерите", "Как работят куриерите", "Доставчик на доставка"]
tags: [shipping, couriers, providers, integrations, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Shipping provider mechanism

## Definition

The **shipping provider mechanism** is the common pattern CloudCart uses across all 30+ shipping-courier integrations on the platform — Econt, Speedy, BoxNow, Cargus, Sameday, DPD Bulgaria, DPD Romania, DHL, DHL Express, GLS, Fan Courier, Bulgarian Posts, Albanian Courier, ACS Courier, and every other carrier in [[settings-shipping]]. Despite hugely different transit networks (national couriers, parcel-locker networks, international air freight), every shipping provider plugs into CloudCart through the same lifecycle: **configure carrier credentials → install + activate → quote live at checkout → customer picks pickup point or address → generate waybill on fulfillment → sync delivery status back**. The merchant adds the carrier from [[settings-shipping]] (or from the Apps catalog filtered to category 4), saves the API credentials the carrier provided, and the integration appears as a shipping method at storefront checkout.

This concept page describes the **shared mechanism** — what every shipping provider has in common — so the 30+ per-carrier feature pages (e.g., [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-cargus]], [[apps-dhl]]) don't have to repeat the boilerplate. When a merchant asks the AI Assistant "how do I configure a courier?", "why doesn't a shipping option show up at checkout?", "how does cash on delivery work with the courier?", or "what determines the shipping price?", the answer derives from this pattern; carrier-specific quirks (Econt's pallet rules, Speedy's three channels, BoxNow's locker-only delivery) are documented on each carrier's page.

This concept is split into **7 aspect pages** below, each covering one slice. For the per-row data shape of a configured carrier (the database entity, attributes, capability flags), see the sister cluster [[shipping-provider]].

## Sub-pages (in this cluster)

The Assistant should drill into the aspect that matches the question, not read every page.

- [[shipping-provider-mech-configuration]] — install + credentials shape per carrier + sender address book + allowed channels + active/inactive toggle.
- [[shipping-provider-mech-pricing-models]] — three pricing models (live API quote, merchant rate rows, local pickup / free / fixed) and the per-method scope rules.
- [[shipping-provider-mech-pickup-points]] — pickup-point picker at checkout (office vs. locker), per-carrier network coverage, server-side cache window.
- [[shipping-provider-mech-waybill]] — per-order waybill action that calls the carrier API, tracking number, label print + return waybills.
- [[shipping-provider-mech-cod]] — Cash on Delivery: surcharge model, 10,000 BGN currency-aware cap, automatic paid-sync flow, COD-account validation.
- [[shipping-provider-mech-geo-routing]] — Geo Zone gating for custom methods + carrier-API coverage for integrations + multi-currency FX conversions at carrier-call time.
- [[shipping-provider-mech-status-tracking]] — webhook-driven shipping-status updates, polling fallback, Cart Rules overrides, customer-group restrictions, default selection, delete protection.

## Scope

What this concept covers (across the 7 sub-pages): configuration model (credentials, sender address book, allowed channels); three pricing models (live API quote, merchant rate rows, free / fixed / local pickup); pickup-point selection; waybill generation; cash on delivery (surcharge, cap, auto-sync); geo zone routing + multi-currency FX at carrier-call time; status tracking via webhooks + polling; and side overrides (Cart Rules, customer groups, default selection, delete protection).

What it does NOT cover:

- The exact credential fields, sender-address structure, or pallet rules of each individual carrier — those live on the 30+ per-carrier feature pages.
- The full **shipping calculation** arithmetic — see [[shipping-calculation]] and its sub-pages.
- Geographic zone definitions — see [[settings-geo-zones]] and [[geo-targeting]].
- Per-order waybill UI details — see [[orders-shipping-waybill]].
- The data-model entity (attributes, capability flags) — see [[shipping-provider]] and its aspects ([[shipping-provider-attributes]], [[shipping-provider-checkout-filters]], [[shipping-provider-cod]], [[shipping-provider-delivery-channels-waybill]], [[shipping-provider-lifecycle]], [[shipping-provider-pricing-models]]).

## Contrasts

- **Shipping provider vs. payment provider**: both are third-party integrations the merchant configures with credentials and activates at checkout. They differ in what they're paid for (money in vs. parcel out) and where in the customer flow they appear (payment after cart, shipping during cart). See [[payment-provider-mechanism]] for the payment equivalent.
- **Carrier integration vs. custom method**: carrier integrations call the carrier's live API for a real-time price quote; the merchant cannot edit rate rows. Custom methods have merchant-editable rate-row tables and merchant-set geo scopes. Both kinds appear side-by-side at checkout. See [[shipping-provider-mech-pricing-models]].
- **To address vs. to office / branch vs. to locker**: most Bulgarian / Romanian carriers expose three delivery channels with potentially different prices; the customer picks one at checkout. BoxNow is locker-only. See [[shipping-provider-mech-pickup-points]].
- **Mechanism (cross-cutting pattern) vs. entity (per-row data shape)**: this concept describes the *shared lifecycle every carrier follows*. The sister cluster [[shipping-provider]] documents the *database entity* (attributes, capability flags, soft-delete state). The two are complementary — mechanism = behaviour, entity = data shape.
- **COD via carrier integration vs. COD as standalone payment**: when the customer picks Cash on Delivery and a carrier-integration shipping method, the carrier collects the cash at delivery and remits it back, with automatic paid-sync. Standalone COD ([[payment-providers-cod]]) without a carrier integration means the merchant collects the cash themselves and marks paid manually.

## Where it applies

- **Configuration**: [[settings-shipping]] (hub), [[apps]] (catalog filtered to category 4), and the per-carrier app pages — [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-cargus]], [[apps-sameday]], [[apps-dpdbulgaria-speedy]], [[apps-dpdromania]], [[apps-fancourier]], [[apps-dhl]], [[apps-dhlexpress]], [[apps-gls]], [[apps-acscourier]], [[apps-albanian-courier]].
- **Customer side**: [[checkout-flow]] (method picker), [[cart]] / [[order]] (carry the selection + pickup point), [[shipping-calculation]] (cost arithmetic).
- **Order side**: [[orders-details]] (shipping section), [[orders-shipping-waybill]] (label issue), [[orders-sync-cod]] (COD paid-sync).
- **Settings & status**: [[settings-geo-zones]] / [[geo-polygons-settings-main-new]] / [[settings-geo-distances]] (geographic gating); [[settings-cart]] (defaults, COD options, Maps API key); [[settings-boxes]] (package dimensions); [[settings-general]] (operation country); [[shipping-status]] + [[settings-statuses]] (status labels); [[notification-delivery]] (carrier-webhook-triggered emails).

## Related

- [[settings-shipping]] — the merchant's shipping-methods hub; central point for adding, editing, and toggling methods.
- [[shipping-calculation]] — the full arithmetic of how the chosen shipping cost is computed.
- [[shipping-status]] — the enum tracking dispatch and delivery progression.
- [[shipping-provider]] — sister entity cluster (per-row data shape, attributes, capability flags).
- [[checkout-flow]] — the cart-to-order transition where the customer picks a shipping method.
- [[orders-shipping-waybill]] — the per-order action that calls the carrier's waybill API.
- [[orders-sync-cod]] — the COD-sync sub-flow.
- [[orders-details]] — per-order edit hub.
- [[settings-geo-zones]] / [[geo-polygons-settings-main-new]] / [[settings-geo-distances]] / [[geo-targeting]] — geographic gating used by custom methods.
- [[settings-cart]] — defaults (default carrier, auto-select toggle, COD options, Google Maps API key).
- [[settings-boxes]] — package dimensions feeding carrier weight / volumetric calculations.
- [[settings-general]] — operation country filters which carrier apps are available.
- [[settings-statuses]] — Shipping tab.
- [[notification-delivery]] — carrier webhooks update shipping status.
- [[multi-currency]] — FX-rate conversions for carrier API calls (Speedy = BGN, Cargus = RON, etc.).
- [[apps-cart-rules]] — Cart Rules override shipping availability / line.
- [[customers-custom-groups]] — customer-group restrictions on method visibility.
- [[payment-provider-mechanism]] — sister concept for payment integrations.
- [[payment-providers-cod]] — standalone COD payment provider (no carrier collection).
- Top carriers — per-app configuration pages: [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]], [[apps-cargus]], [[apps-sameday]], [[apps-dpdbulgaria-speedy]], [[apps-dpdromania]], [[apps-dhl]], [[apps-dhlexpress]], [[apps-gls]], [[apps-acscourier]], [[apps-albanian-courier]].

## Open Questions

- ⏸️ Per-carrier behaviour details (auto re-quote on payment-method change, tracking-webhook vs polling, pallet rules outside Econt) vary across the 30+ shipping integrations. The per-carrier admin screens ([[apps]] → individual shipping-provider pages) document each integration's specifics; this concept page describes the shared mechanism only. Merchants integrating a specific carrier should consult that carrier's dedicated page for behaviour particulars.

All other previously-flagged questions resolved. See the aspect pages for details.
