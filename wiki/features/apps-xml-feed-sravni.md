---
type: feature
nav_path: "Apps → XML Feed → Sravni"
route_name: apps.sravni.overview
route_path: /admin/apps/xml_feed/sravni
aliases: ["Sravni", "Sravni feed", "Sravni.ru", "price comparison Russia", "Сравни"]
tags: [apps, exports, xml, feed, price-comparison, russia, sravni]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# Sravni (price-comparison feed)

## Purpose

**Sravni** is a Russian **price-comparison** site. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed Sravni ingests.

## Where to find it

Sidebar → Apps → **XML Feed** → **Sravni** (`/admin/apps/xml_feed/sravni`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Sravni feed.
- Scope which products are included (shared sub-feed controls below).
- Copy the public feed URL.

### What the merchant CANNOT do here

- **Map categories to Sravni categories** — no target taxonomy; the feed sends the store's own category path (see Business rules).
- Set feed-specific defaults — Sravni exposes no consumer-specific settings beyond the shared controls; it reads the product data directly.

## Settings & fields

Sravni has **no consumer-specific settings fields** — only the shared sub-feed controls:

- **Product filter** — category / vendor / product / tag / selection / all.
- **In-stock only** vs all products.
- **Include / exclude hidden products.**

(Common to every XML-Feed consumer — see [[apps-xml-feed]].)

### What the Sravni feed includes

Product id, item id, name, site URL, picture URL, **category** (the store category path), description, manufacturer, net price, gross price, gross price incl. carriage (shipping), and stock quantity.

## Business rules

### No category mapping — sends the store category path
The `category` element is the product's own store category breadcrumb; there is no Sravni target taxonomy and no mapping screen. (Category mapping in [[apps-xml-feed]] applies only to consumers with a target taxonomy.)

### Net + gross prices
The Sravni feed emits both a net price and a gross price (and a gross price including carriage), unlike most feeds that emit a single price.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours) — never category mapping. See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.sravni`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category path the feed sends.
- [[apps-xml-feed-generator]] — for a fully custom feed.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
- Whether Sravni's availability/stock element has special thresholds (verify).
