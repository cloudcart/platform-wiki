---
type: concept
nav_path: "Concept → Shipping provider mechanism → Geo routing & multi-currency"
aliases: ["Geo zone routing", "Shipping geo gating", "Multi-currency carrier conversion", "FX at carrier-call time", "Geo zone per method", "Гео зона за метод", "Гео гейтване на доставка", "Валутна конверсия за куриер"]
tags: [shipping, couriers, providers, geo, multi-currency, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 2
---

> Part of [[shipping-provider-mechanism]]. See the hub for the other aspects (configuration, pricing models, pickup points, waybill, COD, status tracking).

# Shipping provider mechanism — Geo routing & multi-currency

## Definition

**Geo routing** is the per-method filter that decides whether a shipping option is even shown to a particular customer based on their delivery address. **Multi-currency conversion** is the per-API-call FX step that translates monetary amounts into whatever currency the carrier bills in. Both are *gating* concerns — they decide before pricing whether a method participates in the customer's checkout, and they ensure the carrier receives amounts in a currency it understands.

For custom methods, the merchant picks a Geo Zone per method. For carrier-integration methods, the carrier's API decides coverage, within an optional Geo Zone the merchant sets on the courier's **Ships to** box. For multi-currency stores, the platform converts COD / insurance / subtotal amounts on the fly when calling carriers like Speedy (BGN) or Cargus (RON).

## Scope

Covered:

- Geo zone routing for custom methods (one zone per method).
- Carrier-API coverage decisions for integration methods.
- Multi-currency conversions at carrier-call time.
- The currency-aware behaviour of the COD cap.
- How a non-matching method disappears from the checkout candidate list.

Not covered:

- Geographic zone definitions (Geo Zone rules, polygons, distance from a point) — see [[settings-geo-zones]], [[settings-geo-distances]], [[geo-polygons-settings-main-new]], [[geo-targeting]].
- The full shipping-calculation cascade — see [[shipping-calc-cascade]] and [[shipping-calc-geo-gating]].
- The COD cap itself (the 10,000 BGN number) — see [[shipping-provider-mech-cod]].
- The order's currency snapshot — see [[multi-currency]].

## Contrasts

- **Custom method vs. carrier integration**: both can have ONE Geo Zone picked by the merchant, checked locally against the customer's address. An integration method then also needs the carrier's API to return a quote for the destination; if it rejects, the method silently disappears from checkout.
- **Geo gating (filter) vs. shipping pricing (arithmetic)**: gating decides whether a method is a candidate at all. Pricing decides what the candidate costs once it is. The cascade runs gating first, then pricing — see [[shipping-calc-cascade]].
- **Store currency (display) vs. carrier billing currency (API)**: the order is *stored* in the store's currency (snapshotted at checkout per [[multi-currency]]). The carrier API call uses the carrier's *billing* currency. The conversion is one-way and transparent — merchants don't see the converted amount in the admin UI.

## Where it applies

### Geo zone routing for custom methods

For custom methods, each method has ONE geographic scope:

- **The whole world** — the method appears for any customer address.
- **A specific Geo Zone** — the method appears only for customers whose address matches at least ONE rule in that zone. Rules within a zone are OR-combined. Zones can have multiple rule types: country, region, city, postcode pattern, polygon shape, distance from a center point. See [[settings-geo-zones]].

A method that doesn't match the customer's shipping address is excluded from the candidate list at checkout. The cascade for which methods survive the filter is documented in [[shipping-calc-geo-gating]].

### Carrier-API coverage for integration methods

For carrier-integration methods, the courier's settings screen has a **Ships to** box (all couriers except Glovo): the switch **Set custom shipping regions** off means everywhere; on, a Geo Zone is picked and the method appears only for addresses in that zone, and offices and lockers outside the zone are hidden from the pickup list. Within that, the carrier's API decides coverage. The platform sends the destination to the carrier's `getQuotes` API; if the carrier returns one or more service options, the method is a candidate. If the carrier rejects the address (out of service area, embargoed country, locker not in range, etc.), the method is **silently dropped** at checkout for that customer.

The "Deliver to" column in [[settings-shipping]] still reads *"Regions are determined by the provider"* for every integration method, even one limited by a **Ships to** zone; the zone is edited on the courier's own screen.

### Multi-currency conversions at carrier-API call time

For multi-currency stores, the platform converts amounts to the carrier's billing currency at the time of the API request. Common cases:

- **Speedy** requires amounts in BGN (Speedy's billing currency); for a store in EUR or RON, the platform converts COD / insurance / subtotal to BGN using the internal Fixer.io-synced FX rate before calling Speedy.
- **Cargus** requires amounts in RON; for a non-RON store, the platform converts to RON.
- **DHL** typically supports multi-currency directly — no platform-side conversion needed.
- **BoxNow, GLS, DPD** — verify per carrier.

The order's currency stays in its original currency (snapshotted at checkout per [[multi-currency]]); the conversion is only for the carrier's API request. Merchants don't see the converted amount in the admin UI — it's transparent.

### Currency-aware COD cap

The COD cap (10,000 BGN for Bulgarian carriers, documented in [[shipping-provider-mech-cod]]) is enforced **only when the store currency is BGN**. For non-BGN stores, no platform-side cap applies — the carrier's own server-side limits take over. The platform reads the store currency at quote time and applies the cap conditionally.

### When a method disappears from the candidate list

A method is excluded from the checkout candidate list when:

- **Custom method**: the customer's address doesn't match the assigned Geo Zone.
- **Integration method**: the address is outside its **Ships to** zone, or the carrier's API rejects the destination (silent drop).
- **Either**: Cart Rules ([[apps-cart-rules]]) explicitly hide it; the customer's [[customers-custom-groups|customer group]] isn't in the allowed list; the method is toggled Inactive in [[settings-shipping]].

See [[shipping-calc-cascade]] for the full filter sequence the cart runs through.

## Related

- [[shipping-provider-mechanism]] — hub.
- [[shipping-calc-cascade]] — the full filtering cascade.
- [[shipping-calc-geo-gating]] — the geo-gating step of the cascade.
- [[settings-geo-zones]] / [[settings-geo-distances]] / [[geo-polygons-settings-main-new]] / [[geo-polygons-settings-main-new]] — define the regions.
- [[geo-targeting]] — cross-cutting geo concept.
- [[shipping-provider-mech-pricing-models]] — pricing once gating passes.
- [[shipping-provider-mech-cod]] — currency-aware COD cap referenced here.
- [[multi-currency]] — store currency snapshot + FX-rate source.
- [[settings-cart]] — store-wide shipping defaults.

## Open Questions

- ⏸️ For carrier integrations, the platform may convert COD / insurance / subtotal to the carrier's billing currency. The exact list of carriers needing conversion vs. accepting multi-currency natively is partially documented (Speedy, Cargus confirmed; others need verification).
