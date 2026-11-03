---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → Google Maps"
route_name: customers-shipping-addresses
route_path: /admin/customers/details/:id/shipping-addresses
aliases: ["Customer shipping address Google Maps", "Google Maps autocomplete address panel", "Google Map marker drag reverse-geocode"]
tags: [customers, addresses, shipping, google-maps]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (list, modal, defaults, save-hooks, storage, validation, API).

# Customer shipping addresses — Google Maps integration

## Purpose

The optional Google-Maps-powered helpers inside the Add / Edit address panel: the **Places autocomplete bar** and the **interactive map with a draggable marker**. Both speed up address entry by pre-filling country / state / city / street / postcode from one selection or one marker-drag — and they're gated behind a Google Maps API key configured by the merchant. Without the key, the panel falls back to manual entry only.

## Where to find it

Inside the [[customer-shipping-address-modal]] Address card (the autocomplete bar sits above the manual fields; the map sits below it). The behaviour described here also applies to billing addresses — see [[customers-details-billing-addresses]] — because the same panel serves both.

## What the merchant can do here

- Type a city or street into the autocomplete bar — Google's suggestions appear; selecting one auto-fills the address fields and centres the map marker.
- Drag the map marker to a new location — reverse-geocoding fires and updates the address fields automatically.
- Edit the address fields manually after either action — the map does NOT re-centre on manual field edits (one-way sync from map → fields, not fields → map).

### What the merchant CANNOT do here

- Use a different map provider (Apple Maps, OpenStreetMap, Mapbox) — Google Maps is the only built-in option.
- Pick a courier's office or locker through the map — that has its own form. See [[customer-shipping-address-pickup-point]].

## Settings & fields

### API-key setting

Configured at [[settings-cart]] under `google_maps_api_key`. Without it, the autocomplete + map are HIDDEN; a static info banner replaces them.

### API-version flag (server-side)

The platform supports two Google Maps API versions, selected by `google_map_api_version`. When the value is `new`, the panel uses Google's **New API** autocomplete; otherwise Google's classic autocomplete. The merchant doesn't choose this directly — it's a server-side flag. `(verify)` how the merchant influences this in the UI.

### Initial map state

| Setting | Value |
|---|---|
| Initial map centre | lat **42.6977082**, lng **23.3218675** (Sofia, BG) |
| Marker | Single draggable pin |

For Edit-mode openings on an address that already has lat/lng, the map centres on the stored coordinates instead.

### No-map banner copy

Visible when `google_maps_api_key` is empty:

> To see Google Map, you need to set up a Google Maps Api Key

The banner links to [[settings-cart]] (opens in new tab).

### Geo-error banner copy

Visible when validation returns `geo_name_city_id` or `city_id` errors:

> Currently the address can not be saved, please try again later, or contact our support team.

## Business rules

### Autocomplete fills the manual fields

Selecting a suggestion from the Places autocomplete dispatches each component of the selected place into the country / state / city / street / street-number / post-code fields. The map marker is centred on the selected coordinates. A place with no street, number or post code of its own (for example a Google Plus Code) keeps what those fields already hold.

### Marker-drag triggers reverse-geocoding

Dragging the marker fires Google's `dragend` event. The platform then:

1. Runs reverse-geocoding via Google's Geocoder against the dropped lat-lng.
2. Calls the platform's internal geo-zone-format endpoint `/admin/api/v1/geo-zones/format/<locale>/` to map the Google place to CloudCart's internal geo-name records (city / state / country IDs needed for tax + shipping lookups).
3. Updates the country / state / city / street / postcode fields from the resolved place.

If step 2 fails, the fields are filled from Google's own values and an error message shows. If the Geocoder finds nothing for the dropped point, the address fields are cleared.

### One-way sync map → fields

Manual edits to the address fields do NOT re-centre the map or move the marker. Only autocomplete selections and marker drags update the fields. The merchant who corrects a misspelled street name by typing will NOT see the map update.

### Geo-name resolution feeds tax + shipping

The geo-names lookup maps the Google place ID to CloudCart's internal city / state / country records — the same records [[settings-geo-zones]] uses for shipping rate matching and [[settings-taxes]] uses for VAT bracket matching. So selecting an address from Google's suggestion list is what gives the platform a usable record for downstream pricing.

### Without a key, manual entry is the only path

For Bulgarian merchants (or any merchant) without a Google Maps API key configured, the entire autocomplete + map block is hidden. There is no built-in EKATTE / Royal Mail / other postal-service fallback. The merchant types all fields manually.

### Lat/lng auto-fill happens even without an API key in the UI

Even when the merchant types the address manually with no autocomplete and no map, the platform server-side still tries to geocode the address on save (using `<post_code> <city_name> <country_iso2>`) — see [[customer-shipping-address-save-hooks]]. So most manually-entered addresses still end up with lat/lng populated.

### Side effects

- Selecting an autocomplete result: fills 6 fields + centres marker. No save fires until the merchant clicks Save.
- Marker drag: triggers a spinner over the map; the address fields are disabled while it runs.
- The geo-error banner shows when saving returns `geo_name_city_id` or `city_id` errors.

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customer-shipping-address-modal]] — the panel that contains this map block.
- [[customer-shipping-address-save-hooks]] — the server-side lat/lng auto-fill that runs without Google Maps in the UI.
- [[customer-shipping-address-validation]] — Google Maps adds extra required fields (`country.iso2`, `latitude`, `longitude`, `locality`, `text`).
- [[settings-cart]] — Google Maps API key + `google_map_api_version` flag.
- [[settings-geo-zones]] — geo-zone records resolved against on autocomplete + marker-drag.
- [[settings-taxes]] — taxes use the resolved country for VAT bracket matching.

## Open questions

- How does the merchant select between the old and new Google Maps API variants? Is `google_map_api_version` exposed in [[settings-cart]] or only a backend flag? `(verify)`
