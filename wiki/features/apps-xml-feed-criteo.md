---
type: feature
nav_path: "Apps → XML Feed → Criteo"
route_name: apps.criteo.overview
route_path: /admin/apps/xml_feed/criteo
aliases: ["Criteo", "Criteo feed", "Criteo dynamic ads", "Criteo retargeting feed"]
tags: [apps, exports, xml, feed, ads, retargeting, criteo]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# Criteo (dynamic-ads feed)

## Purpose

**Criteo** is a dynamic-retargeting ad network. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the **product feed Criteo ingests** to power dynamic retargeting ads (showing shoppers the products they viewed).

## Where to find it

Sidebar → Apps → **XML Feed** → **Criteo** (`/admin/apps/xml_feed/criteo`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Criteo feed and copy its public URL.
- Scope which products are included (shared sub-feed controls).

## Settings & fields

The Criteo feed exposes **no consumer-specific settings** — only the shared sub-feed controls:

- **Product filter** — category / vendor / product / tag / selection / all.
- **In-stock only** vs all products.
- **Include / exclude hidden products.**

(Common to every XML-Feed consumer — see [[apps-xml-feed]].)

### What the Criteo feed includes

Title, link, description, price, image, and the **`g:google_product_category`** element.

## Business rules

### Category = the category's Google taxonomy (not a per-feed mapping tab)
Like the [[apps-xml-feed-google|Google]] and [[apps-xml-feed-facebook|FaceBook]] feeds, Criteo reads each **category's Google Product Taxonomy** (`taxonomy_id`, set on the category — see [[products-categories-taxonomy]]); there is no per-feed category-mapping tab.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.criteo`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-xml-feed-google]] / [[apps-xml-feed-facebook]] — the other feeds that use the category's Google taxonomy.
- [[products-categories-taxonomy]] — where `g:google_product_category` comes from.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
- Whether Criteo needs an account/partner id configured elsewhere (verify).
