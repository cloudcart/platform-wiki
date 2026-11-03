---
type: entity
aliases: ["Geo Polygon lifecycle", "Polygon create edit flow", "Drawing a polygon", "Polygon editing", "Vertex drag-to-edit", "Гео полигон — жизнен цикъл"]
tags: [shipping, settings, geo, polygons, maps, lifecycle, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[geo-polygon]]. See the hub for the other aspects (model, matching, delete cascade).

# Geo Polygon — lifecycle

## Identity

The **Geo Polygon lifecycle** is the create → available → edit flow the merchant follows to draw, reshape, and maintain a polygon. The draw / edit mechanics run entirely on the Google Map module; saves are synchronous and flush the polygon lookup cache so the next checkout sees the new shape. This page covers everything except the destructive delete path — that is on [[geo-polygon-delete-cascade]] because it has surprising cascade behaviour that warrants its own page.

What the record stores is on [[geo-polygon-model]]; how a saved polygon is matched at checkout is on [[geo-polygon-matching]].

## Aliases

- "Geo Polygon lifecycle" / "Polygon create edit flow" — the wiki terms for the create-to-edit path.
- "Vertex drag-to-edit" — the only way to reshape an existing outline.
- Bulgarian: "Гео полигон — жизнен цикъл".

## Key Attributes

| Stage | What happens | Notes |
|-------|--------------|-------|
| **Drawn / created** | Name + traced outline saved as a new record | Cache invalidates; the next checkout sees the shape. |
| **Available as zone input** | Appears in the operation-9 polygon picker on [[settings-geo-zones]] | From here it influences whichever feature consumes the parent zone. |
| **Edited** | Outline reloads as editable; vertices drag / insert / delete | Save invalidates cache; every referencing zone picks up the new shape automatically. |
| **Deleted** | Per-row Remove button | ON DELETE CASCADE — see [[geo-polygon-delete-cascade]]. |

### Drawn / created

On [[geo-polygons-settings-main-new]] (or the modern variant [[geo-polygons-settings-main-new]]) the merchant types a name, pans / zooms the Google Map to the right area, switches the drawing tool to polygon mode, clicks point-by-point to place vertices, and closes the shape by clicking the starting vertex (or double-clicking). The merchant can optionally pick a colour from the colour-rectangle picker. On save, the polygon record is created with the serialised coordinates in `area` (see [[geo-polygon-model]]). The platform's geo-polygon lookup cache invalidates so the next checkout sees the new shape.

### Available as zone input

Once saved, the polygon appears in the polygon picker on [[settings-geo-zones]] when the merchant adds a rule of operation **9** to a Geo Zone. From that point on, the polygon influences whichever feature consumes the parent zone.

### Edited

The merchant opens the polygon's Edit form ([[geo-polygons-settings-main-new]]); the saved outline reloads as editable. They can drag any vertex to reshape, right-click a vertex to delete it (standard Google Maps Drawing Library behaviour), or insert intermediate vertices. The name is editable too. On save, the cache invalidates and every zone referencing this polygon picks up the new shape on the next address-matching computation — no re-save needed on the zone itself.

### Cache invalidation on save

Saves flush the geo-polygon lookup cache so the next geo-zone evaluation at checkout uses the new coordinates. Standard Settings cache behaviour.

### No queue, no notifications, no webhooks

Creating, updating, or deleting a polygon is purely synchronous. No background jobs, no admin notifications, no webhooks fire from this page.

### Permission

Standard settings-area permission applies; no granular per-feature permission distinct from the parent Settings. Moderators with the Settings permission can manage polygons.

## Where it appears

- [[geo-polygons-settings-main-new]] — the Add (drawing) screen. Modern variant: [[geo-polygons-settings-main-new]].
- [[geo-polygons-settings-main-new]] — the Edit screen where the saved outline reloads as editable.
- [[settings-geo-zones]] — where a saved polygon becomes an operation-9 rule.
- [[settings-cart]] — the Google Maps API key prerequisite for the drawing module.

## Related

- [[geo-polygon]] — hub.
- [[geo-polygon-model]] — what each saved record holds.
- [[geo-polygon-delete-cascade]] — the destructive delete path and its silent rule loss.
- [[geo-polygons-settings-main-new]] — the Add screen.
- [[geo-polygons-settings-main-new]] — the Edit screen.
- [[geo-polygons-settings-main-new]] — modern Geo Polygons feature page.
- [[geo-zone]] — entity that references the saved polygon via operation 9.
- [[settings-cart]] — Google Maps API key prerequisite.

## Open Questions

- ⏸️ **Re-geocoding on edit** — confirm whether reshaping a polygon affects any cached customer-address matches retroactively or only forward from the next checkout. (verify)
