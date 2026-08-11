---
type: feature
nav_path: "Apps → XML Feed → CloudCart"
route_name: apps.cloudcart.overview
route_path: /admin/apps/xml_feed/cloudcart
aliases: ["CloudCart feed", "CloudCart native XML", "CloudCart full catalogue export", "native product feed"]
tags: [apps, exports, xml, feed, native, cloudcart]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# CloudCart (native XML feed)

## Purpose

This sub-feed of the [[apps-xml-feed|XML Feed]] app generates CloudCart's **own native XML format** — the **most complete** of all the predefined feeds. It exposes far more of the product record than a price-comparison feed (options, properties, meta fields, units, minimum order, etc.), which makes it useful for **migrating to another CloudCart store**, feeding a generic / custom consumer, or as a full-catalogue export. For a fully bespoke field layout, use [[apps-xml-feed-generator]] instead.

## Where to find it

Sidebar → Apps → **XML Feed** → **CloudCart** (`/admin/apps/xml_feed/cloudcart`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the native feed and copy its public URL.
- Scope which products are included (shared sub-feed controls).

## Settings & fields

The native feed exposes **no consumer-specific settings** — only the shared sub-feed controls:

- **Product filter** — category / vendor / product / tag / selection / all.
- **In-stock only** vs all products.
- **Include / exclude hidden products.**

(Common to every XML-Feed consumer — see [[apps-xml-feed]].)

### What the CloudCart feed includes

The fullest field set of any feed: id, title / name, SKU, barcode, model(s), price + original price + discounted price, quantity, weight, manufacturer / brand, **category** (store path), category properties, variant **options + values**, meta title / meta description, short description, tags, unit / unit step / unit text, minimum order, shop, and product code.

## Business rules

### Most complete export
Because it mirrors the native product record, this feed is the right choice when the **receiving system is another CloudCart store** or a tool that can consume rich product data — not when a marketplace expects its own narrow schema (use that marketplace's dedicated sub-feed).

### Category is the store path
The `category` element is the store's own category breadcrumb; there is no external taxonomy mapping.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.cloudcart`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-xml-feed-generator]] — build a fully custom feed layout instead.
- [[products-categories]] — the category path the feed sends.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
- Whether this feed is intended/supported as a store-to-store migration source (verify).
