---
type: feature
nav_path: "Apps → Data Layer"
route_name: apps.datalayer.settings
route_path: /admin/apps/datalayer
aliases: ["Datalayer", "Data Layer", "GTM data layer", "Tracking data layer"]
tags: [apps, others, tracking, tag-manager, advanced]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 6
---
# Data Layer

## Purpose

**Data Layer** integration — emits a structured **dataLayer JavaScript object** on every storefront page with rich ecommerce context (page type, products, customer info, cart contents, etc.). Used in conjunction with [[apps-google-tags]] (GTM) and other tag managers — the merchant's tags consume the data layer to fire pixels with full context (Facebook, TikTok, custom partners).

Critical for advanced tracking setups where the standard GTM data layer isn't rich enough.

## Where to find it

Sidebar → Apps → install → **Data Layer**.

## What the merchant can do here

- Enable / configure custom data-layer enrichment.
- (Verify) define custom data-layer variables / events.

### What the merchant CANNOT do here
- Replace GTM — Data Layer is a SOURCE for GTM, not an alternative.

## Settings & fields

Manager exposes:
- `supportUninstall` — whether the app can be uninstalled cleanly.

## Business rules

### Companion to GTM

Data Layer is most useful when paired with [[apps-google-tags]]. Without GTM, the data layer emits but nothing consumes it (browser console only).

### Permission

Standard apps permission scope.

## How it works (verified against backend)

### Standard schema, not user-extensible
The data layer follows a fixed schema of standard ecommerce events emitted by the storefront. The merchant **cannot add custom fields** through the app's own settings — the schema is determined by CloudCart's storefront code.

