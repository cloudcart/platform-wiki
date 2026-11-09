---
type: feature
nav_path: "Apps → Google Analytics → Purchase event"
route_name: ""
route_path: ""
aliases: ["GA4 purchase event", "GA4 purchase missing", "purchase event thank-you page", "GA4 revenue lower than orders", "GA4 purchase consent", "GA4 purchase value", "Покупка в Google Analytics", "purchase събитие"]
tags: [apps, google, analytics, purchase, conversion-tracking, thank-you]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[apps-google-analytics]]. See the hub for the other events and the app's settings.

# Google Analytics → purchase event on the thank-you page

## Purpose

How the GA4 `purchase` event leaves the store: what sends it, when it is sent or skipped, what it carries, how `value` is computed, how cookie consent gates it, and why GA4 can show fewer purchases than the store has orders. It also says what the Google Ads app and Google Tag Manager receive on the same page.

## Where to find it

There is no screen of its own. The event is sent by the storefront while [[apps-google-analytics]] is active with a `G-` code, entered under Apps → Google Analytics → Settings, field **Google Analytics code** (`/admin/apps/google_analytics/settings`). No "Online sales → Tracking" screen exists: each tracking ID lives in its own app.

## What the merchant can do here

- Find out why a purchase is missing in GA4, with the checks at the end of this page.
- Compare GA4 revenue with order totals, knowing how `value` is built.

## Settings & fields

None beyond the code and the debug switch on [[apps-google-analytics-settings]].

## Business rules

### What sends it

Every storefront page carries a page-data block that is pushed to `dataLayer` as `cc_page_data`. On the thank-you page it holds the order (type `checkout`). The Google tracking script, loaded on every page while Google Analytics or [[apps-google-dynamic]] is active, reads that block and calls `gtag('event', 'purchase', …)`. The Fast Order success panel ([[apps-fast-order]]) carries the same block, so a fast order is reported too. Crawlers and a logged-in admin viewing the store send nothing.

### Payload

Flat gtag parameters addressed to the GA4 ID: `transaction_id` (the order ID), `value`, `currency`, `shipping`, `tax`, `coupon`, `affiliation` (the store's address) and `items`, each with `item_id`, `item_name`, `item_brand`, `item_category`, `price`, `quantity`, `discount` and `currency`. The storefront never pushes a `{event: 'purchase', ecommerce: {…}}` object, so a GTM tag that reads `ecommerce` finds nothing; see [[apps-google-tags]].

### How `value` is computed

`value` is the sum, over the order lines, of the line's unit price after the line's own discounts times the quantity. Shipping is not in it: it goes separately in `shipping`, and the order's tax lines in `tax`. GA4 revenue is therefore normally below the order total. The Google Ads conversion sent by [[apps-google-dynamic]] uses the order total, shipping included. Whether an order-level discount that the cart does not spread over the lines lowers `value` is not confirmed (verify).

### Once per order, decided on the first render

The first time the page data is built for an order, the order is flagged; every later render carries `js_events: false` and sends no purchase. The flag is set when the page is rendered, not when Google receives the event. If the event did not go out on that first render (consent not given before the visitor left, a blocker, the app inactive), a reload does not send it.

### No payment-status gate

The purchase is sent for every return status except `cancel`: `completed`, `pending` and `requested` alike. A bank-transfer or cash-on-delivery order, and an order whose payment the gateway has not confirmed yet, are reported. A `cancel` return sends the buyer back to checkout, and nothing is sent. Only the retired Universal Analytics mode checked the payment status.

### Cookie consent

- GDPR app off: the purchase is sent.
- GDPR app on, with its **Google Consent Mode** cookie group active: the Google tag and its events wait for that group, which counts as "no" until the visitor accepts it. A visitor who never answers the banner sends no purchase; one who accepts while still on the thank-you page sends it at that moment.
- GDPR app on, that group inactive: Analytics waits for the Performance group, which counts as "yes" until the visitor answers. An unanswered banner sends the purchase; only a refusal stops it.

The Google Ads tag follows the same rule with the Targeting group in place of Performance. See [[apps-gdpr-overview-script-gating]].

### No fallback when the buyer never reaches the page

The classic storefront sends no GA4 purchase from the server. The payment provider's confirmation reaches the store without any analytics event, so there is nothing to deduplicate and nothing that fills the gap. A buyer who pays and closes the tab, or whose return from the payment page fails, is never reported to GA4. This is the usual reason GA4 shows fewer purchases than the store has orders. Server-side reporting exists only for Storefront API clients such as a Nitrogen storefront; see [[headless-analytics-consent]].

### A custom thank-you page

A thank-you page made in Pages is served at the same return address inside the store's layout, so the page data and the purchase go out as on the default page. A page of the landing type is returned as raw content without the store's scripts, so nothing fires on it (verify whether such a page can be set as the thank-you page).

### What else goes out on the same page

- [[apps-google-dynamic]]: a `purchase` to the Ads ID and a `conversion` to the Ads ID with the conversion label, both with the order total.
- [[apps-google-tags]] (GTM): nothing purchase-specific. The container sees the `cc_page_data` push and fires whatever tags the merchant built on it.
- CloudCart's own analytics records the order separately ([[analytics-pipeline]]); that is not a GA4 event.

### When a purchase is missing

1. The app is active and the code starts with `G-`.
2. The consent rule above let it through.
3. The order was not already flagged by an earlier render.
4. The buyer reached the return page or the fast-order panel.
5. The thank-you page is not of the landing type.

## Related

- [[apps-google-analytics]] — hub; the other GA4 events.
- [[apps-google-analytics-settings]] — the code, the API secret and debug mode.
- [[apps-google-dynamic]] — the Google Ads purchase and conversion.
- [[apps-google-tags]] — what a GTM container receives.
- [[checkout-complete]] — the thank-you page itself.
- [[checkout-return-emails-tracking]] — what else the return page does.
- [[apps-gdpr-overview-script-gating]] — consent groups.

## Open questions

- Whether an order-level discount not spread over the lines lowers `value` (verify).
- Whether a landing-type page can be chosen as the thank-you page (verify).
