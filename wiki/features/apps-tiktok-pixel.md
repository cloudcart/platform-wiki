---
type: feature
nav_path: "Apps → TikTok Dynamic Ads"
route_name: apps.tiktok.overview
route_path: /admin/apps/tiktok
aliases: ["TikTok Dynamic Ads", "TikTok Pixel", "TikTok tracking pixel", "TikTok conversion tracking", "TikTok catalog feed", "app.xml_feed.tiktok"]
tags: [apps, social, tiktok, tracking, pixel, capi, feed, dynamic-ads, analytics]
plan_gates: []
created: 2026-05-22
updated: 2026-06-23
source_count: 3
---
# TikTok Dynamic Ads (Pixel + CAPI + Catalog feed)

## Purpose

**TikTok Dynamic Ads** is the all-in-one TikTok integration (app key `app.xml_feed.tiktok`) that combines two halves in a single app:

- **Conversion tracking** — the TikTok **Pixel** + server-side **Events API (CAPI)**, firing standard ecommerce events (`ViewContent`, `AddToCart`, `InitiateCheckout`, `CompletePayment`, etc.) from the storefront to TikTok.
- **Product catalog feed** — an XML product feed TikTok pulls for catalog / dynamic-showcase ads — see [[apps-tiktok-catalog-feed]].

It **replaces the former standalone TikTok Pixel app**: existing installs were migrated into this unified app (pixel ID, access token, CAPI toggle, test-event code carried over) and the old `tiktok_pixel` app was retired from the App Store. It is the TikTok equivalent of [[apps-facebook-pixel|Facebook's Pixel + Catalog]] Dynamic Ads bundle. Used by merchants who run TikTok ads ([[apps-tiktok-ads]]) and need conversion measurement, retargeting / lookalike audiences, and a product catalog for dynamic ads.

## Where to find it

Sidebar → Apps → install → **TikTok Dynamic Ads** (route `apps.tiktok.*`). See [[apps-tiktok-pixel-settings]] for the Pixel / CAPI + feed configuration, and [[apps-tiktok-catalog-feed]] for the product catalog feed.

## What the merchant can do here

- Configure TikTok Pixel ID (`pixel-id` format from TikTok Events Manager).
- Activate to inject the pixel snippet on storefront pages.
- (Verify) configure server-side Events API for better attribution.

### What the merchant CANNOT do here
- View pixel analytics inside CloudCart — those are in TikTok Events Manager.
- Use without a TikTok for Business account + Pixel created there.

## Settings & fields

App key: `app.xml_feed.tiktok` (the former `tiktok_pixel` key is retired; existing installs were migrated). Pixel / CAPI fields (pixel code, access token, CAPI toggle, test-event code) plus the feed-side settings (UTM tracking, variant colour/size attributes, product filter) are on [[apps-tiktok-pixel-settings]].

The integration injects TikTok's pixel snippet (head + body initialization) on every storefront page **and** exposes a product catalog feed ([[apps-tiktok-catalog-feed]]).

## Business rules

### Standard ecommerce event taxonomy

The pixel fires the standard event vocabulary at key user actions:
- `ViewContent` (product page view).
- `AddToCart`.
- `Search`.
- `InitiateCheckout`.
- `AddPaymentInfo`.
- `CompletePayment` (purchase).

These map to TikTok's conversion events for Ads optimization.

### Cookie consent integration

When [[apps-gdpr-overview]] is active and the customer rejects marketing cookies, the pixel should NOT fire. Verify the platform's pixel-loader respects consent state.

### Equivalent to Facebook Pixel + Google Analytics

Architecturally same model — embedded JS pixel firing standardised events. Easy mental model carry-over for marketers familiar with FB / GA tracking.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-tiktok-pixel-settings]] — settings sub-page (Pixel/CAPI + feed config).
- [[apps-tiktok-catalog-feed]] — the product catalog feed half of this app.
- [[apps-tiktok-ads]] — paired advertising platform (uses pixel data for conversion optimization).
- [[apps-tiktok-shop]] — sister marketplace app.
- [[apps-google-analytics]] / [[apps-facebook-comments]] — sister tracking pixels.
- [[apps-google-tags]] — alternative path (manage pixel via GTM instead of direct injection).
- [[apps-gdpr-overview]] — cookie consent gating.

## How it works (verified against backend)

### Server-side Events API (CAPI) — free for all