Storefront page types covered (each emits its own `cc_page_data` shape):
- **Home** (`site.home`).
- **Product view** (`product.view`).
- **Category** (`category.view`).
- **Selection / smart collection**.
- **Vendor / vendors list** (`site.vendor.view`, `site.vendors`).
- **Tag** (`site.tag`).
- **Page** (a CMS page).
- **Blog list / blog article** (`blog.list`, `blog.view`, `blog.article.view`).
- **Contacts**.
- **Cart** (`cart.list`).
- **Checkout** (`checkout`, plus `checkout/login`, `checkout/register`, `checkout/shipping-address`).
- **Checkout return / thank-you** (`checkout.return`).
- **Other** (anything that doesn't match the above).

### Customer / subscriber enrichment
Each page also emits `cc_customer_data` and `cc_subscriber_data`. When the customer is logged in or has a subscriber UUID cookie (from the marketing module), the data layer carries personalisation context — the customer's identifier, plus a UUID + QR code link for the subscriber profile.

### Client-side delivery
The data layer is emitted **client-side** as a script tag on every storefront page. It uses the page-data view (`var cc_page_data = {...}; dataLayer.push({cc_page_data});`) and a dynamic-content endpoint that loads the customer + subscriber data. There is no separate server-to-server data-layer variant; the merchant's tag manager (GTM, etc.) reads `dataLayer` from the browser.

### Crawlers are skipped
For bot / crawler requests, the dynamic data-layer script is not emitted (saves the customer / subscriber lookup work).

### Browser-fingerprint collection
On each storefront page load, the integration also dispatches a `CollectBrowserData` job (cached for one week per user-agent) so the marketing module can analyse the browser / device population visiting the store.

### Two-stage data layer: static `cc_page_data` + dynamic `cc_customer_data` / `cc_subscriber_data`

The data layer is built in TWO stages so it can be cached + personalised at the same time:

**Stage 1 — `cc_page_data`** is emitted inline in the page HTML at render time. It contains the page-type-specific blob (product details, cart totals, order data on `checkout.return`, etc.). This is the same payload regardless of who is viewing — cacheable, search-engine-friendly.

**Stage 2 — `cc_customer_data` + `cc_subscriber_data`** are loaded asynchronously via a dynamic JS endpoint (`/datalayer.js`). This endpoint:
- Reads the logged-in customer (the platform code) OR guest cart customer.
- Reads the subscriber UUID cookie (from the marketing campaigns module).
- Returns customer / subscriber blobs that include identifiers, names, country, group, custom fields, subscriber QR code, etc.
- Is cached per-customer for 5 minutes (`datalayer.customer.{id}`).

This split means the page HTML can be CDN/edge-cached without leaking customer identity; the customer-specific portion is filled in by a second JS request.

### Customer "country" auto-detection via MaxMind

If the customer's profile has no shipping/billing address country, the `cc_customer_data.country` defaults to the country detected from the visitor's IP via MaxMind GeoIP. Useful for personalisation tags that key off country (e.g., showing different ads to BG vs RO visitors before the customer ever logs in).

### Admin sessions are NOT injected into the dynamic data layer (except in dev)

If a CloudCart admin is logged into the storefront (impersonating a customer for preview), the dynamic-content endpoint skips the subscriber data lookup unless running in `inDevelopment` mode. This avoids admin previews polluting marketing analytics with admin-side activity.

### `cc_page_data` also handles checkout sub-routes (`/checkout/login`, `/checkout/register`, `/checkout/shipping-address`)

These routes don't match the `match` block by name but fall into the `default` branch first; then the controller checks `request->is([...])` and substitutes the checkout payload. So the data layer correctly identifies these intermediate checkout pages as `type: checkout` instead of `type: other`.

### `purchase` event fires only ONCE per order

The `getCheckoutData` method on `checkout.return` writes a `js_events` meta value on the order. If the customer reloads the thank-you page later, `js_events` is already set and `js_events: false` is returned in the payload — signalling tag managers / pixels to NOT re-fire the `purchase` event. This prevents duplicate purchase tracking when customers refresh / re-visit the order confirmation URL.

### `cpadm` flag distinguishes admin previews

The `cc_customer_data.cpadm` field is `1` when a logged-in admin is impersonating the storefront, `0` otherwise. Tag managers can read this and conditionally skip events when `cpadm = 1` (i.e., don't pollute analytics with admin previews). This is a separate flag from the cookie-consent / GDPR flags.

### Failure isolation: any single section returning `[]` doesn't break the rest

Every data-formatting branch (`__productView`, `__categoryView`, `__pageCart`, etc.) is wrapped in `try / catch (Throwable)` returning `[]` on error. If a single product / category / order lookup fails (e.g., orphaned reference), the data layer still emits a (partial) `cc_page_data` — it doesn't crash the page render. Exceptions are logged to `DataLayerJs Response` log channel for support diagnostics.

### Where the data layer FAILS to emit useful content

The list of explicitly-mapped routes is fixed. For these routes, `type: other` is emitted with no payload:
- Showcase pages (`site.showcase`) — commented out in the code (intentional, but no data).
- Bundle list pages (`bundles.list.list`, `bundles.list.category`) — also commented out.
- Account pages, login, register (outside checkout flow).
- Any custom route not in the `match` block.

For these merchant pages, GTM tags that depend on rich product data won't get it from `cc_page_data`.

### App has NO settings page

Like [[apps-google-connect]], the Data Layer app's Vue Index uses `:supportConfig="false"` and `:installOnly="true"` — the app is install-only with no settings tab and no configuration fields. There are NO toggles for which events fire, which page types to include, or which fields to enrich. Behaviour is entirely defined by the platform's storefront data-layer view + dynamic-content endpoint; the merchant cannot tune it via UI. Install → events emit; uninstall → events stop. That's the entire merchant-facing control surface.

### Single route, no children

The Vue router exposes ONE route: `apps.datalayer.settings` at `/admin/apps/datalayer`. No child routes — clicking through to "Settings" actually shows the install-only Application wrapper with no editable fields.

## Related

- [[apps]] — App Store.
- [[apps-google-tags]] — primary consumer of the data layer.
- [[apps-google-analytics]] — uses similar event data.
- [[apps-tiktok-pixel]] / [[apps-facebook-comments]] — alternative pixel consumers.

## Open questions

_None — all questions answered above._
