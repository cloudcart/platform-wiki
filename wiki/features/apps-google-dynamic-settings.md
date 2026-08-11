---
type: feature
nav_path: "Apps → Google Dynamic → Settings"
route_name: apps.google_dynamic.settings
route_path: /admin/apps/google_dynamic/settings
aliases: ["Google Dynamic Settings", "Google Ads Remarketing config"]
tags: [apps, google, ads, remarketing, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 4
---
# Google Dynamic → Settings

## Purpose

The **Settings** tab is where the merchant enters **Google Ads Conversion ID + Label** for the Dynamic Remarketing tags fired on the storefront. See [[apps-google-dynamic]] for the full feature set.

## Where to find it

Sidebar → Apps → Google Dynamic → **Settings tab**. Route: `/admin/apps/google_dynamic/settings`.

## What the merchant can do here

### Configuration

The Vue Settings panel (single `SettingsBox`, `editMethod: 'panel'` slide-over) exposes:

| Field | Notes |
|---|---|
| **Remarketing event snippet** (`remarketing_event_snippet`) | Switch — whether the event-snippet variant of the tag fires. |
| **Google Ads tracking ID** (`google_dynamic`) | `AW-XXXXXXXXXX` format. The platform auto-prepends `AW-` if pasted as digits only. |
| **Conversion label** (`google_variable`) | Per-event label string. |
| **Choose the type of the parameter** (`type`) | Dropdown: `Retail` or `Custom`. |
| **URL** | Read-only — link to the Google Shopping app (Retail mode pulls product data from Merchant Center). |

`ecomm_pagetype` / `ecomm_prodid` / `ecomm_totalvalue` are always emitted automatically when the tag fires — there is **no per-field opt-out toggle**.

### Privacy / consent integration

When [[apps-gdpr-overview]] is active and the customer rejects Marketing cookies, this tag should NOT fire.

### What the merchant CANNOT do here
- Create remarketing campaigns — that's in Google Ads.
- View audience size — Google Ads dashboard.
- Use without a Google Ads account.

## Settings & fields

Per [[apps-google-dynamic]] Manager:
- the configured check — credential validity check.

## Business rules

### Pairs with Google Tags

The cleaner pattern: install [[apps-google-tags]] (GTM) and configure dynamic remarketing IN GTM's UI. This integration is the legacy direct-injection alternative.

### Cookie consent gating

When [[apps-gdpr-overview]] indicates rejected Marketing cookies, the tag must NOT fire. Verify the platform's loader respects consent state.

### Permission
Standard apps permission scope.

## Related

- [[apps-google-dynamic]] — hub.
- [[apps-google-tags]] — preferred GTM-based path.
- [[apps-google-analytics]] — measurement.
- [[apps-google-shopping]] — feed integration (provides catalog data for remarketing ads).
- [[apps-gdpr-cookies]] — consent gating.

## How it works (verified against backend)

### Four saveable fields

Per the controller's `$only` allowlist, the settings page saves exactly:
- `google_dynamic` — Google Ads Conversion ID (auto-prefixed with `AW-` if the merchant pasted only digits).
- `google_variable` — the Google Ads variable used in the tag (e.g., conversion label).
- `type` — the conversion type, controlling which event format the tag fires.
- `remarketing_event_snippet` — optional custom HTML/JS snippet that the merchant can paste from Google Ads' event-snippet generator.

### Direct injection — pick this over GTM only when the merchant doesn't use GTM

This app injects the remarketing tag directly into the storefront. The merchant should choose this path when **NOT** also running [[apps-google-tags]] (Google Tag Manager); if GTM is installed, configure the remarketing tag inside GTM instead and leave this app uninstalled — running both leads to double-firing of events.

### Consent Mode v2 is governed by the GDPR app

This page has no consent-mode toggle. When [[apps-gdpr-overview]] is installed and "Google Consent Mode" is active on the cookie groups, the storefront emits `gtag('consent', 'default', ...)` (all denied) on load and `gtag('consent', 'update', ...)` (all granted) after the customer accepts — the remarketing tag automatically respects these signals.

### Audience criteria are not configurable here

The fields above are the entire allowlist — there is no rule editor that would let the merchant condition the tag (e.g., "only fire if cart_value > 100"). For conditional firing, the merchant uses GTM rules ([[apps-google-tags]]) or defines the audience in Google Ads itself based on the data the standard tag sends.

### Vue UI fields, in order

The Vue Settings panel shows:
1. **Remarketing event snippet** — switch (toggle whether the event-snippet variant of the tag fires).
2. **Google Ads tracking ID** — text input (the `AW-XXXXXXXXX` conversion ID; the platform auto-prepends `AW-` if pasted as digits only).
3. **Conversion label** — text input (the `google_variable` setting).
4. **Choose the type of the parameter** — dropdown: `Retail` or `Custom`.
5. **URL** — read-only display with a link to the [[apps-google-shopping]] page (presented because Retail-mode remarketing depends on the Merchant Center feed for dynamic creative).

### Save triggers a regenerate of the shared apps JS file

Because the Google Dynamic manager implements `AppJsRegenerate`, saving the page rebuilds `cc_applications_config.js`. The new conversion ID takes effect on the next storefront page load (when the file URL's `last_build` timestamp cache-busts).

### Wiki note: Page-type / product-ID / total-value toggles do NOT exist

The wiki's earlier table mentioning toggles for "Page-type emission", "Product ID emission", and "Total value emission" is NOT backed by the actual UI. Those values are always emitted automatically when the tag fires — there is no per-field opt-out.

### Settings box uses `editMethod: 'panel'` (right-side slide-over)

The Vue renders ONE `SettingsBox` with `editMethod: 'panel'` — clicking Edit opens a right-side drawer with all 5 fields stacked. The drawer-edit pattern is the same as Google Shopping settings (vs the inline-edit used by GTM / Analytics / Search Console). The "URL" row at the bottom is a read-only HTML cell rendered by the `CopyUrl` Vue component — it shows a `router-link` styled like an external-link button: *"Open Google AdWords Feed app"* linking to the [[apps-google-shopping]] overview page (the dynamic remarketing feed comes from Merchant Center, hence the cross-link).

### `google_dynamic` ID field has long inline help text

The Settings field for the Conversion ID has a `help` payload with a multi-line walkthrough: *"Sign in to Google Ads. Click Shared library. Under Audiences click View. ... select the dynamic remarketing option, then select your business type. ... If you select Retail, follow the instructions to link your Merchant Center and Google Ads accounts. Click Tag details. Select and copy the remarketing tag code. This tag works on both desktop and mobile websites."* — surfaced via the inline help icon next to the field label.

## Open questions

(None currently outstanding for this page.)
