---
type: feature
nav_path: "Settings → Geo distances → Deletion cascade"
route_name: geo_distances.settings
route_path: /admin/settings/geo-distances
aliases: ["Geo distances deletion", "Geo distance ON DELETE CASCADE", "Geo distance silent removal", "Geo distance FK cascade", "Delete geo distance"]
tags: [settings, geo, distance, deletion, cascade, foreign-key, risk]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-distances]]. See the hub for the other aspects (list/form, units, map module, storage, runtime matching, defaults).

# Geo distances — deletion cascade behaviour

## Purpose

Deleting a Geo distance record looks harmless — the merchant clicks Remove on a row and the record disappears. But the `distance_id` foreign key on `geo_zone_values` is configured `ON DELETE CASCADE`, so every [[settings-geo-zones|geo zone]] rule that referenced the distance is **silently removed** at the same time. There is no warning, no FK error, and no surfaced summary of which zone rules just vanished. This aspect documents the cascade behaviour, the risk to checkout configuration, and the recommended pre-delete safety check.

## Where to find it

The per-row Remove button on [[settings-geo-distances-list-add|the Geo distances list view]].

## What the merchant can do here

- Delete a distance entry from the list — the record is removed from `geo_distances`.
- The same delete cascades to remove every `geo_zone_values` row whose `distance_id` referenced the deleted distance.
- After deletion, the cascade is **not undoable** from the UI — the merchant would need to recreate the distance + re-add the rule to every affected zone.

## Settings & fields

There are no merchant-visible settings on this aspect. The cascade behaviour is set at the database-schema level by the migration `2024_06_28_121355_update_geo_zone_values_table_fix_fk`:

| Foreign key column | On parent delete |
|--------------------|------------------|
| `geo_zone_values.distance_id` | `ON DELETE CASCADE` — referencing zone rule rows are silently removed when the parent distance is deleted. |

## Business rules

### Deleting a distance does NOT error — it silently removes referencing zone rules

The `geo_zone_values.distance_id` foreign key was set up with `ON DELETE CASCADE`. So:

- Deleting a `geo_distances` row **does NOT** raise an FK constraint error.
- Every `geo_zone_values` row that references it via `distance_id` is silently removed by the database.
- Every [[settings-geo-zones|geo zone]] that had a rule of operation 10 (`OPERATION_DISTANCE`) pointing at the deleted distance now has **one fewer rule**.

The wiki's earlier "FK-blocked on delete" note (in the original page version) was incorrect at the DB level — there is no protection.

### Practical risk — silent loss of shipping / tax / discount geometry

The merchant impact of a silent cascade can be significant:

- A merchant deletes a distance named "10 km from main warehouse" without checking what references it.
- An "Express delivery" shipping method scoped to a zone that had a rule using that distance now has one fewer condition in its zone — meaning the zone matches a different set of customers.
- Tax rules / discount targeting scoped to the same zone behave the same way.
- The merchant sees no error, no warning, no log of the change.

Checkout behaviour shifts silently. A support ticket six weeks later — "why are some customers paying the wrong shipping?" — can be hard to trace back to a long-forgotten distance deletion.

### Recommended pre-delete safety check

Before deleting a distance entry, the merchant should manually inspect [[settings-geo-zones|Geo zones]] for any rule of operation 10 that references it. The list view has **no inline "used by N zones" indicator** (verified 2026-06-11 against `SettingsGeoDistancesListPage.vue` — the `CcTable` only renders `distance_name` and `actions` columns; no usage badge, no warning modal on delete), so the check is fully manual:

1. Open Geo zones.
2. For each zone with a Distance rule, open the rule editor.
3. Confirm whether the referenced distance is the one about to be deleted.
4. Either replace the rule with a different distance or accept the cascade.

A safer alternative: rename the distance to something obviously "to be deleted" first, then run a test checkout against an address that should match the affected zone, observe the shipping options. If checkout behaves as expected without the rule, deletion is safe.

### No undo / audit log surface

- Deletion is not recorded in any merchant-visible audit log on the Geo distances feature itself.
- The cascading `geo_zone_values` row removals are not surfaced either.
- The merchant who wants a record of what was deleted needs to keep their own notes or query the DB directly.

### No queue, no notifications, no webhooks on delete

Deletion is fully synchronous. No background job, no admin email, no webhook fires from this path. The cache for [[settings-geo-distances-matching-runtime|runtime matching]] flushes immediately so the next checkout sees the cascaded state.

### Cascade applies on every type of deletion path

The cascade is at the DB level — it applies whether the merchant deletes via:

- The list view's per-row Remove button.
- **Bulk-delete IS surfaced in the list UI** — the `CcTable` is wired with `delete-default-bulk-action-url="/admin/api/core/settings/geo-distances"` and `delete-type-default-bulk-action="delete"`, so selecting multiple rows and triggering the standard table bulk-delete deletes them all (each one cascading its own zone-rule rows). Verified 2026-06-11.
- A JSON-API v2 DELETE request.
- A direct DB delete (during support intervention or migration).

Anyone deleting a distance row should assume referencing zone rules go with it.

## Related

- [[settings-geo-distances]] — hub.
- [[settings-geo-distances-list-add]] — where the Remove button lives.
- [[settings-geo-zones]] — the rules table that gets silently cascaded.
- [[settings-geo-zones-deletion-cascade]] — analogous cascade behaviour on the zone side; same migration created both FK definitions.
- [[settings-geo-distances-matching-runtime]] — how the cascaded rule removals affect checkout behaviour silently.

## Open questions

None — list-view columns + bulk-delete surface verified against `SettingsGeoDistancesListPage.vue` (2026-06-11).

