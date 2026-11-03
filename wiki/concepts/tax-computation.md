---
type: concept
nav_path: "Concept → Tax computation"
route_name: (none)
route_path: (none)
aliases: ["Tax computation", "VAT computation", "Tax calculation", "How taxes are computed", "VAT calculation", "Tax engine", "Изчисляване на данък", "Изчисляване на ДДС", "Калкулация на данък", "Данъчно изчисление"]
tags: [taxes, vat, finance, invoicing, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Tax computation

## Definition

How CloudCart figures out the **tax line on every order** — the rate it applies, the amount it withholds, and the explanation it prints on the invoice. The engine supports two pricing models (prices include tax / prices exclude tax), a per-country VAT rate driven by [[settings-geo-zones]], optional per-category and per-region overrides, EU One-Stop-Shop semantics for cross-border B2C sales, separate handling for fees vs VAT, and a frozen-on-order snapshot so historical orders stay accurate even when the merchant edits the rate later.

The engine answers four questions at checkout, in this order: (1) Which tax rules match this customer's location and the products in the cart? (2) Of those, which single VAT-type tax wins? (3) What rate is applied to which line items? (4) Are there any fees that should ALSO stack on top? The result is written to the order as a tax breakdown — per-line + total — and stored as a snapshot.

The merchant's mental model: *"I configure ONE VAT rule per region, tell the platform whether my product prices already include VAT, and let the engine pick the right rule at checkout. For odd cases — books at a reduced rate, fees for cash-on-delivery — I add per-category overrides or Fees."*

This concept is the **tax-engine** (runtime behaviour). The **Tax / Fee management UI** itself (the create / edit / list flow) is a separate page — see [[settings-taxes]].

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[tax-rate-selection]] — VAT rule matching engine; single-winner picker; country-only restriction; regional-beats-RoW; newest-zone-wins tie-breaker.
- [[tax-pricing-models]] — `price_with_vat = 1` (GROSS) vs `price_with_vat = 0` (NET); storefront display + invoice arithmetic.
- [[tax-overrides]] — per-region + per-category override precedence ladder (combined → category-only → region-only → base).
- [[tax-oss-semantics]] — `oss_registration` flag (B2B reverse-charge suppressor, NOT auto destination-rate lookup); manual per-country setup; VIES / APIS validation; *"without VAT reasons"* invoice wording.
- [[tax-address-resolution]] — billing-vs-shipping priority via `invoicing_address`; the under-documented per-order address-priority snapshot.
- [[tax-order-snapshot]] — frozen-on-order `orders_taxes` snapshot; `vat_included`; recompute-on-edit carve-out for `pending` / `paid` / `authorized` orders.
- [[tax-fees-vs-vat]] — `vat = yes` (one winner) vs `vat = no` (additive); the corrected *"VAT applies to fees regardless of `vat = no`"* rule; `shipping` flag bucketing.

## Why it matters to the merchant

- **Legal compliance.** VAT rules differ by country (and sometimes by region within a country); the merchant is legally responsible for charging the correct rate. See [[tax-rate-selection]].
- **Pricing display.** `price_with_vat` controls whether the storefront shows gross or net prices. Wrong setting = wrong storefront prices. See [[tax-pricing-models]].
- **Cross-border EU sales.** OSS requires destination-country rates above the €10,000 threshold. **The `oss_registration` flag does NOT auto-swap to the destination rate** — the merchant must define per-country VAT rules manually. See [[tax-oss-semantics]].
- **B2B reverse charge** for VAT-registered EU buyers via VIES. See [[tax-oss-semantics]].
- **Historical accuracy.** Tax rates change; the platform snapshots the applied tax onto each order at creation. See [[tax-order-snapshot]].
- **Multi-currency exposure.** Percentage taxes are currency-independent; flat taxes need conversion. See [[multi-currency]] and [[tax-order-snapshot]].

## Scope

What this concept covers (across the 7 sub-pages):

- The two pricing models and how each affects storefront display + invoice rendering.
- The VAT tax-matching engine (geo-scope, country-only, regional-beats-RoW, newest-wins).
- Per-region + per-category overrides (precedence ladder).
- Fees — additive stacking, payment/shipping scoping, VAT-on-fee behaviour.
- EU OSS semantics + B2B reverse charge via VIES-validated VAT numbers.
- VAT validation against APIS (BG), VIES (EU), and format-check for GB / CH.
- *"Without VAT reasons"* wording on invoices for EU vs non-EU zero-rated sales.
- Order snapshot — frozen at creation; later edits don't retroactively re-tax.
- Currency interaction (percentage vs flat; FX rate at order-creation time).

