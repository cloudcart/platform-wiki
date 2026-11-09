---
type: feature
nav_path: "Apps → Google Dynamic Remarketing"
route_name: apps.google_dynamic.overview
route_path: /admin/apps/google_dynamic
aliases: ["Google Dynamic", "Google Dynamic Remarketing", "Dynamic Remarketing", "Google Ads Remarketing", "Ремаркетинг"]
tags: [apps, google, ads, remarketing, marketing]
plan_gates: ["google_dynamic"]
created: 2026-05-22
updated: 2026-11-09
source_count: 6
---
# Google Dynamic Remarketing

## Purpose

**Google Dynamic Remarketing** integration — fires Google Ads dynamic remarketing tags on the storefront. When a customer views products, adds to cart, or completes a purchase, the integration sends the product IDs + page categorization to Google Ads. Google then re-targets these visitors with **personalised ads showing the EXACT products they viewed** (instead of generic brand ads).

## Where to find it

Sidebar → Apps → install → **Google Dynamic Remarketing**. See [[apps-google-dynamic-settings]] for configuration.

## What the merchant can do here

- Configure Google Ads conversion ID + label.
- Activate dynamic remarketing event firing on the storefront.
- Validate the integration is configured.

### What the merchant CANNOT do here
- Create remarketing campaigns from this page — those are built in Google Ads (ads.google.com).
- View remarketing audience size from this page — done in Google Ads.
- Use without an active Google Ads account.

## Settings & fields

The Manager exposes:
- the configured check — credential / Ads ID check.

Configuration typically requires:
- **Google Ads Conversion ID** (`AW-XXXXXXXXXX` format).
- **Conversion label** — the label of the purchase conversion (below).

## Business rules

### Pairs with Google Tags

The cleaner pattern: install [[apps-google-tags]] (GTM) and configure the dynamic remarketing tag IN GTM's UI. This integration is the legacy direct-injection alternative for merchants who don't use GTM.

### What the tag sends

The tag is `gtag('config', 'AW-…')` with page views and enhanced conversions allowed, plus these events addressed to the Ads ID. Each item is `{id, google_business_vertical}`: the product's ID and the **type** setting (`retail` or `custom`). No `ecomm_pagetype`, `ecomm_prodid` or `ecomm_totalvalue` parameters are sent.

- `view_item_list` on category, smart collection, brand and tag pages; `view_search_results` on search results.
- `view_item` on a product page, only while **Remarketing event snippet** is on.
- `add_to_cart` for a product or a bundle.
- On the thank-you page and the fast-order panel, once per order: the buyer's e-mail, phone, name and address set as enhanced-conversion data, then `purchase` (value = the order total, currency, transaction ID = the order ID, items), then `conversion` to `AW-ID/Conversion label` with the same value, currency and transaction ID. The label serves only this conversion: it is the part after the slash in a Google Ads `send_to` value. Like the GA4 purchase, it is sent for any return status except `cancel`, with no fallback for buyers who never reach the page; see [[apps-google-analytics-purchase-event]].

### Cookie consent integration

