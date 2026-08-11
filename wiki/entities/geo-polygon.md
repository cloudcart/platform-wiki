---
type: entity
aliases: ["Geo Polygon", "Polygon", "Custom delivery shape", "Drawn shape", "Service area polygon", "Гео полигон", "Полигон"]
tags: [shipping, settings, geo, polygons, maps, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Geo Polygon

## Identity

A **Geo Polygon** is a **named, merchant-drawn shape on a Google Map** that defines an arbitrary geographic outline (a closed polygon of latitude/longitude vertices). The merchant uses Geo Polygons when neither administrative regions (country / region / city) nor distance circles ([[geo-distance|Geo Distances]]) accurately describe the area they want to target — typical examples are *"Sofia center cropped at the river"*, *"a specific neighborhood with irregular boundaries"*, *"the part of Plovdiv our courier actually services"*, or *"an island reachable only by ferry"*. Each Geo Polygon stores a single closed outline (multi-area shapes require multiple polygon records) and has nothing to do with shipping, tax, or discounts on its own.

A Geo Polygon is an **INPUT to a [[geo-zone|Geo Zone]] rule**, never consumed directly. The merchant draws the polygon ONCE on [[geo-polygons-settings-main-new]] (or its modern variant), then references it from one or more Geo Zones via zone operation **9** (`OPERATION_POLYGON`). The zone is what shipping methods, tax rules, payment providers, discounts, fees, customer-group restrictions, and Cart Rules attach to — the polygon merely tells the zone "addresses inside THIS shape count as inside the zone." See [[geo-targeting]] for the end-to-end mechanism.

A Geo Polygon is distinct from a **[[geo-distance|Geo Distance]]** (a center point + radius, used for circular areas like *"within 30 km of the warehouse"*) and from a **[[geo-zone|Geo Zone]]** (the merchant-named container that references polygons and distances alongside country / region / city / post-code rules).

This entity is split into four aspect pages (below). The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[geo-polygon-model]] — what the record stores (`name`, `area`, color, ID); the single-outline-per-record rule; the JSON storage shape; the Google Maps API-key prerequisite; drawing as the only input method.
- [[geo-polygon-matching]] — how a polygon is matched at checkout (point-in-polygon against the customer's coordinates); the inputs-to-zones rule; the critical "tax matching ignores polygons" gotcha; performance scaling with polygon and vertex count.
- [[geo-polygon-lifecycle]] — the draw / edit flow; vertex drag-to-edit; cache invalidation on save; permissions; no queue / notifications / webhooks.
- [[geo-polygon-delete-cascade]] — the ON DELETE CASCADE behaviour on delete; silent rule loss in dependent zones; how to audit affected zones before deleting.

## Aliases

- "Geo Polygon" — the canonical merchant-facing wiki term.
- "Polygon" — the short form; appears in the Sidebar label ("Geo polygons"), the list-page title, and the in-page help text.
- "Custom delivery shape" / "Drawn shape" / "Service area polygon" — informal merchant language emphasising the draw-on-map mechanic.
- Bulgarian: "Гео полигон", "Полигон".

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** (`name`) | Required free text on the Add / Edit form | Display label everywhere — list view, edit form, zone rule picker. Validation: Zod `min(1)` — *"The Polygon name field is required"*. Placeholder: *"Add the name of the Polygon. Example: Paris or France"*. |
| **Drawing area** (`area`) | Drawn on the Google Map module | An array of `{lat, lng}` pairs forming a single closed outline, stored as Google Maps' JSON representation. Required. See [[geo-polygon-model]]. |
| **Polygon color** | Colour-rectangle picker on the right side of the map | Fill / stroke colour for the on-map rendering — purely UI sugar. Does not affect matching. |
| **Created at** / **Updated at** | n/a (auto-set) | Standard timestamps. |
| **ID** | n/a (auto-assigned) | Foreign-key target referenced from `geo_zone_values.polygon_id` (zone operation 9 rules). |

Full storage shape, the single-outline-per-record constraint, and the Google Maps prerequisite are on [[geo-polygon-model]].

## Where it appears

- [[geo-polygons-settings-main-new]] — Add new polygon screen (drawing form). Modern variant: [[geo-polygons-settings-main-new]].
- [[geo-polygons-settings-main-new]] — Edit existing polygon screen.
- [[settings-geo-zones]] — Geo Zones reference polygons via operation 9 (`OPERATION_POLYGON`) rule entries. Where the merchant attaches a polygon to a zone.
- [[settings-shipping]] — shipping methods scope to zones that may reference polygons.
- [[settings-taxes]] — tax rules scope to zones, but tax matching IGNORES polygons (country-only rule). See [[geo-polygon-matching]].
- [[marketing-discounts]] — discounts can restrict to zones that reference polygons.
- [[settings-cart]] — the Google Maps API key (Box: Google Maps) is the prerequisite for the drawing module.

## Related

- [[geo-polygons-settings-main-new]] — Add screen.
- [[geo-polygons-settings-main-new]] — Edit screen.
- [[geo-polygons-settings-main-new]] — modern Geo Polygons feature page.
- [[geo-zone]] — entity that references polygons via operation 9.
- [[geo-distance]] — sibling input (center + radius) referenced via operation 10.
- [[geo-targeting]] — concept page on how Zones / Polygons / Distances combine end-to-end.
- [[shipping-calculation]] — how zones (and polygons through them) gate shipping quotes.
- [[tax-computation]] — explains the country-only rule for tax matching that makes polygons invisible to the tax engine.
- [[settings-shipping]] — shipping methods consume zones.
- [[settings-taxes]] — tax rules consume zones.
- [[settings-cart]] — Google Maps API key prerequisite.
- [[plan-gates]] — concept page on plan gating (polygons themselves are not plan-gated, but related features may be).

## Open Questions

- ⏸️ **Coordinate format / export** — the `area` field stores Google Maps JSON. Is there a documented format spec? Can polygons be exported / imported between stores or via API? See [[geo-polygon-model]].
- ⏸️ **Self-intersecting polygons** — what happens when a polygon is drawn as a figure-8 or otherwise self-intersects? Standard point-in-polygon implementations vary on this case (even-odd vs winding-number rules). See [[geo-polygon-matching]].
- ⏸️ **Bulk import / migration** — there's no UI for importing polygons from GIS files. How would a merchant migrating from another platform load dozens of pre-existing service-area polygons efficiently? See [[geo-polygon-model]].
