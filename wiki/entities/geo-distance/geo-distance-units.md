---
type: entity
aliases: ["Geo Distance units", "Distance radius unit", "Meters vs feet radius", "unit_system distance", "distance_in_meters", "30 km misconfiguration", "Гео разстояние — мерна единица"]
tags: [shipping, settings, geo, distance, radius, units, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[geo-distance]]. See the hub for the other aspects (model, matching, lifecycle).

# Geo Distance — radius units

## Identity

The **radius unit** of a Geo Distance is the single most error-prone part of the entity. The `distance` input takes a plain integer with **no unit picker** — the unit is whatever the store's `unit_system` setting says. A merchant who thinks in kilometres or miles must convert manually, and getting this wrong silently produces a zone no customer ever matches.

This page covers **what unit the `distance` value is in, how the store's `unit_system` decides it, and the canonical misconfiguration**. The record's other fields are on [[geo-distance-model]]; the actual checkout match (which always runs in metres internally) is on [[geo-distance-matching]].

## Aliases

- "Geo Distance units" / "Distance radius unit" — the wiki terms.
- "Meters vs feet radius" — the metric-vs-imperial split.
- "`distance_in_meters`" — the derived column used for the actual match.
- "30 km misconfiguration" — the canonical merchant mistake.
- Bulgarian: "Гео разстояние — мерна единица".

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Distance value** (`distance`) | Required integer ≥ 1 | The radius, expressed in the store's unit system. Suffix label reflects the unit. No decimals. |
| **Unit system** (`unit_system`) | Set store-wide (not on this form) | Decides whether the `distance` value is read as metres or feet. Snapshotted onto the record at save time. |
| **Derived metres** (`distance_in_meters`) | n/a (auto-computed) | On imperial stores, the platform stores the entered feet value AND auto-computes the equivalent metres into this separate column, which is what the great-circle match actually uses (see [[geo-distance-matching]]). |

### Distance unit follows the store's `unit_system` setting

The Distance input takes integers in the store's configured unit system:

- **Metric stores** — the input is in **metres**. 1 km = `1000`, 10 km = `10000`, 30 km = `30000`, 50 km = `50000`.
- **Imperial stores** — the input is in **feet**. The platform stores the entered value AND auto-computes the equivalent in metres into the separate `distance_in_meters` column used for the actual great-circle match. 1 mile ≈ `5280` feet.

The save handler snapshots the store's current `unit_system` onto the record at save time, so subsequent stores of the same record stay consistent even if the store later changes its unit system. The integer-only validation rejects decimals.

### The "entered 30 thinking 30 km" misconfiguration

**Entering `30` thinking "30 km" on a metric store is the single most common merchant misconfiguration with geo distances.** It produces a 30-**metre** radius (essentially the building itself), so no customer's address ever falls inside the zone and the merchant reports *"my local-delivery zone never matches anyone."* The fix is always the same: multiply by 1000 for kilometres (30 km = `30000`), or by ~1609 for miles when thinking in miles on a metric store. On imperial stores the analogue is entering a mile count instead of feet.

When a support ticket says a distance-based zone matches no one, **check the `distance` value against the intended kilometres first** — it is almost always a missing three zeros.

## Where it appears

- [[settings-geo-distances]] — the Add / Edit form where the merchant types the `distance` value (with the unit suffix label).
- [[settings-general]] — where the store-wide `unit_system` is set (metric / imperial), which decides how the value is read.

## Related

- [[geo-distance]] — hub.
- [[geo-distance-model]] — the full record shape the `distance` field lives on.
- [[geo-distance-matching]] — the checkout match always runs in metres (`distance_in_meters`).
- [[settings-geo-distances]] — the management feature.

## Open Questions

- ⏸️ **Imperial display round-tripping** — on imperial stores, confirm whether the Edit form re-displays the originally entered feet value or the derived metric value when `unit_system` is later changed. (verify)
