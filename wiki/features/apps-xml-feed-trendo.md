---
type: feature
nav_path: "Apps → XML Feed → Trendo"
route_name: apps.trendo.overview
route_path: /admin/apps/xml_feed/trendo
aliases: ["Trendo", "Trendo feed", "Trendo fashion feed"]
tags: [apps, exports, xml, feed, fashion, trendo]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# Trendo (fashion feed)

## Purpose

**Trendo** is a fashion-focused marketplace / aggregator. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed Trendo ingests.

## Where to find it

Sidebar → Apps → **XML Feed** → **Trendo** (`/admin/apps/xml_feed/trendo`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Trendo feed.
- Scope which products are included (shared sub-feed controls below).
- Copy the public feed URL.

### What the merchant CANNOT do here

- **Map categories to Trendo categories** — no target taxonomy; the feed derives a Main/Sub category from the store's own category path.
- Set feed-specific defaults — no consumer-specific settings beyond the shared controls.

## Settings & fields

Trendo has **no consumer-specific settings fields** — only the shared sub-feed controls:

- **Product filter** — category / vendor / product / tag / selection / all.
- **In-stock only** vs all products.
- **Include / exclude hidden products.**

(Common to every XML-Feed consumer — see [[apps-xml-feed]].)

### What the Trendo feed includes

Product id, name, SKU, barcode, price, currency code, image(s), **MainCategory** + **SubCategory** (derived from the store category path), manufacturer, description, and quantity.

## Business rules

### Category as Main + Sub (from the store path)
Unlike a single `category` element, the Trendo feed splits the store category path into a **MainCategory** and a **SubCategory**; there is no Trendo target taxonomy and no mapping screen.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.trendo`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category path the feed splits into Main/Sub.
- [[apps-xml-feed-generator]] — for a fully custom feed.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
- How MainCategory vs SubCategory are chosen when the path is deeper than two levels (verify).
