---
type: concept
nav_path: "Concept → Geo targeting"
route_name: (none)
route_path: (none)
aliases: ["Geo targeting", "Geographic targeting", "Geo zones", "Geo polygons", "Geo distances", "Location-based rules", "Geo-targeting (zones, polygons, distances)", "Гео таргетиране", "Географско таргетиране", "Гео-зони", "Гео полигони", "Гео разстояния"]
tags: [shipping, tax, geo, zones, polygons, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Geo targeting

## Definition

**Geo targeting** is the set of mechanisms CloudCart provides for deciding whether a customer is **"in scope"** for a shipping method, a tax rule, a discount, a fee, or a customer-group restriction — based on the customer's address (country, region, city, neighborhood, polygon shape, distance from a point, post-code pattern) or the visitor's detected IP.

The merchant's mental model: *"I draw the shapes once (Polygons / Distances), I assemble them with country / region / city / post-code rules into named Zones, and I attach the Zones to shipping methods, tax rules, discounts, fees, and customer-group restrictions. At runtime the platform resolves the customer's address against the zone's rules and gates the feature accordingly."*

Three building blocks combine to express any geographic rule a merchant needs:

1. **[[settings-geo-zones|Geo Zones]]** — named collections of one or more location rules. A zone is the merchant's label ("EU", "Sofia city", "Bulgaria except Sofia") and the underlying rules that make it concrete. Rules within a single zone are OR-combined. Zones are the primary unit other features reference. See [[geo-targeting-zones]].
2. **[[geo-polygons-settings-main-new|Geo Polygons]]** — merchant-drawn shapes on a Google Map. Each polygon has a set of coordinates defining its boundary. Used when neither administrative regions nor distance circles match the delivery area. See [[geo-targeting-polygons]].
3. **[[settings-geo-distances|Geo Distances]]** — a center point + radius in **meters**. Used when the merchant wants "deliver within X km of point Y" (local delivery, food, on-demand). See [[geo-targeting-distances]].

Polygons and Distances are **inputs to Zones** — they're referenced by zone rules (operation 9 polygon, operation 10 distance), not used directly by shipping / tax / discount features. The merchant builds the primitive shape ONCE and references it from multiple zones if needed.

Two further pieces complete the system: **[[geo-targeting-ip-detection|MaxMind IP detection]]** seeds storefront defaults before the customer enters an address, and **[[geo-targeting-feature-resolution|per-feature resolution]]** decides how multi-match ambiguity is handled differently by each consuming feature.

## Sub-pages (in this cluster)

This concept is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[geo-targeting-zones]] — the primary unit; the **11 operation types** for zone rules (countries / regions / cities / neighborhoods / polygons / distances / post-codes plus exclusion variants); OR-semantics inside and across zones; the AND-of-locations workaround.
- [[geo-targeting-polygons]] — merchant-drawn shapes on Google Maps; point-in-polygon matching; spatial geometry storage; self-intersection caveats.
- [[geo-targeting-distances]] — center+radius circles; great-circle (spherical law of cosines) matching; the **radius-is-in-meters** gotcha; multi-warehouse OR-pattern.
- [[geo-targeting-post-codes]] — operation 11 pattern syntax: exact / wildcard (`*`) / range (`<from>....<to>`, four dots, numeric only); country pairing.
- [[geo-targeting-ip-detection]] — MaxMind IP-to-country for pre-login storefront defaults (currency, tax display, customer group); ISO 3166-1 alpha-2 country normalisation; VPN / proxy reliability caveats.
- [[geo-targeting-feature-resolution]] — per-feature multi-match resolution (shipping all-shown, tax most-recent-wins, fees additive, discounts can stack); the **country-only rule for tax matching**; "rest of world" fallback.
- [[geo-targeting-address-resolution]] — which address each feature reads (shipping vs `invoicing_address`); Google Maps Places autocomplete + auto-heal; static dataset fallback; zone names not per-language translatable; performance.

## Scope

What this cluster covers (across the 7 sub-pages):

- The **three building blocks** (Geo Zones, Geo Polygons, Geo Distances) and the **11 zone-rule operation types**.
- **Post-code pattern syntax** (exact / wildcard / range).
- **IP-based geo detection** via MaxMind for pre-login storefront pre-filling and **country normalisation** to two-letter ISO 3166-1 alpha-2 codes.
- **Per-feature resolution differences** when multiple zones match (shipping shows all, tax picks one, fees stack additively, discounts may stack) and the **country-only rule for tax matching**.
- **Google Maps integration** (Places autocomplete, draw-on-map, center-pin) + the static dataset fallback.
- Which **customer address** is read per feature (shipping vs invoicing per [[settings-cart]]).

