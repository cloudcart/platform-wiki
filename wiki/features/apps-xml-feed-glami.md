---
type: feature
nav_path: "Apps → XML Feed → Glami"
route_name: apps.glami.overview
route_path: /admin/apps/xml_feed/glami
aliases: ["Glami", "Glami feed", "Glami.bg", "Glami fashion", "Glami category mapping", "Glami size system", "Glami pixel"]
tags: [apps, exports, xml, feed, fashion, price-comparison, glami]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# Glami (fashion feed — category mapping + size system)

## Purpose

**Glami** is a fashion aggregator / price-comparison site (BG, CZ, RO, HU, SK). This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the product feed Glami ingests. Unlike most feeds, Glami requires **mapping your categories to Glami's category tree** and declaring a **size system**, and it can fire the **Glami Pixel** for conversion tracking.

## Where to find it

Sidebar → Apps → **XML Feed** → **Glami** (`/admin/apps/xml_feed/glami`). Tabs: Overview / Settings / Status, **plus a Category-mapping tab** (Glami has a target taxonomy — see [[apps-xml-feed]] for the mapping UI). The public feed URL is shown on the app.

## What the merchant can do here

- Activate / deactivate the Glami feed.
- **Map store categories to Glami categories** (required — see Business rules).
- Pick the **Size parameter** and the **Size system** Glami should read.
- Set delivery name / price / availability and the **Glami Pixel API key**.
- Copy the public feed URL.

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Size parameter** (`size_parameter`) | Which product parameter holds the size value Glami reads. |
| **Size system** (`size`) | The sizing standard for that parameter — one of EU, UK, US, IT, INT, RU, AGE, CM, MM, ML, LITERS, COLLAR, SOCKS, TROUSERS, EU/INT BRA, UK BRA. |
| **Pixel API key** (`pixel`) | The Glami Pixel key for conversion tracking on the storefront. |
| **Delivery name** (`delivery_id`) | Delivery-method label sent in the feed. |
| **Delivery price** (`delivery_price`) | Default delivery price in the feed. |
| **Availability in stock** (`delivery_time`) | Availability / delivery-time text. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the Glami feed includes

ITEM_ID + ITEMGROUP_ID (variant grouping), product name, URL, main image + alternative images, **CATEGORYTEXT** (the **mapped Glami category**), price with VAT, manufacturer, delivery id / price / date, the size **PARAM_NAME + VAL**, and description.

## Business rules

### Category mapping IS required (target taxonomy)
Glami's `CATEGORYTEXT` element comes from the **per-feed category mapping** (store category → Glami category), not from the store path. Categories you have not mapped to a Glami category produce no/empty Glami category, so map every category you sell from. This is one of the few feeds (with [[apps-xml-feed-shopzilla|ShopZilla]]) that uses the mapping tab — see [[apps-xml-feed]].

### Size system matters
Glami validates sizes against the declared **Size system**; pointing the **Size parameter** at the wrong product parameter, or choosing the wrong system, produces rejected or mis-sized listings.

### Glami Pixel
With a Pixel API key set, the storefront fires the Glami conversion pixel (distinct from the feed itself).

### Why a product might be missing
Unmapped category (empty Glami category), hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.glami`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub (the category-mapping UI lives here).
- [[apps-xml-feed-shopzilla]] — the other feed that uses per-feed category mapping.
- [[products-categories]] — the categories you map to Glami's tree.
- [[products-variants-options]] — the Size parameter Glami reads.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
