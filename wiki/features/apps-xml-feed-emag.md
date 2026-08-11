---
type: feature
nav_path: "Apps → XML Feed → Emag"
route_name: apps.emag.overview
route_path: /admin/apps/xml_feed/emag
aliases: ["eMAG feed", "Emag XML feed", "eMAG product feed", "eMAG marketplace feed"]
tags: [apps, exports, xml, feed, marketplace, emag]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. For the full two-way eMAG **marketplace** integration (offers, orders, stock sync) see the dedicated app [[apps-emag-sync]].

# Emag (marketplace product feed)

## Purpose

This sub-feed of the [[apps-xml-feed|XML Feed]] app generates a **product feed for the eMAG marketplace**. It is a one-way export (catalogue → feed file). The full **two-way** eMAG integration — pushing offers, receiving orders, syncing stock — is the separate [[apps-emag-sync]] app; use that when you actually sell on eMAG rather than just publish a feed.

## Where to find it

Sidebar → Apps → **XML Feed** → **Emag** (`/admin/apps/xml_feed/emag`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the eMAG feed and copy its public URL.
- Scope which products are included (shared sub-feed controls).

### What the merchant CANNOT do here

- **Map categories to eMAG categories** — this feed sends the store's own category path; eMAG category mapping (and offer/order sync) is handled by [[apps-emag-sync]], not here.
- Receive orders or sync stock — that is [[apps-emag-sync]], not this feed.

## Settings & fields

The eMAG feed exposes **no consumer-specific settings fields** — only the shared sub-feed controls:

- **Product filter** — category / vendor / product / tag / selection / all.
- **In-stock only** vs all products.
- **Include / exclude hidden products.**

(Common to every XML-Feed consumer — see [[apps-xml-feed]].)

### What the eMAG feed includes

Product id + variant id, name, SKU, barcode, brand, **category_path** (the store category path), price + price without VAT, discounted price (+ without VAT), quantity, weight, **handling time**, URL, and product images.

## Business rules

### Feed vs marketplace sync
This is a feed FILE only. Selling on eMAG (offers, orders, stock, category mapping to eMAG's taxonomy) requires [[apps-emag-sync]] — a different integration. Don't send a merchant here for order/stock issues.

### No category mapping — sends the store category path
`category_path` is the product's own store category breadcrumb; there is no per-feed eMAG taxonomy mapping in this consumer.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.emag`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-emag-sync]] — the full two-way eMAG marketplace integration.
- [[products-categories]] — the category path the feed sends.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
