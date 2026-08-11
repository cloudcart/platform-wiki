---
type: feature
nav_path: "Settings → Geo polygons → Delete cascade"
route_name: geo_polygons.settings.new
route_path: /admin/settings/geo-polygons-new
aliases: ["Polygon delete cascade", "ON DELETE CASCADE polygon", "Silent rule loss geo zone", "Deleting a polygon in use"]
tags: [settings, geo, polygons, shipping, maps]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Geo polygons — delete cascade

> Part of [[geo-polygons-settings-main-new]]. See the hub for related aspects (list/form, drawing limits, zone integration).

## Purpose

What happens when the merchant deletes a polygon that is still referenced by one or more geo zones. The short answer: the delete is **destructive and silent** — there is no warning, and the polygon rule disappears from every zone that used it, without affecting the zone's other rules.

## Where to find it

The Delete action is the per-row trash icon on the Geo polygons list (see [[geo-polygons-settings-list-form]]). There is no confirmation listing affected zones before the delete commits.

## What the merchant can do here

- **Delete a polygon** from the list. If the polygon is unused, nothing downstream is affected.
- **Audit before deleting** — to find out which zones will lose a rule, the merchant manually browses [[settings-geo-zones]] and looks for operation-9 (`OPERATION_POLYGON`) rules referencing this polygon. There is no built-in "where is this polygon used?" report.
- **Detach first (recommended)** — remove the polygon's operation-9 rule from each zone that references it before deleting, so the loss is intentional rather than silent.

## Settings & fields

This aspect documents delete behaviour rather than fields. The relevant database relationship:

| Element | Notes |
|---------|-------|
| `geo_zone_values.polygon_id` | FK to `geo_polygons(id)`, declared `ON DELETE CASCADE`. |
| `geo_zone_values` rows | Each represents a single rule (e.g. *"Includes only for polygon X"*) inside a specific zone. |
| `geo_zones` rows | Parent zones — never directly FK-referenced from the polygon, so they survive the delete. |

## Business rules

### Delete is ON DELETE CASCADE — silent rule loss in dependent zones

Verified against the database (migration `2020_11_23_134155_update_geo_zone_values_table.php`):

```sql
ALTER TABLE geo_zone_values
  ADD CONSTRAINT geo_zone_values_polygon_id
  FOREIGN KEY (polygon_id) REFERENCES geo_polygons(id)
  ON DELETE CASCADE ON UPDATE NO ACTION;
```

So when the merchant deletes a polygon:

1. The `geo_polygons` row is deleted.
2. **All `geo_zone_values` rows pointing at it are silently cascade-deleted.** These rows are rules like *"Includes only for polygon X"* inside specific geo zones.
3. The parent `geo_zones` rows themselves **survive** (they were never directly FK-referenced from the polygon). They just lose the specific polygon rule from their rule list.

### Merchant-visible effect

The merchant sees their geo zone is still there, but the "polygon: X" rule has disappeared from its rule list. Other rules in the same zone are unaffected. **There is no warning before delete** — the merchant cannot tell from the UI which zones (or which shipping methods / taxes / discounts that reference those zones) will lose a rule. The safe path is to first detach the polygon from any zone referencing it, then delete.

## Related

- [[geo-polygons-settings-main-new]] — hub.
- [[geo-polygons-settings-zone-integration]] is the other side of this relationship — how zones reference polygons in the first place.
- [[settings-geo-zones]] — where operation-9 (`OPERATION_POLYGON`) rules live; the merchant audits here before deleting.
- [[geo-polygon]] — entity page.
- [[geo-zone]] — entity page.

## Open questions

_None — delete behaviour verified against the FK constraint in the database._
