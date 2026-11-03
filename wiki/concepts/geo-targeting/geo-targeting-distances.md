---
type: concept
nav_path: "Concept → Geo targeting → Distances"
aliases: ["Geo Distances", "Distance zones", "Radius zones", "Local delivery radius", "OPERATION_DISTANCE", "Гео разстояния", "Радиус на доставка"]
tags: [shipping, geo, distances, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[geo-targeting]]. See the hub for the other aspects (zones, polygons, post-codes, IP detection, feature resolution, address resolution).

# Geo targeting — Distances

## Definition

A **Geo Distance** is a center point (lat/lng) plus a radius — a circular catchment around a fixed location. Distances are used when the merchant wants "deliver within X km of point Y", typical for local delivery, food, on-demand fulfilment, and warehouse catchments.

Like polygons, a distance is **not directly referenced by shipping, tax, or discount features**. It is an **input to a zone rule** of operation 10 (`OPERATION_DISTANCE`). The merchant creates the distance entry once at [[settings-geo-distances]] and references it from one or more zones (see [[geo-targeting-zones]]).

## Scope

Covered:

- The distance model (name, center point, radius in METERS, optional unit display).
- Great-circle (spherical law of cosines) matching against the customer's coordinates.
- The "radius is in meters, not kilometres" gotcha.
- Multi-warehouse pattern (two distances OR-combined in one zone).

Not covered:

- The 11 zone operation types — see [[geo-targeting-zones]].
- Polygon shapes — see [[geo-targeting-polygons]].
- How the customer's coordinates are produced — see [[geo-targeting-address-resolution]].

## Contrasts

- **Distance vs Polygon** — distance is a perfect circle (one center + one radius). Polygon is an arbitrary outline (many vertices). Pick distance for round catchments; pick polygon for irregular boundaries. See [[geo-targeting-polygons]].
- **Distance vs Post-code** — distance is spatial (haversine on coordinates); post code is textual (pattern on the address's `post_code`). Distance needs reliable geocoding; post code only needs the customer's typed post code. See [[geo-targeting-post-codes]].
- **Single warehouse vs multi-warehouse coverage** — one distance covers one center. For "within 30 km of either of my two warehouses" → create two distance entries and reference both from one zone (OR-combined rules); see the example below.

## How it works

A distance has:

- A **name** (merchant-set, store-wide).
- A **center point** (lat/lng) — the merchant places the pin on the [[settings-geo-distances]] map.
- A **radius** in **meters** — see the gotcha below.
- An optional unit display preference (used for input convenience; stored value is always meters) (verify).

Matching uses **great-circle distance** (spherical law of cosines) from the center to the customer's coordinates, compared to the radius. The customer's coordinates come from address geocoding (see [[geo-targeting-address-resolution]]). When the address has no coordinates, the distance rule cannot match.

## Distance unit is meters — the most common misconfiguration

The `radius` value on a distance is **stored in meters, not kilometres**. A 30 km radius is `30000`. Confusing this is the most common merchant misconfiguration — the merchant types `30` (intending km), the platform reads it as 30 m, and effectively no customer matches.

The form may display the value in the merchant's chosen unit for input convenience, but the persisted value is meters (verify).

## Example — local delivery within 30 km of warehouse

Setup:

- Distance "Warehouse 30km radius" — center at the warehouse's lat/lng, radius = `30000` meters.
- Zone "Local delivery" — operation 10 (distance = "Warehouse 30km radius"). For tax, add operation 1 (country = BG) — see [[geo-targeting-feature-resolution]].
- Custom shipping method "Local courier" scoped to "Local delivery" zone, fixed price (e.g., 5 BGN).

Result:

- Customer's address geocoded → if within 30 km, the Local courier method appears at checkout.
- Outside 30 km, the method is hidden and other carriers (e.g., Econt) take over.

## Example — multi-warehouse via OR-combined distances

Setup:

- Distance "Sofia warehouse 30km" — center at Sofia warehouse, radius `30000`.
- Distance "Plovdiv warehouse 30km" — center at Plovdiv warehouse, radius `30000`.
- Zone "Local delivery (either warehouse)" — two rules, both operation 10, OR-combined. The zone matches if the customer is within 30 km of either warehouse.

This is the canonical pattern for multi-warehouse local-delivery scoping. The OR-semantics inside a zone (see [[geo-targeting-zones]]) does this naturally.

## Where it applies

- [[settings-geo-distances]] — distance management screen.
- [[geo-zone]] — zones reference distances via operation 10 rules.
- [[settings-shipping]] — local-delivery shipping methods that scope to a distance-based zone.
- [[settings-cart]] — the Google Maps API key drives the center-pin map UI.

## Related

- [[geo-targeting]] — hub.
- [[settings-geo-distances]] — distance management UI.
- [[geo-distance]] — entity page.
- [[geo-targeting-zones]] — zone operations including operation 10 (distance).
- [[geo-targeting-polygons]] — alternative shape primitive.
- [[geo-targeting-post-codes]] — alternative scoping primitive.
- [[geo-targeting-feature-resolution]] — why distance zones need a paired country rule for tax.
- [[geo-targeting-address-resolution]] — how the customer's coordinates are produced.

## Open Questions

None.
