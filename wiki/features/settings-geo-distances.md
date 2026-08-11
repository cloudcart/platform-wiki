---
type: feature
nav_path: "Settings → Geo distances"
route_name: geo_distances.settings.main
route_path: /admin/settings/geo-distances
aliases: ["Geo distances", "Distance zones", "Circular delivery zones", "Radius zones", "Гео разстояния", "Радиус зони"]
tags: [settings, geo, distance, radius, shipping, maps]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 9
---
# Geo distances

## Purpose

A circular-shape geographic zone definition: the merchant picks a point on a Google Map (by typing an address, or by dragging the marker), enters a distance in **meters**, and saves the named entry. The platform stores `(name, address text, distance, lat, lng)` and uses the entry — referenced from [[settings-geo-zones]] operation 10 (`OPERATION_DISTANCE`) — to match customer addresses that fall within the radius for shipping pricing, taxes, or discount targeting.

CloudCart's page-header summary: *"With geo distances from point functionality, you can calculate distances and set your shipping prices based on this."* Common use cases: "deliver within 10 km of the warehouse", "free shipping within 5 km of any store location", "premium 24h delivery within 30 km of central hub".

Distance entries are conceptually simpler than [[geo-polygons-settings-main-new|polygon]] entries — single centre point + single radius vs. arbitrary polygon vertices — and are evaluated at checkout by a native spatial distance computation rather than polygon containment, so they scale cleanly to hundreds of entries per merchant.

## Where to find it

Sidebar → Settings → **Geo distances**.

The page's breadcrumb reads "Settings → Geo distances" (with "Add new Geo distance" appended on add / edit). The route is `/admin/settings/geo-distances` (list root) or `/add` / `/edit/:id`. The header icon is the globe-africa icon.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect matching the question, not read every page.

- [[settings-geo-distances-list-add]] — list view, Add / Edit form layout, field grid, sub-routes, what the merchant can / cannot do.
- [[settings-geo-distances-distance-units]] — Distance input in meters; the **imperial-store FEET quirk**; `distance` vs `distance_in_meters` DB columns; unit-system display labels.
- [[settings-geo-distances-map-module]] — `CcGoogleMapsRadius` (new) and `GMapMap` (legacy) modules; Google Places autocomplete; draggable marker; live circle; auto-fit on radius change; mobile touch support; Maps API key prerequisite.
- [[settings-geo-distances-storage-spatial]] — `geo_distances` table layout, spatial `POINT` geometry column with a spatial index, coordinate precision, validation rules (name 191 chars, distance ≤ 5,000,000, lat/lng range).
- [[settings-geo-distances-matching-runtime]] — how customer addresses match at checkout: `ST_Distance_Sphere`, cache invalidation on save, integration via geo-zone operation 10.
- [[settings-geo-distances-defaults-prepopulation]] — MaxMind GeoIP pre-population of the Add form; Sofia 42.6977, 23.3219 fallback centre; default 1 km radius; default circle style + hidden fill/stroke columns.
- [[settings-geo-distances-deletion-cascade]] — `ON DELETE CASCADE` on the `distance_id` FK; deletion silently removes every zone rule that referenced the distance; merchant-facing risk.

## Sub-screens

| Label | Route name | Route path |
|-------|------------|------------|
| Geo distances (root) | `geo_distances.settings.main` | `/admin/settings/geo-distances` |
| List | `geo_distances.settings` | `/admin/settings/geo-distances` |
| Add | `geo_distances_add.settings` | `/admin/settings/geo-distances/add` |
| Edit | `geo_distances_edit.settings` | `/admin/settings/geo-distances/edit/:id` |

## What the merchant can do here

- Create / edit / delete distance entries — see [[settings-geo-distances-list-add]] for the field grid and the Add / Edit form layout.
- Pick a centre by typing an address (Google Places autocomplete) or by dragging a marker — see [[settings-geo-distances-map-module]].
- Enter a radius in **meters** (or **feet** on imperial-unit stores — see [[settings-geo-distances-distance-units]] for the unit quirk).
- Reference saved distance entries from a [[settings-geo-zones|geo zone]] rule of operation 10 (`OPERATION_DISTANCE`); the rule then drives shipping / tax / discount geometry.

## Settings & fields

See [[settings-geo-distances-list-add]] for the full field grid (Name, Address, Distance, Latitude, Longitude) with validation, placeholders, and the 12-column layout.

## Business rules

The high-impact rules per aspect (drill into the linked sub-page for full mechanics):

- **Meters is the input unit on metric stores; FEET on imperial stores** — the UI label always says "meters" but the backend interprets the integer per the store's `unit_system`. See [[settings-geo-distances-distance-units]].
- **Distance is stored as a spatial `POINT` geometry with a spatial index** — the centre point has a spatial index, so the runtime match scales to hundreds of entries in single-digit ms. See [[settings-geo-distances-storage-spatial]].
- **Customer-address matching uses a native spherical-distance computation in the database** — spherical-earth distance, accuracy ~0.5% (excellent for retail-scale delivery radii). See [[settings-geo-distances-matching-runtime]].
- **Deleting a distance silently removes referencing zone rules** — the FK is `ON DELETE CASCADE`. The merchant who deletes a distance used by an "Express delivery" method loses that rule without warning. See [[settings-geo-distances-deletion-cascade]].
- **Add form pre-populates from MaxMind GeoIP** — opens centred on the merchant's IP-located city with a 1000 m radius. See [[settings-geo-distances-defaults-prepopulation]].
- **No Google Maps API key → page is non-functional** — the autocomplete + map modules require it; configured on [[settings-cart]]'s Google Maps box. See [[settings-geo-distances-map-module]].
- **Permission**: standard settings-area permission; no granular per-feature permission distinct from the parent Settings.
- **No queue, no notifications, no webhooks** — CRUD is fully synchronous.

## Related

- [[settings]] — parent hub.
- [[settings-geo-zones]] — operation 10 (`OPERATION_DISTANCE`) references distance entries.
- [[geo-polygons-settings-main-new]] — alternative geometry for non-circular service areas.
- [[settings-cart]] — Google Maps API key (Box: Google Maps) prerequisite.
- [[settings-taxes]] — tax rules can scope to geo zones referencing these.
- [[shipping]] — shipping methods can scope to geo zones referencing these.
- [[geo-distance]] — entity page.
- [[geo-zone]] — entity page.
- [[geo-targeting]] — concept page on how shipping/tax/discounts use geometries at runtime.
- [[geo-targeting-distances]] — distance-specific geo-targeting mechanics.
- [[shipping-calculation]] — concept page.
- [[shipping-calc-geo-gating]] — distance + polygon geo-gating in the shipping calculator.
- [[tax-computation]] — concept page.

## Open questions

None — all previously-flagged items resolved against backend or distributed to sub-pages.
