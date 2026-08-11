---
type: entity
aliases: ["Geo Distance", "Geo Distance Rule", "Distance", "Radius zone", "Circular delivery zone", "Distance-from-point", "Гео разстояние", "Радиус", "Радиус зона"]
tags: [shipping, settings, geo, distance, radius, maps, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Geo Distance

## Identity

A **Geo Distance** is a **named radius around a fixed center point on a Google Map** — the merchant picks a center (by typing an address or dragging the marker), enters a radius value, and saves a record like *"Warehouse 30 km radius"* or *"Sofia center 10 km delivery zone"*. The merchant uses Geo Distances when the area they want to target is well-approximated by a circle: typical examples are *"local delivery within 30 km of the warehouse"*, *"premium 24h service within 5 km of central hub"*, *"food / on-demand delivery within 3 km of the store location"*, or *"free shipping inside 50 km of any retail location"*. The radius is the same in every direction from the center point — for non-circular service areas, the merchant uses a [[geo-polygon|Geo Polygon]] instead.

A Geo Distance is an **INPUT to a [[geo-zone|Geo Zone]] rule**, never consumed directly. The merchant defines the center + radius ONCE on [[settings-geo-distances]], then references it from one or more Geo Zones via zone operation **10** (`OPERATION_DISTANCE`). The zone is what shipping methods, tax rules, payment providers, discounts, fees, customer-group restrictions, and Cart Rules attach to — the distance entry merely tells the zone *"addresses within the configured radius of this center count as inside the zone."* See [[geo-targeting]] for the end-to-end mechanism.

A Geo Distance is distinct from a **[[geo-polygon|Geo Polygon]]** (an arbitrary drawn outline, used when a circle isn't a good fit) and from a **[[geo-zone|Geo Zone]]** (the merchant-named container that references distances and polygons alongside country / region / city / post-code rules).

This entity is split into four aspect pages (below). The Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[geo-distance-model]] — what the record stores (`name`, `text`, `distance`, `lat`, `lng`); the single-center-single-radius shape; read-only lat/lng; the Google Maps API-key prerequisite.
- [[geo-distance-units]] — the radius unit gotcha: metres on metric stores vs feet on imperial; the `unit_system` snapshot + `distance_in_meters` column; the "entered 30 thinking 30 km" misconfiguration.
- [[geo-distance-matching]] — how a distance is matched at checkout (great-circle / haversine against the customer's coordinates); performance + accuracy; the inputs-to-zones rule; why tax matching ignores distances.
- [[geo-distance-lifecycle]] — create / edit / delete flow; live map auto-fit to radius; cache invalidation on save; multi-center coverage via several distances in one zone; permissions; no queue / notifications / webhooks.

## Aliases

- "Geo Distance" — the canonical merchant-facing wiki term.
- "Geo Distance Rule" — used in some internal phrasing emphasising that the entry is a rule input to a zone, not a standalone gate.
- "Distance" — the short form; appears in the Sidebar label ("Geo distances"), the page title, and the validation messages (*"The Distance name field is required"*).
- "Radius zone" / "Circular delivery zone" / "Distance-from-point" — informal merchant language emphasising the geometric shape.
- Bulgarian: "Гео разстояние", "Радиус", "Радиус зона".

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** (`name`) | Required free text on the Add / Edit form | Display label everywhere — list view, edit form, zone rule picker. Validation: *"The Distance name field is required"*. |
| **Address text** (`text`) | Picked from Google Places autocomplete on the form | Required (*"The Address field is required"*). Picking from the dropdown also populates `lat` and `lng`. Placeholder: *"Sofia, Bulgaria"*. |
| **Distance** (`distance`) | Required integer radius, in the store's unit (metres / feet) | Drives the circle's radius on the map. Minimum `1`. **NO unit picker.** See [[geo-distance-units]] for the metric-vs-imperial behaviour and the most common misconfiguration. |
| **Latitude** (`lat`) / **Longitude** (`lng`) | Read-only — populated from the autocomplete pick or marker drag | Signed decimal degrees. The merchant cannot type coordinates manually. See [[geo-distance-model]]. |
| **Created at** / **Updated at** / **ID** | n/a (auto) | `ID` is the FK target referenced from `geo_zone_values.distance_id` (zone operation 10 rules). |

Full storage shape, the single-center-per-record constraint, and the Google Maps prerequisite are on [[geo-distance-model]].

## Where it appears

- [[settings-geo-distances]] — the master list + Add / Edit form. Where the merchant creates, edits, and deletes distance entries.
- [[settings-geo-zones]] — Geo Zones reference distances via operation 10 (`OPERATION_DISTANCE`) rule entries. Where the merchant attaches a distance to a zone.
- [[settings-shipping]] — shipping methods scope to zones that may reference distances.
- [[settings-taxes]] — tax rules scope to zones, but tax matching IGNORES distances (country-only rule). See [[geo-distance-matching]].
- [[marketing-discounts]] — discounts can restrict to zones that reference distances.
- [[settings-cart]] — the Google Maps API key (Box: Google Maps) is the prerequisite for the autocomplete + map modules.

## Related

- [[settings-geo-distances]] — the management feature.
- [[geo-zone]] — entity that references distances via operation 10.
- [[geo-polygon]] — sibling input (arbitrary drawn outline) referenced via operation 9.
- [[geo-targeting]] — concept page on how Zones / Polygons / Distances combine end-to-end.
- [[shipping-calculation]] — how zones (and distances through them) gate shipping quotes.
- [[tax-computation]] — explains the country-only rule for tax matching that makes distances invisible to the tax engine.
- [[settings-shipping]] — shipping methods consume zones.
- [[settings-taxes]] — tax rules consume zones.
- [[settings-cart]] — Google Maps API key prerequisite.
- [[plan-gates]] — concept page on plan gating (distances themselves are not plan-gated, but related features may be).

## Open Questions

- ⏸️ **FK-protected delete vs cascade** — confirm whether deleting a distance entry that's referenced by a Zone returns HTTP 422 with the affected Zone names, or silently cascades like the [[geo-polygon]] FK. See [[geo-distance-lifecycle]].
- ⏸️ **Geocoding fallback when Google Maps is unset** — distances require coordinates for the customer's address. Without a Google Maps API key, the platform falls back to a bundled coordinate dataset (see [[geo-zone]] / [[geo-targeting]]), but the exact coverage / accuracy of that dataset is not published.
- ⏸️ **Address re-geocoding on edit** — when the merchant re-types the address, does the platform re-geocode and overwrite lat/lng, or does it require an explicit autocomplete pick to update coordinates? See [[geo-distance-lifecycle]].
