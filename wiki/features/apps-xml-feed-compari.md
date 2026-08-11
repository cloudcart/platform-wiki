---
type: feature
nav_path: "Apps → XML Feed → Compari"
route_name: apps.compari.overview
route_path: /admin/apps/xml_feed/compari
aliases: ["Compari", "Compari.hu", "Compari feed", "Árukereső Compari", "Compari reviews", "Compari Trusted Shop", "Compari Унгария"]
tags: [apps, exports, xml, feed, price-comparison, hungary, compari]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# Compari (Hungarian price-comparison feed + reviews)

## Purpose

**Compari** (compari.hu) is a Hungarian **price-comparison** site. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed Compari ingests, and — with a **Web Api Key** — adds Compari's **Trusted Shop** post-purchase flow that invites the customer to review the store and the products they bought. It behaves like the [[apps-xml-feed-pazaruvaj|Pazaruvaj]] feed (same Árukereső-family reviews mechanism).

## Where to find it

Sidebar → Apps → **XML Feed** → **Compari** (`/admin/apps/xml_feed/compari`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL to paste into the Compari dashboard is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Compari feed.
- Set the feed defaults (barcode, SKU, delivery cost, delivery time).
- Enter the **Web Api Key** to enable Compari reviews (Trusted Shop).
- Copy the public feed URL.

### What the merchant CANNOT do here

- **Map categories to Compari categories** — Compari has **no target taxonomy**, so there is no category-mapping step; the feed sends the store's own category path (see Business rules).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Web Api Key** (`web_api_key`) | Compari-issued key that enables the **Trusted Shop** reviews script. Without it the feed still generates; only review collection is off. |
| **Barcode** (`barcode`) | A fallback barcode added to products that have none. |
| **SKU** (`sku`) | A fallback SKU added to products that have none. |
| **Delivery cost** (`delivery_cost`) | Default delivery cost added to all products in the feed. |
| **Delivery time** (`delivery_time`) | Default delivery time. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the Compari feed includes

Identifier, product URL, name, manufacturer, price, **category** (the store category path), main image + additional images, description, EAN code, productid, delivery cost, delivery time.

## Business rules

### No category mapping — sends the store category path
The `category` element is the product's own store category breadcrumb (e.g. *"Electronics > Phones > Smartphones"*); there is no Compari target taxonomy and no mapping screen, and products are not dropped for being "unmapped." (Category mapping in [[apps-xml-feed]] applies only to consumers with a target taxonomy — Google, Glami, ShopZilla.)

### Reviews / Trusted Shop (Web Api Key)
With a Web Api Key set, a post-purchase script sends the buyer's email + purchased products to Compari so it can request store and product reviews; the product IDs must match those in the feed.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours) — never category mapping. See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.compari`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-xml-feed-pazaruvaj]] / [[apps-xml-feed-arukereso]] — sibling Árukereső-family feeds with the same reviews mechanism.
- [[products-categories]] — the category path the feed sends.
- [[apps-product-review]] — native CloudCart reviews (distinct from Compari's external reviews).
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