What it does NOT cover:

- Zone / polygon / distance UI details — see [[settings-geo-zones]] / [[geo-polygons-settings-main-new]] / [[settings-geo-distances]].
- How each consuming feature USES the matched zones (cascade and pricing arithmetic) — see [[shipping-calculation]] / [[tax-computation]] / [[discount-stacking]].
- VAT validation of the customer's company VAT number — see [[tax-computation]].
- The storefront language picker — see [[multi-language]].

## Contrasts

- **Zone vs Polygon vs Distance** — Zone is the merchant-facing unit other features reference. Polygons / Distances are INPUTS to zone rules. See [[geo-targeting-zones]].
- **Rules within a zone (OR) vs zones referenced by a feature (also OR)** — no AND at either level. For AND, use a compound operation (operation 5) or a polygon.
- **Tax matching vs shipping matching** — tax sees ONLY country rules; shipping evaluates every rule type. See [[geo-targeting-feature-resolution]].
- **Most-recent-wins (tax) vs all-shown (shipping) vs additive (fees, discounts)** — same multi-match address, different resolution per feature.
- **IP geo vs address geo** — IP geo seeds defaults pre-login; the explicit address overrides once entered. See [[geo-targeting-ip-detection]].
- **Static dataset vs Google Places** — dropdowns are CloudCart-bundled; Google Places is a CONVENIENCE INPUT that ultimately maps to the same static codes. See [[geo-targeting-address-resolution]].
- **Geo Zone vs Customer-group regionalisation** — discounts can scope by zone directly OR via a region-restricted customer group; the customer-group path persists across the customer's profile.

## Where it applies

- [[settings-geo-zones]] — zone management (the primary unit).
- [[geo-polygons-settings-main-new]] / [[geo-polygons-settings-main-new]] — polygon creation / edit (input to zone rules).
- [[settings-geo-distances]] — distance creation (input to zone rules).
- [[settings-shipping]] — shipping methods scope to a zone.
- [[settings-taxes]] — tax rules scope to a zone (country-only matching).
- [[settings-payment-providers]] — payment-method fees can scope to zones.
- [[marketing-discounts]] — discounts can restrict to a zone.
- [[customers-custom-groups]] — customer groups can be region-restricted.
- [[apps-cart-rules]] — geo-conditional Cart Rules.
- [[settings-cart]] — `invoicing_address` chooses tax address; Google Maps API key enables autocomplete.
- [[checkout-flow]] — customer address triggers zone matching.
- [[orders-details]] — order snapshots the matched zones and address.
- [[analytics-orders-by-country]] — country-level aggregation of orders.

## Related

- [[inventory-multi-warehouse]] — geo zones drive which warehouse's stock a customer sees (multi-location availability).
- [[apps-store-locations]] — the app that routes per-warehouse availability by geo zone.
- [[settings-geo-zones]] — zone management.
- [[geo-polygons-settings-main-new]] — polygon creation.
- [[geo-polygons-settings-main-new]] — polygon edit.
- [[settings-geo-distances]] — distance creation.
- [[settings-shipping]] — shipping consumes zones.
- [[settings-taxes]] — tax consumes country-level zone rules.
- [[settings-payment-providers]] — fees on payment methods can scope to zones.
- [[settings-cart]] — `invoicing_address`, Google Maps API key.
- [[customers-custom-groups]] — customer-group region restrictions.
- [[marketing-discounts]] — discount region restrictions.
- [[apps-cart-rules]] — geo-conditional Cart Rules.
- [[geo-zone]] — entity page.
- [[geo-polygon]] — entity page.
- [[geo-distance]] — entity page.
- [[shipping-calculation]] — how zones gate shipping quotes.
- [[tax-computation]] — how zones gate tax matching (country-only).
- [[discount-stacking]] — how zones interact with stacking.
- [[checkout-flow]] — where zone matching fires.
- [[multi-language]] — zone names are NOT per-language translatable.
- [[settings-translations]] — does NOT override zone names.
- [[analytics-orders-by-country]] — country-level analytics.
- [[product-visibility]] — geo-zone scoping is one reason a product may not show for a given shopper.

## Open Questions

None at the hub level — see individual aspect pages for residual `(verify)` items (notably polygon self-intersection on [[geo-targeting-polygons]], VAT tie-break on [[geo-targeting-feature-resolution]], auto-heal scope on [[geo-targeting-address-resolution]], alphanumeric post-code range validation on [[geo-targeting-post-codes]]).
