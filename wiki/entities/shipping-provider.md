---
type: entity
nav_path: "Entity → Shipping Provider"
aliases: ["Shipping Provider", "Shipping carrier", "Courier", "Courier integration", "Shipping integration", "Shipping method provider", "Delivery provider", "Доставчик", "Куриер", "Куриерска фирма", "Метод за доставка"]
tags: [entity, shipping, couriers, providers, integrations, settings]
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---

# Shipping Provider

## Identity

A **Shipping Provider** is a configured courier / delivery integration on the merchant's store — Econt, Speedy, BoxNow, Cargus, Sameday, DPD Bulgaria, DPD Romania, DHL, DHL Express, GLS, Fan Courier, ACS Courier, Albanian Courier, Bulgarian Posts, plus 15+ more. Each provider, once installed and activated in [[settings-shipping]] (or from the Apps catalog filtered to category 4), exposes one or more shipping methods at the storefront checkout — the customer picks one to receive the parcel. CloudCart ships 30+ courier integrations covering Bulgarian / Romanian / Greek / Cypriot / Croatian / Albanian / international networks.

A Shipping Provider is the **configuration record** — one row per installed courier per store — that carries the merchant's API credentials, sender address book, allowed delivery channels (to address / to office / to locker), COD agreement number, pallet rules (where applicable), and the per-provider activation state. It is distinct from a single [[shipping-status]] (the *state* of one parcel on one order) and from a per-order shipping line (the actual chosen method + price snapshot on that order). The Shipping Provider is what the merchant edits in admin; the per-order shipping rows and waybill records are what get written each time a customer checks out and the merchant dispatches. See [[shipping-provider-mechanism]] for the shared lifecycle every courier follows.

## Aliases

- **Shipping Provider** — canonical term in the admin UI and across the wiki.
- **Shipping carrier** / **Courier** — used interchangeably; the customer-facing word is often "delivery method" or "shipping method".
- **Courier integration** / **Shipping integration** — emphasises the third-party API connection.
- **Delivery provider** — alternate phrasing in some legal / contract surfaces.
- **Доставчик** / **Куриер** / **Куриерска фирма** / **Метод за доставка** — Bulgarian equivalents.

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[shipping-provider-attributes]] — the configuration fields the merchant edits: Provider code, Storefront name, Active toggle, credentials, sender address book, allowed delivery channels, COD agreement number, pallet rules, pricing-model type. Includes save-time field normalisation.
- [[shipping-provider-lifecycle]] — the six states (Available → Installed → Configured → Active → Suspended → Uninstalled), credential validation, permanent Type, delete protection, cascade cleanup of shipping-hours / external-provider / meta rows.
- [[shipping-provider-pricing-models]] — the three pricing patterns: live API quote (`integration`), rate rows (`price` / `weight` / `price_and_weight`), Local Pickup / Fixed flat (`marketplace`). Plus category-rate split, multi-currency conversions, Econt-only pallet rules.
- [[shipping-provider-checkout-filters]] — Geo Zone scope, allowed-payment-methods filter, customer-group restrictions, country-default Recommended filter, default selection, *"Automatically select shipping if only one is available"* toggle, Cart Rules override, per-carrier re-quote-on-payment-change.
- [[shipping-provider-cod]] — COD surcharge, **10,000 BGN cap** (currency-aware), automatic COD-paid sync via [[orders-sync-cod]], the three preconditions, silent drop of outdated COD agreements.
- [[shipping-provider-delivery-channels-waybill]] — three delivery channels (to address / to office / to locker), BoxNow locker-only, Econt 1,000 kg office cap, pickup-point picker, waybill generation via [[orders-shipping-waybill]], webhook vs poll tracking, no native multi-package split.

## Key Attributes

For the full field-by-field table see [[shipping-provider-attributes]]. High-level shape:

- **Identity & display** — Provider code (`econt` / `speedy` / `boxnow` / etc.), Storefront name, Logo, Active toggle.
- **Auth** — Credentials (username + password, client ID + secret, or API key; carrier-specific).
- **Sender side** — Sender address book.
- **Customer side** — Allowed delivery channels (`to_address` / `to_office` / `to_locker`), pickup-point cache window.
- **COD** — COD agreement number, COD-sync toggle.
- **Pricing** — Pricing model (`integration` / `price` / `weight` / `price_and_weight` / `marketplace`), category-rate split (Custom only), Econt-only pallet rules, insurance, additional services.
- **Targeting** — `target` (`regions` / `restofworld`), `geo_zone_id` (Custom only), allowed-payments multi-select, allowed-customer-groups multi-select (Custom only).

