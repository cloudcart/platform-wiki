---
type: concept
nav_path: "Concept → Tax computation → Rate selection"
aliases: ["Tax rate selection", "VAT rule matching", "Tax rule picker", "Newest-zone-wins", "Country-only tax matching", "VAT single-winner"]
tags: [taxes, vat, finance, matching, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax-computation]]. See the hub for the other aspects (pricing models, overrides, OSS, address resolution, order snapshot, fees-vs-VAT).

# Tax — rate selection

## Definition

The single-winner pick that the engine performs to decide **which VAT-type [[settings-taxes]] row applies** to a given order. The matcher walks every `vat = yes` rule, filters by the customer's resolved address (see [[tax-address-resolution]] for which address it reads), and returns exactly **one** rule. Fees are a separate additive flow — see [[tax-fees-vs-vat]].

## Scope

Covered:

- The filter chain: collect → geo-scope → sort → pick first.
- The **country-only** matching restriction for VAT.
- **Regional beats rest-of-world** — non-null `geo_zone_id` always sorts ahead of null.
- **Newest-zone-wins** tie-breaker between two overlapping regional zones.
- The "VAT can't see polygons / cities / post-codes" gotcha.

Not covered here:

- Which address the matcher reads (billing vs shipping) — see [[tax-address-resolution]].
- The per-line override layer that runs AFTER the winner is picked — see [[tax-overrides]].
- OSS's effect on the matched rule's B2B behaviour — see [[tax-oss-semantics]].
- Fees (additive, no single-winner pick) — see [[tax-fees-vs-vat]].

## The filter chain

When an order is placed, the platform finds the applicable VAT rule through this chain:

1. **Collect** every Tax / Fee row where `vat = yes`. Fees (`vat = no`) are routed to the additive fee flow instead.
2. **Filter by geographic scope.** For rules with `target = regions`, the customer's resolved address must fall inside the rule's `geo_zone_id`. Rules with `target = restofworld` match every address as a fallback.
3. **Sort by `geo_zone_id` DESC and take the first.**

That third step encodes two distinct rules:

- **Regional always beats rest-of-world.** Regional rules have a non-null `geo_zone_id`; rest-of-world has `null`, which sorts last under DESC. (verify)
- **Newest zone wins on overlap.** When two regional rules both match the same address, the one attached to the geo zone with the **highest `geo_zone_id`** wins. Because zone IDs are auto-incrementing, this approximates *"most recently created zone wins"* — but it's the **zone** that's most recently created, not the tax rule. Editing a tax rule's name or rate does NOT change which rule wins; only the underlying zone's creation order matters.

## Contrasts

- **Single VAT winner vs additive fee stacking** — VAT picks ONE, fees apply ALL. See [[tax-fees-vs-vat]].
- **Newest-zone-wins vs most-specific-zone** — there is NO most-specific logic. Two zones both containing country `BG` (one zone for "BG", another for "BG + RO") that both have VAT rules attached produce *whichever zone has the higher ID wins*, regardless of how broadly defined. This surprises merchants used to most-specific-wins logic from shipping engines or DNS.
- **Tax-zone matching vs shipping-zone matching** — the tax engine looks ONLY at country rules inside a zone. The [[shipping-calculation]] engine looks at every rule type (country, region, city, polygon, distance, post-code, neighbourhood). A zone built purely from city / polygon / post-code rules with no country rule works for shipping but **never** matches a tax.

## Country-only matching for VAT

Within a matched zone, **only the COUNTRY rule in the zone counts for VAT matching**. The richer geo-zone operations (region, city, neighborhood, polygon, distance, post-code) are evaluated by [[shipping-calculation]] and discount targeting BUT NOT by the VAT engine. A zone like *"only Sofia city"* (operation 5) with no country rule matches **no VAT**. Merchants must always include at least one country rule in any zone used for VAT.

**Different pathway for fees:** the country-only restriction applies to VAT. **Fees use the full geo-zone scope** (all 11 zone-value operations — country, region, city, polygon, distance, post-code) — so a fee can target *"Sofia city only"* and it will fire when the customer's address resolves to a Sofia-area cart. See [[tax-fees-vs-vat]] for the asymmetry.

## Overlapping-zones gotcha

Setup:

- Two VAT rules both match Bulgaria: one created last year at 20%, one created last week at 22%.

Result:

- The platform picks the **newest** (22%) by default. The older rule is ignored.
- To revert: delete the 22% rule, then RE-CREATE the 20% rule (its creation date is now the newest).
- Merchant tip: avoid overlapping zones for the same product / region. Aim for one rule per (region, category) combination.

## "Sofia city only" gotcha

Setup:

- Merchant creates a zone "Sofia city only" using operation 5 (city), with no country rule.
- Tax rule scoped to that zone.

Result:

- The tax NEVER matches any customer — the tax engine only evaluates country-level rules in zones.
- To fix: **add** a country rule (operation 1: includes Bulgaria) to the same zone, or use a separate "Bulgaria" zone for the tax and keep "Sofia city only" for shipping / discounts.

## Where it applies

- [[settings-taxes]] — the rule list the matcher reads from.
- [[settings-geo-zones]] — the zone whose `geo_zone_id` is the sort key.
- [[checkout-flow]] — where the matcher fires for the customer's cart.
- [[orders-details]] — order edits re-run the matcher (but the original snapshot is preserved per [[tax-order-snapshot]]).

## Related

- [[tax-computation]] — hub.
- [[settings-taxes]] — management screen for VAT rules.
- [[settings-geo-zones]] — geographic scoping.
- [[shipping-calculation]] — uses the full geo-zone scope, unlike VAT.
- [[geo-targeting]] — geo scoping mechanics.

## Open Questions

None.
