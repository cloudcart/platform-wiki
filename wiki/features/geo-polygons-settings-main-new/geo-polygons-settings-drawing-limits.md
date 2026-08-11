---
type: feature
nav_path: "Settings → Geo polygons → Drawing module & limits"
route_name: geo_polygons_add.settings.new
route_path: /admin/settings/geo-polygons-new/add
aliases: ["Polygon drawing tool", "Google draw map", "One outline per polygon", "Polygon drawing limits"]
tags: [settings, geo, polygons, shipping, maps]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Geo polygons — drawing module & limits

> Part of [[geo-polygons-settings-main-new]]. See the hub for related aspects (list/form, zone integration, delete cascade).

## Purpose

How the embedded Google Map drawing tool works on the Add / Edit form, and the hard limits on what a single polygon record can hold. The merchant draws one closed outline directly on the map; there is no numeric coordinate entry and no file import.

## Where to find it

On the Add / Edit form at `/admin/settings/geo-polygons-new/add` (or `/edit/:id`) — the map module block sits below the **Polygon name** field. See [[geo-polygons-settings-list-form]] for the surrounding form.

The block is a card containing a help paragraph + the Google draw-map component bound to the form's `area`. The help text reads verbatim: *"Use the small buttons located in the upper left corner of the map to outline the polygon. Note you can only have one field on one polygon. You cannot make more than one outline. Change the polygon color from the rectangles on the right side of the map."*

## What the merchant can do here

The embedded draw-map module provides standard Google Maps Drawing Library behaviour:

- **Pan / zoom** standard Google Maps controls. The map loads centred at a default position; the merchant pans / zooms to the relevant area.
- **Drawing tools** at the top-left of the map (polygon drawing mode + selection mode).
- **Click during drawing mode** — place a vertex, point by point.
- **Double-click or click the starting vertex** — close the polygon.
- **After drawing** — drag any vertex to reshape; right-click a vertex to delete it.
- **Colour picker** — rectangles on the right side of the map set the polygon fill / stroke colour.

When the merchant finishes a shape, the new outline is written back into the form's `area` field. On Edit, the existing outline is loaded as an editable shape.

## Settings & fields

| Control | What it does | Notes |
|---------|--------------|-------|
| Drawing tool (top-left) | Switches between polygon-draw mode and selection mode. | Standard Maps Drawing Library control. |
| Vertex placement | Click places a vertex; double-click / click-start closes the shape. | One closed outline only. |
| Vertex edit | Drag to reshape; right-click to delete a vertex. | Post-draw editing. |
| Colour rectangles (right) | Set polygon fill / stroke colour. | Cosmetic; does not affect matching. |

The same draw-map component is used by the legacy interface. It supports both the legacy and the new Google Maps API; the platform auto-detects which version is active (the merchant does not choose), and warnings about a legacy version surface in [[settings-cart]].

## Business rules

### One outline per record
Each polygon record stores exactly one closed outline. The in-page help is explicit: *"you can only have one field on one polygon. You cannot make more than one outline."* To define a multi-area service zone (e.g. "Sofia AND Plovdiv but not the connecting highway"), the merchant creates a **separate polygon record per area** and references them all from a single geo zone — see [[geo-polygons-settings-zone-integration]].

### Drawing only — no numeric entry, no file import
The outline is drawn directly on the map. The merchant **cannot**:
- Paste a list of lat/lng pairs to define the polygon numerically.
- Import polygons from KML, GeoJSON, or shapefile.
- Edit individual vertices via numeric coordinate entry — only via drag-to-edit on the map.

For merchants with existing GIS data (e.g. a city-issued service-area shapefile), the workflow is to display the reference in another tool and manually trace the outline on the CloudCart map.

### Google Maps API key prerequisite
The drawing module cannot function without a valid Google Maps API key configured in [[settings-cart]] → Google Maps. Without the key, the map fails to render, which blocks polygon creation entirely. There is no offline / alternative drawing mode.

## Related

- [[geo-polygons-settings-main-new]] — hub.
- [[settings-cart]] — Google Maps API key (Box: Google Maps) is the prerequisite for the drawing module.
- [[settings-geo-distances]] — alternative geometry (distance-from-point) for circular service areas; polygons cover non-circular custom shapes.

## Open questions

_None — drawing surface fully verified against the modern Vue component._
