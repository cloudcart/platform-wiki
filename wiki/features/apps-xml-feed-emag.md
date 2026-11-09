---
type: feature
nav_path: "Apps → XML Feed → Emag"
route_name: apps.emag.overview
route_path: /admin/apps/xml_feed/emag, /admin/apps/xml_feed/emag/status, /admin/apps/xml_feed/emag/settings, /admin/apps/xml_feed/emag/mapping, /admin/apps/xml_feed/emag/frame
aliases: ["eMAG feed", "Emag XML feed", "eMAG product feed", "eMAG marketplace feed"]
tags: [apps, exports, xml, feed, marketplace, emag]
plan_gates: []
created: 2026-06-11
updated: 2026-11-09
source_count: 2
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. This feed is CloudCart's whole eMAG integration; [[apps-emag-sync]] describes the same feed from the marketplace side.

# Emag (marketplace product feed)

## Purpose

This sub-feed of the [[apps-xml-feed|XML Feed]] app generates a **product feed for the eMAG marketplace**. It is a one-way export (catalogue → feed file at a public address that eMAG reads). It is the only eMAG integration in CloudCart: no app pushes offers, receives eMAG orders or lowers CloudCart stock when eMAG sells ([[apps-emag-sync]]).

## Where to find it

Sidebar → Apps → **XML Feed** → **Emag** (`/admin/apps/xml_feed/emag`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the eMAG feed and copy its public URL.
- Scope which products are included (shared sub-feed controls).

### What the merchant CANNOT do here

- **Map categories to eMAG categories** — the feed sends the store's own category path; matching to eMAG's categories happens on eMAG's side.
- Receive eMAG orders or have eMAG sales lower CloudCart stock — no CloudCart integration does that.

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
This is a feed file only. Orders, offers and category matching are handled in the merchant's eMAG seller account; CloudCart stock does not change when eMAG sells.

### No category mapping — sends the store category path
`category_path` is the product's own store category breadcrumb; there is no per-feed eMAG taxonomy mapping in this consumer.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.emag`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-emag-sync]] — the eMAG marketplace view of this feed: one-way, onboarding, product allowance.
- [[products-categories]] — the category path the feed sends.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
