---
type: feature
nav_path: "Settings → Geo Zones → Polygon and distance"
route_name: geo_zones.settings.main
route_path: /admin/settings/geo-zones
aliases: ["Geo zone polygon", "Geo zone distance", "OPERATION_POLYGON", "OPERATION_DISTANCE", "ST_Contains", "ST_Distance_Sphere", "Point in polygon", "Distance from point"]
tags: [settings, geo, zones, polygon, distance, spatial]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-geo-zones]]. See the hub for the other aspects (operations, post-codes, Maps, matching, deletion-cascade, save-semantics).

# Geo Zones — Polygon and distance operations

## Purpose

Two of the 11 zone-rule operations reference **separate entities** managed on their own settings screens:

- **Operation 9 — `OPERATION_POLYGON`** — references a row in geo-polygons (the polygon defines the actual coordinates drawn on a Google Map).
- **Operation 10 — `OPERATION_DISTANCE`** — references a row in geo-distances (the distance entry defines a center point + radius + unit).

Both operations rely on the database's native spatial functions at checkout time — a true point-in-polygon containment test for polygons (not approximation) and a spherical-earth great-circle distance for distances (accuracy ~0.5% — fine for retail delivery). Both require a Google Maps API key — see [[settings-geo-zones-google-maps]].

## Where to find it

- The **polygon dropdown** appears on a rule row when the merchant picks operation `9` from the Operation dropdown.
- The **distance dropdown** appears on a rule row when the merchant picks operation `10`.
- The polygon and distance entries themselves are managed on separate screens — see [[geo-polygons-settings-main-new]] and [[settings-geo-distances]].

## What the merchant can do here

### On the Geo zone Add / Edit form

- Pick one of the merchant's saved polygons from the polygon dropdown (operation 9).
- Pick one of the merchant's saved distance entries from the distance dropdown (operation 10).
- Both dropdowns are searchable and lazy-loaded:
  - Polygon list endpoint: `/admin/api/core/settings/geo-polygons`.
  - Distance list endpoint: `/admin/api/core/settings/geo-distances`.

### Outside the Geo Zone form

- Create / edit / delete the polygon shape on [[geo-polygons-settings-main-new]].
- Create / edit / delete the distance entries on [[settings-geo-distances]].

## Settings & fields

| Field | What it does | Notes |
|-------|--------------|-------|
| **Polygon** (`polygon_id`) | FK to a polygon row. | Operation 9 only. Stored on `geo_zone_values.polygon_id`. |
| **Distance** (`distance_id`) | FK to a distance row. | Operation 10 only. Stored on `geo_zone_values.distance_id`. |

## Business rules

### Operation 9 — point-in-polygon test

At checkout, the polygon-zone matcher runs a spatial containment test (does the polygon contain the customer point?) directly in the database. The polygon is stored as a `GEOMETRY POLYGON` column with potential `SPATIAL INDEX`; the customer's `(lat, lng)` is wrapped in a spatial point. This is a **true point-in-polygon test, not approximation**.

Multi-polygon support exists at the model layer (the polygon-paths attribute handles both `Polygon` and `MultiPolygon`) — but the modern UI validator only accepts a single `Polygon`. So `MultiPolygon` shapes can only arrive via legacy data, not via a fresh save on the modern UI.

### Operation 10 — spherical-earth distance

The distance matcher computes the spherical-earth distance between the distance entry's centre and the customer point in the database, and compares against the entry's `distance_in_meters` column. This is the spherical-earth great-circle distance (not WGS84 ellipsoid; accuracy ~0.5% — fine for retail delivery).

### 2-stage filtering keeps checkout latency low

Both spatial calls are routed by the `compareGeoZone` matcher path — first a DB-side broad `scopeZone` query trims the candidate list to zones whose country / region already loosely match the customer, then PHP iterates the matched zones and runs the spatial test per row. This 2-stage filtering keeps checkout latency low even with hundreds of zones — see [[settings-geo-zones-matching]] for the broader matching flow.

### Both operations require a Google Maps API key

Operations 9 and 10 disappear from the operation dropdown when no Google Maps API key is set on [[settings-cart]] — see [[settings-geo-zones-google-maps]] for the full 3-of-11 gate. Drawing polygons on the map and picking a distance reference point both rely on the Maps embed.

### Cascading delete — polygon / distance delete silently rewires zones

The `geo_zone_values.polygon_id` and `geo_zone_values.distance_id` FKs both have `ON DELETE CASCADE`. So deleting a polygon or distance entry **silently removes** all zone rules referencing it. There is **no FK protection error** and no admin warning — the merchant who deletes a polygon will lose every zone rule that used it. See [[settings-geo-zones-deletion-cascade]] for the full cascade story (this is the most surprising part of the geo-zones deletion model).

### Internal database id 3, 7, 10 carve-out for distance matching

(Internal — not relevant to typical merchants.) The platform skips distance evaluation entirely on certain internal database ids; merchants on the standard infrastructure are not affected.

## Related

- [[settings-geo-zones]] — hub.
- [[settings-geo-zones-operations]] — operations 9 and 10 in the full 11-operation table.
- [[settings-geo-zones-google-maps]] — Maps key requirement.
- [[settings-geo-zones-matching]] — the 2-stage `scopeZone → compareGeoZone` matching flow.
- [[settings-geo-zones-deletion-cascade]] — polygon / distance delete silently rewires zone rules via `ON DELETE CASCADE`.
- [[geo-polygons-settings-main-new]] — polygon management screen.
- [[settings-geo-distances]] — distance management screen.
- [[geo-polygon]] — entity page.
- [[geo-distance]] — entity page.

## Open questions

None.
