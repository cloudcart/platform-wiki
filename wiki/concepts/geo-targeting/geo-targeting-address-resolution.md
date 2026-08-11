---
type: concept
nav_path: "Concept → Geo targeting → Address resolution"
aliases: ["Address-to-zone resolution", "Shipping vs invoicing address for geo", "invoicing_address setting", "Google Maps Places autocomplete", "Static country / region / city dataset", "Auto-heal saved addresses", "Zone name translation", "Geo performance", "Адреси и зони"]
tags: [shipping, tax, geo, addresses, google-maps, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[geo-targeting]]. See the hub for the other aspects (zones, polygons, distances, post-codes, IP detection, feature resolution).

# Geo targeting — Address resolution

## Definition

Once a customer enters an explicit address (at checkout or in their profile), the platform must decide **which address** feeds zone matching for which feature, **how** that address is converted into the inputs zone rules need (country / region / city / coordinates / post code), and **what** assists or backfills the resolution.

This page covers the input side of geo-targeting: address selection, the Google Maps integration that enriches input, the static dataset fallback when Google is absent, zone-name behaviour, and the resulting performance characteristics.

## Scope

Covered:

- Which customer address each feature reads (shipping address vs invoicing address; the `invoicing_address` setting on [[settings-cart]]).
- Google Maps integration (Places autocomplete on zone forms; draw-on-map for polygons; center-pin for distances; auto-heal of saved addresses).
- The static country / region / city dataset shipped with CloudCart.
- Zone names are not per-language translatable.
- Performance / caching properties of the zone-matching engine.

Not covered:

- The pre-login IP fallback — see [[geo-targeting-ip-detection]].
- The actual zone rule types — see [[geo-targeting-zones]].
- Polygon / distance shape mechanics — see [[geo-targeting-polygons]] / [[geo-targeting-distances]].

## Contrasts

- **Shipping address vs invoicing address** — shipping always uses the shipping address; tax uses the invoicing address (controlled by `invoicing_address` on [[settings-cart]] — defaults to Billing, can be switched to Shipping).
- **Google Places autocomplete vs static dropdown** — with the Google Maps API key set, the zone-add form uses Places autocomplete. Without the key, the merchant uses CloudCart's bundled country / region / city dropdowns. Both ultimately persist the same ISO codes — Google is a CONVENIENCE INPUT.
- **Google-supported places vs CloudCart static codes** — Google Places autocomplete can suggest places that don't exist in CloudCart's static dataset, but under the hood the platform maps the picked place back to its static codes. Places without a CloudCart entry don't gain coverage just because the autocomplete shows them.
- **Per-locale zone name (NO) vs per-locale storefront strings (YES)** — zone names are single store-wide strings, no per-language overrides through [[settings-translations]].

## Which address each feature reads

Once a customer has an explicit address on file:

- **Shipping zone** uses the **shipping address**.
- **Tax zone** uses the **invoicing address** controlled by [[settings-cart]] → `invoicing_address` (default Billing, switchable to Shipping).
- **Discount region** uses the same address as tax by default (but discount-specific rules can override).
- **Customer-group region** uses the customer's primary address.

Switching `invoicing_address` from Billing to Shipping shifts which address feeds tax matching — useful when the merchant's accounting policy treats the delivery location as the tax-relevant one.

## Google Maps integration

When the merchant has a Google Maps API key set in [[settings-cart]] → Google Maps section:

- The Add Zone form's location inputs are replaced with a **Google Places autocomplete** ("Start typing the name of the state, county or country..."). The user picks from suggestions and the platform parses the picked Place into the appropriate country / region / city fields.
- For polygons, [[geo-polygons-settings-main-new]] shows a **draw-on-map UI** where the merchant clicks to define polygon vertices.
- For distances, [[settings-geo-distances]] shows a **center-pin + radius UI**.
- The **auto-heal step** that backfills missing `state` and `city_id` on saved addresses is also gated by the Google Maps key — without the key, the heal is skipped and addresses are saved with whatever fields the customer entered, no automatic coordinate enrichment (verify).

Without a Google Maps API key, the merchant uses the platform's bundled country / region / city dropdowns. Polygons and distances still work — the underlying coordinate math doesn't depend on Google.

## Static country / region / city dataset

The country / region / city dropdowns are populated from CloudCart's bundled locale data (ISO 3166-1 / ISO 3166-2 codes plus city tables). Coverage is comprehensive for major countries; smaller towns may not have a dropdown entry. For those, the merchant can:

1. Use the **post-code operation (11)** with the matching postal pattern — see [[geo-targeting-post-codes]].
2. Use the **polygon operation (9)** to draw the area on a map — see [[geo-targeting-polygons]].

## Zone names are NOT per-language translatable

The zone's `name` is a single store-wide string. There is no `locale` field. The same name appears in every storefront language and every admin language. Multi-language merchants should pick a name that works across all storefront languages (a country code, a brand-style label) since it shows verbatim everywhere — there is no path through [[settings-translations]] to override zone names per locale.

## Performance

The geo-zone matching engine iterates each defined zone's rules at checkout / cart-display time. Each rule type has a dedicated lookup strategy (verify):

- Country / region / city — lookup tables.
- Polygons — spatial geometry index.
- Distances — haversine (spherical law of cosines) on lat/lng.
- Post-code — patterns table.

For a merchant with hundreds of zones, iteration cost stays in the order of milliseconds. The full lookup cache invalidates on save so changes take effect immediately (verify).

## Customer-group regionalisation example (wholesale only in EU)

Setup:

- Customer group "EU wholesale" with a region restriction → references zone "EU" (a zone containing all EU country rules).
- Group has its own price list (lower prices).

Result:

- A logged-in customer in Germany → assigned to "EU wholesale" automatically → sees wholesale prices.
- A logged-in customer in USA → falls back to default group → sees retail prices.

The customer-group path persists across the customer's profile, which is why some merchants prefer it over a direct discount-region restriction.

## Where it applies

- [[checkout-flow]] — where the customer enters an address; zone matching fires here.
- [[settings-cart]] — `invoicing_address` chooses which address feeds tax; Google Maps API key enables autocomplete and auto-heal.
- [[customers-custom-groups]] — group region restrictions read the customer's primary address.
- [[orders-details]] — the order snapshots the matched address and zone state.
- [[analytics-orders-by-country]] — country-level analytics rolls up from snapshotted addresses.

## Related

- [[geo-targeting]] — hub.
- [[settings-cart]] — `invoicing_address`, Google Maps API key.
- [[settings-translations]] — does NOT override zone names.
- [[geo-targeting-ip-detection]] — the pre-address fallback layer.
- [[geo-targeting-zones]] — what the address resolves AGAINST.
- [[geo-targeting-feature-resolution]] — how the matched zones are consumed.
- [[checkout-flow]] — where matching fires.
- [[customers-custom-groups]] — customer-group region restrictions.
- [[orders-details]] — order address snapshot.
- [[analytics-orders-by-country]] — country-level analytics.

## Open Questions

- ⏸️ **Auto-heal scope.** The auto-heal step backfills missing `state` and `city_id` on saved addresses when the Google Maps key is present. (verify whether this also touches `country_iso2`, `latitude`, `longitude`)
- ⏸️ **Cache invalidation granularity.** "Full lookup cache invalidates on save" — (verify whether this is per-zone or store-wide, and whether it propagates instantly or via a queue).
