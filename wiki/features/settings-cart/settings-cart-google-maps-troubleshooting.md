---
type: feature
nav_path: "Settings → Cart and checkout → Google Maps → Key validation & legacy Places API"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Google Maps key not working", "Google autocomplete not working at checkout", "Places API New", "Places API legacy", "legacy Places API deprecated", "google_map_api_version", "REQUEST_DENIED google maps", "Полето Въведете улица и град за доставка се изисква когато Област няма стойност", "Въведете улица и град за доставка се изисква", "Моля напишете област", "checkout address autocomplete broken", "selected suggestion does not fill address fields", "address not populating after selecting google suggestion", "Област stays empty after picking address", "Google suggestions show but fields stay empty", "validate google maps key", "googleMapKeyStatus", "google maps key status", "migrate to Places API New"]
tags: [settings, cart, checkout, google-maps, troubleshooting, integration]
plan_gates: []
created: 2026-06-26
updated: 2026-11-09
source_count: 3
---

> Part of [[settings-cart]]. The Google Maps key box itself (field, map switches, legacy warning) is on [[settings-cart-google-maps]].

# Cart and checkout — Google Maps key: the legacy Places API problem & validation

## Purpose

The single most common storefront-checkout breakage tied to Google Maps: a key still running on **Google's legacy Places API**. Google has wound the legacy Places API down, so on keys that have **not** enabled **Places API (New)** the checkout address autocomplete still shows suggestions but **selecting one no longer fills the address fields** — which blocks the checkout address step. This page is the symptom → cause → fix for that, plus the live key-status diagnostic. The key-configuration box (API-key field, the three map switches, the inline legacy warning) is documented on [[settings-cart-google-maps]].

## Where to find it

Sidebar → Settings → **Cart and checkout** → box **Google Maps**. The same box live-validates the key, detects whether it is on the legacy or new Google Maps Platform, and shows a migration warning when it is still legacy.

## What the merchant can do here

### Symptom

On the storefront **checkout address step**, Google **still shows** the autocomplete suggestions — but **selecting one does not populate the form fields**. Street, city, and especially **Област** / region stay **empty** after the pick. When the customer tries to continue, the address validation fails, most commonly with:

> **"Полето Въведете улица и град за доставка се изисква, когато Област няма стойност"**
> (the *"Въведете улица и град за доставка"* field is required because the **Област** / region field is empty)

The visible tell is exactly this: the dropdown appears and the customer clicks a suggestion, but the fields below don't fill (or fill partially and won't validate), and checkout is blocked. This is **different** from the address-shape false-negative (picking a bare neighbourhood / city) — here a proper suggestion is selected and still nothing lands in the fields.

### Cause

The store's Google Maps API key is on the **legacy Places API**, which Google has deprecated. The legacy autocomplete still **renders the dropdown**, but the deprecated **place-details / address-components** call behind the selection (the part that feeds the structured fields) no longer returns usable data — often with **`REQUEST_DENIED`** — so picking a suggestion writes **nothing** into street / city / **Област**. The platform stores the detected version as `google_map_api_version`; a `legacy` key shows the migration warning in the Google Maps box ([[settings-cart-google-maps]]).

### Fix

1. In the **Google Cloud Console**, enable **Places API (New)** for the same API key. This is done on **Google's side** — CloudCart cannot enable it for the merchant.
2. Return to **Settings → Cart and checkout → Google Maps** and click **Validate** in the legacy warning. It tests **Places API (New) only**; on success it stores `google_map_api_version = new` and clears the warning. While the new API is still off it answers *"Places API (New) is disabled. Enable it by visiting Google Cloud Console then retry."*
3. The checkout address autocomplete works again.

Until the key is migrated and re-validated, the workaround is to **clear the Google Maps key** or switch **Show Google Map** off, which switches checkout to the **manual country / city dropdown form** (no autocomplete) — see [[shipping-calc-geo-gating]] for that non-Google fallback.

## Settings & fields

- `google_map_api_key` — the merchant's key; live-validated at save-time (full field detail on [[settings-cart-google-maps]]).
- `google_map_api_version` — the **detected** version stored alongside the key: **`legacy`** or **`new`**. Drives the inline migration warning.
- **Validate** (in the legacy warning) runs through the separate `/google-map-key` endpoint, so the same key is re-tested without re-saving the whole page.

## Business rules

### How validation detects the version (live probe)

When the page is saved with a key (and in the staff diagnostic below), the platform runs a **live probe** against Google, sent as coming from the store's address: it **first tries the new Places API**, and only if that fails **falls back to the legacy Places API**. The version that responds successfully is stored as `google_map_api_version`. So a key that works only on legacy is stored `legacy` (+ warning); a key with Places API New enabled is stored `new`. Empty / cleared key resets the version to `new`.

The probe also enforces basic key format (minimum 20 / maximum 50 characters, allowed character set) before the network test. When it fails, the key is not saved and the error *"Invalid Google Maps API key: …"* carries Google's reason (e.g. `REQUEST_DENIED`). The **Validate** button skips the legacy fallback (step 2 above).

Messages after *"Invalid Google Maps API key: "*: *"API key is too short (minimum 20 characters)"*, *"API key is too long (maximum 50 characters)"*, *"API key contains invalid characters"*, and from Google *"API key is invalid or request was denied"* or *"API key has exceeded quota limits"*. The legacy warning reads: *"Your Google Maps API key is currently using the legacy Places API. … enable the new Places API (New) by visiting the Google Cloud Console and activating it for your project. After activation, click the validation button."*

## Related

- [[settings-cart-google-maps]] — the Google Maps key box (field, map switches, legacy-version warning).
- [[settings-cart]] — Cart and checkout settings hub.
- [[shipping-calc-geo-gating]] — the checkout address **country restriction** and the **no-Google-Maps manual dropdown** fallback (what checkout looks like with the key removed).
- [[checkout-flow]] — the checkout the address autocomplete runs on.

## Open questions

None.