CloudCart supports TikTok's server-side **Events API** in addition to the browser pixel. To turn it on, the merchant: (1) provides an **Access Token** from TikTok Events Manager in [[apps-tiktok-pixel-settings]], and (2) flips the **Enable Events API (Server-Side)** toggle (`capi_status`). When both are set, CloudCart sends conversion events server-side from the storefront's order/checkout actions, which improves post-iOS-14 attribution. **There is no plan-feature gate** — the old `tiktok.capi` gate was removed, so CAPI is available on every plan. If the access token is empty or `capi_status` is off, only the browser pixel fires.

### Cookie consent gates both browser pixel and CAPI

Both the browser pixel and the server-side event firing check whether the visitor has accepted the `targeting` cookie group. If the customer rejects the Targeting / Marketing cookie group, neither path sends data to TikTok. So GDPR/consent compliance is enforced before any event leaves the store.

### Test events route — TikTok Test Event Code field

Per the `test_event_code` setting: the merchant can paste a Test Event Code from TikTok Events Manager. When set, server-side events get tagged with that code so they appear in the TikTok Events Manager "Test Events" panel for debugging. Leave empty for production.

### Standard event vocabulary only — no custom events

Only a fixed set of TikTok standard events is fired — `PageView`, `ViewContent`, `Search`, `AddToCart`, `AddToWishlist`, `InitiateCheckout`, `CompletePayment`, `PlaceAnOrder`. Anything else is ignored. The merchant cannot configure additional custom events (such as "Newsletter signup") from inside this integration — those would need to be wired via [[apps-google-tags]] or custom storefront code.

### Single Pixel ID per store

Per the `pixel_code` setting (singular): the integration accepts one TikTok Pixel ID per store install. There is no multi-pixel UI — if the merchant needs different pixels for different ad accounts, they would have to use Tag Manager ([[apps-google-tags]]) and disable this app.

### Pixel only fires on the storefront, not in admin

The pixel data is exposed only via the storefront JS bundle. The admin panel does not include the pixel — there's no risk of admin previews firing events. The pixel also requires the app to be active AND a non-empty `pixel_code` before being included in the storefront bundle.

### Server-side events hash all PII before sending

When the storefront fires an event and CAPI is enabled, the customer's email, phone, and external identifier are all hashed with SHA-256 before being included in the payload to TikTok. The email is lowercased and trimmed before hashing; the phone number is stripped of everything except digits and `+`. So TikTok receives only hashes, not raw email or phone numbers — this is the standard practice for Events API attribution.

### TikTok click-ID cookies captured for attribution — `ttclid` and `_ttp`

When TikTok's ad-click landing redirect sets the `ttclid` cookie (TikTok Click ID) or the JS pixel sets the `_ttp` cookie (TikTok browser ID), CloudCart reads those cookies directly from the browser and forwards them with every server-side event. This closes the attribution loop between TikTok-side ad clicks and CloudCart-side conversions. Without these cookies, TikTok can still ingest the event but cannot tie it back to the specific ad-click.

### CAPI requests have a 5-second timeout

Each server-side event POST to TikTok has a hard 5-second timeout (3 seconds connect, 5 seconds total). If TikTok's API does not respond within that window, the event is dropped without affecting the storefront request. Slow CAPI responses do not block checkout or any other storefront page.

### Event payload includes content_id, contents array, currency, value, and search query

For each event, the payload sent to TikTok carries `pixel_code`, the standard event name, an `event_id` (idempotency key), a Carbon-formatted timestamp, the visitor's `ip` + `user_agent`, the current `page.url`, and the user object (hashed email / phone / external_id + ttclid + ttp). Properties include `currency` (defaults to the store currency), `value` (cart / order amount when relevant), `content_type`, a flat `content_id` string (comma-joined when multiple), and a `contents` array per item (`content_id`, `content_type=product`, `content_name`, `quantity`, `price`). The Search event additionally sends `query` from `search_string`.

### CSRF token required on every storefront pixel call

The storefront-to-CloudCart leg (browser → `apps.site.tiktok.pixel`) requires a `_token` (CSRF) in the request body — anonymous requests without a token receive an empty JSON response. So the pixel can only fire from authenticated storefront sessions; embedded iframes or external sites cannot trigger CloudCart's CAPI relay.

### Event name remapping — frontend names normalised to TikTok's standard

The storefront fires events with CloudCart-internal names (e.g. `Purchase`, `FastPurchase`, `InitiateFastCheckout`). The controller maps those to TikTok's standard event vocabulary before sending: `Purchase` and `FastPurchase` both become `CompletePayment`, `InitiateFastCheckout` becomes `InitiateCheckout`, `PageView` becomes `Pageview`. Unknown event names are silently dropped.

## Open questions
