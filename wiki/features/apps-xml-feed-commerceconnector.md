---
type: feature
nav_path: "Apps → XML Feed → CommerceConnector"
route_name: apps.commerceconnector.overview
route_path: /admin/apps/xml_feed/commerceconnector
aliases: ["CommerceConnector", "Commerce Connector", "CommerceConnector feed", "where to buy CommerceConnector"]
tags: [apps, exports, csv, feed, where-to-buy, commerceconnector]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. This one is a **CSV** feed.

# CommerceConnector ("where to buy" feed)

## Purpose

**CommerceConnector** powers brand-site **"where to buy" / buy-online** buttons (like [[apps-xml-feed-channelsight|ChannelSight]]) — it routes shoppers from a manufacturer's page to retailers that stock the product. This sub-feed of the [[apps-xml-feed|XML Feed]] app exposes the store's catalogue as a **CSV** so CommerceConnector can list the store as a retailer.

## Where to find it

Sidebar → Apps → **XML Feed** → **CommerceConnector** (`/admin/apps/xml_feed/commerceconnector`). Standard sub-feed tabs (Overview / Settings / Status); the public CSV feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the CommerceConnector feed and copy its CSV URL.
- Set the default **delivery time**.
- Scope which products are included (shared sub-feed controls).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Delivery time** (`delivery_time`) | Default delivery time sent for all products in the feed. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the CommerceConnector feed includes

The product fields (id, name, URL, price, image, availability, identifiers) plus the **category** as the store category path. (Exact CSV columns — verify.)

## Business rules

### Identifiers drive retailer matching
Like other "where to buy" feeds, CommerceConnector matches catalogue items by identifiers (barcode / SKU); products without them may match less reliably.

### No category mapping — sends the store category path
The category value is the store's own category breadcrumb; there is no CommerceConnector target taxonomy.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.commerceconnector`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[apps-xml-feed-channelsight]] — the other "where to buy" feed.
- [[products-categories]] — the category path the feed sends.
- [[plan-gates]] — per-consumer gating.

## Open questions

- The exact CSV column set CommerceConnector receives (verify).
- Exact public feed URL pattern shown on the Status tab (verify).
