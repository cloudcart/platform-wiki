---
type: feature
nav_path: "Apps → Google Analytics → Settings"
route_name: apps.google_analytics.settings
route_path: /admin/apps/google_analytics/settings
aliases: ["Google Analytics Settings", "GA settings", "GA4 config"]
tags: [apps, google, analytics, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 6
---
# Google Analytics → Settings

## Purpose

The **Settings** tab is where the merchant enters the **GA Measurement ID** (GA4) or **Tracking ID** (legacy UA), picks the version, and configures basic GA behaviour. See [[apps-google-analytics]] for the full feature set.

## Where to find it

Sidebar → Apps → Google Analytics → **Settings tab**. Route: `/admin/apps/google_analytics/settings`.

## What the merchant can do here

### Configuration

The Vue Settings UI exposes exactly TWO fields:

| Field | Notes |
|---|---|
| **Google Analytics code** (`code`) | Text input, placeholder `G-XXXXXXXXXX`. Accepts GA4 (`G-...`) or legacy UA (`UA-XXXXXX-Y`); the version is auto-detected by prefix. |
| **DEBUG mode** (`debug`) | Switch (1 / 0). Enables GA's DebugView during testing. |

The fields are rendered as a single `SettingsBox` with `editMethod: 'slide'` — Edit opens a right-side drawer.

### Privacy / consent integration

- **Respect cookie consent** — when [[apps-gdpr-overview]] is active and customer rejects analytics cookies, GA does NOT fire. Consent Mode v2 is governed entirely by the GDPR app, NOT a toggle on this page.

### What the merchant CANNOT do here
- Configure cross-domain tracking, Enhanced Ecommerce toggle, Anonymize IP, or custom dimensions on this page — those don't exist here (use Google's own GA admin or [[apps-google-tags]] for tag-level tuning).
- Use without a Google Analytics account at analytics.google.com.
- Pre-fill historical data — GA only captures events going forward.

## Settings & fields

Per [[apps-google-analytics]] Manager:
- `isGVersion` — boolean: GA4 vs UA.
- the configured check — credential validity.

## Business rules

### GA4 default

Google retired Universal Analytics in July 2023. New properties default to GA4. The `isGVersion` flag preserves legacy UA compatibility for stores not yet migrated.

### Ecommerce events

When Enhanced ecommerce is enabled, CloudCart fires the standard GA4 event taxonomy at key user actions (per [[apps-google-analytics]]).

### Cookie consent gating

When [[apps-gdpr-overview]] is active, GA script loading + event firing should respect the customer's cookie consent state (Analytics cookies category).

### Permission
Standard apps permission scope.

## Related

- [[apps-google-analytics]] — hub.
- [[apps-google-tags]] — Tag Manager alternative.
- [[apps-google-dynamic]] — dynamic remarketing.
- [[apps-gdpr-cookies]] — cookie consent gating.
- [[apps-datalayer]] — data layer for advanced tracking.

## How it works (verified against backend)

### Two configurable settings

The Settings controller's `$only` allowlist is exactly `['code', 'debug']`. The merchant configures:
- **Tracking ID** (`code`) — GA4 Measurement ID (`G-XXXXXXXXXX`) or legacy UA Tracking ID (`UA-XXXXXX-Y`). Auto-detected by prefix.
- **Debug mode** (`debug`) — toggle for GA DebugView during testing.

Other GA features (cross-domain, custom dimensions, anonymize IP) are NOT exposed on this page. For those, use [[apps-google-tags]] (Google Tag Manager).

### Validation

The `code` field is required only when the app is active (`required_if:active,1`). Installing without immediately setting a code is allowed; activating without a code triggers: *"Google analytics tracking ID is required"*.

### GA4 vs UA: auto-detect by prefix

The Manager's `isGVersion` method checks if the code starts with `G-` — if so, GA4 mode; otherwise UA mode. The merchant doesn't have to pick a version explicitly; just paste the right ID format.

### Consent Mode v2 ships via the GDPR app, not from this settings page

The Settings page does NOT have a toggle for Consent Mode v2. Consent Mode is activated when [[apps-gdpr-overview]] is installed AND the "Google Consent Mode" cookie group is set to active — at that point the storefront emits `gtag('consent', 'default', ...)` on page load (all signals denied) and `gtag('consent', 'update', ...)` after the customer accepts. From this Google Analytics Settings page, the merchant configures only the GA tracking ID; consent governance is in [[apps-gdpr-cookies]].

### Server-side measurement is not built in

CloudCart's GA integration is purely client-side via `gtag.js`. There is no field on this page (and no separate app) that lets the merchant configure GA's Measurement Protocol for server-side events. Merchants who need server-side measurement either route through [[apps-google-tags]] with a server-side GTM container OR build a custom integration outside CloudCart.

### Custom dimensions per product / per-customer-group are not configurable here

The only fields the merchant can edit on this page are the tracking ID and the debug flag. Pushing custom dimensions tied to specific products, customer groups, or order attributes requires using [[apps-google-tags]] (GTM) where the merchant defines tag variables that read from CloudCart's data layer (see [[apps-datalayer]]).

### Settings save triggers a global JS regenerate

The Google Analytics manager class implements an `AppJsRegenerate` contract. Saving the GA settings (changing the code or toggling debug) causes the shared `cc_applications_config.js` file in CDN/S3 to be regenerated with the new `code`. Until that regenerate completes and the storefront browser fetches the new file, the OLD code keeps firing. The file is versioned by `last_build` timestamp so it cache-busts naturally on the next page load.

### No GA dashboard or "View Analytics" inside CloudCart

Confirmed: no field, button, or panel on this page that pulls GA reports into CloudCart. The setting page collects the tracking ID + debug toggle. To view reports the merchant logs into analytics.google.com.

### Vue Settings UI has TWO fields: code + debug

The Vue settings page only renders two fields:
- **Google Analytics code** — text input, placeholder `G-XXXXXXXXXX`.
- **DEBUG mode** — switch (true value=1, false value=0).

The wiki's longer field list (Cross-domain, Enhanced ecommerce, Anonymize IP) is NOT present in the actual settings UI — those features are configured either in Google's own GA admin or via [[apps-google-tags]].

### Single box rendered with `editMethod: 'slide'`

The Vue uses ONE `SettingsBox` with `editMethod: 'slide'` — clicking Edit opens a slide-over drawer with the two fields. The page's `Index.vue` also intercepts initial config load (`handleInitialConfig`) to default `debug = 0` and `is_active = 0` when missing — so newly-installed apps start with debug off and inactive.

### `disable-save` ties into the `ApplicationSettings` wrapper

The parent `ApplicationSettings` component receives a `disable-save` prop that flips to true while a setting box is open (via `settingOpen` watcher) — preventing the save bar from posting while a slide-over edit is active. This is part of the shared settings-page UX and applies to all `editMethod: 'slide'` settings.

## Open questions

(None currently outstanding for this page.)
