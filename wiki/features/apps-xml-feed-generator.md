---
type: feature
nav_path: "Apps → XML Feed Generator"
route_name: apps.xml_feed_generator.overview
route_path: /admin/xml-feed-generator/overview
aliases: ["XML Feed Generator", "Xml Feed Generator", "Outbound product feed", "Generic product XML feed", "Custom partner feed", "no enable disable button", "app has no active toggle"]
tags: [apps, exports, xml, feed, plan-gated]
plan_gates: ["xml_feed_generators", "xml_feed_generator_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# XML Feed Generator (outbound product feeds)

## Purpose

**XML Feed Generator** publishes the store's product catalogue as one or more **outbound XML feeds**, each served at its own public URL for an external consumer — a marketplace, a partner / affiliate network, a price-comparison site, or an internal warehouse / accounting system — to pull on its own schedule.

The feed uses CloudCart's **own fixed XML format**; the merchant does **not** design the XML structure. What the merchant controls per feed is *which* products go in (filters), an optional price markup, UTM tags on the product links, optional access protection, and a few display toggles. For a consumer that needs a SPECIFIC pre-built structure (Google Shopping, Facebook, Skroutz, Glami, …) use [[apps-xml-feed]] instead.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.

## Where to find it

Sidebar → **Apps** → install → **XML Feed Generator**. Two tabs:

- **Overview** (`/admin/xml-feed-generator/overview`) — install / app status.
- **Features** ([[apps-xml-feed-generator-features]]) — plan quota + usage.

The feed definitions are created and edited inside the app.

## What the merchant can do here

- Create **multiple** feed definitions — one per consumer.
- Choose which products each feed includes (all, or by category / vendor / tag / smart collection / specific products).
- Apply a price markup or markdown to the feed prices.
- Append `utm_source` / `utm_medium` / `utm_campaign` to the product links in the feed.
- Toggle whether the feed shows stock numbers, discounted price, hidden products, and out-of-stock products.
- Optionally password-protect the feed URL.
- Copy each feed's public URL to hand to the consumer.

### What the merchant CANNOT do here

- Design or hand-edit the XML structure — the format is fixed (CloudCart-native). For a consumer-specific layout use [[apps-xml-feed]].
- Map products to a custom schema / custom fields, or switch a feed's currency or language.
- Exceed the plan caps on number of feeds (`xml_feed_generators`) or products per feed (`xml_feed_generator_products`).

## Settings & fields

Per feed definition:

| Field | What it controls |
|---|---|
| `name` | Feed label (required, max 191). |
| `url_handle` | Slug in the public URL `/app/feed/{url_handle}`. |
| `filter` + `filter_value` | Which products: `all`, or `category` / `vendor` / `tag` / `selection` / `product`. A value is required for every filter except `all` (*"Filter value is required"*). |
| `manipulate_price` + `price_type` + `price_value` | Optional markup: `percent` (capped ±100) or `flat` (capped ±100000), applied to each feed price. |
| `utm_source` / `utm_medium` / `utm_campaign` | UTM params appended to product links in the feed. |
| `display_quantity` | Show numeric stock vs status-only. |
| `display_discounted_price` | Include the discounted price. |
| `display_hidden_products` | Include hidden products. |
| `all_products` | Include out-of-stock products (vs in-stock only). |
| `password_protect` + `username` + `password` | Optional access protection on the feed URL — see Business rules. |
| `stores` | Per-store product filter (when the multi-store app is installed). |

## Business rules

### Fixed CloudCart XML format

Every feed uses the platform's single built-in XML format — no template picker, no visual schema editor, no hand-editing. Products appear as items; a product's variants are **nested** under a `<variants>` group inside the parent item (not as separate top-level items). Image links point at CloudCart's CDN, so consumers crawl images directly.

### Public feed URL + optional access protection

Each feed is served at the public URL `/app/feed/{url_handle}` and is reachable by anyone with the link. When `password_protect` is on, the consumer must pass the credentials as URL query parameters (`?username=…&password=…`); wrong or missing credentials return **HTTP 401 — *"Access denied. Contact your key account!"***. This is lightweight URL-level protection, not standard HTTP Basic Auth. Appending `?action=download` to the URL forces a file download instead of an inline view.

### Background regeneration (~6 h)

Feeds rebuild in the background, so the merchant never waits. A change-scan runs about **every 6 hours** and regenerates a feed only when the catalogue actually changed — so a feed refreshes at most every ~6 hours. There is no incremental "changed since" parameter: a consumer always fetches the full feed and diffs on its own side. Track in-progress regenerations on [[settings-queue-view]].

### Plan gates

Two separate plan-feature limits apply: `xml_feed_generators` caps how many feed definitions the merchant can create, and `xml_feed_generator_products` caps how many products each feed may include. Hitting either opens a plan-upgrade prompt. See [[apps-xml-feed-generator-features]] for current usage.

### Uninstall deletes all feeds

Uninstalling the app deletes every feed definition and stops the background regeneration; the public feed URLs stop responding.

## Related

- [[apps]] — App Store.
- [[apps-xml-feed-generator-features]] — plan quota + usage screen.
- [[apps-xml-feed]] — predefined marketplace feeds (Google Shopping, Facebook, Skroutz, …) — use when the consumer needs a specific structure.
- [[apps-xml-sync]] — inbound counterpart (you publish a feed; sync consumes one).
- [[apps-google-shopping]] — Google-specific feed alternative.
- [[products-products]] — the product catalogue the feed draws from.
- [[settings-queue-view]] — watch in-progress feed regenerations.
- [[background-queue-inventory]] — background-process catalogue.
- [[plan-gates]] — plan-feature gating model.

## Open questions

- Whether the merchant is warned before uninstall deletes all feed definitions (verify).