## Relationships

A Shipping Provider **has many** shipping methods (e.g. "Econt to address" + "Econt to office" as two rows). It is **referenced by** the [[order|Order]] (shipping line) and the [[cart|Cart]] (in-progress selection). It is **scoped / filtered by** [[settings-geo-zones|Geo Zones]], [[payment-provider|Payment Provider]] (allowed-payments list), [[customer-group|Customer Group]], and [[category|Category]] — see [[shipping-provider-checkout-filters]] + [[shipping-provider-pricing-models]]. It **drives** [[shipping-status]] transitions via carrier webhooks / polling (see [[shipping-provider-delivery-channels-waybill]]) and [[payment-status]] for COD orders (see [[shipping-provider-cod]] + [[orders-sync-cod]]).

A Shipping Provider is NOT the same as [[shipping-status]] (parcel-state enum), a per-order shipping line (one captured quote), or [[payment-provider]] (sister entity for payment integrations).

## Where it appears

- [[settings-shipping]] — the central hub: every installed shipping method as a row, plus the "Browse shipping integrations" modal listing every available carrier for the merchant's country.
- [[apps]] — the apps catalog (the "View more Shipping methods" link from [[settings-shipping]] navigates here, filtered to category 4).
- Per-carrier app pages — one page per courier:
  - **Bulgarian carriers**: [[apps-econt]] (dominant), [[apps-dpdbulgaria-speedy|Speedy]], [[apps-boxnow]] (also RO / GR / CY / HR), [[apps-dpdbulgaria-speedy]].
  - **Romanian carriers**: [[apps-cargus]], [[apps-sameday]], [[apps-dpdromania]], [[apps-fancourier]].
  - **International**: [[apps-dhl]], [[apps-dhlexpress]], [[apps-gls]].
  - **Other regional**: [[apps-acscourier]], [[apps-albanian-courier]].
- [[orders-details]] — per-order edit hub; the shipping section shows the chosen carrier + delivery channel + pickup point + any COD / insurance flags.
- [[orders-shipping-waybill]] — the per-order action that calls the carrier's waybill API.
- [[orders-sync-cod]] — the COD-sync sub-flow that marks the order paid when the carrier reports the COD collected.
- [[checkout-flow]] — where the customer picks one of the active shipping methods.
- [[settings-cart]] — defaults (default carrier, auto-select toggle, COD options).
- [[settings-boxes]] — package dimensions used by carrier-integration weight / volumetric calculations.
- [[settings-statuses]] → Shipping tab — merchant renames shipping-status labels (underlying enum unchanged).

## Related

### Related entities

- [[shipping-status]] — the canonical enum every courier's tracking events map into.
- [[order]] — every non-digital Order has a shipping line associated with one Shipping Provider.
- [[cart]] — the customer's in-progress checkout, carrying the picked shipping method before order creation.
- [[payment-provider]] — sister entity; both are third-party integrations gated at checkout.
- [[customer-group]] — groups can restrict shipping methods per loyalty tier.
- [[geo-zone]] — Custom methods are scoped by Geo Zones.
- [[settings-boxes]] — package dimensions fed into carrier weight / volumetric calculations.

### Cross-cutting concepts

- [[shipping-provider-mechanism]] — the shared lifecycle every courier follows (configure → activate → quote at checkout → waybill on fulfillment → sync delivery status).
- [[shipping-calculation]] — the full arithmetic of how the chosen shipping cost is computed.
- [[checkout-flow]] — the cart-to-order transition where the shipping method is selected.
- [[multi-currency]] — FX-rate conversions for carrier API calls (Speedy = BGN, Cargus = RON, etc.).
- [[payment-provider-mechanism]] — sister concept for payment integrations.
- [[geo-targeting]] — geographic gating used by Custom methods.

### Settings & webhooks

- [[settings-shipping]] — the central shipping-methods hub.
- [[settings-cart]] — checkout defaults (default carrier, auto-select toggle, COD options).
- [[settings-statuses]] — the Shipping tab lets the merchant rename shipping-status labels.
- [[settings-hooks]] — shipping-status changes are part of the `order.updated` webhook payload.
- [[settings-boxes]] — package-dimension defaults feeding carrier integrations.

## Open Questions

None at the hub level — outstanding sub-questions live on the specific aspect pages.
