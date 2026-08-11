---
type: feature
nav_path: "Apps → XML Feed → Hotdeals"
route_name: apps.hotdeals.overview
route_path: /admin/apps/xml_feed/hotdeals
aliases: ["Hotdeals", "Hotdeals.bg", "Hotdeals feed", "deals feed Bulgaria"]
tags: [apps, exports, json, feed, deals, bulgaria, hotdeals]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. This one outputs **JSON**, not XML.

# Hotdeals (deals feed)

## Purpose

**Hotdeals** (hotdeals.bg) is a Bulgarian **deals / discounts** site. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates a **JSON** feed of the store's products with their original vs discounted price, so Hotdeals can list the store's offers.

## Where to find it

Sidebar → Apps → **XML Feed** → **Hotdeals** (`/admin/apps/xml_feed/hotdeals`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Hotdeals feed and copy its public URL.
- Scope which products are included (shared sub-feed controls).

## Settings & fields

The Hotdeals feed exposes **no consumer-specific settings** — only the shared sub-feed controls:

- **Product filter** — category / vendor / product / tag / selection / all.
- **In-stock only** vs all products.
- **Include / exclude hidden products.**

(Common to every XML-Feed consumer — see [[apps-xml-feed]].)

### What the Hotdeals feed includes (JSON)

For each product: id, code, name, URL, image, brand, **category** (the store category path), **old_price**, **new_price**, and **discount** (the deal amount/percentage).

## Business rules

### Built around the discount
Hotdeals is a deals site, so the feed centres on the **old vs new price** and the resulting **discount**. Products without an active price reduction still export, but the deal value is what Hotdeals surfaces.

### JSON, not XML
Unlike most consumers, Hotdeals emits a JSON document; the public URL serves JSON.

### No category mapping — sends the store category path
The `category` value is the store's own category breadcrumb; there is no Hotdeals target taxonomy.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.hotdeals`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category path the feed sends.
- [[marketing-discounts]] — where the price reductions Hotdeals surfaces come from.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL pattern shown on the Status tab (verify).
- Whether Hotdeals only includes products that currently have a discount (verify).
