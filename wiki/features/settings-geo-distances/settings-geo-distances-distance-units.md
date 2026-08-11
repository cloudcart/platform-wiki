---
type: feature
nav_path: "Settings → Geo distances → Distance units"
route_name: geo_distances.settings
route_path: /admin/settings/geo-distances
aliases: ["Geo distance units", "Meters vs feet", "Imperial-store geo distance", "distance_in_meters", "Geo distance unit quirk", "Geo distance imperial"]
tags: [settings, geo, distance, units, imperial, metric]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-distances]]. See the hub for the other aspects (list/form, map module, storage, runtime matching, defaults, deletion).

# Geo distances — distance units (meters vs feet)

## Purpose

The Distance field on the [[settings-geo-distances-list-add|Add / Edit form]] looks like a single "meters" input, but the platform actually interprets the typed integer against the **store's `unit_system`**. On metric stores the input is meters, but on imperial stores the **same input is interpreted as feet** even though the UI suffix label keeps saying "meters". This aspect documents the quirk, the storage shape that supports it, and the display-label behaviour for downstream consumers.

## Where to find it

The Distance input lives in the Add / Edit form (col 9–12 of the field grid) — see [[settings-geo-distances-list-add]]. The store's `unit_system` is set on [[settings-general]] (one of `metric`, `imperial`, or `N` for nautical).

## What the merchant can do here

- Type an integer ≥ 1 in the Distance field on the Add / Edit form.
- See a "meters" suffix label regardless of unit system (the label is **not** unit-aware).
- See the live map's circle update reactively to match the typed radius (the map auto-fits the viewport — see [[settings-geo-distances-map-module]]).

## Settings & fields

| Field | Type | Validation | Notes |
|-------|------|------------|-------|
| **Distance** (`distance`) | integer | `min:1 \| numeric \| int \| max:5000000` | Required. Suffix label always *"meters"* — but the backend interprets the value per `unit_system`. |

The DB persists **two columns**:

| Column | What it holds |
|--------|---------------|
| `distance` | The raw integer the merchant typed. |
| `distance_in_meters` | Always meters — computed from `distance` + `unit` on save. |
| `unit` | The store's `unit_system` at save time (`metric` / `imperial` / `N`). |

## Business rules

### Metric stores — input is meters (the obvious case)

When `unit_system = metric` on [[settings-general]]:

- The integer the merchant types **is** meters.
- 1 km = `1000`, 10 km = `10000`, 50 km = `50000`.
- `distance_in_meters = distance`.

The UI suffix label says "meters" and the value behaves like meters. No surprises.

### Imperial stores — input is FEET, not meters

When `unit_system = imperial` on [[settings-general]]:

- The integer the merchant types **is interpreted as FEET**, even though the UI label still says "meters".
- The model's `saving` hook converts feet → metres: `distance_in_meters = distance × 0.3048` (the standard foot-to-metre constant).
- Practical impact: a merchant on an imperial store who types `10000` in the Distance field gets a **10,000-foot radius ≈ 3,048 metres**, not a 10,000-metre radius.
- The map module always draws the circle at the unit-converted metre value — so visual verification after save is the merchant's best safeguard against this surprise.

This is the platform's true unit behaviour. The "meters" suffix label is misleading on imperial stores; merchants should verify the radius on the map preview after save.

### Nautical stores — `unit_system = N`

The platform also persists `unit = N` for nautical-system stores. Conversion follows the platform's distance helper; merchants on nautical-unit stores are rare in retail e-commerce, so the practical impact is minimal — but the `unit` column records which system was active at save time so a later recomputation can be done correctly.

### Display labels read the consumer's `unit_system`

When a [[settings-geo-zones|geo zone]] of type Distance (operation 10) is rendered in the admin UI or for a customer-facing reference, the label inserts the unit dynamically:

- `metric` → `m`
- `imperial` → `ft`

So the same distance record can render as either "10000 m" or "10000 ft" depending on which store consumes it. The displayed integer is always the raw `distance` value, not the converted `distance_in_meters`.

### No unit picker, no decimal support

- There is no UI picker to switch the input between meters / km / miles / feet — the field is always "the integer the merchant types, interpreted per the store's `unit_system`".
- The integer-only validation rejects decimals (e.g., `5.5` km cannot be entered as `5500.5` — the merchant rounds to `5500`).
- Backend rule: `min:1 | numeric | int | max:5000000`. Decimals are rejected with a 422 validation error.

### Validation cap at 5,000,000

The backend caps the integer at 5,000,000. Practical interpretation:

- Metric store: max radius ≈ **5,000,000 metres ≈ 5,000 km** (far beyond any practical delivery zone).
- Imperial store: max radius ≈ **5,000,000 feet ≈ 1,524 km**.

In all practical cases the cap is invisible; merchants typing a normal delivery radius will never hit it.

### What this means for runtime matching

The runtime matching uses `distance_in_meters` (the converted value), not the raw `distance` integer — see [[settings-geo-distances-matching-runtime]]. So once saved, the value is unambiguous regardless of how it was typed; the unit ambiguity only matters at data-entry time.

## Related

- [[settings-geo-distances]] — hub.
- [[settings-geo-distances-list-add]] — where the Distance field lives in the form.
- [[settings-geo-distances-storage-spatial]] — the `distance`, `distance_in_meters`, `unit` columns + DB-level validation.
- [[settings-geo-distances-matching-runtime]] — `ST_Distance_Sphere` evaluates against `distance_in_meters`.
- [[settings-general]] — store's `unit_system` setting (metric / imperial / nautical).
- [[settings-geo-zones]] — operation-10 display labels read the consumer's `unit_system`.

## Open questions

None — foot-to-metre conversion uses the **international foot** constant `0.3048` exactly, defined in the third-party library `crisu83/php-conversion` (`Quantity/Length/Length.php` ratio table). Verified 2026-06-11. The US-survey-foot variant (`0.30480060960121919`) is NOT used anywhere in the geo-distance code path.

