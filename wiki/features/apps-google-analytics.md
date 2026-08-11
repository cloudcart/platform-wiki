---
type: feature
nav_path: "Apps → Google Analytics"
route_name: apps.google_analytics.overview
route_path: /admin/apps/google_analytics
aliases: ["Google Analytics", "GA", "GA4", "Universal Analytics", "Google Analytics 4", "Гугъл Аналитикс", "enable disable button", "app active toggle"]
tags: [apps, google, analytics, tracking, measurement]
plan_gates: ["google_analytics"]
created: 2026-05-22
updated: 2026-08-06
source_count: 8
---
# Google Analytics

## Purpose

**Google Analytics** integration — tracks visitor behaviour, traffic sources, conversions, and ecommerce metrics on the storefront. CloudCart injects the appropriate tracking script (GA4 by default; legacy Universal Analytics — UA — also supported through a version flag) and emits the platform's ecommerce events (view_item, add_to_cart, begin_checkout, purchase, etc.) so the merchant sees rich ecommerce reporting in the GA console.

Used by virtually every merchant for measurement. Free to set up (Google Analytics itself is free); CloudCart just provides the integration plumbing.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Where to find it

Sidebar → Apps → install → **Google Analytics**. See [[apps-google-analytics-settings]] for configuration details.

## What the merchant can do here

- Configure the GA measurement ID (GA4) OR tracking ID (legacy UA). There is no version toggle — the platform auto-detects GA4 vs UA from the prefix (`G-` = GA4, otherwise UA).
- Toggle the `debug` switch to fire events to GA's DebugView for testing.
- Activate / deactivate the app.

### What the merchant CANNOT do here
- View analytics data directly in CloudCart — for reports the merchant goes to the GA console at analytics.google.com.
- Configure cross-domain tracking, custom dimensions / event mapping, or Anonymize IP. Those live in Google's own GA admin or in [[apps-google-tags]] (GTM).
- Edit GA's event schema — CloudCart emits the standard ecommerce events; GA decides how to report them.
- Use Google Analytics without a free Google account.

## Settings & fields

Only two fields are saved by this app (configured via [[apps-google-analytics-settings]]):

- `code` — the GA4 Measurement ID (`G-XXXXXXXXXX`) or legacy UA Tracking ID (`UA-XXXXXX-Y`). Required once the app is active (`required_if:active,1`); error when missing: *"Google analytics tracking ID is required"*. The merchant can install without configuring, but activation forces a valid ID.
- `debug` — debug toggle; enables GA's DebugView.

No other GA fields exist here. Cross-domain linkers, send-to multiple property IDs, sub-domain config, and per-product custom dimensions are all handled in Google's UI or via [[apps-google-tags]] (GTM) reading from the storefront data layer.

## Business rules

### GA4 default + UA legacy mode (auto-detected from the code prefix)

Google retired Universal Analytics in July 2023. New properties default to GA4 (Measurement ID format `G-XXXXXXXXXX`). Some legacy stores may still need the older UA mode (`UA-XXXXXX-Y`). The merchant sets no version toggle — the platform routes to the correct tag implementation purely from the prefix: `G-` → GA4, otherwise UA. Because detection is per-code, a single CloudCart instance can serve GA4 and UA stores side by side. A **single store** running BOTH GA4 + UA at once is not supported by this one-field design — the merchant uses [[apps-google-tags]] to manage both tags in GTM.

### Ecommerce events

CloudCart emits the standard GA4 ecommerce event taxonomy, client-side via the browser's `gtag.js`:
- `view_item`
- `view_item_list`
- `add_to_cart`
- `remove_from_cart`
- `view_cart`
- `begin_checkout`
- `add_shipping_info`
- `add_payment_info`
- `purchase`
- `refund`

These appear in GA's Realtime + Conversion reports.

### `purchase` event fires once per order — no duplicates on reload

The `purchase` event is dispatched ONLY the first time the customer lands on the order-confirmation page. After that first pageview the order is flagged so subsequent reloads of the same thank-you URL emit `js_events: false` in the data layer, signalling GA / GTM tags to skip re-firing the purchase event. A customer who bookmarks the thank-you page and revisits it, or refreshes after a poor connection, does NOT cause duplicate conversion attribution. Confirmed in [[apps-datalayer]] — the same mechanism applies to TikTok Pixel and any other tag managers consuming the data layer.

### `refund` event is NOT fired automatically

Although `refund` is in the taxonomy above, the storefront never fires it when an order is refunded via [[orders-payment-refund]]. Merchants who need refund tracking in GA build it externally (GTM triggers on the admin refund action, or direct GA Measurement Protocol calls).

### Client-side only — no server-side measurement

The integration is entirely client-side; there are no server-side GA Measurement Protocol calls for storefront events. Server-side measurement requires [[apps-google-tags]] with a server-side tag manager OR a custom integration.

### Cookie consent (Google Consent Mode v2)

When [[apps-gdpr-overview]] is installed and its "Google Consent Mode" cookie group is active, the storefront emits **Google Consent Mode v2** signals before any GA tracking fires. The default state on page load is all-denied (`ad_personalization`, `ad_storage`, `ad_user_data`, `analytics_storage` all `denied`); when the customer accepts the banner, the storefront sends a consent `update` with the signals granted. Without the GDPR app + that cookie group active, no consent signals are emitted and GA fires unconditionally.

### Crawler and admin-preview traffic is excluded

The storefront tag loader skips crawler requests (so Googlebot's visits don't fire `gtag` events) and admin "View as customer" preview sessions, keeping the merchant's GA stats clean of bot and staff noise. CloudCart's own admin UI uses a separate, CloudCart-managed GA property — the merchant's GA only ever receives storefront events.

### Changing the code requires a JS rebuild before it takes effect

The GA snippet is not emitted inline per page; the merchant's code is baked into the shared storefront apps-config file that every page loads from CDN. When the merchant changes, installs, uninstalls, or activates the app, that file is **regenerated automatically** before browsers pick up the new code. The file URL is versioned by build timestamp, so a hard browser refresh isn't usually needed. Google Analytics and [[apps-google-dynamic]] share a single storefront loader: it boots whenever EITHER GA or Dynamic Remarketing is active, so running only one of the two still loads the shared runtime.

### Two tabs: Overview + Settings

The app always shows exactly two tabs — **Overview** (`/admin/apps/google_analytics`) and **Settings** (`/admin/apps/google_analytics/settings`). There is no conditional tab visibility, OAuth state, or extra tabs after configuration. The same pattern is used by [[apps-google-tags]], Google Search Console, and [[apps-google-dynamic]].

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `google_analytics` | Access gate (install URL) | The install URL `/admin/apps/google_analytics/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-google-analytics-settings]] — settings sub-page.
- [[apps-google-tags]] — Tag Manager for managing multiple tracking scripts in one place.
- [[apps-google-dynamic]] — dynamic remarketing tags.
- [[apps-google-connect]] — OAuth Connect (some GA features may use it).
- [[apps-google-shopping]] — sister product feed integration.
- [[apps-gdpr-overview]] — cookie consent gates analytics tracking.
- [[apps-tiktok-pixel]] / [[apps-facebook-comments]] — alternative tracking pixels.

## Open questions

(None currently outstanding for this page.)
