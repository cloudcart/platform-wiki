---
type: feature
nav_path: "Apps → XML Feed → AdScout"
route_name: apps.adscout.overview
route_path: /admin/apps/xml_feed/adscout
aliases: ["AdScout", "AdScout feed", "AdScout api key domain code"]
tags: [apps, exports, csv, feed, ads, adscout]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. This one is a **CSV** feed.

# AdScout (feed)

## Purpose

**AdScout** is an advertising / product-data platform. This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the **CSV product feed** AdScout ingests and connects the store with an API key + domain code.

## Where to find it

Sidebar → Apps → **XML Feed** → **AdScout** (`/admin/apps/xml_feed/adscout`). Standard sub-feed tabs (Overview / Settings / Status); the public CSV feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the AdScout feed and copy its CSV URL.
- Enter the **API Key** and **domain code** that connect the store to AdScout.
- Scope which products are included (shared sub-feed controls).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **API Key** (`api_key`) | The AdScout API key connecting the store (required). |
| **Domain code** (`domain_code`) | The AdScout domain code for the store (required). |

Both fields are **required** — the app prompts "Enter API Key" / "Enter domain code" if left blank.

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

### What the AdScout feed includes

The product fields plus the **category** as the store category path.

## Business rules

### Requires API key + domain code
Both credentials are mandatory; without them the feed can't be associated with the merchant's AdScout account.

### No category mapping — sends the store category path
The category value is the store's own category breadcrumb; there is no AdScout target taxonomy.

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.adscout`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category path the feed sends.
- [[plan-gates]] — per-consumer gating.

## Open questions

- The exact CSV column set AdScout receives (verify).
- Exact public feed URL pattern shown on the Status tab (verify).
