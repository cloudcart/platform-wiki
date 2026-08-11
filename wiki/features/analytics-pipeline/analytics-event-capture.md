---
type: feature
nav_path: "Concept → Analytics pipeline → Event capture"
route_name: ""
route_path: ""
aliases: ["Storefront tracker", "CCE tracker", "Analytics event capture", "uuid_generate middleware", "subscriber_uuid middleware", "Analytics ingest"]
tags: [analytics, pipeline, tracker, storefront, data-ingest]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[analytics-pipeline]]. See the hub for the other aspects (event processing, aggregation, dashboard reads, known gaps, backfill commands).

# Analytics — event capture (storefront tracker + UUID identity)

## Purpose

This page covers the **front edge** of the analytics pipeline — how a shopper's browser activity on the storefront becomes a tracked record. Two pieces of machinery live here:

1. The browser-side tracker script that fires a tracking event on each storefront route.
2. The two visitor-identity steps (`uuid_generate` and `subscriber_uuid`) that mint and bind the anonymous-visitor identifier (the `uuid` cookie).

Everything downstream — raw event storage, per-order denormalisation, hourly aggregation, dashboard reads — depends on these capture-side pieces firing correctly. If an ad blocker prevents the tracker from reaching the analytics service, or the `uuid` cookie is never set, the visit silently disappears from **Total Visits**, **Cart Conversion Rate**, and every traffic-source box.

## Where to find it

This is invisible to the merchant — no admin screen. The tracker script is injected automatically into every storefront page by the platform. The `uuid` + `_ccases` cookies are set in the visitor's browser; the merchant never sees these directly. The analytics service runs on a separate hostname (`cca.ccdev.info` by default), independent of the storefront.

## What the merchant can do here

Nothing directly — this is automatic capture. The merchant's actions that pass through this stage:

- Open a storefront page → the tracker fires a tracking event with the route-specific event type.
- Land via a marketing campaign link (`?cc_subscriber.id=...`) → the campaign-binding step links the visitor UUID to the subscriber, enabling attribution in **Sales by Traffic Source**.
- Reach the post-purchase thank-you page → fires the `purchase` event with the order snapshot.

## Settings & fields

Not applicable — capture is automatic. Two ops-side config knobs influence it:

| Setting source | Field | Effect |
|----------------|-------|--------|
| Ops config (not UI) | `URL_CC_ANALYTICS` env var | Default `cca.ccdev.info`; sets the ingest hostname the tracker POSTs to. |
| Ops config (not UI) | Crawler-detection ruleset | Decides whether the tracker script is emitted and whether `uuid_generate` mints a cookie. |

## Business rules

- The tracker is gated by crawler detection. If the platform classifies the request as a bot at page render, no tracker script is emitted and no `uuid` cookie is set — the visit is invisible to the pipeline.
- The UUID-minting step runs **only** on the storefront GET routes listed above. AJAX calls and `site.account*` routes do NOT mint a UUID.
- The `uuid` cookie is **10 years (3650 days)**. A returning visitor stays attributed across sessions unless they clear cookies.
- The call to the analytics service's `/init` endpoint has a **2-second timeout**. If the analytics service is slow, no UUID is minted on that request; the next page-view retries.
- The campaign-binding step binds the subscriber **on success only** — a failed response leaves the UUID unbound.
- The AI listing-engine usage counter that runs on the same storefront routes is NOT analytics — it's a separate counter; don't conflate.

## What gets captured

### The storefront tracker

When a storefront page loads, the platform includes the tracker script and bootstraps a page-level tracker. The tracker points at the analytics service for this store — by default `cca.ccdev.info/{store}` (the hostname is configurable by ops via the `URL_CC_ANALYTICS` setting).

On every page that renders the analytics-events placeholder, the platform emits a tracking call for that page — `product`, `initiatedCheckout`, `purchase`, etc. The event type is decided by the active route:

