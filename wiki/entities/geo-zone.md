---
type: entity
nav_path: "Entity → Geo Zone"
aliases: ["Geo Zone", "Geographic zone", "Shipping zone", "Tax zone", "Delivery zone", "Region", "Гео зона", "Географска зона", "Зона", "Регион"]
tags: [entity, geo, zones, shipping, tax, settings]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---

# Geo Zone

## Identity

A **Geo Zone** is a named geographic region the merchant defines and then attaches to other features to gate them by customer location — which shipping methods are offered, which tax rates apply, which payment providers / discounts / Cart Rules / customer groups are available, and what fees stack. CloudCart's wording from the management screen: *"CloudCart allows the grouping of countries into Geo Zones (regions) regardless of their geographic location."*

A zone is essentially the merchant's **label + a set of location rules**. The label is the merchant-friendly name ("EU", "Bulgaria", "Sofia delivery area"); the rules are one-or-more `(operation, location)` pairs that say which addresses fall inside the zone. Rules within a zone are OR-combined. The 11 operation types cover country / region / city / neighborhood, exclusions, post-code patterns, plus references to [[geo-polygon|Polygons]] and [[geo-distance|Distances]]. The merchant manages zones on [[settings-geo-zones]]. Polygons and Distances are created separately and referenced from zone rules — the primitive shape is defined ONCE and reused across multiple zones.

Zones are the PRIMARY UNIT other features reference. Shipping methods, tax rules, discounts, fees, and customer-group restrictions all point at zones (or at "rest of world"). At runtime, the platform resolves the customer's address against each zone's rules and gates the feature accordingly. See [[geo-targeting]] for the full mechanism.

## Aliases

- **Geo Zone** — the canonical term in admin UI and across the wiki.
- **Geographic zone** — full descriptive name.
- **Shipping zone** / **Tax zone** / **Delivery zone** — used contextually depending on which feature consumes the zone.
- **Region** — informal merchant phrasing; conflicts with administrative-region operations within the zone (so the wiki prefers "Geo Zone").
- **Гео зона** / **Географска зона** / **Зона** / **Регион** — Bulgarian equivalents.

## Key Attributes

The Geo Zone entity is documented across six aspect pages:

- **Zone fields** — `Name`, `Rules` (one or more `(operation, location)` pairs), implicit `Active`. Names NOT per-language translatable. See [[geo-zone-fields]].
- **Operations** — 11 IDs covering country / region / city / neighborhood / polygon / distance / post-code with exclusion variants. See [[geo-zone-operations]].
- **Post-code patterns** — comma-separated mix of exact codes, wildcards (`*`), four-dot ranges. See [[geo-zone-post-code-syntax]].
- **Consumers + inputs** — shipping / tax / payment / discounts / Cart Rules / customer groups REFERENCE zones; polygons + distances are INPUTS. See [[geo-zone-relationships]].
- **Save behaviour** — synchronous CRUD, cache invalidates on save, country normalisation to ISO-2, FK-protected delete. See [[geo-zone-lifecycle]].
- **Matching** — OR within a zone, OR across zones bound to one feature, tax uses country-only rules, tax tie-breaker is "most recently created wins". See [[geo-zone-matching-rules]].

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[geo-zone-fields]] — verbatim attribute catalogue (Name, Rules, per-rule inputs by operation type) + zone-level conventions (no explicit Active flag, not per-language translatable, sort by creation date).
- [[geo-zone-operations]] — the 11 operation types in depth: what each matches, what inputs it needs, when to use which, country / region / city dataset semantics.
- [[geo-zone-post-code-syntax]] — operation 11 deep dive: exact / wildcard (`*`) / range (`1000....1999`) forms, validation rules, mixed-list examples.
- [[geo-zone-relationships]] — what references the zone (shipping methods, tax rules, payment providers, discounts, Cart Rules, customer groups, cart, order) and what the zone references (polygons, distances).
- [[geo-zone-lifecycle]] — Created / In use / Edited / Deleted states, synchronous CRUD, cache invalidation, country normalisation, FK-protected delete.
- [[geo-zone-matching-rules]] — OR-combination within a zone, OR across zones for a single consumer, the tax country-only rule, the tax "most recently created wins" tie-breaker, the per-feature resolution table, the rest-of-world fallback.

