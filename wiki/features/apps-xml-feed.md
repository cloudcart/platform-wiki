---
type: feature
nav_path: "Apps → XML Feed"
route_name: apps.{consumer}.overview / apps.{consumer}.settings / apps.{consumer}.status / apps.{consumer}.mapping (per-consumer routes — {consumer} = facebook, google, skroutz, glami, pazaruvaj, etc.)
route_path: /admin/apps/xml_feed/{consumer} (e.g. /admin/apps/xml_feed/facebook, /admin/apps/xml_feed/google/settings)
aliases: ["XML Feed", "Predefined feed exports", "Price comparison feeds", "Pricerunner feed"]
tags: [apps, exports, xml, feed, marketplace, price-comparison]
plan_gates: []
created: 2026-05-22
updated: 2026-06-24
source_count: 2
---
# XML Feed (predefined marketplace feeds)

## Purpose

**XML Feed** integration — generates **pre-built XML feeds** for major price-comparison sites and marketplaces. Unlike [[apps-xml-feed-generator]] (where the merchant designs custom XML), this app ships ready-made feed formats for the most-common consumers in the merchant's market.

Each pre-built sub-feed targets a specific marketplace's required XML structure. The merchant just activates the relevant ones; the platform generates the feed at a known URL.

## Pre-built sub-feeds

The platform ships **21 predefined consumers** (14 XML, 2 JSON, 5 CSV). Each has the app key `app.xml_feed.<consumer_name>`.

- **XML (14)**: Google (Merchant Center / Shopping), FaceBook (product catalog for Dynamic Ads), Skroutz (Greece), Glami (fashion — BG/CZ/RO/HU/SK), [[apps-xml-feed-pazaruvaj|Pazaruvaj]] (Bulgaria), Arukereso (Hungary), Compari (compari.hu), ShopMania (Romania), ShopZilla (international), Sravni (Russia), Criteo (dynamic ads), Emag (marketplace), ChannelSight, Trendo (fashion), CloudCart (native format).
- **JSON (2)**: Retargeting (behavioural retargeting), Hotdeals (hotdeals.bg).
- **CSV (5)**: GoogleAdWords (Google Ads dynamic remarketing — also at the vanity URL `/google-adwords.csv`), AdScout, CommerceConnector, ProfitShare (Romania affiliate network), Retargeting (CSV variant, separate from the JSON one).

## Where to find it

Sidebar → Apps → install → **XML Feed**.

## What the merchant can do here

- Activate / deactivate specific sub-feeds.
- Configure per-sub-feed settings (currency, category mapping, included product filter).
- Copy the public feed URL to provide to the consumer (Google Merchant Center, Skroutz dashboard, etc.).

### What the merchant CANNOT do here
- Modify the XML structure of pre-built feeds — they're designed to match the consumer's required schema exactly. For custom XML, use [[apps-xml-feed-generator]].
- Combine multiple consumers in one feed (one feed per consumer).

## Settings & fields

Each sub-feed has its own settings page; activation toggles per sub-feed; no global settings — every consumer is independent. Per-consumer controls:

- **Product filter** — `filter` (`category`, `vendor`, `product`, `tag`, `selection`, or `all`) plus `filter_value`. Scopes the feed to a subset of products.
- **`stock`** — `in_stock` (only in-stock products) vs all.
- **`hidden_products`** — include / exclude hidden products.
- **Category mapping** — appears **only for consumers that publish a target taxonomy** (Google product category, Glami, ShopZilla, etc.): a per-row mapping UI — left column = internal CloudCart category path, right column = the consumer's external category. Add / Edit / Delete per row; explicit per-category only (no pattern matching); the mapped-row count is returned as `total_mapped`. **Consumers WITHOUT a target taxonomy (Pazaruvaj, Compari, Arukereso, Sravni, ShopMania, …) have no mapping step — their feed sends the product's own store category *path* as a breadcrumb string, and nothing is excluded for being "unmapped."** Do not send a merchant to a category-mapping screen for those feeds — see e.g. [[apps-xml-feed-pazaruvaj]].
- **Consumer-specific toggles** — each template declares its own fields the merchant fills in (e.g., Google AdWords exposes `username`, `utm_source`).

**Currency and language are NOT separate config knobs** — the feed uses the site's primary currency + locale. To publish in multiple currencies/languages, use separate sites (see [[apps-multilang]]). Free-form custom XML attributes are not supported here — use [[apps-xml-feed-generator]] for that.

## Business rules

### Each sub-feed is independent

Activating Skroutz doesn't activate Glami. Each sub-feed has its own settings + activation state. The merchant picks which markets to target based on where they sell.

### Consumer-specific schema compliance

Each sub-feed is engineered to match the consumer's EXACT XML requirements:
- Google AdWords → Google Merchant Center format.
- Facebook Pixel → Facebook Catalog format.
- Skroutz → Skroutz's required tags.
- (etc.)

Schema changes upstream (Google updates its required attributes) → the platform updates the sub-feed accordingly.

### Public feed URL per sub-feed