What it does NOT cover:

- The **Tax / Fee management UI** itself — that's [[settings-taxes]].
- The **invoice rendering** of the breakdown — that's [[settings-invoicing]] and [[orders-invoice]].
- The merchant's own VAT registration with CloudCart (CloudCart billing the merchant) — that's [[billing-invoicing]].
- The **discount mechanism** in the same totals pipeline — that's [[marketing-discounts]] / [[discount-stacking]].
- The **shipping cost calculation** — that's [[shipping-calculation]] (though tax can bucket via the `shipping` flag — see [[tax-fees-vs-vat]]).

## Contrasts

- **Tax vs Fee** — `vat = yes` is a jurisdiction-bound VAT rule (one winner); `vat = no` is a fee (all matching stack). See [[tax-fees-vs-vat]].
- **Tax-zone matching vs shipping-zone matching** — VAT only sees country rules; [[shipping-calculation]] sees the full geo-zone scope. See [[tax-rate-selection]].
- **Newest-zone-wins vs most-specific-zone** — there is NO most-specific logic. See [[tax-rate-selection]].
- **OSS on vs OSS off** — suppresses B2B reverse-charge, does NOT swap to destination-country rates. See [[tax-oss-semantics]].
- **GROSS vs NET pricing** — the entire storefront-display layer hinges on `price_with_vat`. See [[tax-pricing-models]].
- **B2C vs B2B EU sale** — B2B EU with valid VIES → reverse charge zero-rating (unless OSS on). See [[tax-oss-semantics]].
- **Tax computation vs tax snapshot** — the engine recomputes at every cart/checkout render; once the order is placed, the result is SNAPSHOTTED. See [[tax-order-snapshot]].

## Where it applies

- [[settings-taxes]] — Tax / Fee management screen (the runtime engine reads this).
- [[settings-geo-zones]] — geographic scoping (country-only matching for VAT).
- [[settings-invoicing]] — invoice rendering with the tax breakdown + *"without VAT reasons"* wording.
- [[settings-cart]] — `invoicing_address` + `checkout_validate_company_vat`.
- [[settings-general]] — `operation_country` default jurisdiction.
- [[order]] / [[orders-details]] / [[orders-invoice]] / [[orders-credit]] / [[orders-receipt]] — all carry / read the snapshot.
- [[checkout-flow]] — where the engine fires.
- [[product]] — prices entered in the chosen pricing model.
- [[category]] — drives per-category overrides.
- [[order-processing-pipeline]] — tax computation happens at Stage 1; snapshot preserved through the pipeline.

## Related

- [[settings-taxes]] — management screen.
- [[settings-geo-zones]] — geographic scoping.
- [[settings-invoicing]] — invoice rendering.
- [[settings-cart]] — `invoicing_address`, `checkout_validate_company_vat`.
- [[settings-general]] — `operation_country`.
- [[settings-payment-providers]] / [[settings-shipping]] — fee scoping.
- [[order]] / [[orders-invoice]] / [[orders-credit]] / [[orders-receipt]] — snapshot carriers.
- [[billing-invoicing]] — the merchant's own invoicing setup (CloudCart billing the merchant — separate from store-side invoicing).
- [[tax]] — entity page.
- [[multi-currency]] — currency conversion for flat fees.
- [[checkout-flow]] — where the tax engine fires.
- [[geo-targeting]] — geo scoping mechanics.
- [[shipping-calculation]] — separate computation; `allow_modify_vat` decides VAT-on-shipping.
- [[discount-stacking]] — discounts interact with the post-tax total.
- [[order-processing-pipeline]] — tax computation happens at Stage 1; tax-line snapshot in the webhook payload.
- [[order-totals-pipeline]] — where VAT lands in the total: VAT-on-goods (stage 3) and VAT-on-shipping (stage 5) are separate stages.

## Open Questions

- ⏸️ **OSS threshold tracking is NOT a CloudCart feature.** EU merchants exceeding the OSS distance-selling threshold must register for OSS via their tax authority and reconcile manually — CloudCart does not auto-detect when the threshold is crossed nor automatically switch to OSS-rate VAT. See [[tax-oss-semantics]].
- ⏸️ **Tax bulk-export for accounting is NOT a current feature.** There is no one-click *"export all orders with tax breakdown by country"* report today. See [[tax-order-snapshot]].

All other previously-flagged questions resolved. See sub-pages for details.
