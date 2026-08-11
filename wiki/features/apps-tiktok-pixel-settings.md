---
type: feature
nav_path: "Apps → TikTok Dynamic Ads → Settings"
route_name: apps.tiktok.settings
route_path: /admin/apps/tiktok/settings
aliases: ["TikTok Pixel Settings", "TikTok tracking pixel config", "TikTok Dynamic Ads settings", "TikTok feed settings"]
tags: [apps, social, tiktok, pixel, capi, feed, tracking, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-06-23
source_count: 3
---
# TikTok Dynamic Ads → Settings

## Purpose

The **Settings** tab of the [[apps-tiktok-pixel|TikTok Dynamic Ads]] app — the merchant enters the **TikTok Pixel ID** + CAPI config (the tracking half) and the **catalog-feed** options (UTM, colour/size attribute mapping, product filter). See [[apps-tiktok-pixel]] for the full feature set and [[apps-tiktok-catalog-feed]] for the feed.

## Where to find it

Sidebar → Apps → TikTok Dynamic Ads → **Settings tab**. Route: `apps.tiktok.settings` (`/admin/apps/tiktok/settings`).

## What the merchant can do here

### Configuration

The Settings UI groups the config into boxes. The **TikTok Pixel** box has four fields:

| Field | Notes |
|---|---|
| **Pixel Code** (`pixel_code`) | Required (min 3 chars). Placeholder `e.g. C5XXXXXXXXX`. From TikTok Events Manager. |
| **Access Token** (`access_token`) | Required only when **Enable Events API** is ON (min 10 chars). Placeholder *"Required for Events API (CAPI)"*. |
| **Test Event Code** (`test_event_code`) | Optional — for testing fires in TikTok's Test Events panel. |
| **Enable Events API (Server-Side)** (`capi_status`) | Switch (1/0). Activates the server-side CAPI path. |

There are **NO per-event toggles** (ViewContent / AddToCart / Search / etc.). CloudCart fires the full standard event vocabulary automatically when the pixel is configured — the merchant cannot opt-out per event.

### Catalog-feed boxes (the feed half)

Because this is now the unified **TikTok Dynamic Ads** app, the Settings tab also carries the catalog-feed config (the feed itself is on [[apps-tiktok-catalog-feed]]):

- **UTM tracking parameters** — `utm_source` / `utm_medium` / `utm_campaign` appended to the product links in the feed.
- **Variant attributes** — `color_parameter` / `size_parameter`: pick which variant parameters represent colour / size; they feed `g:color` / `g:size` in the catalogue.
- **Filter products** — restrict which products are included in the feed (by category / vendor / tag / selection, the standard XML-feed product scope).

### Privacy / consent integration

When [[apps-gdpr-overview]] is active and the customer rejects the **Targeting** cookie group, the pixel does NOT fire (browser AND server paths are gated).

### What the merchant CANNOT do here
- View pixel analytics inside CloudCart — go to TikTok Events Manager.
- Use without a TikTok for Business account + a Pixel created there.

## Settings & fields

Per [[apps-tiktok-pixel]] Manager: `APP_KEY = 'tiktok_pixel'`.

## Business rules

### Standard event taxonomy

CloudCart fires the standard TikTok event vocabulary at key user actions. Maps to TikTok's conversion events for ad optimization.

### Cookie consent gating

Tracking should respect cookie consent (per [[apps-gdpr-cookies]]).

### Permission
Standard apps permission scope.

## Related

- [[apps-tiktok-pixel]] — hub.
- [[apps-tiktok-ads]] — paired advertising (uses pixel data).
- [[apps-tiktok-shop]] — marketplace sister.
- [[apps-google-analytics]] / [[apps-facebook-comments]] — sister tracking pixels.

## How it works (verified against backend)

### Server-side Events API field — Access Token + toggle

Per the platform code and `capi_status` lang keys: the Settings tab exposes an **Access Token** field (generated in TikTok Events Manager) and an **Enable Events API (Server-Side)** toggle. When both are set, server-side conversion events are fired in addition to the browser pixel. Without an Access Token, the CAPI path is disabled — only the in-browser pixel runs. **CAPI is free for all** — there is no longer a plan-feature gate (the old `tiktok.capi` gate was removed); only the `capi_status` toggle + a valid Access Token are required.

### Test Event Code for staging

An optional Test Event Code field forwards events tagged for the TikTok Events Manager → Test Events panel. Use this to verify integration before going live; leave empty in production so real events aren't filtered.

### Consent enforcement — Targeting cookie group

Both the browser-pixel and server-side paths check whether the visitor accepted the `targeting` cookie group. If the customer hasn't accepted the Targeting cookie category, neither path sends any data. The merchant doesn't configure granular per-event consent — it's a single all-or-nothing gate tied to the Targeting consent group.

### Standard events only — no custom event editor

Only TikTok's standard event vocabulary is recognised (`Pageview`, `ViewContent`, `Search`, `AddToCart`, `AddToWishlist`, `InitiateCheckout`, `CompletePayment`, `PlaceAnOrder`). There is no UI to add custom events — sending "newsletter signup" or other non-standard events requires switching to [[apps-google-tags]].

### One Pixel ID per store install

Per the `pixel_code` setting (single value): only one TikTok Pixel can be configured per store. Stores that advertise from multiple ad accounts and need separate pixels have to use Tag Manager instead.

### Form validation — Pixel Code required, Access Token enforced only when CAPI toggle is on

The save controller requires `pixel_code` (min 3 chars) at all times — empty / too-short values are rejected with "TikTok Pixel Code is required" / "TikTok Pixel Code must be at least 3 characters". The `access_token` field is conditionally required: only when the merchant flips the **Enable Events API (Server-Side)** toggle does the save check for an access token (min 10 chars, "Access Token appears to be invalid" otherwise). So merchants who run only the browser pixel never need to fill the Access Token field — but turning CAPI on forces them to fill it in the same save.

### Settings whitelist — these are the exact saved fields

Only these settings are persisted from the form submission: `pixel_code`, `access_token`, `test_event_code`, `capi_status` (boolean). Everything else in the submission is discarded. So adding custom fields via browser dev-tools or third-party automation won't sneak past — the controller has an explicit whitelist.

## Open questions
