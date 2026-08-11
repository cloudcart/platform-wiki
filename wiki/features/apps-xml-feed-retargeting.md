---
type: feature
nav_path: "Apps → XML Feed → Retargeting"
route_name: apps.retargeting.overview
route_path: /admin/apps/xml_feed/retargeting
aliases: ["Retargeting", "Retargeting.biz", "Retargeting feed", "behavioural retargeting", "product recommendations feed"]
tags: [apps, exports, json, csv, feed, retargeting, marketing]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics.

# Retargeting (Retargeting.biz feed)

## Purpose

**Retargeting.biz** is a behavioural-retargeting / product-recommendation and email-automation platform. This sub-feed of the [[apps-xml-feed|XML Feed]] app exposes the store's catalogue to Retargeting.biz and connects the store via its two API keys. The product feed ships in **two formats** (a JSON variant and a CSV variant) — both carry the same product data.

## Where to find it

Sidebar → Apps → **XML Feed** → **Retargeting** (`/admin/apps/xml_feed/retargeting`). Standard sub-feed tabs (Overview / Settings / Status); the public feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the Retargeting feed and copy its public URL.
- Enter the **REST API KEY** and **TRACKING API KEY** to connect the store to Retargeting.biz.
- Scope which products are included (shared sub-feed controls).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **REST API KEY** (`rest_api`) | Connects the store's catalogue / data to Retargeting.biz over its REST API. |
| **TRACKING API KEY** (`tracking_api`) | The key for Retargeting.biz's storefront tracking (browsing / cart / purchase events). |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the Retargeting feed includes

Product code, price, **sale_price**, stock, **margin** and **acquisition price** (`acq_price`), brand, **category** / categories (the store category path), and **variations**. (Same fields in the JSON and CSV variants.)

## Business rules

### Two formats, one dataset
Retargeting ships as both a JSON and a CSV feed; they contain the same product fields — pick whichever Retargeting.biz asks for.

### Margin / acquisition price are exposed
Unusually, the feed includes the product's **margin** and **acquisition (cost) price** so Retargeting.biz can optimise recommendations by profitability — be aware this commercially-sensitive data leaves the store in the feed.

### No category mapping — sends the store category path
The category value is the store's own category breadcrumb; there is no Retargeting target taxonomy.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.retargeting`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category path the feed sends.
- [[plan-gates]] — per-consumer gating.

## Open questions

- Exact public feed URL(s) for the JSON vs CSV variants (verify).
- Whether `margin` / `acq_price` are always sent or gated by a setting (verify).
