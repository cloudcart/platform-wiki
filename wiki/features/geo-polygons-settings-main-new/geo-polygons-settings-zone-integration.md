---
type: feature
nav_path: "Settings → Geo polygons → Zone integration & runtime matching"
route_name: geo_polygons.settings.new
route_path: /admin/settings/geo-polygons-new
aliases: ["Polygon geo zone integration", "OPERATION_POLYGON", "Polygon address matching", "Polygon storage shape"]
tags: [settings, geo, polygons, shipping, maps]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Geo polygons — zone integration & runtime matching

> Part of [[geo-polygons-settings-main-new]]. See the hub for related aspects (list/form, drawing limits, delete cascade).

## Purpose

How a saved polygon is consumed downstream: how [[settings-geo-zones]] reference it (operation 9 — `OPERATION_POLYGON`), how the coordinates are stored, how the platform tests a customer address against the shape at checkout, and the runtime performance trade-off of very detailed outlines.

## Where to find it

Polygons are created on the Geo polygons screen (see [[geo-polygons-settings-list-form]]) but referenced from the geo-zone editor. A merchant who wants a polygon to actually affect shipping / tax / discounts must add it as an operation-9 rule inside a zone on [[settings-geo-zones]].

## What the merchant can do here

The integration is mostly read-side — the merchant's actions on the polygon screen feed these downstream uses:

- **Scope shipping, taxes, and discounts to a drawn area** — by referencing the polygon from a geo zone (operation 9), then attaching that zone to a shipping method ([[shipping]]), tax rule ([[settings-taxes]]), or discount target.
- **Combine multiple polygons** — a single geo zone can reference several polygons (OR-combined per zone semantics), so a multi-area service zone is built from multiple single-outline polygon records.
- **Verify which polygon a zone uses** — by browsing [[settings-geo-zones]] and looking for operation-9 (`OPERATION_POLYGON`) rules that name the polygon.

## Settings & fields

This aspect has no editable fields of its own — it documents how the polygon's stored data is referenced. The relevant identifiers:

| Element | Notes |
|---------|-------|
| `polygon_id` | Foreign key from a geo-zone rule row to the polygon. |
| operation 9 (`OPERATION_POLYGON`) | The geo-zone rule operation type that means "match if address is inside this polygon". |
| `area` (paths array) | The polygon's stored coordinates, read by the address-matching layer. |

## Business rules

### Storage shape
Each polygon row stores `(id, name, area, created_at, updated_at)`. `area` holds the Google Maps polygon coordinates (a paths array of `{lat, lng}` pairs) as JSON. The platform's address-matching layer reads this JSON, builds a polygon contains-point predicate, and tests customer addresses against it during checkout / cart computation. See [[geo-targeting]] for the cross-cutting concept of how geometries gate shipping / tax / discounts at runtime.

### Referenced by geo zones via operation 9
Polygons are referenced from [[settings-geo-zones]] operation 9 (`OPERATION_POLYGON`) via `polygon_id`. A polygon does nothing on its own — it only affects the storefront once a zone references it and that zone is attached to a shipping method, tax rule, or discount.

### Multi-area zones use multiple polygons
Because each polygon holds exactly one outline (see [[geo-polygons-settings-drawing-limits]]), a multi-area service zone is assembled by referencing several polygon records from one geo zone.

### Runtime performance trade-off
When CloudCart computes a customer's geo-zone match at checkout, it iterates the polygons referenced by the zones under test. With many polygons or very complex outlines (hundreds of vertices), this can add latency. There is **no in-page warning** about polygon complexity — merchants drawing very detailed shapes should be aware of the trade-off and prefer simpler outlines where possible.

## Related

- [[geo-polygons-settings-main-new]] — hub.
- [[settings-geo-zones]] — operation 9 (`OPERATION_POLYGON`) references polygons; the building block for custom-shape zones.
- [[geo-targeting]] — concept page: how shipping / tax / discounts use geometries at runtime.
- [[shipping]] — shipping methods scope to zones that reference polygons.
- [[shipping-calculation]] — concept page; references geo zones (and indirectly polygons).
- [[settings-taxes]] — tax rules scope to zones that reference polygons.
- [[tax-computation]] — concept page; same.
- [[geo-zone]] — entity page.

## Open questions

_None — integration surface verified against the geo-zone rule model._
