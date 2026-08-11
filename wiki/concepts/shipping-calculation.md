---
type: concept
aliases: ["Shipping calculation", "Shipping cost", "Delivery cost", "Shipping rate", "How shipping is calculated", "Доставка", "Цена за доставка", "Изчисление на доставка", "Калкулация на доставка"]
tags: [shipping, checkout, geo, couriers, omniship, concepts]
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---

# Shipping calculation

## Definition

**Shipping calculation** is the platform-wide pipeline that decides — for every customer cart at checkout — which shipping methods are *available*, what each one *costs*, and which one is *pre-selected*. The platform takes the customer's **shipping address**, the cart's **subtotal + total weight + product categories + payment method + customer group**, then walks every method from [[settings-shipping]] through a cascade: active toggle → geographic gating → rate-model quote → category-rate split → COD surcharge → allowed-payment filter → customer-group filter → discount + Cart Rule layer → persist on cart/order.

The merchant's mental model: **"I configure WHO ships (the methods), WHERE they ship to (the geo zones), and HOW they price (the rate table OR the carrier's quote)."** The customer picks one of the matching options. Free-shipping promotions layer on top via [[marketing-discounts-shipping]]; partial-shipping overrides ("10 % off shipping") only exist through [[apps-cart-rules]].

Two foundational distinctions thread through the whole pipeline. **Custom methods vs. carrier integrations** — custom methods use merchant-editable **rate-row tables**; carrier integrations ask the carrier's live API (Econt, Speedy, BoxNow, Cargus, etc.) and pass the quote through unchanged. **Free-shipping-as-rate-row vs. free-shipping-as-discount** — a `$0` rate row makes the SHIPPING METHOD free for a bracket; a Free-Shipping discount adds a negative totals line that zeros whatever the carrier quoted.

## Sub-pages (in this cluster)

This concept is split into 8 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[shipping-calc-rate-models]] — the five rate models (`price`, `weight`, `price_and_weight`, `marketplace`, `integration`); rate-row table semantics (`from` inclusive, blank `to` = unbounded, `$0` = free); category-rate split.
- [[shipping-calc-geo-gating]] — Step 2 of the cascade; `target = restofworld` vs `geo_zone`; the 11 zone rule types; polygon point-in-polygon test; spherical-law-of-cosines distance check; country normalization to ISO.
- [[shipping-calc-carrier-integrations]] — the `getQuotes` live-API path; per-carrier behaviour (Econt pallets / weight cap, DPD Bulgaria delivery channels / EUR insurance, BoxNow locker-only, Cargus re-quote on payment switch); multi-currency FX conversion.
- [[shipping-calc-rate-card-fields]] — the per-channel "Delivery price calculation" select and **the fields each type reveals** (processing fee, minimum-order-value for free delivery + free-service selects, the `fixed_*` rate tables, the fallback-price switch, the per-category sub-table) + which of the six types each courier offers.
- [[shipping-calc-cascade]] — the full Step 1–8 checkout cascade; active → geo → rate → category → COD → allowed-payment → customer-group → present; zero-match debug checklist; auto-select-if-only-one rule.
- [[shipping-calc-cod-surcharge]] — COD surcharge mechanics; custom methods (flat fee) vs. carrier integrations (carrier-quoted); the 10,000 BGN COD cap for BG carriers; re-quote on payment-method switch.
- [[shipping-calc-discounts-rules]] — free-shipping discount with `order_over` vs. `$0` rate row; one-shipping-discount-per-cart cap; [[apps-cart-rules]] for percentage / fixed-amount / force-method overrides; Cart-Rules-run-AFTER-Discounts ordering.
- [[shipping-calc-persistence]] — how the chosen method + quote is saved to `cart_shipping_quotes`, copied to the order at checkout, frozen on the order, and re-quoted via the order-detail "Recalculate shipping" action.

## Why it matters to the merchant

Shipping is one of the few systems where misconfiguration silently breaks the storefront — either as **zero-matching-methods checkout errors** or as **wrong-quote complaints** (carrier charges X, customer paid Y). Two non-obvious facts cause most tickets:

- **The cascade is silent.** A method that fails ANY gate simply *disappears* from checkout — no on-screen explanation, no log entry. The debug procedure on [[shipping-calc-cascade]] is the first port of call for "why don't I see Econt at checkout?".
- **Per-method scope is a single value.** Each method has ONE geographic scope (whole world OR one geo zone) and ONE rate model. To offer the same carrier at different prices in different regions, the merchant creates MULTIPLE methods — see [[shipping-calc-geo-gating]].

