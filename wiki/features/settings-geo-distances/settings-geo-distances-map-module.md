---
type: feature
nav_path: "Settings → Geo distances → Map module"
route_name: geo_distances.settings
route_path: /admin/settings/geo-distances
aliases: ["Geo distances map", "Google Maps radius module", "Geo distances autocomplete", "CcGoogleMapsRadius", "GMapMap radius", "Google Places geo distance", "Geo distance marker drag"]
tags: [settings, geo, distance, google-maps, places, autocomplete, map]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-distances]]. See the hub for the other aspects (list/form, units, storage, runtime matching, defaults, deletion).

# Geo distances — map module (Google Maps + Places)

## Purpose

The Add / Edit form's interactive map is the only way to set a distance entry's centre point — there is no raw lat/lng entry. The merchant types in a Google Places autocomplete to pick a place, or drags the marker on the rendered map to fine-tune, and the lat/lng readouts populate reactively. A circle around the marker shows the chosen radius. This aspect documents the two module variants the platform ships, the Google Places autocomplete behaviour, marker / circle interactions, and the Maps API key prerequisite.

## Where to find it

The map module renders inside the Add / Edit form below the inputs (col 1–12 of the field grid — see [[settings-geo-distances-list-add]]). The Google Maps API key prerequisite is configured on [[settings-cart]]'s Google Maps box.

## What the merchant can do here

- Type an address in the Google Places autocomplete and pick a suggestion from the dropdown — the marker jumps to the picked place; lat/lng readouts fill in.
- Drag the marker on the rendered map — lat/lng readouts update reactively.
- Pan / zoom standard Google Maps controls.
- Change the Distance value (see [[settings-geo-distances-distance-units]]) — the circle radius redraws live and the map auto-fits the viewport.
- On mobile (iOS / Android touchscreens) — drag the marker with one finger, pinch-to-zoom, two-finger pan.

## Settings & fields

The merchant does not pick which module variant to use. The page reads the `isNewGoogleMapsApi` flag from [[settings-cart]]'s Google Maps configuration and renders the appropriate module:

| Mode | Component | Behaviour |
|------|-----------|-----------|
| **New Maps API** | `CcGoogleMapsRadius` | Interactive map with centre marker + radius circle, both updated reactively from form inputs. |
| **Legacy Maps API** | `GMapMap` with `GMapMarker` (draggable) + `GMapCircle` | Same functional shape; older binding patterns. |

Both modules expose the same merchant-visible behaviour — autocomplete, draggable marker, live circle, auto-fit, touch support.

### Circle style

| Property | Default | Notes |
|----------|---------|-------|
| Stroke colour | `#1E90FF` (dodger blue) | Not surfaced in the new form; see [[settings-geo-distances-defaults-prepopulation]] for hidden columns. |
| Stroke opacity | 0.8 | Hidden — not surfaced. |
| Fill colour | `#1E90FF` | Hidden — not surfaced. |
| Fill opacity | 0.45 | Hidden — not surfaced. |
| Stroke weight | 2 | Hidden — not surfaced. |

The merchant cannot change the circle colour from the modern UI — the DB table has the columns for it (legacy form used to set them) but the new Vue form does not surface them.

## Business rules

### Google Maps API key is a hard prerequisite

Without a valid Google Maps API key configured in [[settings-cart]]'s Google Maps box:

- The autocomplete field cannot render suggestions.
- The map module fails to render the basemap.
- The merchant cannot create or visually verify entries — save is effectively blocked because lat/lng cannot be set.
- There is no offline fallback (no raw lat/lng entry option).

### Address disambiguation — Google Places autocomplete dropdown

When the merchant types an address (e.g., "Sofia"), Google Places returns a ranked dropdown of plausible matches — Sofia BG, Sofia in the US, place names containing "Sofia", etc. The merchant **explicitly selects** one from the dropdown — that selection determines:

