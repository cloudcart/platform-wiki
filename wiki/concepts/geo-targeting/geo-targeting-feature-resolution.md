---
type: concept
nav_path: "Concept → Geo targeting → Feature resolution"
aliases: ["Per-feature zone resolution", "Multi-match resolution", "Tax country-only matching", "Most-recent-wins tax", "Shipping multi-match", "Fees stack", "Discount stacking by zone", "Zone overlap behaviour"]
tags: [shipping, tax, fees, discounts, geo, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[geo-targeting]]. See the hub for the other aspects (zones, polygons, distances, post-codes, IP detection, address resolution).

# Geo targeting — Feature resolution

## Definition

A customer's address can match **multiple zones** simultaneously. How that ambiguity is resolved depends on **which feature is asking** — the geo-targeting layer does the matching, but each consuming feature applies its own selection / stacking semantics on top.

There are also feature-specific **scope restrictions** on what counts as a match — most importantly, the tax engine ignores all non-country operations inside a zone.

## Scope

Covered:

- The per-feature multi-match resolution table (shipping, tax-VAT, tax-fees, discounts, customer groups, Cart Rules).
- The **country-only matching rule for tax** — the single most common merchant misconfiguration.
- "Rest of world" fallback semantics.
- Design implications (when to overlap zones intentionally).

Not covered:

- The actual shipping cascade or carrier-quote integration — see [[shipping-calculation]].
- The VAT formula or VIES validation — see [[tax-computation]].
- The discount stacking algorithm itself — see [[discount-stacking]].

## Contrasts

- **Most-recent-wins (tax-VAT) vs all-shown (shipping) vs additive (fees, discounts)** — the same multi-match address, three different resolutions per feature. The merchant must design zones with the consuming feature in mind.
- **Tax country-only vs shipping every-rule-type** — tax sees only operations 1 and 4 (and the country sub-component of compound rules); shipping evaluates every rule type. A zone with no country rule works for shipping but never matches a tax.
- **Most-specific-wins (intuitive) vs most-recently-created-wins (actual)** — for VAT, the platform does NOT pick the most specific rule. It picks the most recently created rule among matching ones. (verify)

## Per-feature multi-match resolution

| Feature | Resolution |
|---------|-----------|
| **Shipping methods** | ALL matched methods are presented to the customer. Customer picks one. Two methods bound to two zones that both match → both shown. See [[shipping-calculation]]. |
| **Tax rules (VAT)** | EXACTLY ONE rule applies. Regional rules beat rest-of-world. Between two regional rules that both match, the most recently created wins. See [[tax-computation]]. |
| **Tax rules (Fees)** | ALL matched fees stack additively. Three fees match → three separate fee lines. |
| **Discount targets** | A customer who matches multiple geo-scoped discounts can have all of them applied (subject to [[discount-stacking]] rules). |
| **Customer groups** | One group is in effect per customer; the merchant's group-assignment logic decides which one wins. |
| **Cart Rules** | All matching rules fire in their configured order. See [[apps-cart-rules]]. |

## Design implications

- For **tax**, avoid overlapping zones — since only one wins, redundant rules just cost maintenance. Design zones to be non-overlapping per-product-category.
- For **shipping**, overlapping zones are FINE — they produce multiple shipping options the customer chooses from. Intentional overlap can be a feature.
- For **discounts** with stacking enabled, overlapping zones can compound discounts. Intentional or accidental — verify against [[discount-stacking]] when designing.
- For **fees**, overlap means additive stacking. Three matching surcharges = three line items. Usually you want non-overlapping fee zones.

## Tax sees ONLY country-level matches — the single biggest gotcha

A subtle but critical rule: **for tax matching, the platform looks only at country rules (operations 1, 4 — and the country sub-component of compound rules)** inside the zone. The richer geo-zone operations (region, city, neighborhood, polygon, distance, post-code) are **IGNORED by the tax engine**.

Consequence: a zone like *"only Sofia city in Bulgaria"* (operation 5 alone) with no separate country rule matches NO tax rule. To use that zone for both tax AND shipping, the merchant either:

1. Adds a separate country rule (operation 1: includes Bulgaria) to the same zone, OR
2. Creates two zones — one for tax with the country rule, one for shipping with the city rule.

This is the single most common merchant misconfiguration in geo-targeting. It is documented in [[settings-taxes]] and [[tax-computation]] under "Country-level matching only".

## "Rest of world" fallback

Every customer who doesn't match any specific zone falls back to features scoped to `target = restofworld`. A typical store therefore has:

- Specific zones for major markets (EU member states, USA, etc.).
- A rest-of-world fallback tax rule (often 0% with a "Export outside EU" note).
- A rest-of-world fallback shipping method (e.g., "International parcel" via a carrier that ships globally).

Without the fallback, customers from unconfigured countries see no shipping method and can't complete checkout.

## Example — overlapping zones and the consumer feature

Two zones, both match Sofia:

- "Bulgaria" — country rule only (operation 1, BG).
- "Sofia delivery" — city rule (operation 5) + country rule (operation 1, BG).

Resolution:

- **Tax (VAT)** — with both having a VAT rule, the **newest wins**. If "Sofia delivery"'s VAT rule was created last, that one applies; otherwise the "Bulgaria" rule. No "most-specific" logic.
- **Shipping** — if both zones have shipping methods bound to them, BOTH methods appear at checkout. Customer picks.
- **Discounts** — if both zones have discount restrictions matching, both discounts can apply (subject to [[discount-stacking]] rules).

## Example — Sofia metro polygon needing a country pair for tax

A polygon-based zone "Sofia metro" containing only operation 9 (polygon = "Sofia + suburbs") works for shipping but matches no tax. Adding operation 1 (country = BG) to the same zone makes tax matching work without breaking shipping (the polygon and country rules are OR-combined; the customer still falls inside the polygon for the shipping side). See [[geo-targeting-polygons]] for the worked example.

## Where it applies

- [[shipping-calculation]] — all-matched, customer chooses.
- [[tax-computation]] — country-only, most-recent-wins.
- [[discount-stacking]] — multi-zone discounts can compound subject to stacking.
- [[settings-taxes]] / [[settings-shipping]] / [[marketing-discounts]] / [[settings-payment-providers]] / [[apps-cart-rules]] — the consuming features.

## Related

- [[geo-targeting]] — hub.
- [[geo-targeting-zones]] — zone rules and operations referenced by this resolution layer.
- [[shipping-calculation]] — shipping cascade.
- [[tax-computation]] — tax matching and rate selection.
- [[discount-stacking]] — discount stacking algorithm.
- [[settings-taxes]] — tax-rule configuration (Country-level matching only).
- [[settings-shipping]] — shipping-method configuration.
- [[settings-payment-providers]] — fees stacking by zone.
- [[marketing-discounts]] — discount geo-scoping.
- [[customers-custom-groups]] — customer-group region restrictions.
- [[apps-cart-rules]] — geo-conditional Cart Rules.

## Open Questions

- ⏸️ **VAT tie-break logic.** Documented as "most recently created wins" between two matching regional rules. (verify whether the platform uses `created_at` or another ordering field on the tax rule record)
