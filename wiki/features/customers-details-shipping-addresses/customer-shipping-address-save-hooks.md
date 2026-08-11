---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → Save-time hooks"
route_name: customers-shipping-addresses.new
route_path: /admin/customers-new/details/:id/shipping-addresses
aliases: ["Customer shipping address save hooks", "Address phone E.164 normalisation", "Address lat/lng auto-fill", "OmniShip courier-mapping regeneration on address save"]
tags: [customers, addresses, shipping, hooks, side-effects]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (list, modal, Google Maps, defaults, storage, validation, API).

# Customer shipping addresses — Save-time hooks

## Purpose

Every shipping-address save — whether from the admin modal, the [[customers-details]] sidebar pen icon, or [[customer-shipping-address-api]] — runs **four hooks** in order. They handle phone normalisation, lat/lng auto-fill, country ISO normalisation, and the heavy post-save courier-mapping regeneration. This aspect documents what each hook does, in what order, and what its visible effects are.

## Where to find it

These hooks are not UI-visible — they run on the server after a successful save. The user-facing entry points that trigger them are:

- The Save button on the [[customer-shipping-address-modal]] (Add OR Edit).
- The "Set as default" action on the [[customer-shipping-address-list]] (does NOT re-save the address, but pointer updates don't re-trigger hooks).
- A PATCH / POST through JSON-API v2 — see [[customer-shipping-address-api]].
- The `setAddressFromOrder` re-sync path from order edits — see [[customer-shipping-address-storage]].

## What the merchant can do here

The merchant doesn't interact with these hooks directly — they're side effects of saving. But the merchant CAN observe them:

- Phone field is reformatted to E.164 after the modal closes.
- Lat/lng populated (visible on the map next time the modal opens for that address) even when the merchant only typed manually.
- Save takes longer on stores with many active couriers — the post-save courier-mapping regeneration dominates the wall-clock time.

### What the merchant CANNOT do here

- Skip the hooks. They run on every save.
- Disable the courier-mapping regeneration. It's automatic for non-office addresses.
- Override the E.164 phone format with a different formatting choice.

## Settings & fields

The hooks read several fields off the address being saved:

| Hook | Reads | Writes |
|---|---|---|
| Phone normalisation | `phone`, `country_iso2` | `phone` (E.164), `phone_international`, `phone_e164`, `phone_national`, `phone_rfc3966` |
| Lat/lng auto-fill | `latitude`, `longitude`, `post_code`, `city_name`, `country_iso2` | `latitude`, `longitude` |
| Country ISO normalisation | `country_iso2` | `country_iso2` (upper), `country_iso3`, `country_name` |
| Courier-mapping regeneration | All address fields | The address's mapping table |

## Business rules

The hooks run in this exact order on every shipping-address save:

### 1. Phone normalisation (libphonenumber → E.164)

When the address has both `phone` AND `country_iso2`, the platform passes the phone through libphonenumber, parses it against the country ISO, and stores it in **E.164** format (e.g., `+359888123456`). The five derived representations (international, E.164, national, RFC3966) are stored alongside.

Bad phones fail **silently** — the original value is kept, no exception is raised. So the merchant who pastes a malformed phone might end up with an unformatted value rather than an error.

### 2. Lat/lng auto-fill (Google Maps geocoding)

When `latitude` + `longitude` are empty AND `post_code` + `city_name` + `country_iso2` are present, the platform queries Google Maps geocoding with the string `"<post_code> <city_name> <country_iso2>"` and stores the first match's coordinates.

This is why even manually-typed addresses (no autocomplete, no map interaction in the UI) end up with a map pin the next time the modal opens. The auto-fill runs even on stores without a Google Maps API key in the UI — the server uses its own geocoder credentials. `(verify)` whether the platform has a server-side Google credential separate from the merchant's UI key.

### 3. Country ISO normalisation

- `country_iso2` is **upper-cased**.
- The ISO 3166 **alpha-3** code (`country_iso3`) is auto-derived from `country_iso2`.
- `country_name` is set from the **current store language** — English admin sees "Bulgaria", French admin sees "Bulgarie". So the same address record can render different names depending on which admin language was active during the most recent save.

### 4. Courier-mapping regeneration (POST-SAVE, OmniShip)

When the saved address is NOT an office address (no `office_id`) AND any field changed, the platform:

1. **Deletes** ALL existing rows in the address's mapping table — every cached "this address resolves to courier X's zone Y / office Z" mapping is wiped.
2. **Loops** over every active courier on the store via the OmniShip framework and calls `getOmniShipMapping` to recompute the mapping row for THIS address against THIS courier.

Each active courier gets one mapping row recomputed. For merchants with many active couriers (Speedy + Econt + DPD + EuShipment sub-couriers + ...) this is a substantial per-save operation — easily the largest single cost of every shipping-address edit.

**Skipped on office addresses.** When the address has an `office_id` (pickup point at a courier's office, e.g. Speedy office), the mapping regeneration does NOT run — the office is already tied to the courier's office record, so re-mapping it across every other courier is meaningless. See [[customer-shipping-address-storage]] for the pickup-point discriminator scheme.

### Text snapshot

A side effect that's not technically a numbered hook but runs every save: the formatted **text snapshot** (`text` column) is recomputed. This is the string most API responses + list views render — *"Tsar Boris III 100, Sofia 1612, BG"* etc. Re-saving an address always re-derives this string from the current field values.

### Side effects (visible)

- Phone in the list shows the E.164 format after save (e.g., `+359888123456`).
- Lat/lng pin appears on next open of the modal, even for manually-typed addresses.
- Save can take 1-5+ seconds on stores with many active couriers — for support tickets like *"why does the save spinner take so long?"*, this is the answer.
- The address text snapshot updates across every place that renders it: the list table's Address column, the [[customers-details]] sidebar, JSON-API v2 responses, past order labels (for new orders only — past orders carry their own snapshot from order-placement time; see [[customer-shipping-address-storage]]).

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customer-shipping-address-modal]] — the main UI entry point that triggers these hooks.
- [[customer-shipping-address-api]] — JSON-API v2 saves fire the same hooks.
- [[customer-shipping-address-storage]] — the office-address discriminator that skips hook #4.
- [[customer-shipping-address-google-maps]] — the UI autocomplete that fills lat/lng before save, complementing hook #2.
- [[settings-cart]] — where the Google Maps API key lives.

## Open questions

- Does the lat/lng auto-fill (hook #2) use the merchant's `google_maps_api_key` from [[settings-cart]], a platform-wide server credential, or neither (skipped when no key)? `(verify)`