- The `text` value (the formatted address string).
- The `lat` and `lng` (the picked place's coordinates).

After selection, the marker on the live map jumps to that location, giving the merchant a final visual confirmation before saving.

If the merchant types a string but **doesn't select from the dropdown**, the address text is recorded but no coordinates are set — the validation rejects the save because the `lat` / `lng` fields are empty.

### Marker drag updates lat/lng live — reverse-geocode behaviour differs per module

The marker on the map is draggable. On drag:

- The `lat` and `lng` readouts in the form update reactively (7-decimal-place precision — see [[settings-geo-distances-storage-spatial]]).
- The circle around the marker repositions with it.
- **The `text` field behaviour depends on which module is active** — verified 2026-06-11:
  - **Modern Vue module (`CcGoogleMapsRadius`, `isNewGoogleMapsApi = true`)** — the drop handler calls `google.maps.Geocoder.geocode({location: coordinates})` and writes `results[0].formatted_address` back into `text`. So the address text stays in sync with the dropped coordinates. On reverse-geocode failure (no result, error, etc.) the handler emits **empty** `text` rather than leaving stale text — better to look obviously-blank than to mislead the merchant.
  - **Legacy `GMapMap` module (`isNewGoogleMapsApi ≠ 'new'`)** — `onMarkerDragEnd` only writes the new `lat` / `lng` and **does NOT touch `text`**. So `text` goes stale immediately on drag until the merchant types into the autocomplete again.

So on the modern API, drag is "complete": text follows. On the legacy API, the merchant should retype the address in the autocomplete after dragging if they want `text` to match — otherwise the saved record's `text` describes the original pick, not the dragged centre.

### Map auto-fits viewport on radius change

When the merchant changes the Distance value:

- The circle redraws to the new radius.
- The map auto-fits its viewport to show the whole circle. Typing 100,000 m = 100 km zooms out automatically; dragging down to 100 m zooms back in.
- The merchant should not need to manually zoom to verify their configured radius.

This behaviour works on both module variants (new and legacy).

### Mobile touch support

Both `CcGoogleMapsRadius` and `GMapMap` ship Google's standard touch-drag handling. On iOS / Android touchscreens:

- Drag the marker under the finger; lat/lng readouts update reactively.
- Pinch-to-zoom works as expected.
- Two-finger pan works as expected.

Merchant testing on tablets / phones works the same as desktop.

### Module variant is platform-selected, not merchant-selected

The `isNewGoogleMapsApi` flag — set on [[settings-cart]]'s Google Maps configuration — decides whether `CcGoogleMapsRadius` (new) or `GMapMap` (legacy) renders. The merchant does not pick this per page; it applies platform-wide. Migration from legacy to new should be invisible since both modules expose the same merchant-visible behaviour.

### Address text is free-form after save

Although the autocomplete writes a human-readable formatted address, the `text` column is just `TEXT` on the DB — the merchant could technically save any non-empty text (e.g., editing it after the autocomplete pick). The lat/lng are what actually drive matching at checkout (see [[settings-geo-distances-matching-runtime]]); `text` is for the merchant's reference only.

## Related

- [[settings-geo-distances]] — hub.
- [[settings-geo-distances-list-add]] — where the map module lives in the form.
- [[settings-geo-distances-storage-spatial]] — the lat/lng precision + range validation.
- [[settings-geo-distances-defaults-prepopulation]] — Sofia 42.6977, 23.3219 fallback centre; default zoom 14; hidden fill/stroke columns.
- [[settings-cart]] — Google Maps API key + `isNewGoogleMapsApi` flag.
- [[geo-polygons-settings-main-new]] — the polygon-geometry equivalent that uses the same Google Maps tech.

## Open questions

None — modern vs legacy marker-drag reverse-geocode behaviour verified against `CcGoogleMapsRadius.vue` (lines 100-145) and `SettingsGeoDistancesCreateOrEditPage.vue` `onMarkerDragEnd` (line 229) on 2026-06-11.

