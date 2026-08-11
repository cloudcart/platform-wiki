---
type: feature
nav_path: "Apps → XML Feed → ChannelSight"
route_name: apps.channelsight.overview
route_path: /admin/apps/xml_feed/channelsight
aliases: ["ChannelSight", "ChannelSight feed", "Where to Buy", "buy online channel feed"]
tags: [apps, exports, xml, feed, where-to-buy, channelsight]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# ChannelSight ("where to buy" feed)

## Purpose

**ChannelSight** powers **"Where to Buy" / buy-online** buttons on brand and manufacturer sites — it routes shoppers from a brand page to retailers that stock the product. This sub-feed of the [[apps-xml-feed|XML Feed]] app exposes the store's catalogue so ChannelSight can list the store as a retailer.

## Where to find it

Sidebar → Apps → **XML Feed** → **ChannelSight** (`/admin/apps/xml_feed/channelsight`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the ChannelSight feed.
- Scope which products are included (shared sub-feed controls below).
- Copy the public feed URL to give to ChannelSight.

### What the merchant CANNOT do here

- **Map categories to ChannelSight categories** — no target taxonomy; the feed sends the store's own category path.
- Set feed-specific defaults — no consumer-specific settings beyond the shared controls.

## Settings & fields

ChannelSight has **no consumer-specific settings fields** — only the shared sub-feed controls:

- **Product filter** — category / vendor / product / tag / selection / all.
- **In-stock only** vs all products.
- **Include / exclude hidden products.**

(Common to every XML-Feed consumer — see [[apps-xml-feed]].)

### What the ChannelSight feed includes

Product name, product URL, image URL, **Category** (the store category path), product price, currency code, EAN, SKU, a retailer product code, manufacturer, and availability.

## Business rules

### No category mapping — sends the store category path
The `Category` element is the product's own store category breadcrumb; there is no ChannelSight target taxonomy and no mapping screen.

### Identifiers matter for matching
ChannelSight matches catalogue items to brand pages by identifiers — EAN, SKU, and the retailer product code are all emitted; products without a barcode/SKU may match less reliably (verify the brand-side matching requirements with ChannelSight).

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.channelsight`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category path the feed sends.
- [[apps-xml-feed-generator]] — for a fully custom feed.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
