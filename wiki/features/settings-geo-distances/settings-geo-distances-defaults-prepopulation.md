---
type: feature
nav_path: "Settings → Geo distances → Defaults & pre-population"
route_name: geo_distances_add.settings
route_path: /admin/settings/geo-distances/add
aliases: ["Geo distances defaults", "Geo distance MaxMind", "Geo distance prepopulation", "Geo distance Sofia fallback", "Geo distance circle style", "Geo distance default radius", "Add geo distance defaults"]
tags: [settings, geo, distance, defaults, maxmind, geoip, prepopulation, styling]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-geo-distances]]. See the hub for the other aspects (list/form, units, map module, storage, runtime matching, deletion).

# Geo distances — defaults & pre-population (MaxMind GeoIP, Sofia fallback)

## Purpose

When the merchant clicks **+ New Geo distance**, the form is **not** empty — the platform pre-populates the address, centre coordinates, and default radius using a MaxMind GeoIP lookup on the merchant's current request IP. A merchant in Sofia opening the Add form sees Sofia already entered, a marker on Sofia, and a 1 km radius. If MaxMind has no data, only the default 1000 m radius is set and the map falls back to a Sofia-default centre. This aspect documents the pre-population behaviour, the fallback chain, and the default styling of the rendered circle.

## Where to find it

The pre-population happens on the Add form (`/admin/settings/geo-distances/add`). The Edit form (`/edit/:id`) loads the saved record's actual values — pre-population doesn't apply there.

## What the merchant can do here

- Open the Add form and see the form pre-filled with the merchant's IP-located city (Address, Latitude, Longitude, marker position) — typically saving the merchant 1–2 manual steps.
- Override any pre-populated value before saving — pre-population is just defaults, not constraints.
- Adjust the default 1000 m radius up or down before saving.

## Settings & fields

### Pre-population on Add (MaxMind GeoIP lookup)

When the merchant clicks **+ New Geo distance**, the create endpoint runs a MaxMind GeoIP lookup on the merchant's current request IP and returns:

| Field | Pre-populated value (if MaxMind has data) | Fallback (no MaxMind data) |
|-------|-------------------------------------------|----------------------------|
| `text` | `"City, Country"` of the merchant's IP location | (empty — merchant types) |
| `lat`, `lng` | Latitude / longitude of the IP-located city | (empty — map renders the Sofia default centre) |
| `distance` | `1000` | `1000` |
| `name` | (empty — merchant types) | (empty) |

So the merchant typically opens Add with the form centred on their likely location and a 1 km radius pre-filled. They edit the name + tweak the radius and save.

### Default circle style (rendered by the map module)

| Property | Default value |
|----------|---------------|
| Stroke colour | `#1E90FF` (dodger blue) |
| Stroke opacity | 0.8 |
| Fill colour | `#1E90FF` |
| Fill opacity | 0.45 |
| Stroke weight | 2 |

Merchants cannot change the circle colour from the modern Vue form — the table has `fillColor`, `fillOpacity`, `strokeColor`, `strokeOpacity`, `strokeWeight` columns but they are not surfaced. Legacy the application framework admin used to set them; the new form does not.

### Default map view (when there's no MaxMind data and no record)

| Property | Value |
|----------|-------|
| Centre latitude | `42.6977082` (Sofia, Bulgaria) |
| Centre longitude | `23.3218675` |
| Default zoom | `14` |

## Business rules

### MaxMind is best-effort, not authoritative

The pre-population is a **convenience**, not a constraint:

- If MaxMind returns a city, the form is pre-filled and the merchant can edit or accept.
- If MaxMind has no data for the IP (rare but possible — corporate VPNs, datacentre IPs, etc.), the form is partially empty (only `distance: 1000` is set; no `text`, no `point`).
- The merchant must then type an address in the autocomplete — see [[settings-geo-distances-map-module]] — before saving.

### Sofia fallback centre — the map's last resort

When neither MaxMind nor a saved record provides coordinates, the map module renders at:

- Centre: Sofia, Bulgaria — `(42.6977082, 23.3218675)`.
- Zoom: 14.

This is the platform's default centre — chosen because CloudCart is headquartered in Sofia and the majority of merchants are Bulgarian. It is **not** localised per merchant — a German merchant whose MaxMind data is missing also gets the Sofia centre. The merchant types in the autocomplete to reposition the map.

### Default radius of 1000 meters

The pre-populated `distance = 1000` corresponds to:

- 1 km on a metric store (the obvious case).
- 1000 feet ≈ 305 metres on an imperial store (see [[settings-geo-distances-distance-units]] for the unit quirk).

The default is small enough that the merchant always sees the entire circle in the initial map viewport — the auto-fit (see [[settings-geo-distances-map-module]]) makes the circle visible at any zoom.

### Circle styling is hidden but persisted

The DB persists styling columns (`fillColor`, `fillOpacity`, `strokeColor`, `strokeOpacity`, `strokeWeight`) — see [[settings-geo-distances-storage-spatial]]. They are kept for:

- Backward compatibility with the legacy the application framework admin (which did surface them).
- Possible future styling features in the modern form.

For now, the merchant cannot change the dodger-blue colour from the UI. (verify) Whether direct DB / API edits to those columns persist visually on the form's map preview, or whether the modern map module hard-codes the defaults regardless of stored values.

### Pre-population only on Add, not on Edit

The Edit form (`/edit/:id`) always loads the saved record's actual values — MaxMind lookup does not run. So a merchant editing an existing record sees the record's saved address / lat / lng / distance, not an IP-derived default.

### Pre-population uses the merchant's current request IP

The IP used for the MaxMind lookup is the IP making the admin request (the merchant's browser session). Some practical implications:

- Merchants on corporate VPNs or proxies will get the VPN exit-node city, not their physical location.
- Merchants logging in from travel will get the travel-location city — easy to overlook and accidentally save the wrong centre.
- Merchants are recommended to always verify the marker position on the map preview before saving.

## Related

- [[settings-geo-distances]] — hub.
- [[settings-geo-distances-list-add]] — the Add / Edit form into which these defaults populate.
- [[settings-geo-distances-map-module]] — the map module that renders the pre-populated marker + the Sofia fallback centre.
- [[settings-geo-distances-distance-units]] — why 1000 means 1 km on metric and ~305 m on imperial.
- [[settings-geo-distances-storage-spatial]] — the hidden `fillColor` / `strokeColor` columns.

## Open questions

- (verify) Whether the hidden styling columns affect the modern form's map preview if edited directly via DB or API.

