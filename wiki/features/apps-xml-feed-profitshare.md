---
type: feature
nav_path: "Apps → XML Feed → ProfitShare"
route_name: apps.profitshare.overview
route_path: /admin/apps/xml_feed/profitshare
aliases: ["ProfitShare", "Profitshare", "ProfitShare feed", "affiliate network Romania", "profitshare.bg", "profitshare tracking"]
tags: [apps, exports, csv, feed, affiliate, romania, profitshare]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

> One of the predefined sub-feeds of [[apps-xml-feed]] (the XML Feed app). See that hub for the shared activation / settings / status / public-URL mechanics. This one is a **CSV** feed plus an affiliate **conversion-tracking** script.

# ProfitShare (affiliate-network feed + tracking)

## Purpose

**ProfitShare** is an affiliate-marketing network (Romania / Bulgaria). This sub-feed of the [[apps-xml-feed|XML Feed]] app generates the **CSV product feed** ProfitShare ingests, and installs ProfitShare's **conversion-tracking** script so affiliate sales are attributed back — with the order data **encrypted** using a key ProfitShare provides.

## Where to find it

Sidebar → Apps → **XML Feed** → **ProfitShare** (`/admin/apps/xml_feed/profitshare`). Standard sub-feed tabs (Overview / Settings / Status); the public CSV feed URL is shown on the app — see [[apps-xml-feed]].

## What the merchant can do here

- Activate / deactivate the ProfitShare feed and copy its public CSV URL.
- Enter the affiliate tracking codes + the encryption key/algorithm.
- Paste the ProfitShare conversion-tracking JavaScript.
- Scope which products are included (shared sub-feed controls).

## Settings & fields

| Field | What it does |
|-------|--------------|
| **Advertiser tracking code** (`advertiser_code`) | The merchant's ProfitShare advertiser id. |
| **Cod Click** (`click_code`) | The ProfitShare click-tracking code. |
| **Encryption algorithm** (`encryption`) | How the conversion data is encrypted — **AES-128-CBC** or **AES-256-ECB**. |
| **Encryption key** (`password`) | The shared secret ProfitShare issues, used to encrypt the conversion payload. |
| **JavaScript** (`script`) | The ProfitShare tracking script. It must match the format `<script type="text/javascript" src="//profitshare.bg/files_shared/tr/****.js"></script>` — an invalid format or URL is rejected on save. |

### Shared sub-feed controls

Product filter (category / vendor / product / tag / selection / all), in-stock-only, include-or-exclude hidden products — common to every XML-Feed consumer ([[apps-xml-feed]]).

## Business rules

### Conversion data is encrypted
ProfitShare attribution relies on the order data being encrypted with the chosen **algorithm** + **key**; a wrong key or algorithm breaks attribution even though the feed itself still generates.

### Tracking-script format is validated
The **JavaScript** field is validated against ProfitShare's expected `//profitshare.bg/files_shared/tr/****.js` script shape; a malformed script or URL is rejected at save with a format error.

### CSV feed
ProfitShare consumes a CSV product file (not XML/JSON).

### Why a product might be missing
Hidden product, the included-product filter, plan gating, or the feed not yet regenerated (~every 4 hours). See [[apps-xml-feed]].

### Plan gating
Per-consumer (app key `app.xml_feed.profitshare`) — see [[plan-gates]].

## Related

- [[apps-xml-feed]] — the XML Feed app hub.
- [[products-categories]] — the category path the feed sends.
- [[plan-gates]] — per-consumer gating.

## Open questions

- The exact CSV column set ProfitShare receives (verify).
- Exact public feed URL pattern shown on the Status tab (verify).
