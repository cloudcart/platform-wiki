---
type: entity
aliases: ["Geo Distance model", "Geo Distance record", "Distance record shape", "Distance storage", "Center + radius record", "Гео разстояние — запис"]
tags: [shipping, settings, geo, distance, radius, maps, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[geo-distance]]. See the hub for the other aspects (units, matching, lifecycle).

# Geo Distance — record model

## Identity

The **Geo Distance record** is the stored shape of a single circular delivery zone: one center point plus one radius. Each record stores `(id, name, text, distance, lat, lng, created_at, updated_at)` — no polygon coordinates, no per-direction radius, just the center + radius pair. At runtime, the platform's address-matching layer reads the row and tests the customer's coordinates with one great-circle call per record (see [[geo-distance-matching]]).

This page covers **what a distance record holds and how the merchant fills it in**. The unit semantics of the `distance` field are on [[geo-distance-units]]; how the record is matched at checkout is on [[geo-distance-matching]]; the create / edit / delete flow is on [[geo-distance-lifecycle]].

## Aliases

- "Geo Distance model" / "Distance record shape" — the wiki terms for the stored fields.
- "Center + radius record" — emphasises the single-center-single-radius constraint.
- Bulgarian: "Гео разстояние — запис".

## Key Attributes

| Field | What the merchant controls | Notes |
|-------|----------------------------|-------|
| **Name** (`name`) | Required free text on the Add / Edit form | Display label everywhere — list view, edit form, zone rule picker. Validation: Zod `min(1)` — *"The Distance name field is required"*. |
| **Address text** (`text`) | Picked from Google Places autocomplete | Required (Zod `min(1)` — *"The Address field is required"*). The display value of the selected place. Picking from the dropdown also populates `lat` and `lng`. Placeholder: *"Sofia, Bulgaria"*. If the merchant types but doesn't select from the dropdown, the lat/lng stay empty and the save is rejected. |
| **Distance** (`distance`) | Required integer, ≥ 1 | The circle's radius. Validation rejects decimals and rejects values below 1. The unit (metres / feet) follows the store's `unit_system` — see [[geo-distance-units]]. |
| **Latitude** (`lat`) | Read-only — from autocomplete pick or marker drag | Number; standard signed decimal degrees. |
| **Longitude** (`lng`) | Read-only — same source | Number; standard signed decimal degrees. |
| **Created at** / **Updated at** | n/a (auto-set) | Standard timestamps. |
| **ID** | n/a (auto-assigned) | Foreign-key target referenced from `geo_zone_values.distance_id` (zone operation 10 rules). |

### Single center + single radius per record

Each Geo Distance record stores exactly one center point + one radius. There is no way to give a record a second center or an asymmetric (non-circular) shape. For multi-warehouse coverage (e.g. *"within 30 km of EITHER of our two warehouses"*), the merchant creates one distance entry per warehouse and references both from a single Geo Zone via multiple operation-10 rule entries — see [[geo-distance-lifecycle]] for the multi-center pattern.

### Read-only lat / lng on the form

The Latitude and Longitude inputs are present but **read-only** — they are populated by the autocomplete pick or by dragging the marker on the live map. The merchant cannot manually enter coordinates. Typing an address string without selecting a place from the autocomplete dropdown produces an empty lat/lng and the form rejects the save.

### Google Maps API key is a hard prerequisite

The autocomplete + map module cannot function without a valid Google Maps API key configured in [[settings-cart]] → Google Maps. Without the key, the autocomplete fails and the map iframe doesn't render — distance creation is blocked. There is no offline fallback for record creation; the merchant cannot type raw lat/lng instead. The Google Maps API version is auto-detected from the `isNewGoogleMapsApi` flag (legacy `GMapMap` / `GMapMarker` / `GMapCircle` vs new `CcGoogleMapsRadius`) — the merchant doesn't pick. Both implementations render pan / zoom controls, a draggable marker, and a circle that updates reactively with the `distance` input, and both work on iOS / Android touchscreens via standard Google touch handling.

## Where it appears

- [[settings-geo-distances]] — the master list + Add / Edit form where each record is created and edited.
- [[settings-geo-zones]] — the record's ID is referenced from a zone via an operation-10 rule entry.
- [[settings-cart]] — the Google Maps API key prerequisite for the autocomplete + map.

## Related

- [[geo-distance]] — hub.
- [[geo-distance-units]] — what the `distance` value means in metric vs imperial stores.
- [[geo-zone]] — entity that references the record via operation 10.
- [[geo-polygon]] — sibling input with a different storage shape (arbitrary outline coordinates).
- [[settings-geo-distances]] — the management feature.
- [[settings-cart]] — Google Maps API key prerequisite.

## Open Questions

- ⏸️ **Address re-geocoding on edit** — when the merchant re-types the address, does the platform re-geocode and overwrite lat/lng, or does it require an explicit autocomplete pick to update coordinates? (verify) See [[geo-distance-lifecycle]].
