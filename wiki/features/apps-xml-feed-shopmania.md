---
type: feature
nav_path: "Apps → XML Feed → ShopMania"
route_name: apps.shopmania.overview
route_path: /admin/apps/xml_feed/shopmania
aliases: ["ShopMania", "ShopMania feed", "ShopMania price comparison", "ShopMania Romania"]
tags: [apps, exports, xml, feed, price-comparison, romania, shopmania]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# ShopMania (price-comparison feed)

## Purpose

**ShopMania** is an international (Romania-rooted) **price-comparison** marketplace. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed ShopMania ingests.

## Where to find it

Sidebar → Apps → **XML Feed** → **ShopMania** (`/admin/apps/xml_feed/shopmania`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL to paste into the ShopMania dashboard is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the ShopMania feed.
- Set the feed defaults (barcode, SKU, delivery cost).
- Copy the public feed URL.

### What the merchant CANNOT do here

- **Map categories to ShopMania categories** — no target taxonomy; the feed sends the store's own category path (see Business rules).
- Collect reviews — ShopMania has no reviews/Trusted-Shop flow here (unlike [[apps-xml-feed-pazaruvaj|Pazaruvaj]] / [[apps-xml-feed-compari|Compari]]).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Default Barcode** (`barcode`) | Fallback barcode added to products that have none. |
| **Default SKU** (`sku`) | Fallback SKU added to products that have none. |
| **Delivery cost** (`delivery_cost`) | Default delivery cost added to all products in the feed. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the ShopMania feed includes

Name, product URL, **Category** (the store category path), image, price, currency, manufacturer, description, availability, GTIN, MPN, MPC, and shipping.

## Business rules

### No category mapping — sends the store category path
The `Category` element is the product's own store category breadcrumb; there is no ShopMania target taxonomy and no mapping screen. (Category mapping in [[apps-xml-feed]] applies only to consumers with a target taxonomy.)

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours) — never category mapping. See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.shopmania`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category path the feed sends.
- [[apps-xml-feed-generator]] — for a fully custom feed when no predefined consumer fits.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
