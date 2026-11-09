---
type: feature
nav_path: "Apps → XML Feed → Google AdWords"
route_name: apps.google_adwords.overview
route_path: /admin/apps/xml_feed/google_adwords, /admin/apps/xml_feed/google_adwords/status, /admin/apps/xml_feed/google_adwords/settings, /admin/apps/xml_feed/google_adwords/mapping, /admin/apps/xml_feed/google_adwords/frame
aliases: ["Google AdWords", "Google Ads feed", "Google Ads dynamic remarketing", "google-adwords.csv", "dynamic remarketing feed"]
tags: [apps, exports, csv, feed, google, ads, remarketing]
plan_gates: []
created: 2026-06-11
updated: 2026-11-09
source_count: 2
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. This one is a **CSV** feed.

# Google AdWords (Google Ads dynamic-remarketing feed)

## Purpose

This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the **CSV product feed for Google Ads dynamic remarketing** (the "business data" feed Google Ads reads to show shoppers the exact products they viewed). It is distinct from the Merchant Center [[apps-xml-feed-google|Google]] feed (Shopping) and from the [[apps-google-shopping]] integration.

## Where to find it

Sidebar → Apps → **XML Feed** → **Google AdWords** (`/admin/apps/xml_feed/google_adwords`). Standard sub-feed tabs (Overview / Settings / Status). The CSV is also served at the vanity URL **`/google-adwords.csv`**; copy it into Google Ads → Business data.

## What the merchant can do here

- Start / stop the feed and copy its CSV link on the Status tab — see [[apps-xml-feed-status-tab]]. **Start task** needs a product filter saved on Settings: all products, or a category / vendor / product / tag / selection with at least one value; otherwise it asks to configure the application first.
- Set **UTM parameters** appended to product links for campaign attribution.
- Scope which products are included (shared sub-feed controls).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Source** (`utm_source`) | The `utm_source` appended to each product URL in the feed. |
| **Medium** (`utm_medium`) | The `utm_medium` appended to each product URL. |
| **Campaign** (`utm_campaign`) | The `utm_campaign` appended to each product URL. |

These UTM fields belong to the shared sub-feed settings; Google AdWords has no fields of its own.

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

## Business rules

### UTM tagging for attribution
The UTM source / medium / campaign values are appended to the product links in the feed so Google Ads traffic is attributed correctly in analytics.

### CSV at a vanity URL
Besides the standard feed URL, this feed is reachable at `/google-adwords.csv` for Google Ads' business-data uploader.

### CSV columns
ID, Item title, Final URL, Image URL, Item description, Item Category, Price, Sale Price, Formatted Price, Formatted sale price. How Google Ads accepts and uses the file is Google's own rule set.

### Why a product might be missing
Hidden product, the included-product filter, a plan cap on this sub-feed, a stopped task, or the feed not yet regenerated (every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.google_adwords`) — on lower plans this feed may require an upgrade while another is unlocked. See [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-xml-feed-google]] — the Merchant Center / Shopping feed (different purpose).
- [[apps-google-shopping]] — the full Google Shopping integration.
- [[plan-gates]] — per-consumer gating.

## Open questions

(None currently outstanding for this page.)
