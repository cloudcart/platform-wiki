---
type: feature
nav_path: "Apps → XML Feed → Arukereso"
route_name: apps.arukereso.overview
route_path: /admin/apps/xml_feed/arukereso
aliases: ["Arukereso", "Árukereső", "Arukereso.hu", "Arukereso feed", "Arukereso reviews", "Arukereso Trusted Shop", "price comparison Hungary"]
tags: [apps, exports, xml, feed, price-comparison, hungary, arukereso]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# Arukereso (Hungarian price-comparison feed + reviews)

## Purpose

**Árukereső** (arukereso.hu) is Hungary's leading **price-comparison** site. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed Árukereső ingests, and — with a **Web Api Key** — adds its **Trusted Shop** post-purchase flow that invites the customer to review the store and the products they bought. The feed and reviews work exactly like the [[apps-xml-feed-pazaruvaj|Pazaruvaj]] and [[apps-xml-feed-compari|Compari]] feeds (same Árukereső-family format).

## Where to find it

Sidebar → Apps → **XML Feed** → **Arukereso** (`/admin/apps/xml_feed/arukereso`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Arukereso feed.
- Set the feed defaults (barcode, SKU, delivery cost, delivery time).
- Enter the **Web Api Key** to enable Árukereső reviews (Trusted Shop).
- Copy the public feed URL.

### What the merchant CANNOT do here

- **Map categories to Árukereső categories** — no target taxonomy; the feed sends the store's own category path (see Business rules).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Web Api Key** (`web_api_key`) | Árukereső-issued key that enables the **Trusted Shop** reviews script. Without it the feed still generates; only review collection is off. |
| **Barcode** (`barcode`) | Fallback barcode added to products that have none. |
| **SKU** (`sku`) | Fallback SKU added to products that have none. |
| **Delivery cost** (`delivery_cost`) | Default delivery cost added to all products in the feed. |
| **Delivery time** (`delivery_time`) | Default delivery time. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the Arukereso feed includes

Product id, product URL, price (uses the discounted price when set), **category** (the store category path), main image + additional images, name, manufacturer, description, delivery cost, delivery time, barcode (the variant's own, else the default), and productid (the variant's SKU, else the default). (Identical output to the Pazaruvaj feed.)

## Business rules

### No category mapping — sends the store category path
The `category` element is the product's own store category breadcrumb; there is no Árukereső target taxonomy and no mapping screen, and products are not dropped for being "unmapped."

### Reviews / Trusted Shop (Web Api Key)
With a Web Api Key set, a post-purchase script sends the buyer's email + purchased products to Árukereső so it can request store and product reviews; the product IDs must match those in the feed.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours) — never category mapping. See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.arukereso`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-xml-feed-pazaruvaj]] / [[apps-xml-feed-compari]] — sibling Árukereső-family feeds (same format + reviews).
- [[products-categories]] — the category path the feed sends.
- [[apps-product-review]] — native CloudCart reviews (distinct from Árukereső's external reviews).
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