## Where it appears

- [[settings-geo-zones]] — the management screen (List view + Organize / Add / Edit form).
- [[geo-polygons-settings-main-new]] — adds a new polygon (drawn on map). Referenced by zone operation 9.
- [[geo-polygons-settings-main-new]] — edits an existing polygon.
- [[settings-geo-distances]] — adds / edits center + radius distance entries. Referenced by zone operation 10.
- [[settings-shipping]] — each shipping method references one zone (or "rest of world").
- [[settings-taxes]] — each tax rule references one zone (or "rest of world"); country-level rules drive tax matching.
- [[settings-payment-providers]] — providers can be scoped by country / zone for availability and fee stacking.
- [[marketing-discounts]] — discounts can restrict to zones via "Regions" or customer-group restriction.
- [[customers-custom-groups]] — customer groups can be region-restricted.
- [[apps-cart-rules]] — Cart Rules can target by geo for arbitrary logic.
- [[checkout-flow]] — where the customer's address triggers zone matching.
- [[orders-details]] — order's snapshotted address determines its geo for analytics / re-quote.
- [[analytics-orders-by-country]] — country-level order aggregation.
- [[settings-cart]] — the `invoicing_address` setting picks which address the tax zone uses; the Google Maps API key enables Places autocomplete.

## Related

### Related entities

- [[geo-polygon]] — drawn shape on a Google Map. Input to zone rule operation 9.
- [[geo-distance]] — center point + radius in meters. Input to zone rule operation 10.
- [[shipping-provider]] — every shipping method references a zone (or "rest of world").
- [[payment-provider]] — providers can be scoped by country / zone for availability.
- [[customer-group]] — groups can be region-restricted via zones.
- [[discount]] — discounts can restrict to zones via "Regions" rules.
- [[cart]] — customer's in-progress checkout; resolves against zone matching.
- [[order]] — snapshots the matched zones at checkout.

### Cross-cutting concepts

- [[geo-targeting]] — the canonical concept page on how zones / polygons / distances work end-to-end.
- [[geo-targeting-address-resolution]] — which customer address feeds zone matching (shipping vs invoicing); Google Maps Places autocomplete; static dataset; zone-name behaviour.
- [[geo-targeting-ip-detection]] — pre-login IP-to-country defaults via MaxMind.
- [[shipping-calculation]] — how zones gate shipping quotes (and the per-feature resolution).
- [[tax-computation]] — how zones gate tax matching (country-only rule + most-recent-wins tie-breaker).
- [[discount-stacking]] — how zones interact with discount stacking.
- [[checkout-flow]] — where zone matching fires.
- [[multi-currency]] — currency pickers and the BGN → EUR transition; geo + currency drive customer-facing pricing.
- [[multi-language]] — zone names are NOT per-language translatable.

### Settings & webhooks

- [[settings-geo-zones]] — zone management.
- [[geo-polygons-settings-main-new]] — polygon creation.
- [[settings-geo-distances]] — distance creation.
- [[settings-cart]] — `invoicing_address` + Google Maps API key.
- [[settings-translations]] — does NOT have a zone-name override path.

## Open Questions

- ⏸️ **Geocoding fallback when Google Maps is unset** — polygons and distances require coordinates for the customer's address. Without a Google Maps API key, the platform falls back to a CloudCart-bundled coordinate dataset, but the exact coverage / accuracy isn't documented.
- ⏸️ **Tax country-only rule UI hint** — tax consumes ONLY country rules in zones. Whether the zone form or tax form warns merchants when they build a zone with no country rule but try to use it for tax is unclear. See [[geo-zone-matching-rules]].
- ⏸️ **Customer-group geo restriction format** — [[customers-custom-groups]] mentions region restrictions but the exact zone-reference format (single zone, list, or arbitrary geo logic) isn't documented.
- ⏸️ **Bulk import of zones** — there's no UI for importing zones from CSV / JSON. How a merchant migrating from another platform loads many country-specific zones efficiently is not documented.