| Active route | Event type emitted |
|--------------|--------------------|
| `product.view` | `product` (with product id, variant, price, quantity) |
| `category.view` / `ajax.category` | `category` (list view) |
| `site.vendor.view` / `ajax.vendor` | `vendor` |
| `selection` / `ajax.selection` | `collection` |
| `site.tag` / `ajax.tags` | `tag` |
| `products.search` / `ajax.search` | `search` |
| `site.home` | `home` |
| `page` (custom page) | `page` |
| `cart.site` / `cart.list` / `cart.panel` | `cart` |
| `checkout` | `initiatedCheckout` |
| `checkout.return` (post-purchase thank-you) / `apps.fast_order.save_order` | `purchase` |

Routes explicitly NOT initialising the tracker: `site.account`, `site.account.address.shipping.default`, `site.account.address.billing.default`, `datalayer.js`.

### `uuid_generate` — visitor identity

The UUID-minting step runs on GET requests to `/`, `/category/*`, `/selection/*`, `/showcase/*`, `/vendors/*`, `/tag/*`, `/page/*`, and `/product/*`. Behaviour:

- If the visitor doesn't already have a `uuid` cookie, the step calls the analytics service's `/init` endpoint for this store (with a 2-second timeout) to mint a fresh UUID.
- It sets that UUID as a **10-year (3650-day) cookie** alongside `_ccases`.
- The UUID is the **anonymous visitor identifier** used as the primary attribution key for all browser events the analytics service stores.

This step is also gated by the platform's bot detection — if the request is from a crawler, no UUID cookie is set and the storefront tracker does NOT fire (see [[analytics-known-gaps]] for the full bot-filtering layered model).

### `subscriber_uuid` — campaign-click binding

The campaign-binding step runs on the same storefront routes as the UUID-minting step. If the URL carries `?cc_subscriber.id=...` (typically from a marketing-campaign link), the step reads it. On a successful response, it queues a background task that binds the visitor's UUID cookie to that subscriber id in the analytics data store.

This is what makes campaign click-throughs land in **Sales by Traffic Source** correctly attributed — see [[analytics-event-processing]] for how subsequent purchases on that UUID inherit the attribution at order time.

### AI listing-engine counter — NOT analytics

The AI-listing-engine usage counters that run on the home / category / product storefront routes are a **separate usage counter** for the AI-powered listing engine — they are NOT part of the analytics pipeline. They increment an internal usage counter for billing / quota purposes, not for merchant-visible analytics. Easy to confuse with the UUID-minting step because both run on the same routes; they're independent.

## How the capture stage fails (and shows up downstream)

- **Ad blockers / corporate proxies blocking `cca.*`** — the tracking call never reaches the analytics service, so the visit / cart / purchase event is never recorded. The visit silently disappears from **Total Visits** and every event-driven box.
- **Crawler detection false positives** — if the platform's bot detection misclassifies a real visitor, no `uuid` cookie is set and no events fire. The visitor is invisible to the pipeline.
- **2-second UUID-mint timeout** — if the analytics service's `/init` call doesn't respond within 2 seconds, no UUID is minted on that request. The next page-load retries; transient analytics-service outages produce gaps for the visitor's session start, not the whole session.
- **Tracker NOT initialised on `site.account*` routes** — visits to a logged-in customer's account pages produce no events. This is by design (account pages aren't shopping activity), but it means session length can look shorter than the actual visit.

## Related

- [[analytics-pipeline]] — hub.
- [[analytics-event-processing]] — where the captured events get stored + the per-order fast lane that runs in parallel.
- [[analytics-known-gaps]] — bot-filtering layers; ad-blocker blind spots; admin-preview UUID filtering.
- [[apps-google-analytics]] — parallel GA4 push consuming the same storefront events.
- [[subscriber-vs-customer]] — UUID-to-subscriber binding (anonymous → subscriber → customer attribution).
- [[cart-vs-order-lifecycle]] — what gets tracked at each storefront stage.

## Open questions

None.
