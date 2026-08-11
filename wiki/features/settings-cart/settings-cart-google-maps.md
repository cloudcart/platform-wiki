---
type: feature
nav_path: "Settings → Cart and checkout → Google Maps"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Google Maps API key", "google_map_api_key", "google_map_api_version", "checkout_hide_address_map", "checkout_hide_office_map", "checkout_hide_locker_map", "Address picker map", "Office delivery map", "Locker delivery map", "SettingsCartLegacyGoogleKey", "SettingsCartAddGoogleKey"]
tags: [settings, cart, checkout, google-maps, integration]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-cart]]. See the hub for the other aspects (accounts, abandoned reminder, payment/shipping defaults, limits, checkout fields, UI behavior, marketing consent).

# Cart and checkout — Google Maps integration

## Purpose

The box on the Cart and checkout page that enables **storefront Google Maps modules** during checkout — address picker maps, office-delivery selection maps, and locker-delivery selection maps. The merchant supplies their own Google Maps API key; the platform validates it against Google's API at save-time, detects whether the key is on the legacy or new Google Maps Platform, and then unlocks the three map switches. The three switches are visually disabled until a valid key is saved.

## Where to find it

Sidebar → Settings → **Cart and checkout** → box **Google Maps** (`google_api_key`).

## What the merchant can do here

- Paste their own Google Maps API key into the text input. The key is live-validated against Google's API at save-time; the version (legacy vs new) is detected and stored alongside the key.
- Enable / disable the **address picker map** that appears on the storefront's address step (`checkout_hide_address_map`, inverted switch).
- Enable / disable the **office-delivery map** that appears when the customer picks office pickup (`checkout_hide_office_map`, inverted switch).
- Enable / disable the **locker-delivery map** that appears when the customer picks locker pickup (`checkout_hide_locker_map`, inverted switch).
- See an inline warning when the saved key is still on the legacy Google Maps version.
- See an inline help/setup module linking to Google's API-key creation instructions when no key is set.

## Settings & fields

### Box: Google Maps (`google_api_key`)

The Google Maps API key is required for storefront map modules used during checkout.

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Google Maps API key** (`google_map_api_key`) | The merchant's own Google Maps API key. Saved through a separate `/google-map-key` endpoint that validates the key before persisting. | Plus an embedded validation module (`SettingsCartLegacyGoogleKey`) that warns if the key is still on the legacy Google Maps version (`google_map_api_version='legacy'`). Backend-validated (nullable, max 50 chars; live-validated against Google's endpoint when non-empty). |
| **Show Google map in addresses** (`checkout_hide_address_map`) | Switch (inverted) — when ON the map IS shown on the address step. | Disabled when no API key is set. |
| **Show Google map in Office Delivery Method** (`checkout_hide_office_map`) | Same (inverted) — when ON the map IS shown on office-delivery selection. | Disabled when no API key is set. |
| **Show Google Map in Locker Delivery Method** (`checkout_hide_locker_map`) | Same (inverted) — when ON the map IS shown on locker-delivery selection. | Disabled when no API key is set. |

In addition to the API key text input, two embedded sub-modules appear in this box:

1. **`SettingsCartLegacyGoogleKey`** — a warning panel that surfaces only when the stored key is on the legacy Google Maps version (`google_map_api_version='legacy'`). Tells the merchant to migrate to the new Google Maps Platform. Also has an `setErrors` callback prop for surfacing validation failures inline.
2. **`SettingsCartAddGoogleKey`** — a help / setup module that links the merchant to Google's API-key creation instructions when no key is set yet.

## Business rules

### Key validation happens live at save-time

When the merchant submits a Google Maps API key, the backend calls Google's API to test it. On success, the version (`legacy` vs `new`) is detected from the response and stored alongside the key as `google_map_api_version`. On failure, the validation error message from Google is surfaced to the merchant inline. Empty / null clears the key and resets the version to `new`.

The validation runs through a **separate endpoint** (`/google-map-key`) rather than the main Cart settings save handler — so the merchant can re-validate the same key without re-submitting the entire Cart and checkout page.

### Validation cache is cleared on save

Saving the Google Maps API key clears the related validation cache (`google_map_key_validation_<md5>`) for both the **previous** key AND the **new** key — preventing stale validation results from cached responses. The next storefront load re-validates against Google.

### Three map switches are gated by `hasGoogleApiKey`

The three "Show Google map in …" switches have `disabled: !hasGoogleApiKey.value` — when no key is saved, all three are visually greyed out and unclickable. As soon as the merchant pastes a valid key and saves, the disabled state is lifted.

Saving an **invalid** key still persists the key but the validation cache is cleared so the storefront will retry validation on next request. The merchant should expect maps not to render until a valid key is in place.

### Inverted-switch semantics on all three map toggles

All three map switches use `trueValue: false, falseValue: true`, meaning the UI's "ON" position stores literal `false` in the underlying setting (i.e., "Show map" = the `*_hide_*_map` key stores `false`). Practical merchant-facing wording is positive ("Show Google map in …") but storage is inverted. A support agent looking at a raw API dump should mentally invert these three keys. See the hub [[settings-cart]] for the cross-cutting list of inverted switches.

### Legacy version detection and merchant migration

Google has migrated from the original Google Maps JavaScript API to the new Google Maps Platform. CloudCart detects which one the merchant's key is bound to:

- **`legacy`** — the key works against the older API. `SettingsCartLegacyGoogleKey` warning surfaces, asking the merchant to migrate. CloudCart still renders maps using the legacy API.
- **`new`** (default for empty/new keys) — the key works against the modern Google Maps Platform.

If the merchant migrates their key from legacy to new (or vice versa) on Google's side, they should re-save the key here so the platform re-detects the version. The version is stored in `google_map_api_version`.

### What the maps do at checkout

- **`checkout_hide_address_map`** — adds a draggable-pin map to the address step so the customer can fine-tune the location coordinates. The address fields still drive the order; the map adds precision for delivery.
- **`checkout_hide_office_map`** — when the customer picks "office pickup" as their shipping option, a map renders showing the courier's office locations. The customer clicks a pin to select.
- **`checkout_hide_locker_map`** — same idea for "locker pickup" — the map shows nearby lockers (typically courier-specific networks).

If the merchant's selected shipping carrier doesn't have office/locker pickup options, the corresponding maps don't render even with the switches ON — there's nothing to plot.

### API quota and billing

The Google Maps API key is **the merchant's**, billed to the merchant's Google Cloud account. CloudCart does not pay for the merchant's map usage. If the merchant hits Google's billing limits or the API key is revoked on Google's side, the maps stop rendering on storefront — but the platform won't surface this proactively. The merchant should monitor their Google Cloud console.

## Related

- [[settings-cart]] — hub.
- [[settings-cart-google-maps-troubleshooting]] — fixing the **legacy Places API** breakage (checkout autocomplete stops working) by migrating to **Places API New** + re-validating; plus the `googleMapKeyStatus` diagnostic.
- [[shipping]] — shipping options including office / locker pickup that drive which maps render.
- [[settings-cart-checkout-fields]] — sibling aspect; the address fields the map fine-tunes the location for.
- [[checkout-flow]] — end-to-end checkout sequence concept page; the maps appear at the address and shipping-method steps.
- [[storefront-architecture]] — storefront rendering pipeline that loads the Google Maps JS library when these switches are ON.

## Open questions

_None._
