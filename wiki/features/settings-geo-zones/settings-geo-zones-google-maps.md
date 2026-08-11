---
type: feature
nav_path: "Settings → Geo Zones → Google Maps integration"
route_name: geo_zones.settings.main
route_path: /admin/settings/geo-zones
aliases: ["Geo zone Google Maps", "Geo zone Places autocomplete", "google_map_api_key", "isGoogleApiKeySet", "Geo zone address normalization"]
tags: [settings, geo, zones, google-maps, places]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-zones]]. See the hub for the other aspects (operations, post-codes, matching, polygon/distance, deletion-cascade, save-semantics).

# Geo Zones — Google Maps integration

## Purpose

A Google Maps API key on [[settings-cart]] (Box: Google Maps) unlocks the Google Places autocomplete on each rule row of the Add / Edit Geo zone form — *"Start typing the name of the state, county or country"* — and also unlocks **8 of the 11 zone-rule operations**. Without a Maps key, the Operation dropdown collapses to just 3 entries and the merchant loses access to region-level, city-level, neighborhood-level, polygon-based, and distance-from-point matching. This is effectively a feature gate, not expressed via plan tiers but via configuration.

## Where to find it

The key itself is set on **Settings → Cart → Google Maps** (see [[settings-cart]]). Once `google_map_api_key` is non-empty, the Geo Zones form's rule rows show the autocomplete input wherever applicable.

## What the merchant can do here

- Pick a place from the Google Places suggestions; the parser fills in country / region / city / neighborhood / lat / lng / city_id / etc. automatically.
- Switch between operations 2-10 in the operation dropdown — operations that would otherwise be hidden become available.
- Still use the country picker + post-code text input on operation 11 (post-code patterns); autocomplete doesn't apply to post codes.

## Settings & fields

| Field | What it does | Notes |
|-------|--------------|-------|
| **Google Places autocomplete** | Single input that resolves to country / region / city / neighborhood + lat / lng. | Shown on operations 2, 3, 5, 6, 7, 8. Placeholder: *"Start typing the name of the state, county or country"*. |
| **Polygon dropdown** | Lazy-loaded picker for operation 9. | Searchable. Resolves on load from `/admin/api/core/settings/geo-polygons`. See [[settings-geo-zones-polygon-distance]]. |
| **Distance dropdown** | Lazy-loaded picker for operation 10. | Searchable. Resolves from `/admin/api/core/settings/geo-distances`. |

## Business rules

### Without a Google Maps API key — only 3 of the 11 operations are available

If the store has no Google Maps API key set in [[settings-cart]], the operation-type dropdown collapses from 11 entries down to **just 3**:

- `1` — `OPERATION_ALL_IN_COUNTRY` (Includes country)
- `4` — `OPERATION_ALL_NOT_COUNTRY` (Includes all locations except country)
- `11` — `OPERATION_POST_CODE` (Includes only post codes in country)

So **operations 2, 3, 5, 6, 7, 8, 9, 10 are all gated behind a Google Maps API key**. A merchant who wants region-level, city-level, neighborhood-level, polygon-based, or distance-from-point matching MUST set up Google Maps first. This is a configuration gate, not a plan-tier gate.

The full 11-operation catalogue in [[settings-geo-zones-operations]] applies only when Maps is configured; otherwise the form has no UI affordance to even reach those operations.

### Two Google Places components — new vs legacy API

Two Google Places components exist in the codebase:

- `CcGoogleMapsPlacesInput` — uses the new Google Maps Places API (when `isNewGoogleMapsApi=true`).
- `CcGooglePlacesInputOldApi` — legacy fallback.

The merchant doesn't see which one is in use; selection is automatic based on the Google API version flag.

### Google Places parsing writes every relevant field

When the merchant picks a Google Places suggestion, the parser writes ALL relevant fields into the row: `text`, `country_iso2`, `country_name`, `admin_zone_1_name` / `admin_zone_1_iso` (region), `locality` (city), `neighborhood`, `city_id`, `city_ascii_name`, `lat`, `lng`, `timezone`. The model later uses these on save to populate the appropriate `geo_zone_values` columns based on the operation — see [[settings-geo-zones-save-semantics]].

### Address normalization per country (TR, CZ, GB, US/NY)

The `/admin/api/v1/geo-zones/format` endpoint (called when the merchant picks a Google Places suggestion) applies country-specific remapping:

- **`TR` and `CZ`**: when level_2 is present, locality = level_2 (administrative district treated as the city).
- **`GB`**: level_1 is overwritten by level_2 and locality = level_2 (because Google returns UK counties at level_2).
- **`US` with NY**: locality = level_1 (New York City is technically a level_1 for some place_ids).

This means the merchant's picked place may save with different country/region/city values than what the Google autocomplete strictly returned. Only relevant for the 4 listed countries.

### City-scoped operations auto-backfill region via Geonames

When saving operations 5/6/7/8 (city or neighborhood scoped) without an `admin_zone_1_iso` (region) supplied — typically when the merchant typed city-only into the autocomplete without picking a Google Place suggestion — the model triggers a **Geonames API lookup** to resolve the missing region for the given country + city. This is critical because the runtime `scopeZone` query requires region to match — without it, the rule "silently matches nothing". See [[settings-geo-zones-matching]] for the region requirement, and [[settings-geo-zones-save-semantics]] for the silent-failure mode if Geonames can't resolve the city.

### Country / region / city data is CloudCart's static dataset, not live Google

The country, region, and city dropdowns (where shown) are populated from CloudCart's bundled locale data (static data shipped with the platform), NOT from a live Google Places query. Coverage is comprehensive for major countries (ISO 3166-1/2) but smaller towns may not be available as a dropdown option — for those, the merchant has two options:

- Use the post-code operation (11) with the matching postal pattern — see [[settings-geo-zones-post-codes]].
- Use the polygon operation (9) to manually draw the desired area on the map — see [[settings-geo-zones-polygon-distance]].

The Google Places autocomplete shown when the Maps key is configured is a convenience for the COMMON case — under the hood it still maps the picked Place to CloudCart's internal country/region/city codes.

## Related

- [[settings-geo-zones]] — hub.
- [[settings-cart]] — where the Google Maps API key (`google_map_api_key`) is set.
- [[settings-geo-zones-operations]] — the 11-operation catalogue gated by this setting.
- [[settings-geo-zones-post-codes]] — operation 11 stays available without a key (one of the 3 always-available operations).
- [[settings-geo-zones-polygon-distance]] — operations 9 / 10 require the Maps key both for the dropdown and the on-map polygon drawing UI.
- [[settings-geo-zones-matching]] — the runtime region requirement explains why the Geonames auto-backfill matters.
- [[settings-geo-zones-save-semantics]] — what happens when the Geonames lookup fails silently.

## Open questions

None.
