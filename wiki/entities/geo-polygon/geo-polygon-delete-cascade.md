---
type: entity
aliases: ["Geo Polygon delete cascade", "Polygon delete behaviour", "Polygon cascade delete", "Silent rule loss on polygon delete", "Polygon FK cascade", "Гео полигон — изтриване"]
tags: [shipping, settings, geo, polygons, delete, cascade, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[geo-polygon]]. See the hub for the other aspects (model, matching, lifecycle).

# Geo Polygon — delete cascade

## Identity

The **Geo Polygon delete cascade** is the destructive side-effect of removing a polygon: deleting a polygon record is **ON DELETE CASCADE** at the foreign-key level, so the polygon row AND **every [[geo-zone|Geo Zone]] rule pointing at it are deleted together — silently, with no UI warning**. The parent zones survive but lose the specific polygon rule. This is the one polygon operation that can silently break shipping / discount targeting across multiple zones, so it gets its own page.

The create / edit flow (which is non-destructive) is on [[geo-polygon-lifecycle]]; what the record stores is on [[geo-polygon-model]].

## Aliases

- "Geo Polygon delete cascade" / "Polygon cascade delete" — the wiki terms for the destructive FK behaviour.
- "Silent rule loss on polygon delete" — the support-facing description of the symptom.
- Bulgarian: "Гео полигон — изтриване".

## Key Attributes

| Aspect | Behaviour | Notes |
|--------|-----------|-------|
| **FK behaviour** | ON DELETE CASCADE | The `geo_zone_values_polygon_id` FK cascades. |
| **What is deleted** | Polygon row + all operation-9 rule rows referencing it | The zone-rule rows pointing at this polygon's ID. |
| **What survives** | The parent Geo Zones | They lose only the specific polygon rule; other rules unaffected. |
| **Warning before delete** | None | No confirmation summary of affected zones. |

### Delete is ON DELETE CASCADE — silent rule loss in dependent zones

Verified via migration `2020_11_23_134155_update_geo_zone_values_table.php` (the `geo_zone_values_polygon_id` FK is `ON DELETE CASCADE`). When the merchant uses the per-row Remove button on the polygon list and deletes a polygon:

1. The polygon row is deleted.
2. **All `geo_zone_values` rows pointing at it are silently cascade-deleted** — these rows represent rules like *"Includes only for polygon X"* inside specific zones.
3. The parent Geo Zones SURVIVE; they just lose the specific polygon rule from their rule list. Other rules in the same zone are unaffected.

There is **no UI warning** before delete and **no audit summary** of which zones lost a rule.

### Why this matters to the merchant

Because the consuming features ([[settings-shipping]], [[marketing-discounts]], payment providers, fees, customer groups, Cart Rules) all reference the zone — never the polygon directly (see [[geo-polygon-matching]]) — deleting a polygon can silently change which addresses a shipping method or discount applies to, with no error and no notification. A zone that previously matched *"inside the drawn Sofia outline"* simply stops matching that area; if the polygon was the zone's only meaningful rule, the zone may now match nothing (or, for tax, it may already have matched nothing — see the country-only rule on [[geo-polygon-matching]]).

### How to audit affected zones before deleting

There is no built-in impact report. To know what a delete will break, the merchant must manually browse [[settings-geo-zones]] looking for operation-9 rules referencing this polygon's ID **before** deleting. Recommended workflow:

1. Open [[settings-geo-zones]] and inspect each zone's rule list for a polygon rule naming this polygon.
2. Note which shipping methods / discounts / fees scope to those zones.
3. Only then delete — or, if the polygon is reused widely, reshape it via the Edit form (see [[geo-polygon-lifecycle]]) instead of deleting and redrawing.

## Where it appears

- [[geo-polygons-settings-main-new]] — the polygon list / row context where the Remove button lives.
- [[settings-geo-zones]] — where the cascaded operation-9 rules disappear from zone rule lists.
- [[settings-shipping]] — shipping methods scoped to affected zones may silently change coverage.
- [[marketing-discounts]] — discounts scoped to affected zones may silently change coverage.

## Related

- [[geo-polygon]] — hub.
- [[geo-polygon-lifecycle]] — the non-destructive create / edit flow; reshape instead of delete to avoid the cascade.
- [[geo-polygon-matching]] — why deleting a polygon ripples to shipping / discounts via the zone.
- [[geo-zone]] — the entity whose operation-9 rules are cascade-deleted.
- [[settings-geo-zones]] — where to audit affected zones before deleting.
- [[settings-shipping]] — shipping methods consume the affected zones.
- [[marketing-discounts]] — discounts consume the affected zones.

## Open Questions

- ⏸️ **Cascade vs FK-protection parity with distances** — the sibling [[geo-distance]] FK behaviour is still being confirmed; verify whether distance delete cascades the same way or returns a 422 with affected zone names. (verify)
