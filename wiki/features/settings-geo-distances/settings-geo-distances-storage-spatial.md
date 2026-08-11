---
type: feature
nav_path: "Settings → Geo distances → Storage & spatial schema"
route_name: geo_distances.settings
route_path: /admin/settings/geo-distances
aliases: ["Geo distances storage", "geo_distances table", "MySQL POINT geometry", "Spatial index geo distance", "distance_in_meters column", "Geo distance validation", "DECIMAL lat lng"]
tags: [settings, geo, distance, storage, mysql, spatial, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-distances]]. See the hub for the other aspects (list/form, units, map module, runtime matching, defaults, deletion).

# Geo distances — storage & spatial schema

## Purpose

Distance entries persist in the database with a **spatial-indexed `POINT` geometry column** so the runtime match (native spherical-distance computation — see [[settings-geo-distances-matching-runtime]]) can use spatial filtering and scan hundreds of entries in single-digit milliseconds. This aspect documents the table layout, the dual-column storage of the radius (`distance` raw + `distance_in_meters` computed), coordinate precision, and the backend validation rules that govern what can be saved.

## Where to find it

The `geo_distances` table is internal — merchants don't see the schema directly. The validation rules govern what they can save from the [[settings-geo-distances-list-add|Add / Edit form]].

## What the merchant can do here

The schema is internal — there is no direct merchant UI for storage. The visible behaviour driven by this schema:

- Save a record with a name up to 191 characters, an address up to ~64 KB, a radius integer up to 5,000,000, and lat/lng within the standard ranges. Anything outside these limits gets a 422 validation error from the [[settings-geo-distances-list-add|Add / Edit form]].
- Trust that the `point` column's spatial index makes runtime matching fast — see [[settings-geo-distances-matching-runtime]].
- Edit the record later and re-save; `distance_in_meters` is recomputed on every save against the current store `unit_system`.

## Settings & fields — DB column layout

| Column | Type | Notes |
|--------|------|-------|
| `id` | bigint PK | Auto-increment. |
| `name` | `VARCHAR(191)` | The 4-byte-charset index-friendly limit. Anything longer is rejected with a 422 validation error. |
| `text` | `TEXT` | The formatted address string. Required (`min:1`); no max length enforced server-side beyond the `TEXT` column's natural ~64 KB limit. |
| `distance` | int | The integer the merchant typed. |
| `distance_in_meters` | int | Always meters — computed on save per `unit`. See [[settings-geo-distances-distance-units]]. |
| `unit` | enum | `metric` / `imperial` / `N` — the store's `unit_system` at save time. |
| `lat` | `DECIMAL(17,15)` | Latitude. Range `[-90, 90]` validated by the application framework's `latitude` rule. |
| `lng` | `DECIMAL(18,15)` | Longitude. Range `[-180, 180]` validated by the application framework's `longitude` rule. |
| `point` | `GEOMETRY` (POINT) | The spatial column built from `(lat, lng)`. Has a `SPATIAL INDEX` for fast spherical-distance queries. |
| `fillColor` | string | Hidden — not surfaced in the modern form. See [[settings-geo-distances-defaults-prepopulation]]. |
| `fillOpacity` | float | Hidden. |
| `strokeColor` | string | Hidden. |
| `strokeOpacity` | float | Hidden. |
| `strokeWeight` | int | Hidden. |
| `created_at` | timestamp | Standard the application framework timestamps. |
| `updated_at` | timestamp | Standard the application framework timestamps. |

The column `point` is the runtime-critical one — the `SPATIAL INDEX` on it is what enables fast checkout-time matching.

## Business rules

### Centre point persists as a spatial `POINT` geometry with a spatial index

The platform uses a spatial GIS column to store the centre:

- The `point` column is `GEOMETRY` of subtype `POINT`.
- A `SPATIAL INDEX` exists on the column.
- On save, the platform writes `POINT(lat, lng)` built from the `lat` and `lng` columns.

Practical merchant impact: even with hundreds of distance entries referenced from many zones, the runtime match (native spherical-distance computation — see [[settings-geo-distances-matching-runtime]]) scans them in single-digit milliseconds because the database uses the spatial index to filter candidates.

### Two distance columns: raw input and meters-normalised

The DB persists **both** the raw integer the merchant typed AND the meters-normalised value:

- `distance` — the integer the merchant typed (interpreted per `unit_system` — see [[settings-geo-distances-distance-units]]).
- `distance_in_meters` — always meters. Computed on save:
  - `unit_system = metric` → `distance_in_meters = distance`.
  - `unit_system = imperial` → `distance_in_meters = distance × 0.3048` (feet → metres conversion).
- `unit` — the unit system active at save time, persisted so a later recompute is unambiguous.

Display labels read `unit` to decide whether to render "m" or "ft"; runtime matching uses `distance_in_meters`. See [[settings-geo-distances-distance-units]].

### Coordinate precision — 7 decimal places at the UI; DECIMAL(17,15) / (18,15) at the DB

- The Vue UI rounds latitude and longitude to **7 decimal places** (`toFixed(7)`) when reading from Google Places or marker-drag events.
- At the equator, 7 decimal degrees is ~1.1 cm precision — well beyond any conceivable delivery-radius requirement.
- The DB columns are `DECIMAL(17,15)` for `lat` and `DECIMAL(18,15)` for `lng`, so even higher precision is preserved if data arrives via API.

### Validation cap on `distance` at 5,000,000

Backend rule: `distance` must satisfy `min:1 | numeric | int | max:5000000`. Practical:

- Metric store: max ≈ 5,000,000 metres ≈ 5,000 km (well beyond practical delivery zones).
- Imperial store: max ≈ 5,000,000 feet ≈ 1,524 km.
- Decimals are rejected — `int` rule is enforced.

### Validation: `name` capped at 191 characters

The `name` column is `VARCHAR(191)` (the 4-byte-charset index-friendly limit). Names over 191 characters get a 422 with the validation message.

### Validation: `text` (address) required and free-form

`text` is `required | min:1` — cannot be empty. There is no max length enforced server-side beyond the `TEXT` column's natural ~64 KB limit. The Google Places autocomplete writes a clean formatted address, but the merchant can technically save any non-empty text — the lat/lng drive matching; `text` is for display only.

### Validation: lat/lng range checked by the application framework rules

Backend uses the application framework validation rules `latitude` and `longitude`:

- `lat` must be in `[-90, 90]`.
- `lng` must be in `[-180, 180]`.

Coordinates outside that range are rejected with a 422. In practice this only matters if a merchant manually edits the API payload — the UI's Google Maps module always returns valid values.

### Edge case: high-latitude / date-line precision

The matching at checkout uses `ST_Distance_Sphere` (spherical-earth model). At very high latitudes (above ~75°) and when the radius crosses the date line / poles, distance computation loses precision — not a real-world concern for any normal e-commerce delivery zone.

## Related

- [[settings-geo-distances]] — hub.
- [[settings-geo-distances-distance-units]] — `distance` vs `distance_in_meters` vs `unit` column semantics.
- [[settings-geo-distances-matching-runtime]] — how the `point` spatial column is queried at checkout.
- [[settings-geo-distances-list-add]] — the field grid that maps to these columns.
- [[settings-geo-distances-defaults-prepopulation]] — `fillColor` / `strokeColor` / etc. hidden columns and default values.

## Open questions

None.

