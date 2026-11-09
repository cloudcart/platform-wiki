---
type: feature
nav_path: "Apps → Google Analytics"
route_name: apps.google_analytics.overview
route_path: /admin/apps/google_analytics
aliases: ["Google Analytics", "GA", "GA4", "Universal Analytics", "Google Analytics 4", "Гугъл Аналитикс", "enable disable button", "app active toggle"]
tags: [apps, google, analytics, tracking, measurement]
plan_gates: ["google_analytics"]
created: 2026-05-22
updated: 2026-11-09
source_count: 9
---
# Google Analytics

## Purpose

**Google Analytics** integration — tracks visitor behaviour, traffic sources, conversions, and ecommerce metrics on the storefront. CloudCart injects the appropriate tracking script (GA4 by default; legacy Universal Analytics — UA — also supported through a version flag) and emits the platform's ecommerce events (view_item, add_to_cart, begin_checkout, purchase, etc.) so the merchant sees rich ecommerce reporting in the GA console.

Google Analytics itself is free; CloudCart provides the integration.

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

Google retired Universal Analytics in July 2023. New properties default to GA4 (Measurement ID format `G-XXXXXXXXXX`). Some legacy stores may still need the older UA mode (`UA-XXXXXX-Y`). The merchant sets no version toggle — the platform routes to the correct tag implementation purely from the prefix: `G-` → GA4, otherwise UA. A **single store** running BOTH GA4 + UA at once is not supported by this one-field design — the merchant uses [[apps-google-tags]] to manage both tags in GTM.

### Ecommerce events

CloudCart sends these GA4 events client-side, via the browser's `gtag.js`:
- `view_item` — a product page.
- `view_item_list`, `select_item` — listing pages (below).
- `add_to_cart`, `remove_from_cart`, `add_to_wishlist`.
- `view_cart` — the cart page; `begin_checkout` — the start of checkout.
- `add_shipping_info`, `add_payment_info`.
- `purchase` — the thank-you page (below).
- `login` (Google, Facebook or the login form) and `sign_up` (registration form).

### Listing events: `view_item_list` and `select_item`

- `view_item_list` goes out on category, smart collection, brand, tag and search-results pages, with the products of the page shown. A filter, sort or page change that reloads the list in place brings a new page-data block, so the event is sent again with the new products. The home page, showcase and bundle lists, content pages and product-page carousels send none.
- Its items carry `list_name` (the category, collection, brand or tag name; empty on search) and `list_position` (from 0). There is no `item_list_id` and no event-level `item_list_name` on it.
- `select_item` is sent since 12.10.2026, when the listing cards started carrying the product's ID: a click on a card of that list sends it with `index`, `item_list_name` (the list's name) and `item_list_id` (the page type: `category`, `smart_collection`, `vendor`, `tag` or `search`). Cards outside the list, such as related or cross-sell products, are ignored.

### `purchase` — once per order, no fallback

Sent on the first render of the thank-you page (or the fast-order success panel) for any status except `cancel`; later renders send nothing. No payment-status gate, no server-side copy for buyers who never return from the payment page, and `value` excludes shipping. Details, payload and checks: [[apps-google-analytics-purchase-event]].

### `refund` event is NOT fired automatically

GA4's `refund` event is not among the events above: the storefront never fires it when an order is refunded via [[orders-payment-refund]]. Merchants who need refund tracking in GA build it externally (GTM triggers on the admin refund action, or direct GA Measurement Protocol calls).

### Client-side on the classic storefront, server-side through the Storefront API

On the classic storefront the integration is client-side. Storefront API clients, such as a Nitrogen storefront, can report through GA's Measurement Protocol once the merchant enters its secret on [[apps-google-analytics-settings]]. See [[headless-analytics-consent]].

### Cookie consent (Google Consent Mode v2)

When [[apps-gdpr-overview]] is active with its "Google Consent Mode" cookie group, the storefront emits **Google Consent Mode v2** signals (all `denied` on load, `granted` once the visitor accepts that group), and the Google tag and its events wait for that group, which counts as "no" until accepted. With the GDPR app active but that group inactive, no consent signals are sent and GA waits for the Performance group, which counts as "yes" until the visitor refuses it. Without the GDPR app GA always fires.

### Crawler and admin-preview traffic is excluded

The storefront tag loader skips crawler requests (so Googlebot's visits don't fire `gtag` events) and admin "View as customer" preview sessions, keeping the merchant's GA stats clean of bot and staff noise. CloudCart's own admin UI uses a separate, CloudCart-managed GA property — the merchant's GA only ever receives storefront events.

### Changing the code requires a JS rebuild before it takes effect

The code lives in the shared storefront apps file every page loads. Saving, installing, uninstalling or activating the app **regenerates** that file; its address carries the build time, so no hard refresh is needed. Google Analytics and [[apps-google-dynamic]] share one storefront script, loaded while either is active.

### Two tabs: Overview + Settings

**Overview** (`/admin/apps/google_analytics`) and **Settings** (`/admin/apps/google_analytics/settings`), as on [[apps-google-tags]] and [[apps-google-dynamic]].

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `google_analytics` | Access gate (install URL) | The install URL `/admin/apps/google_analytics/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-google-analytics-settings]] — settings sub-page.
- [[apps-google-analytics-purchase-event]] — the purchase event: payload, value, consent, why purchases go missing.
- [[apps-google-tags]] — Tag Manager for managing multiple tracking scripts in one place.
- [[apps-google-dynamic]] — dynamic remarketing tags.
- [[apps-google-connect]] — OAuth Connect (some GA features may use it).
- [[apps-google-shopping]] — sister product feed integration.
- [[apps-gdpr-overview]] — cookie consent gates analytics tracking.
- [[apps-tiktok-pixel]] / [[apps-facebook-comments]] — alternative tracking pixels.

## Open questions

(None currently outstanding for this page.)
