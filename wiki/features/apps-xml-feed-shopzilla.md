---
type: feature
nav_path: "Apps → XML Feed → ShopZilla"
route_name: apps.shopzilla.overview
route_path: /admin/apps/xml_feed/shopzilla
aliases: ["ShopZilla", "ShopZilla feed", "ShopZilla category mapping", "ShopZilla condition", "price comparison"]
tags: [apps, exports, xml, feed, price-comparison, shopzilla]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# ShopZilla (price-comparison feed — category mapping)

## Purpose

**ShopZilla** is an international **price-comparison** network. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed ShopZilla ingests. Like [[apps-xml-feed-glami|Glami]], it requires **mapping your categories to ShopZilla's category tree**, and it sends a product **condition** and **ship weight**.

## Where to find it

Sidebar → Apps → **XML Feed** → **ShopZilla** (`/admin/apps/xml_feed/shopzilla`). Tabs: Overview / Settings / Status, **plus a Category-mapping tab** (ShopZilla has a target taxonomy — see [[apps-xml-feed]]). The public feed URL is shown on the app.

## What the merchant can do here

- Activate / deactivate the ShopZilla feed.
- **Map store categories to ShopZilla categories** (see Business rules).
- Set the default product **condition**, **ship weight**, default barcode / SKU, and delivery cost.
- Copy the public feed URL.

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Condition** (`condition`) | The product condition sent in the feed — one of New, OEM, Open box, Refurbished, Used. |
| **Ship Weight** (`weight`) | Default ship weight applied to products in the feed. |
| **Default Barcode** (`barcode`) | Fallback barcode added to products that have none. |
| **Default SKU** (`sku`) | Fallback SKU added to products that have none. |
| **Delivery cost** (`delivery_cost`) | Default delivery cost added to all products in the feed. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the ShopZilla feed includes

Product id, title, URL, image + additional image, price, original price, brand, **category** (the **mapped ShopZilla category**), condition, availability, barcode, SKU, weight, and delivery cost.

## Business rules

### Category mapping (target taxonomy)
The ShopZilla `category` element comes from the **per-feed category mapping** (store category → ShopZilla category) when set — not the store path. Map every category you sell from. This is one of the two feeds (with [[apps-xml-feed-glami|Glami]]) that uses the mapping tab — see [[apps-xml-feed]].

### Condition + weight
ShopZilla expects a product condition and a ship weight; the defaults here fill those for every product unless the product carries its own.

### Why a product might be missing
Unmapped category, hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.shopzilla`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub (the category-mapping UI lives here).
- [[apps-xml-feed-glami]] — the other feed that uses per-feed category mapping.
- [[products-categories]] — the categories you map to ShopZilla's tree.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