With [[apps-gdpr-overview]] active, the events wait for the Targeting cookie group ("yes" until the visitor answers), or for the Google Consent Mode group ("no" until accepted) when that group is active. The Google tag library itself waits for the Performance group, or the Consent Mode group.

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `google_dynamic` | Access gate (install URL) | The install URL `/admin/apps/google_dynamic/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[apps]] — App Store.
- [[apps-google-dynamic-settings]] — settings sub-page.
- [[apps-google-tags]] — preferred alternative (GTM-managed).
- [[apps-google-analytics]] — measurement sister.
- [[apps-google-shopping]] — feed integration (provides product data for ads).
- [[apps-gdpr-overview]] — consent gating.
- [[apps-facebook-comments]] / [[apps-tiktok-pixel]] — sister remarketing platforms.

## How it works (verified against backend)

### Saved settings (4 fields)

Per the controller's `$only` allowlist, the merchant configures four fields:
- `google_dynamic` — Google Ads Conversion ID. Stored either with or without the `AW-` prefix — the Manager's `getCode` auto-prepends `AW-` if missing.
- `google_variable` — the **Conversion label**, used only for the purchase conversion.
- `type` — **Retail** or **Custom**, sent as `google_business_vertical` with each item.
- `remarketing_event_snippet` — a switch that adds the product-page `view_item` event.

### Validation

Both `google_dynamic` and `google_variable` are required when the app is `active = 1`. Errors:
- *"Please add your Ads tracking ID"* (when `google_dynamic` is empty).
- *"Please add your Ads variable"* (when `google_variable` is empty).

The `google_dynamic` value is also validated by a custom rule: it must match `~(AW-)?([\d]{1,})~` (optional AW- prefix + digits). Bad format → *"The code is not valid"*.

### Auto AW- prefix

The static `getCode` method on the Manager returns the conversion ID — automatically prepending `AW-` if the merchant pasted just the digits. So merchants can paste `123456789` or `AW-123456789` and the platform formats it correctly for the tag.

### Custom audience triggers are not configurable from this page

The Settings page accepts only the four fields above (`google_dynamic`, `google_variable`, `type`, `remarketing_event_snippet`). The merchant cannot, for example, set "only fire the remarketing tag when cart value > 100" from inside CloudCart — that kind of conditional triggering is done either via [[apps-google-tags]] (Google Tag Manager rules on the data layer) or inside Google Ads' audience definitions.

### Consent Mode v2 applies through the same GDPR mechanism

When [[apps-gdpr-overview]] is active with the "Google Consent Mode" cookie group, the storefront emits the all-denied `gtag('consent', 'default', ...)` on load and the `update` granting `ad_storage` / `ad_user_data` / `ad_personalization` once the visitor accepts; the tag shares the same `gtag.js` runtime.

### No installation warning when Google Shopping is missing

The app does not check whether [[apps-google-shopping]] is also installed. Merchants can configure the Dynamic Remarketing tag without a feed — the tag will fire and the audience will build in Google Ads, but the dynamic creative cannot show actual product cards until a Merchant Center feed exists. CloudCart does not surface a banner reminding the merchant about the feed prerequisite.

### Conversion type is "Retail" or "Custom"

The `type` field is a dropdown, **Retail** or **Custom** (default `custom`). Its value is sent as `google_business_vertical` with every item; the product IDs are the same either way. Retail audiences in Google Ads rely on a Merchant Center feed ([[apps-google-shopping]]).

### Dynamic Remarketing rides the SAME storefront loader as Google Analytics

Both the platform code and the platform code are compiled into a single `google_tracking` entry in the shared `cc_applications_config.js` file. The storefront's `google_tracking` loader handles BOTH:
- The `gtag('config', '{GA_code}')` setup for GA.
- The `gtag('config', 'AW-{ads_code}')` setup for Google Ads.
- The combined ecommerce event firing.

Running ONLY Dynamic Remarketing without GA still loads the full gtag runtime (because Google Ads needs `gtag.js`). Running BOTH at once is the most common deployment — the loader handles it.

### Settings save triggers a global JS regenerate

The Google Dynamic manager implements `AppJsRegenerate`. Saving the settings page (or installing/uninstalling/activating) triggers the shared `cc_applications_config.js` file to be rebuilt with the new code. Cached browser sessions see the OLD code until the file URL's `last_build` timestamp updates.

### `remarketing_event_snippet` is a switch — not a free-text snippet

Despite its name, the field is a **switch** (1 / 0), not a paste area. Its only effect is the `view_item` event on product pages; the listing, cart and purchase events go out either way.

### Two tabs: Overview + Settings

The Vue Index uses `ApplicationSettings` with `:tabs="true"` and the router exposes exactly two routes — `apps.google_dynamic.overview` and `apps.google_dynamic.settings`. The Settings tab also includes the read-only **CopyUrl** row that deep-links to the [[apps-google-shopping]] overview page (so the merchant can quickly install the Merchant Center feed required for Retail-mode dynamic creatives).

## Open questions

(None currently outstanding for this page.)
