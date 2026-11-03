---
type: entity
nav_path: "Entity → Geo Zone → Operations"
aliases: ["Geo Zone operations", "11 operation types", "OPERATION_ALL_IN_COUNTRY", "Zone rule operation IDs", "Country / region / city / polygon / distance / post-code operations"]
tags: [entity, geo, zones, operations, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

# Geo Zone — Operations

> Part of [[geo-zone]]. See the hub for related aspects (fields, post-code syntax, relationships, lifecycle, matching rules).

## Identity

A geo zone is a list of `(operation, location)` rules. The **operation type** is the matcher logic for one rule — what kind of customer addresses it includes. CloudCart ships 11 operation types covering country-level matching, administrative region / city / neighborhood matching, exclusions, drawn polygons, distance radii, and post-code patterns. This page catalogues each, what inputs it accepts, and when the merchant uses it.

The 11 operations divide into four families:

- **Country-level** (1, 4) — every address in (or NOT in) one country.
- **Sub-country administrative** (2, 3, 5, 6, 7, 8) — region / city / neighborhood, with include and exclude variants.
- **Geographic shapes** (9, 10) — polygons drawn on a map; distance radii from a center point.
- **Postal codes** (11) — post-code pattern matching within a country.

## Aliases

- "11 operation types" / "OPERATION_ALL_IN_COUNTRY" / "OPERATION_DISTANCE" — when the merchant or developer references the operation constants.
- "Zone rule operation IDs" — the numeric IDs 1–11 used in admin URLs and API payloads.
- "Country / region / city / polygon / distance / post-code operations" — by family.

## Key Attributes

### The 11 operation types

| ID | Constant | Match logic | Inputs |
|----|----------|-------------|--------|
| **1** | OPERATION_ALL_IN_COUNTRY | Every address in country X | Country picker |
| **2** | OPERATION_ONLY_REGION | Only addresses in region Y of country X | Country + region |
| **3** | OPERATION_ALL_IN_COUNTRY_WITHOUT_REGION | Every address in country X EXCEPT region Y | Country + region |
| **4** | OPERATION_ALL_NOT_COUNTRY | Every address NOT in country X | Country picker |
| **5** | OPERATION_ALL_CITY | Only addresses in city Z of region Y in country X | Country + region + city |
| **6** | OPERATION_ALL_NOT_CITY | Every address in region Y of country X EXCEPT city Z | Country + region + city |
| **7** | OPERATION_ALL_STREET | Only addresses in neighborhood W of city Z | Country + region + city + neighborhood |
| **8** | OPERATION_ALL_NOT_STREET | Every address in city Z EXCEPT neighborhood W | Same as 7 |
| **9** | OPERATION_POLYGON | Addresses inside polygon P | [[geo-polygon|Polygon]] reference |
| **10** | OPERATION_DISTANCE | Addresses within radius R of point Q | [[geo-distance|Distance]] reference |
| **11** | OPERATION_POST_CODE | Addresses with post code matching pattern P in country X | Country + post-code pattern |

### When to use which family

- **Whole country** (typical for tax + international shipping) — operation 1.
- **Everything except a list of restricted countries** (e.g., shipping worldwide except sanctions list) — operation 4, one rule per excluded country (rules within the zone are OR-combined, so each `NOT in country X` is its own rule).
- **One administrative region** (e.g., a state within the US, a province within Bulgaria) — operation 2.
- **One city** (e.g., same-day delivery zone for Sofia city) — operation 5.
- **One city neighborhood** (very narrow same-day delivery) — operation 7. Coverage depends on whether CloudCart's bundled dataset has neighborhoods for that city.
- **A drawn area on a map** (e.g., a non-standard delivery polygon around a warehouse) — operation 9 + a polygon drawn on [[geo-polygons-settings-main-new]].
- **Within N km of a point** (e.g., radius from a brick-and-mortar store) — operation 10 + a distance entry on [[settings-geo-distances]]. **Distance radius is in METERS, not kilometers** (so 30 km = `30000`). See [[geo-distance]].
- **By post code** (e.g., a courier supports only certain post codes) — operation 11 + the post-code pattern. See [[geo-zone-post-code-syntax]] for the grammar.

### Country / region / city dataset

The country, region, and city dropdowns are populated from CloudCart's **bundled** locale data (static ISO 3166-1 / ISO 3166-2 + city tables shipped with the platform), NOT from a live Google Places query. Coverage is comprehensive for major countries but smaller towns may not be in the dropdown. For those:

- Use post-code (operation 11) if the country has a stable post-code scheme.
- Use polygon (operation 9) to draw the area manually on a map.

The Google Maps Places autocomplete (when the merchant has a Maps API key set on [[settings-cart]]) still maps the picked Place back to CloudCart's static codes — so Google-supported places without a CloudCart entry don't gain coverage just because the autocomplete shows them. See [[geo-targeting-address-resolution]] for the dataset-vs-Google details.

### Polygons and distances are INPUTS, not consumers

Operations 9 and 10 reference SEPARATE entities ([[geo-polygon]] / [[geo-distance]]) created on their own admin screens. The polygon defines the coordinates; the distance defines the center + radius. The zone simply REFERENCES them. One polygon or distance can be referenced from many zones.

This separation matters: if the merchant tweaks a polygon's shape, every zone referencing it updates immediately (no need to edit each zone). Conversely, a polygon cannot be deleted while a zone still references it — FK-protected; see [[geo-zone-lifecycle]].

### Country normalisation applies before matching

Every address country is normalised to its ISO 3166-1 alpha-2 code BEFORE matching against a country-bearing operation. So *"United Kingdom"*, *"UK"*, *"Great Britain"* all become `GB`. Same for *"Czech Republic"* / *"Czechia"* → `CZ`, *"Greece"* / *"Hellas"* → `GR` (also accepts `EL` for VIES purposes). The zone stores the ISO code; the customer's address is normalised on save.

## Where it appears

- [[settings-geo-zones]] — the Add / Edit form renders the operation-type dropdown and shows the relevant input fields based on the picked operation.
- [[geo-polygons-settings-main-new]] — where polygons for operation 9 are drawn.
- [[settings-geo-distances]] — where center + radius distances for operation 10 are created.
- [[geo-targeting-zones]] — concept-page view of zones inside [[geo-targeting]].

## Related

- [[geo-zone]] — hub.
- [[geo-zone-fields]] — which input fields the form shows for each operation.
- [[geo-zone-post-code-syntax]] — the operation-11 pattern grammar.
- [[geo-zone-matching-rules]] — how the operations combine at runtime (OR within a zone).
- [[geo-polygon]] — input to operation 9.
- [[geo-distance]] — input to operation 10. Radius stored in METERS.
- [[geo-targeting-address-resolution]] — the dataset behind the country / region / city dropdowns.

## Open Questions

- ⏸️ Coverage of the bundled neighborhood / street dataset for operations 7 / 8 — which countries / cities have working neighborhood dropdowns is not documented.
- ⏸️ Whether a zone with ONLY exclusion rules (operations 3 / 4 / 6 / 8) without a positive include matches *any* address, or implicitly defaults to "all addresses except the listed exclusions" — the boundary case isn't documented.
