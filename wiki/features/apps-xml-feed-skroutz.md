---
type: feature
nav_path: "Apps → XML Feed → Skroutz"
route_name: apps.skroutz.overview
route_path: /admin/apps/xml_feed/skroutz
aliases: ["Skroutz", "Skroutz feed", "Skroutz.gr", "price comparison Greece", "Skroutz size color parameter"]
tags: [apps, exports, xml, feed, price-comparison, greece, skroutz]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# Skroutz (Greek price-comparison feed)

## Purpose

**Skroutz** (skroutz.gr) is Greece's largest **price-comparison** marketplace. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed Skroutz ingests, including Skroutz's required **size / color variation** structure.

## Where to find it

Sidebar → Apps → **XML Feed** → **Skroutz** (`/admin/apps/xml_feed/skroutz`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Skroutz feed.
- Choose which product parameters represent **Size** and **Color** so Skroutz groups variants correctly.
- Set availability labels and an analytics key.
- Copy the public feed URL.

### What the merchant CANNOT do here

- **Map categories to Skroutz categories** — Skroutz has no per-feed mapping tab; the feed sends the store's own category breadcrumb plus the store category id (see Business rules).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Analytics Key** (`analytics`) | Skroutz analytics/tracking key. |
| **Availability in stock** (`availability_in_stock`) | The text Skroutz should show for in-stock products. |
| **Availability out of stock** (`availability`) | The text shown for out-of-stock products. |
| **Color parameters** (`color_parameter`) | Which product parameter is treated as the **color** axis. |
| **Size parameters** (`size_parameter`) | Which product parameter is treated as the **size** axis. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the Skroutz feed includes

Product id, name, link, image + additional image, price with VAT, VAT rate, manufacturer, MPN, EAN, manufacturer SKU, **category** (the store breadcrumb path) and **category_id** (the store category id), availability, quantity, **size** + **color** (from the chosen parameters), weight, and grouped **variations** (variants grouped by color/size with a variation id).

## Business rules

### No per-feed category mapping — sends store breadcrumb + store category id
Skroutz does not use the category-mapping tab. The `category` element is the store category breadcrumb and `category_id` is the store's own category id; there is no Skroutz target-taxonomy mapping. (The per-feed mapping tab exists only for [[apps-xml-feed-glami|Glami]] / [[apps-xml-feed-shopzilla|ShopZilla]].)

### Variants → size / color grouping
Skroutz expects variant products grouped by a size and a color axis. The merchant must point the **Size parameters** and **Color parameters** settings at the right product parameters, or Skroutz can't build the variation block correctly.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.skroutz`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category breadcrumb the feed sends.
- [[products-variants-options]] — the Size / Color parameters Skroutz groups by.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
