---
type: entity
aliases: ["Geo Distance lifecycle", "Distance create edit delete", "Distance map auto-fit", "Distance cache invalidation", "Multi-center coverage", "Гео разстояние — жизнен цикъл"]
tags: [shipping, settings, geo, distance, radius, lifecycle, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[geo-distance]]. See the hub for the other aspects (model, units, matching).

# Geo Distance — lifecycle & management

## Identity

The **lifecycle** of a Geo Distance is the create / edit / delete flow the merchant drives on [[settings-geo-distances]], plus the side-effects of each save: the live map auto-fitting to the chosen radius, the lookup-cache invalidation, and how multiple records combine for multi-center coverage. Creating, editing, or deleting a distance is purely synchronous — **no background jobs, no admin notifications, no webhooks** fire from this page.

This page covers **how the merchant manages records over time**. The stored fields are on [[geo-distance-model]]; the radius unit is on [[geo-distance-units]]; the checkout match is on [[geo-distance-matching]].

## Aliases

- "Geo Distance lifecycle" / "Distance create edit delete" — the wiki terms.
- "Distance map auto-fit" — the viewport behaviour on radius change.
- "Multi-center coverage" — combining several records in one zone.
- Bulgarian: "Гео разстояние — жизнен цикъл".

## Key Attributes

| Stage | What the merchant does | Side-effect |
|-------|------------------------|-------------|
| **Create** | + New Geo distance → name, pick address, enter radius, verify live circle | Record saved as `(name, text, distance, lat, lng)`; lookup cache invalidates. |
| **Available as zone input** | (automatic) | Appears in the distance picker on [[settings-geo-zones]] for operation-10 rules. |
| **Edit** | Open Edit form; address / radius reload on the map; re-type / drag / change radius | On save, cache invalidates; every referencing zone picks up the new center + radius on the next match — no re-save on the zone. |
| **Delete** | Per-row Remove on the list | FK behaviour vs cascade needs verification (see Open Questions). |

### Lifecycle states

1. **Created.** On [[settings-geo-distances]] the merchant clicks **+ New Geo distance**, types a name, picks an address from the Google Places autocomplete (or pans the map and drags the marker), enters a radius (see [[geo-distance-units]]), and verifies the live circle preview. On save, the record is created with `(name, text, distance, lat, lng)` and the geo-distance lookup cache invalidates so the next checkout sees the new record.
2. **Available as zone input.** Once saved, the record appears in the distance picker on [[settings-geo-zones]] when the merchant adds an operation-10 rule to a Geo Zone. From that point on, the distance influences whichever feature consumes the parent zone.
3. **Edited.** The merchant opens the Edit form; the saved address / radius reload as editable on the map. They can re-type a new address, drag the marker, or change the radius. The map auto-fits its viewport to the new radius. On save, the cache invalidates and every zone referencing this record picks up the new center + radius on the next address-matching computation — no re-save needed on the zone itself.
4. **Deleted.** The merchant uses the per-row Remove button on the list. Deletion of a record that's in use by a zone (and transitively by shipping methods / tax rules / discount targets) is expected to be FK-blocked or cascade-warned — the merchant should remove it from any referencing zones first. Exact UX (HTTP 422 with affected-zone names vs cascade) needs verification — see Open Questions.

### Multi-center coverage combines multiple records

Each record stores exactly one center + one radius (see [[geo-distance-model]]). For multi-warehouse coverage (e.g. *"within 30 km of EITHER of our two warehouses"*), the merchant creates one record per warehouse and references both from a single Geo Zone via multiple operation-10 rule entries. Rules within a zone are OR-combined, so the multi-distance zone matches if the customer's address is within any of the referenced radii.

### Map auto-fits to the chosen radius

The map module auto-fits its viewport to the chosen radius when the merchant changes the `distance` value. Typing a very large radius (e.g. `100000` m = 100 km) zooms the map out to show the whole circle without manual interaction; dragging the radius down to `100` m zooms back in. Works on both the new and legacy Google Maps modules. The merchant should not need to manually zoom out to see their configured radius.

### Cache invalidation on save

Saves flush the geo-distance lookup cache so the next geo-zone evaluation at checkout uses the updated values. Standard Settings cache behaviour.

### No queue, no notifications, no webhooks

Creating, updating, or deleting a record is purely synchronous. No background jobs, no admin notifications, no webhooks fire from this page.

### Permission

Standard settings-area permission applies; no granular per-feature permission distinct from the parent Settings. Moderators with the Settings permission can manage distance records.

## Where it appears

- [[settings-geo-distances]] — the master list + Add / Edit form; where create / edit / delete happen.
- [[settings-geo-zones]] — where a saved record is attached to a zone via an operation-10 rule.

## Related

- [[geo-distance]] — hub.
- [[geo-distance-model]] — the record shape created / edited here.
- [[geo-distance-matching]] — what the cached values feed at checkout.
- [[settings-geo-distances]] — the management feature.
- [[settings-geo-zones]] — where the record is consumed.

## Open Questions

- ⏸️ **FK-protected delete vs cascade** — confirm whether deleting a record referenced by a Zone returns HTTP 422 with the affected Zone names, or silently cascades like the [[geo-polygon]] FK. (verify)
- ⏸️ **Address re-geocoding on edit** — when the merchant re-types the address, does the platform re-geocode and overwrite lat/lng, or does it require an explicit autocomplete pick to update coordinates? (verify)
