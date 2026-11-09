---
type: feature
nav_path: "Settings → Cart and checkout → Google Maps"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Google Maps API key", "google_map_api_key", "google_map_api_version", "checkout_hide_address_map", "checkout_hide_office_map", "checkout_hide_locker_map", "Address picker map", "Office delivery map", "Locker delivery map", "SettingsCartLegacyGoogleKey", "SettingsCartAddGoogleKey"]
tags: [settings, cart, checkout, google-maps, integration]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[settings-cart]]. See the hub for the other aspects (accounts, abandoned reminder, payment/shipping defaults, limits, checkout fields, UI behavior, marketing consent).

# Cart and checkout — Google Maps integration

## Purpose

The box on the Cart and checkout page that enables **storefront Google Maps modules** during checkout — address picker maps, office-delivery selection maps, and locker-delivery selection maps. The merchant supplies their own Google Maps API key; the platform validates it against Google's API at save-time, detects whether the key is on the legacy or new Google Maps Platform, and then unlocks the three map switches. The three switches are visually disabled until a valid key is saved.

## Where to find it

Sidebar → Settings → **Cart and checkout** → box **Google Maps** (`google_api_key`).

## What the merchant can do here

- Paste their own Google Maps API key into the text input. The key is live-validated against Google's API at save-time; the version (legacy vs new) is detected and stored alongside the key.
- Turn all of it off at once with **Show Google Map**, to preview checkout without a map.
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
| **Google Maps API key** (`google_map_api_key`) | The merchant's own Google Maps API key, saved with the page after a live check. | Plus an embedded validation module (`SettingsCartLegacyGoogleKey`) that warns if the key is still on the legacy Google Maps version (`google_map_api_version='legacy'`). Backend-validated (nullable, max 50 chars; live-validated against Google's endpoint when non-empty). |
| **Show Google Map** (`show_google_map`) | Switch, on by default. Help text: *"When off, the store works as if no Google Maps API key is set: no map and no address suggestions in checkout, even with your key or on a trial store"*. | Overrides the merchant's key and the platform key trial stores use. The storefront, the admin and the Storefront API's checkout settings all follow it. |
| **Show Google map in addresses** (`checkout_hide_address_map`) | Switch (inverted) — when ON the map IS shown on the address step. | Disabled when no API key is set. |
| **Show Google map in Office Delivery Method** (`checkout_hide_office_map`) | Same (inverted) — when ON the map IS shown on office-delivery selection. | Disabled when no API key is set. |
| **Show Google Map in Locker Delivery Method** (`checkout_hide_locker_map`) | Same (inverted) — when ON the map IS shown on locker-delivery selection. | Disabled when no API key is set. |

The box also shows a warning when the stored key is on the legacy Google Maps version, and links to Google's API-key instructions when no key is set.

## Business rules

### Key validation happens live at save-time

Saving the page with a key checks it first: 20–50 allowed characters, then a live test sent as coming from the store's address, **Places API (New)** first and the legacy Places API as fallback. The version that answers is stored as `google_map_api_version`. A failing key is **not saved**: the save fails with *"Invalid Google Maps API key: …"* and Google's reason. Empty clears the key and resets the version to `new`.

On a legacy key, the warning's **Validate** button (`/google-map-key`) tests **Places API (New) only**: success stores `new` and clears the warning; otherwise *"Places API (New) is disabled. Enable it by visiting Google Cloud Console then retry."* or Google's own error.

**Which key the storefront uses:** none when **Show Google Map** is off; on a store not yet live, the merchant's key, or without one the platform's own key but only on the store's cloudcart.com / cloudcart.net address; on a live store, only the merchant's key. The storefront loads Google's Maps JavaScript API with the Places and Marker libraries; which further APIs or key restrictions Google requires is Google's side (verify).

### Validation cache is cleared on save

Saving the Google Maps API key clears the related validation cache (`google_map_key_validation_<md5>`) for both the **previous** key AND the **new** key — preventing stale validation results from cached responses. The next storefront load re-validates against Google.

### Three map switches are gated by `hasGoogleApiKey`

The three "Show Google map in …" switches have `disabled: !hasGoogleApiKey.value` — when no key is saved, all three are visually greyed out and unclickable. As soon as the merchant pastes a valid key and saves, the disabled state is lifted.

### Inverted-switch semantics on all three map toggles

All three map switches use `trueValue: false, falseValue: true`: the UI's "ON" ("Show Google map in …") stores `false` in the `*_hide_*_map` key. Invert these three keys when reading a raw API dump. See the hub [[settings-cart]] for the cross-cutting list of inverted switches.

### Legacy version detection and merchant migration

CloudCart detects which Places API the merchant's key works with:

- **`legacy`** — the key works against the older API. `SettingsCartLegacyGoogleKey` warning surfaces, asking the merchant to migrate. CloudCart still renders maps using the legacy API.
- **`new`** (default for empty/new keys) — the key works against the modern Google Maps Platform.

After enabling Places API (New) on Google's side, the merchant clicks **Validate** in the warning.

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
