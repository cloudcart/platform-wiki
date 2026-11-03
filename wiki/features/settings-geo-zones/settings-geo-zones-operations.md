---
type: feature
nav_path: "Settings → Geo Zones → Rule operations"
route_name: geo_zones.settings.main
route_path: /admin/settings/geo-zones
aliases: ["Geo zone operations", "Geo rule types", "Geo zone rule operations", "OPERATION_ALL_IN_COUNTRY", "11 operation types"]
tags: [settings, geo, shipping, tax, zones, operations]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-zones]]. See the hub for the other aspects (matching, post-codes, Maps, polygon/distance, deletion-cascade, save-semantics).

# Geo Zones — Rule operations (the 11 operation types)

## Purpose

Every rule inside a geo zone is a `(operation, location)` pair. The **operation** picks which kind of location matching the rule performs, and which location inputs the form shows. Multiple rules within one zone are **OR-combined** — a zone matches a customer's address if ANY of its rules match. There is no AND combination at the zone level — for "Bulgaria AND Sofia city" the merchant picks operation `5` (one rule that constrains country + region + city together).

The merchant picks the operation per rule from the **Operation** dropdown. The dropdown shows up to 11 options when a Google Maps API key is configured on [[settings-cart]]. Without a Maps key, the dropdown collapses to just 3 options (`1`, `4`, `11`) — see [[settings-geo-zones-google-maps]] for the gating rule.

## Where to find it

Sidebar → Settings → **Geo Zones** → click **+ New Geo zone** (or click an existing zone name). Each row in the **Rules** dynamic group exposes the operation dropdown on its left.

## What the merchant can do here

- Pick an operation per rule from the **Operation** dropdown. The row's location inputs swap dynamically based on the choice.
- Click **+ Add another State, Country or Polygon** to append a new rule (defaults to `operation = 1`). Each additional rule is preceded by an **OR** label and gets an **×** delete icon.
- The first rule row is mandatory — its **×** is hidden so the merchant can't remove it.

## Settings & fields — the 11 operation types

Each operation has a numeric ID stored in `form.items[i].operation`. The merchant-visible label is a template with placeholders for the chosen country / region / city / polygon / etc. Constants verbatim from the codebase.

| ID | Constant | Template label | Inputs needed |
|----|----------|----------------|---------------|
| **1** | `OPERATION_ALL_IN_COUNTRY` | *"Includes country `{country}`"* | Country picker |
| **2** | `OPERATION_ONLY_REGION` | *"Includes only region `{region}` in `{country}`"* | Country + region pickers (or Google Places autocomplete) |
| **3** | `OPERATION_ALL_IN_COUNTRY_WITHOUT_REGION` | *"Includes all locations except `{region}` in `{country}`"* | Country + region |
| **4** | `OPERATION_ALL_NOT_COUNTRY` | *"Includes all locations except country `{country}`"* | Country picker |
| **5** | `OPERATION_ALL_CITY` | *"Includes only for city `{city}` in `{region}` from `{country}`"* | Country + region + city |
| **6** | `OPERATION_ALL_NOT_CITY` | *"Includes all cities in region `{region}` from `{country}` except city `{city}`"* | Country + region + city to exclude |
| **7** | `OPERATION_ALL_STREET` | *"Includes only for neighborhood `{neighborhood}` from city `{city}` in `{region}` from `{country}`"* | Country + region + city + neighborhood |
| **8** | `OPERATION_ALL_NOT_STREET` | *"Includes all neighborhood except `{neighborhood}` from city `{city}` in `{region}` from `{country}`"* | Same as above for exclusion |
| **9** | `OPERATION_POLYGON` | *"Includes only for polygon `{polygon}`"* | Polygon picker — see [[settings-geo-zones-polygon-distance]] |
| **10** | `OPERATION_DISTANCE` | *"Includes only for `{radius}{unit}` from point `{distance}`"* | Distance picker — see [[settings-geo-zones-polygon-distance]] |
| **11** | `OPERATION_POST_CODE` | *"Includes only post codes `{post_codes}` in country `{country}`"* | Country + comma-separated post codes — see [[settings-geo-zones-post-codes]] |