Each active sub-feed exposes a unique URL the merchant pastes into the consumer's portal (Google Merchant Center "Pull from this URL", Facebook Catalog Feed URL, etc.). The public endpoint is `/{type}_feed/{xml_feed}/{page?}` where `type ∈ {xml, json, csv}`.

**The feed URL is PUBLIC** — no token query parameter, no Basic Auth, no IP allow-list. Anyone with the URL can fetch the feed, so the merchant should share it only with the intended consumer. The vanity URL `/google-adwords.csv` is likewise unauthenticated.

### Refresh cadence (fixed per consumer)

Each consumer regenerates on a fixed interval the merchant cannot override:
- **Facebook + Google**: every **2 hours** (`7200s`) — the most aggressive cadences.
- **All other consumers** (CloudCart, Pazaruvaj, Sravni, ShopMania, ShopZilla, Compari, Arukereso, Google AdWords, Trendo, Criteo, ChannelSight, Emag, Retargeting, ProfitShare, CommerceConnector, Glami, Skroutz, Hotdeals, AdScout): every **4 hours** (`14400s`).

### Variant representation (template default + the `parameter_type` setting)

How variants appear is driven by the template's default **and** the feed's **`parameter_type`** setting (plus the `variants.listing` plan feature):
- **CloudCart** format: one row per product, with a nested `<variants>` group holding all variants.
- **Google / Facebook / Glami / Skroutz / Pazaruvaj** etc.: normally **one separate `<item>` per variant**, with `item_group_id` binding siblings. When the feed's `parameter_type` is set to **"main" only** (not "variant"), per-variant splitting is turned off and the feed emits **one item per product** (the parent) instead — the same product id then flows consistently into the feed `<id>` and the post-order conversion scripts. Per-variant splitting also requires the `variants.listing` plan feature.

### Per-sub-feed plan-gating

Plan-gating is per consumer, not global: a given sub-feed may require a plan upgrade while another is unlocked on the same plan (e.g., a free-plan merchant might have Pazaruvaj unlocked but Google AdWords requiring an upgrade). The app surfaces a plan-feature meter only when the relevant plan feature applies.

### Permission

Standard apps permission scope.

### Related to apps-google-shopping

[[apps-google-shopping]] is the OAuth-based direct integration with Google Merchant Center (uploads via API). XML Feed's Google AdWords sub-feed is the legacy URL-pull alternative — Merchant Center crawls the URL on a schedule.

The OAuth-based [[apps-google-shopping]] is generally preferred (faster updates, better disapproval feedback) but URL-pull works for merchants who prefer the simpler setup.

## Per-consumer pages

Every predefined consumer has its own page (verified settings, feed output, category handling, plan gating). Drill into the one the merchant asks about:

- **Price comparison:** [[apps-xml-feed-pazaruvaj]] (BG), [[apps-xml-feed-arukereso]] (HU), [[apps-xml-feed-compari]] (HU), [[apps-xml-feed-skroutz]] (GR), [[apps-xml-feed-shopmania]] (RO/intl), [[apps-xml-feed-shopzilla]] (intl), [[apps-xml-feed-sravni]] (RU).
- **Fashion:** [[apps-xml-feed-glami]], [[apps-xml-feed-trendo]].
- **"Where to buy":** [[apps-xml-feed-channelsight]], [[apps-xml-feed-commerceconnector]].
- **Shopping / search / ads:** [[apps-xml-feed-google]] (Merchant Center), [[apps-xml-feed-googleadwords]] (Google Ads remarketing), [[apps-xml-feed-facebook]] (Meta catalog + CAPI), [[apps-xml-feed-criteo]] (dynamic ads).
- **Marketplace:** [[apps-xml-feed-emag]].
- **Retargeting / affiliate / deals:** [[apps-xml-feed-retargeting]], [[apps-xml-feed-profitshare]], [[apps-xml-feed-adscout]], [[apps-xml-feed-hotdeals]].
- **Native:** [[apps-xml-feed-cloudcart]].

**Category handling at a glance:** the per-feed category-mapping tab applies ONLY to [[apps-xml-feed-glami|Glami]] and [[apps-xml-feed-shopzilla|ShopZilla]]; [[apps-xml-feed-google|Google]] / [[apps-xml-feed-facebook|FaceBook]] / [[apps-xml-feed-criteo|Criteo]] read the category's Google taxonomy ([[products-categories-taxonomy]]); every other feed sends the store category **path**.

## Related

- [[apps]] — App Store.
- [[apps-xml-feed-generator]] — custom XML for arbitrary consumers.
- [[apps-google-shopping]] — direct OAuth Merchant Center integration (alternative to Google AdWords sub-feed).
- [[apps-facebook-pixel]] — Facebook Pixel + Conversions API (shares the same app key `app.xml_feed.facebook` and the same Settings page as the Facebook product catalog sub-feed).
- [[apps-facebook-pixel-settings]] — Pixel ID / Access Token / Test Event Code / Enable CAPI settings.
- [[apps-facebook-comments]] — Facebook sister integration.
- [[apps-tiktok-shop]] — TikTok marketplace alternative.
- [[products-products]] — feed source.
- [[products-categories]] — category mapping per sub-feed.

## Open questions

_None._
