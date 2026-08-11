---
type: feature
nav_path: "Settings → Geo polygons"
route_name: geo_polygons.settings.main.new
route_path: /admin/settings/geo-polygons-new
aliases: ["Geo polygons", "Polygons", "Delivery zones (custom)", "Гео полигони", "Полигони"]
tags: [settings, geo, polygons, shipping, maps]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 5
---
# Geo polygons

## Purpose

A map-drawing screen where the merchant defines arbitrary polygonal areas on a Google Map and saves them with a name. Each polygon is a **single closed outline** (multiple separate outlines in one record are not supported). These named polygons are then referenced from [[settings-geo-zones]] (operation 9 — `OPERATION_POLYGON`) to scope shipping methods, taxes, and discounts to customers whose address falls inside the drawn shape.

CloudCart's page header says it directly: *"Set quadrants on the map, according to which you can accept orders in your store."* Common use cases: courier delivery zones around a warehouse, "we deliver within these neighborhoods only" rules for small businesses, and custom service-area definitions that don't match administrative boundaries.

This page is the **hub** for the Geo polygons feature. The detail surfaces are split into the aspect pages below.

## Sub-pages (in this cluster)

- [[geo-polygons-settings-list-form]] — the list view + Add/Edit form: routes, `name` field, save/delete flow, validation.
- [[geo-polygons-settings-drawing-limits]] — the Google Map drawing module: how to outline a polygon, plus the hard limits (one outline per record, no numeric entry, no file import, Maps API key prerequisite).
- [[geo-polygons-settings-zone-integration]] — how geo zones reference polygons (operation 9), the stored coordinate shape, runtime address matching, and the performance trade-off of complex outlines.
- [[geo-polygons-settings-delete-cascade]] — the verified `ON DELETE CASCADE` behaviour: deleting a polygon silently removes its rule from every zone that used it.

## Where to find it

Sidebar → Settings → **Geo polygons**. The breadcrumb reads "Settings → Geo polygons" (with the active sub-action appended on add/edit). The route is `/admin/settings/geo-polygons-new` — the `-new` suffix is the modern Vue interface URL. (The legacy `/admin/settings/geo-polygons` route still works but the merchant is documented to use this version.) The header icon is the globe-africa icon, and a single "Polygons" tab is shown, with a conditional "Add Polygon" / "Edit Polygon" tab on create/edit routes.

For the full route table and the list / Add / Edit surfaces, see [[geo-polygons-settings-list-form]].

## What the merchant can do here

At a glance (each item is detailed in an aspect page):

- **Browse, add, edit, and delete** named polygons — see [[geo-polygons-settings-list-form]].
- **Draw a polygon** on the embedded Google Map with point-by-point vertices and a colour picker — see [[geo-polygons-settings-drawing-limits]].
- **Reference polygons from geo zones** to scope shipping, taxes, and discounts to a drawn area — see [[geo-polygons-settings-zone-integration]].

What the merchant **cannot** do here: draw more than one outline per record, import polygons from KML / GeoJSON / shapefile, enter coordinates numerically, or draw without a Google Maps API key — all detailed in [[geo-polygons-settings-drawing-limits]].

## Settings & fields

The Add / Edit form has just two inputs — **Polygon name** (`name`, required) and the **drawing area** (`area`, the serialized map shape). The full field table, validation strings, and the API payload shape are documented on [[geo-polygons-settings-list-form]]. The drawing-module controls are on [[geo-polygons-settings-drawing-limits]].

## Business rules

The cross-cutting rules, each owned by an aspect page:

- **One closed outline per record** — multi-area zones use multiple polygon records OR-combined in one zone. See [[geo-polygons-settings-drawing-limits]] + [[geo-polygons-settings-zone-integration]].
- **Google Maps API key required** — no key means no drawing module; configured in [[settings-cart]]. See [[geo-polygons-settings-drawing-limits]].
- **Synchronous save** — no background jobs, notifications, or webhooks; saving flushes the geo-polygon cache. See [[geo-polygons-settings-list-form]].
- **Delete is `ON DELETE CASCADE`** — silently strips the polygon rule from every dependent zone, with no warning. See [[geo-polygons-settings-delete-cascade]].

## Related

- [[settings]] — parent hub.
- [[settings-geo-zones]] — operation 9 (`OPERATION_POLYGON`) references polygons defined here. Polygons are the building block for custom-shape geo zones.
- [[settings-cart]] — Google Maps API key (Box: Google Maps) is the prerequisite for the drawing module.
- [[settings-geo-distances]] — alternative geometry: distance-from-point (circular service areas). Polygons are for non-circular custom areas.
- [[settings-taxes]] — tax rules can scope to geo zones that reference polygons.
- [[shipping]] — shipping methods can scope to geo zones that reference polygons.
- [[geo-polygon]] — entity page.
- [[geo-zone]] — entity page.
- [[geo-targeting]] — concept page on how shipping/tax/discounts use geometries at runtime.
- [[shipping-calculation]] — concept page; references geo zones (and indirectly polygons).
- [[tax-computation]] — concept page; same.

## Open questions

_None — feature surface fully verified against the modern Vue + API + DB layer; details distributed across the four aspect pages._