### Per-row location inputs by operation

When the merchant picks an operation, the row's location inputs swap dynamically:

| Operation | Location inputs shown |
|-----------|----------------------|
| **1 — Includes country** | Single country picker (or Google Places autocomplete if Maps key set). |
| **2 — Includes only region** | Google Places autocomplete *"Start typing the name of the state, county or country"* (auto-parses country + region). Maps key required. |
| **3 — Includes all locations except region in country** | Same Google Places autocomplete; auto-parses to country + region for exclusion. |
| **4 — Includes all locations except country** | Country picker only. |
| **5 — Includes only for city** | Google Places autocomplete; parses country + region + city. |
| **6 — Includes all cities except city** | Same Google Places autocomplete. |
| **7 — Includes only for neighborhood** | Google Places autocomplete; parses country + region + city + neighborhood (the Google `sublocality` / `neighborhood` types). |
| **8 — Includes all neighborhood except** | Same Google Places autocomplete. |
| **9 — Includes only for polygon** | Second **polygon** dropdown appears (lazy-loaded from `/admin/api/core/settings/geo-polygons`, searchable). |
| **10 — Includes only for distance from point** | Second **distance** dropdown appears (lazy-loaded from `/admin/api/core/settings/geo-distances`, searchable). |
| **11 — Includes only post codes in country** | Side-by-side: country picker + free-text **Post code** input. Country picker stays even when a Maps key is configured — autocomplete isn't useful for post-code patterns. |

When the merchant picks a Google Places suggestion, the parsing logic writes ALL relevant fields into the row: `text`, `country_iso2`, `country_name`, `admin_zone_1_name` / `admin_zone_1_iso` (region), `locality` (city), `neighborhood`, `city_id`, `city_ascii_name`, `lat`, `lng`, `timezone`. The model later uses these on save to populate the appropriate `geo_zone_values` columns based on the operation — see [[settings-geo-zones-save-semantics]].

## Business rules

### Rules within a zone are OR-combined

A geo zone matches a customer's address if ANY of its rules match. The UI shows an `OR` label between consecutive rules. There is no AND combination at the zone level — for "Bulgaria AND Sofia city" the merchant uses operation `5` (a single rule that already constrains country + region + city together).

### Multiple zones referenced by the same consuming rule create OR-of-OR

A shipping method, tax rule, or discount that references two zones matches any customer who falls inside either zone (zone1 OR zone2). Combining zones via the consuming feature is the only way to express more complex location logic.

### Operation 1 clears `admin_zone_1_iso` on save

When the merchant changes a rule's operation to `1` (Includes country), the model's `saving` hook nulls out `admin_zone_1_iso` and `admin_zone_1_name`. So switching from a country+region rule to "whole country" cleans up the now-unused region columns automatically.

### Country normalization uses two-letter ISO codes

The platform stores `country_iso2` (two-letter ISO 3166-1 alpha-2 code) for every rule and normalizes the customer's address country before matching. So variations like "United Kingdom" / "UK" / "GB" all resolve to `GB` consistently.

### Operations gated behind a Google Maps API key

Operations 2, 3, 5, 6, 7, 8, 9, 10 are all gated behind having a Google Maps API key — see [[settings-geo-zones-google-maps]] for the 3-of-11 collapse when no key is set.

## Related

- [[settings-geo-zones]] — hub.
- [[settings-geo-zones-google-maps]] — gating of operations 2/3/5/6/7/8/9/10 behind a Maps API key, and the address normalization the parser applies per country.
- [[settings-geo-zones-post-codes]] — operation 11 syntax, GR space stripping, range numeric-only rule.
- [[settings-geo-zones-polygon-distance]] — operations 9 / 10, the spatial-function backend, polygon / distance entity references.
- [[settings-geo-zones-matching]] — how the OR-combined rules are evaluated at checkout.
- [[settings-geo-zones-save-semantics]] — how the row format is converted to the backend `values[]` shape on save.
- [[settings-cart]] — Google Maps API key location.
- [[geo-zone]] — entity page.

## Open questions

None.
