---
type: entity
aliases: ["Geo Polygon model", "Geo Polygon record", "Polygon record shape", "Polygon storage", "Drawn-outline record", "Гео полигон — запис"]
tags: [shipping, settings, geo, polygons, maps, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[geo-polygon]]. See the hub for the other aspects (matching, lifecycle, delete cascade).

# Geo Polygon — record model

## Identity

The **Geo Polygon record** is the stored shape of a single merchant-drawn outline: one closed polygon of latitude/longitude vertices plus a display name. Each record stores `(id, name, area, created_at, updated_at)` — the `area` field holds the polygon's coordinates (a paths array of `{lat, lng}` pairs) as Google Maps' JSON representation. There is no per-record second outline and no radius field; this is the arbitrary-shape counterpart to the circular [[geo-distance|Geo Distance]] record.

This page covers **what a polygon record holds, how the merchant fills it in, and the single allowed input method**. How the record is matched at checkout is on [[geo-polygon-matching]]; the create / edit / delete flow is on [[geo-polygon-lifecycle]]; the cascade behaviour on delete is on [[geo-polygon-delete-cascade]].

## Aliases

- "Geo Polygon model" / "Polygon record shape" — the wiki terms for the stored fields.
- "Drawn-outline record" — emphasises that the geometry is produced by drawing, not by typing coordinates.
- Bulgarian: "Гео полигон — запис".

## Key Attributes

| Field | What the merchant controls | Notes |
|-------|----------------------------|-------|
| **Name** (`name`) | Required free text on the Add / Edit form | Display label everywhere — list view, edit form, zone rule picker. Validation: Zod `min(1)` — *"The Polygon name field is required"*. Multi-line allowed. Placeholder: *"Add the name of the Polygon. Example: Paris or France"*. |
| **Drawing area** (`area`) | Drawn on the Google Map module; serialised by the `CcGoogleDrawMap` component | The polygon's coordinates — an array of `{lat, lng}` pairs forming a single closed outline, stored as Google Maps' JSON representation. Required (a polygon with no outline cannot serve any matching purpose). When the merchant re-opens an existing polygon, the saved outline reloads as editable on the map. |
| **Polygon color** | Customised via colour-rectangle picker on the right side of the map | Fill / stroke colour for the on-map rendering — purely UI sugar for the merchant's own visual organisation. Does not affect matching. |
| **Map provider** | n/a — Google Maps (legacy or new API, auto-detected from `isNewGoogleMapsApi`) | The module switches between two implementations based on the platform flag, but the merchant doesn't choose. Both render pan / zoom controls, the drawing tools at the top-left, the colour rectangles on the right, and vertex drag-to-edit behaviour. |
| **Created at** / **Updated at** | n/a (auto-set) | Standard timestamps. |
| **ID** | n/a (auto-assigned) | Foreign-key target referenced from `geo_zone_values.polygon_id` (zone operation 9 rules). |

### Single outline per record — multi-area zones combine multiple polygons

Each Geo Polygon record stores exactly ONE closed outline. Per the in-page help: *"Note you can only have one field on one polygon. You cannot make more than one outline."* For multi-area service zones (e.g. *"Sofia AND Plovdiv but not the highway between them"*), the merchant creates a separate polygon record per area and references all of them in a single Geo Zone via multiple operation-9 rule entries. Rules within a zone are OR-combined, so the multi-polygon zone matches if the customer's address falls inside ANY of the referenced polygons — see [[geo-polygon-matching]].

### Storage shape

The `area` field holds the polygon coordinates (paths array of `{lat, lng}` pairs) as JSON. The platform's address-matching layer reads this JSON, builds the point-in-polygon predicate, and tests customer coordinates against it at runtime.

### Google Maps API key is a hard prerequisite

The drawing module cannot render without a valid Google Maps API key configured in [[settings-cart]] → Google Maps. Without the key, the map iframe fails and polygon creation is blocked. There is no offline / alternative drawing mode (no numeric coordinate entry, no KML / GeoJSON / shapefile import). The Google Maps API version (legacy vs new) is auto-detected from the `isNewGoogleMapsApi` flag — the merchant doesn't pick.

### Drawing is the ONLY input method

The polygon outline is drawn directly on the Google Map module. The merchant CANNOT:

- Paste a list of lat/lng pairs to define the polygon numerically.
- Import polygons from KML, GeoJSON, or shapefile.
- Edit individual vertices via numeric coordinate entry — only via drag-to-edit on the map.

For merchants who have existing GIS data (e.g. a city-issued service-area shapefile), the workflow is to display the reference in another tool and manually trace the outline on the CloudCart map.

## Where it appears

- [[geo-polygons-settings-main-new]] — the Add screen where each record is drawn and created.
- [[geo-polygons-settings-main-new]] — the Edit screen where the saved outline reloads as editable.
- [[settings-geo-zones]] — the record's ID is referenced from a zone via an operation-9 rule entry.
- [[settings-cart]] — the Google Maps API key prerequisite for the drawing module.

## Related

- [[geo-polygon]] — hub.
- [[geo-polygon-matching]] — how the stored `area` JSON is tested against a customer's coordinates.
- [[geo-zone]] — entity that references the record via operation 9.
- [[geo-distance]] — sibling input with a different storage shape (center + radius rather than an outline).
- [[geo-polygons-settings-main-new]] — the Add screen.
- [[settings-cart]] — Google Maps API key prerequisite.

## Open Questions

- ⏸️ **Coordinate format / export** — the `area` field stores Google Maps JSON. Is there a documented format spec? Can polygons be exported / imported between stores or via API? (verify)
- ⏸️ **Bulk import / migration** — there's no UI for importing polygons from GIS files. How would a merchant migrating from another platform load dozens of pre-existing service-area polygons efficiently? (verify)