The other recurring pitfalls are each owned by a sub-page: free shipping is never a global setting (`$0` rate row OR `order_over` discount, see [[shipping-calc-discounts-rules]]); carrier-integration pricing is opaque and merchant-uneditable (see [[shipping-calc-carrier-integrations]]); the quote freezes on the order and only the "Recalculate shipping" action re-quotes it (see [[shipping-calc-persistence]]); and percentage/fixed shipping overrides like "10 % off shipping over 50 BGN" require [[apps-cart-rules]], not Discounts.

## Scope

What this concept covers (across the 8 sub-pages):

- The five rate models + rate-row table semantics + category-rate split.
- Geographic gating (zone, polygon, distance, post-code, country lookup).
- Carrier-integration `getQuotes` mechanics + per-carrier behaviours + multi-currency FX.
- The full 8-step checkout cascade + zero-match debug procedure.
- COD surcharge mechanics + BG 10,000 BGN cap.
- Free-shipping discount vs. `$0` rate row + Cart Rules overrides.
- Quote persistence on cart / order + re-quote pattern.

What it does NOT cover:

- **Waybill generation** (the per-order action of issuing a tracking label and committing the dispatch to the courier) — see [[orders-shipping-waybill]].
- **Address verification** at the customer's checkout step (geocoding, country normalization beyond the ISO step) — see [[checkout-flow]].
- **Pickup time-slot scheduling** — see [[apps-shipping-hours]].
- **Internal carrier-app configuration screens** (credentials, sender data, pallet-rule editors) — see [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]], etc.
- The structural Shipping Provider abstraction — see [[shipping-provider-mechanism]].

## Contrasts

- **Shipping calculation vs. tax computation** — both depend on the customer's address. Tax uses a **single matched VAT rule** (most-recent-created wins on conflict); shipping presents **all matching methods** for the customer to pick. See [[tax-computation]].
- **Custom methods vs. carrier integrations** — merchant-editable rate rows + merchant-set geo scope vs. live-API quote + opaque pricing. See [[shipping-calc-rate-models]] vs. [[shipping-calc-carrier-integrations]].
- **Free shipping (rate row) vs. Free shipping (discount)** — see [[shipping-calc-discounts-rules]].
- **Shipping calculation vs. checkout flow** — calculation is the **arithmetic** of the cost; checkout flow is the **screen** where the customer picks among options. See [[checkout-flow]].
- **Shipping calculation vs. shipping-provider mechanism** — calculation is the runtime price decision; the provider mechanism is the structural abstraction every method registers under. See [[shipping-provider-mechanism]].

## Where it applies

The full application-surface catalogue is on each sub-page; the cross-cutting touchpoints are:

- [[settings-shipping]] — the merchant's shipping-methods hub.
- [[settings-cart]] — checkout defaults (default-shipping-provider, auto-select-if-only-one, COD options, Google Maps API key).
- [[settings-boxes]] — package dimensions feeding volumetric carrier quotes.
- [[checkout-flow]] — customer-facing screen.
- [[orders-shipping-waybill]] — downstream waybill issuance.
- [[orders-details]] — order detail with frozen shipping line + "Recalculate shipping".
- [[order-processing-pipeline]] — fulfillment side-effects fire here.

## Related

- [[settings-shipping]] — shipping-methods hub.
- [[settings-cart]] — checkout defaults + COD options.
- [[settings-boxes]] — package dimensions.
- [[settings-geo-zones]] — geographic gating zones.
- [[geo-polygons-settings-main-new]] / [[settings-geo-distances]] — polygon + radius zones.
- [[checkout-flow]] — customer-facing screen.
- [[orders-shipping-waybill]] — downstream waybill.
- [[orders-details]] — order detail page.
- [[shipping-provider-mechanism]] — structural provider abstraction.
- [[geo-targeting]] — concept covering polygon + distance + zone rule semantics across the platform.
- [[multi-currency]] — FX-rate sourcing for carrier-billed currency conversion.
- [[tax-computation]] — sibling computation also depending on customer address.
- [[order-processing-pipeline]] — downstream fulfillment pipeline.
- [[marketing-discounts-shipping]] — free-shipping discount type.
- [[apps-cart-rules]] — shipping overrides beyond discounts.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-boxnow]] / [[apps-cargus]] / [[apps-sameday]] / [[apps-dhl]] / [[apps-dhlexpress]] — carrier integrations.
- [[apps-shipping-hours]] — delivery-time-slot promises.
- [[customers-custom-groups]] — per-customer-group restrictions.
- [[order-totals-pipeline]] — where the shipping quote lands in the total (stage 4, after goods discounts + VAT-on-goods; COD/payment fee rides here).

## Open Questions

None — all previously-flagged items resolved or distributed to sub-pages. The two open items from the pre-split version (multi-package / split shipments, per-product shipping surcharge) are recorded on [[shipping-calc-rate-models]] and [[shipping-calc-carrier-integrations]] respectively.
