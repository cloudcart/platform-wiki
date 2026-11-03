---
type: concept
nav_path: "Concept → Geo targeting → Polygons"
aliases: ["Geo Polygons", "Polygon zones", "Draw-on-map zones", "Polygon operation", "OPERATION_POLYGON", "Гео полигони", "Полигон"]
tags: [shipping, geo, polygons, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[geo-targeting]]. See the hub for the other aspects (zones, distances, post-codes, IP detection, feature resolution, address resolution).

# Geo targeting — Polygons

## Definition

A **Geo Polygon** is a merchant-drawn shape on a Google Map, defined by a sequence of vertex coordinates that outline an area. Polygons are used when neither administrative regions nor distance circles match the delivery area — e.g., a specific neighborhood, a custom warehouse catchment, an island, an area cropped at a river.

A polygon is **not directly referenced by shipping, tax, or discount features**. It is an **input to a zone rule** of operation 9 (`OPERATION_POLYGON`). The merchant draws the shape once at [[geo-polygons-settings-main-new]] / edits at [[geo-polygons-settings-main-new]] and then references the polygon from one or more zones (see [[geo-targeting-zones]]).

## Scope

Covered:

- The polygon model (name, vertex coordinates, display attributes).
- Point-in-polygon matching against the customer's geocoded address.
- Storage as a spatial POLYGON geometry (WKT internally) (verify).
- The lack of import/export tooling.
- Required pairing with a country rule for tax — see [[geo-targeting-feature-resolution]].

Not covered:

- The 11 zone operation types — see [[geo-targeting-zones]].
- Distance (radius-from-point) — see [[geo-targeting-distances]].

## Contrasts

- **Polygon vs Distance** — polygon defines an arbitrary outline (vertices); distance defines a circle (center + radius). Polygons handle irregular boundaries; distances handle "within X km" cases. See [[geo-targeting-distances]].
- **Polygon vs Post-code pattern** — polygon resolves spatially against the geocoded address; post code resolves textually against the address's `post_code` field. Polygon is more precise where geocoding is reliable; post code is more robust where geocoding may fail or where the merchant already has a clean post-code list. See [[geo-targeting-post-codes]].
- **Polygon stored on the platform vs Google Maps drawing tool** — the drawing UI uses Google Maps when a Google Maps API key is configured in [[settings-cart]], but the persisted polygon coordinates live on CloudCart's `geo_polygons` table (verify). The underlying point-in-polygon math doesn't depend on Google.

## How it works

A polygon has:

- A **name** (merchant-set, store-wide).
- A **set of coordinates** defining its outline, drawn vertex-by-vertex on a Google Map.
- **Display attributes** (fill color, stroke color, stroke weight, opacity) used only when previewing on the map.

Matching uses a **point-in-polygon test** against the customer's coordinates. The customer's coordinates come from one of:

- The Google Places geocode of the address entered at checkout (when the Google Maps API key is set).
- CloudCart's bundled coordinate dataset (city / neighborhood centroid) when no live geocoding is available.

When the address has no usable coordinates, the polygon rule cannot match — see [[geo-targeting-address-resolution]] for the fallback behaviour.

## Storage and tooling

Polygons are persisted as spatial POLYGON geometries (WKT internally) on the `geo_polygons` table along with the display attributes (verify). There is **no UI for importing / exporting polygon coordinates between stores** today — polygons are created per-store via the map drawing tool only.

## Edge case — self-intersection and on-boundary points

Self-intersecting polygons (figure-8, crossover paths) and exact-boundary points are evaluated by the database's spatial functions — third-party behaviour, not CloudCart logic:

- The database treats self-intersecting polygons as invalid for certain spatial predicates and may return inconsistent results. Merchants drawing complex shapes should avoid figure-8 and crossover paths (verify).
- On-boundary points are typically counted as INSIDE the polygon by the spatial containment test, but merchants relying on exact boundary precision should test with a sample address (verify).

## Example — Sofia city + suburbs, irregular boundary

Setup:

- Polygon "Sofia city + suburbs" — drawn on the map, vertices selected to cover the city plus its commuter belt.
- Zone "Sofia metro" — operation 9 (polygon = "Sofia city + suburbs"). ALSO add operation 1 (country = BG) so tax matching works — see [[geo-targeting-feature-resolution]].
- Tax rule scoped to "Sofia metro": this works because the country rule is present.
- Shipping method "Sofia same-day" scoped to "Sofia metro" with a flat 3 BGN price.

Result:

- Customer in Sofia center → both rules match → BG VAT applied, Sofia same-day appears at checkout.
- Customer in Plovdiv → only the country rule matches for tax (so BG VAT still applies); the polygon doesn't match → Sofia same-day is hidden.

## Where it applies

- [[geo-polygons-settings-main-new]] — draws a new polygon on a Google Map.
- [[geo-polygons-settings-main-new]] — edits an existing polygon's vertices and display attributes.
- [[geo-zone]] — zones reference polygons via operation 9 rules.
- [[settings-cart]] — the Google Maps API key enables the draw-on-map UI.

## Related

- [[geo-targeting]] — hub.
- [[geo-polygons-settings-main-new]] — add polygon screen.
- [[geo-polygons-settings-main-new]] — edit polygon screen.
- [[geo-polygon]] — entity page.
- [[geo-targeting-zones]] — zone operations including operation 9 (polygon).
- [[geo-targeting-distances]] — alternative shape primitive.
- [[geo-targeting-post-codes]] — alternative scoping primitive.
- [[geo-targeting-feature-resolution]] — why polygon zones need a paired country rule for tax.
- [[geo-targeting-address-resolution]] — how the customer's coordinates are produced.

## Open Questions

- ⏸️ **Polygon self-intersection / on-boundary points.** Self-intersecting polygons and exact-boundary point coordinates are evaluated by the database's spatial functions (third-party behaviour). Merchants drawing complex shapes should avoid figure-8 / crossover paths; on-boundary precision needs a sample-address test. (verify)
