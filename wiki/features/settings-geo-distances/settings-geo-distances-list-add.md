---
type: feature
nav_path: "Settings → Geo distances → List & Add/Edit form"
route_name: geo_distances.settings
route_path: /admin/settings/geo-distances
aliases: ["Geo distances list", "Add geo distance", "Edit geo distance", "Geo distance form", "Geo distance field grid"]
tags: [settings, geo, distance, form, list]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-distances]]. See the hub for the other aspects (units, map module, storage, runtime matching, defaults, deletion).

# Geo distances — list view + Add / Edit form

## Purpose

The list view + Add / Edit form is the entire merchant-facing UI of the Geo distances feature. The list shows all defined distance entries; the Add / Edit form lets the merchant pick a centre on a map, enter a radius, and name the record. There is no detail view distinct from the editor — clicking a name jumps straight to Edit.

## Where to find it

Sidebar → Settings → **Geo distances**.

| Label | Route name | Route path |
|-------|------------|------------|
| List | `geo_distances.settings` | `/admin/settings/geo-distances` |
| Add | `geo_distances_add.settings` | `/admin/settings/geo-distances/add` |
| Edit | `geo_distances_edit.settings` | `/admin/settings/geo-distances/edit/:id` |

The Add / Edit form is rendered as a **full sub-page** inside the Settings shell (not a centred modal). Sub-tabs read *List* / *Add Geo distance* (or *Edit Geo distance*). The fixed-top page header carries **Cancel** and **Save**.

## What the merchant can do here

### List view

- See all defined distance entries with the entry name and per-row Edit (click name) and Delete actions.
- Sort, filter, paginate.
- Click **+ New Geo distance** in the page header to navigate to the Add form.

### Add / Edit form

- Type an **Address** in the Google Places autocomplete field (e.g., "Sofia, Bulgaria", or the merchant's warehouse address) — picks the centre point of the radius.
- Enter a **Distance** in **meters** (integer ≥ 1) — for the imperial-store FEET quirk see [[settings-geo-distances-distance-units]].
- See a live Google Map preview below the inputs (draggable marker, live-updating circle) — see [[settings-geo-distances-map-module]] for full map behaviour.
- See read-only **Latitude** and **Longitude** values populated from the autocomplete pick or marker drag — for the merchant's reference.
- Save. Redirects to the list on success.

### What the merchant CANNOT do here

- Define multiple circles in a single entry (one centre + one radius per record). For multi-centre coverage, the merchant creates multiple records and references all from one geo zone (OR-combined).
- Enter distance in kilometres or miles directly — the input is integer-meters only.
- Manually enter latitude/longitude — they're read-only and derived from the map position.
- Save without a Google Maps API key — see [[settings-geo-distances-map-module]] for the prerequisite.

## Settings & fields

### List table

| Column | Notes |
|--------|-------|
| **Name** (`name`) | Click navigates to Edit. |
| **(actions)** | Per-row Remove button. Deletion is silent — see [[settings-geo-distances-deletion-cascade]] for the cascade behaviour. |

### Add / Edit form — exact field grid

The form is rendered on a 12-column grid:

| Span | Field | Notes |
|------|-------|-------|
| col 1–12 | **Distance name** (`name`) | Multi-line text. Required (Zod min 1 — *"The Distance name field is required"*). Placeholder: *"Add the name of the Geo distance. Example: 10km from the office"*. Backend caps at 191 characters — see [[settings-geo-distances-storage-spatial]]. |
| col 1–8 | **Address** (`text`) | Google Places autocomplete. Required (Zod min 1 — *"The Address field is required"*). Placeholder: *"Sofia, Bulgaria"*. On suggestion-pick, fills `text`, `lat`, `lng` simultaneously. |
| col 9–12 | **Distance** (`distance`) | Numeric input with the suffix label *"meters"* on the right. Required. Min 1, integer. See [[settings-geo-distances-distance-units]] for the imperial-store quirk where the integer is interpreted as feet. |
| col 1–12 | **Google Map** preview | Below the inputs. Draggable centre marker + live-updating circle. See [[settings-geo-distances-map-module]] for module variants and behaviour. |
| col 1–6 | **Latitude** (`lat`) | Read-only. Populated from autocomplete pick or marker drag. 7-decimal-place precision. |
| col 7–12 | **Longitude** (`lng`) | Read-only. Same source. |

### Validation summary (client-side Zod)

- `name`: non-empty string.
- `text` (address): non-empty string.
- `distance`: number ≥ 1.
- `lat`, `lng`: numbers (only valid coordinates come from Google Places, so range is enforced implicitly; the backend additionally validates `[-90, 90]` / `[-180, 180]` — see [[settings-geo-distances-storage-spatial]]).

Saving validates client-side, then submits to the backend. On success the merchant is redirected to the list with a toast *"Created successfully"* / *"Updated successfully"*. Validation errors render inline next to the offending input.

## Business rules

- **One record = one circle**: a single record cannot describe a non-circular area; for multi-centre coverage the merchant creates multiple records and references them from one [[settings-geo-zones|zone]].
- **No raw lat/lng entry**: the only way to set coordinates is via the autocomplete pick or marker drag — see [[settings-geo-distances-map-module]].
- **Address is required and free-form**: the column is `TEXT`; the autocomplete writes a human-readable "City, Country" string but the merchant can technically save any non-empty text. The lat/lng drive the matching — `text` is for display only.
- **Edit changes are immediate**: a save flushes the geo-distance lookup cache so the next checkout zone match sees the new values — see [[settings-geo-distances-matching-runtime]].
- **No queue, no notifications, no webhooks**: CRUD is fully synchronous.

## Related

- [[settings-geo-distances]] — hub.
- [[settings-geo-distances-distance-units]] — the imperial-store FEET quirk on the Distance input.
- [[settings-geo-distances-map-module]] — Google Maps + Google Places behaviour for the form's map.
- [[settings-geo-distances-storage-spatial]] — backend validation (lat/lng range, `name` 191-char cap, distance ≤ 5,000,000).
- [[settings-geo-distances-deletion-cascade]] — what happens when the merchant clicks the per-row Remove button.
- [[settings-geo-zones]] — where the saved distance gets referenced (operation 10).

## Open questions

None.
