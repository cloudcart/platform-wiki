---
type: feature
nav_path: "Apps → XML Feed → Google"
route_name: apps.google.overview
route_path: /admin/apps/xml_feed/google
aliases: ["Google feed", "Google Merchant Center feed", "Google Shopping XML feed", "g:google_product_category", "Google product feed"]
tags: [apps, exports, xml, feed, google, shopping, merchant-center]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. For the full Google Shopping integration (API submission, product status, attribute diagnostics) see the dedicated app [[apps-google-shopping]].

# Google (Merchant Center / Shopping feed)

## Purpose

This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the **Google Merchant Center / Shopping** product feed (the XML file Google ingests for free + paid Shopping listings). It is the simple feed-file path; the richer **API-based** Google Shopping integration (push submission, per-product status, attribute warnings) lives in [[apps-google-shopping]].

## Where to find it

Sidebar → Apps → **XML Feed** → **Google** (`/admin/apps/xml_feed/google`). Standard sub-feed tabs (Overview / Settings / Status); copy the public feed URL into Google Merchant Center — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Google feed.
- Choose which **identifier** is sent as the product id (Product ID / SKU / barcode).
- Scope which products are included (shared sub-feed controls).
- Copy the public feed URL for Merchant Center.

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Identifier** (`identifier`) | Which value becomes the product identifier in the feed: **Product ID**, **Product SKU**, or **Product barcode**. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the Google feed includes

Title, link, description, the chosen identifier, barcode + SKU, price, image, and the **`g:google_product_category`** element (see below). One `<item>` per variant with an item-group id.

## Business rules

### Category = the category's Google taxonomy (NOT a per-feed mapping tab)
The `g:google_product_category` value comes from each **category's Google Product Taxonomy** (`taxonomy_id`), set on the category itself — see [[products-categories-taxonomy]]. It is **not** the per-feed category-mapping tab used by [[apps-xml-feed-glami|Glami]] / [[apps-xml-feed-shopzilla|ShopZilla]]. Categories with no `taxonomy_id` simply omit the element; for paid Shopping, taxonomize the categories you advertise from.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). For ad-eligibility / rejection diagnostics, use [[apps-google-shopping]]. See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.google`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-google-shopping]] — the full Google Shopping integration (API submission, status, attributes).
- [[products-categories-taxonomy]] — where `g:google_product_category` comes from.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Whether this XML feed and [[apps-google-shopping]] share one activation or are independent (verify).
- Exact public feed URL pattern shown on the Status tab (verify).
