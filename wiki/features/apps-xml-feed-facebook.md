---
type: feature
nav_path: "Apps → XML Feed → FaceBook"
route_name: apps.facebook.overview
route_path: /admin/apps/xml_feed/facebook
aliases: ["Facebook feed", "Meta catalog feed", "Facebook product catalog", "Facebook Dynamic Ads feed", "Facebook CAPI", "Conversions API", "Instagram Shopping feed"]
tags: [apps, exports, xml, feed, facebook, meta, catalog, capi]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. For the storefront Facebook **Pixel** specifically, see [[apps-facebook-pixel]].

# FaceBook (Meta product-catalog feed + CAPI)

## Purpose

This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the **Facebook / Meta product-catalog** feed used for **Dynamic Ads** and Instagram/Facebook Shopping. It also configures the **Facebook Pixel** and the **Conversions API (CAPI)** server-side tracking for the storefront.

## Where to find it

Sidebar → Apps → **XML Feed** → **FaceBook** (`/admin/apps/xml_feed/facebook`). Standard sub-feed tabs (Overview / Settings / Status); paste the public feed URL into Meta Commerce Manager — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Facebook catalog feed and copy its public URL.
- Set the **Facebook Pixel ID** and enable **Extended ViewContent**.
- Enable the **Conversions API (CAPI)** with an **Access token** (and a test event code).
- Scope which products are included (shared sub-feed controls).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Facebook Pixel ID** (`pixel`) | The Meta Pixel id fired on the storefront. |
| **Enable Extended ViewContent** (`product_group`) | Sends richer ViewContent data for variant/group products. |
| **Enable CAPI** (`capi_status`) | Turns on the **Conversions API** (server-side event delivery). |
| **Access token** (`token`) | Meta access token used for CAPI. |
| **Test event code** (`test_event_code`) | Routes CAPI events to Meta's test-events view for debugging. |

> **CAPI is a paid service** (the app surfaces *"The Facebook Conversions API (CAPI) service is paid"*) — see [[plan-gates]].

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the Facebook feed includes

Title, link, description, price, image, and the **`g:google_product_category`** element (one `<item>` per variant with an item-group id).

## Business rules

### Category = the category's Google taxonomy (not a per-feed mapping tab)
Like the [[apps-xml-feed-google|Google]] feed, the Meta catalog reads each **category's Google Product Taxonomy** (`taxonomy_id`, set on the category — see [[products-categories-taxonomy]]); there is no per-feed category-mapping tab.

### Pixel vs feed vs CAPI
Three distinct things share this screen: the **catalog feed** (product data for ads), the **Pixel** (browser-side events), and **CAPI** (server-side events, paid). See [[apps-facebook-pixel]] for the standalone Pixel app.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.facebook`); CAPI is separately paid — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-facebook-pixel]] — the storefront Facebook Pixel app.
- [[products-categories-taxonomy]] — where `g:google_product_category` comes from.
- [[plan-gates]] — per-consumer gating; CAPI is paid.

## Open questions

- Whether the Pixel set here and [[apps-facebook-pixel]] are the same configuration or independent (verify).
- Exact public feed URL pattern shown on the Status tab (verify).
