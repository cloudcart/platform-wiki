---
type: feature
nav_path: "Apps → TikTok Dynamic Ads → Catalog feed"
route_name: apps.tiktok.overview
route_path: /xml_feed/tiktok/{page}
aliases: ["TikTok catalog feed", "TikTok product feed", "TikTok Dynamic Showcase feed", "TikTok XML feed", "TikTok Catalog Manager feed"]
tags: [apps, social, tiktok, feed, catalog, dynamic-ads, xmlfeed]
plan_gates: []
created: 2026-06-23
updated: 2026-06-23
source_count: 1
---

> Part of [[apps-tiktok-pixel]] (TikTok Dynamic Ads). See the hub for the Pixel / CAPI tracking half + the settings tab.

# TikTok Dynamic Ads — catalog feed

## Purpose

The catalog-feed half of the [[apps-tiktok-pixel|TikTok Dynamic Ads]] app — a product XML feed that TikTok pulls to build the catalog behind **dynamic / showcase ads**. The merchant pastes the feed URL into TikTok Catalog Manager; CloudCart regenerates it on a schedule. It pairs with the Pixel/CAPI events so TikTok can match catalogue products to conversions.

## Where to find it

The feed is a **public URL**: `/xml_feed/tiktok/{page}` (paginated). The merchant copies it from the app and registers it as a data-feed source in TikTok Catalog Manager. The feed-side settings (UTM, colour/size attribute mapping, product filter) are on [[apps-tiktok-pixel-settings]].

## What the merchant can do here

- Copy the TikTok catalog-feed URL and register it in TikTok Catalog Manager.
- Control which products are included (the product filter), map colour / size variant attributes, and append UTM parameters — all on [[apps-tiktok-pixel-settings]].

### What the merchant CANNOT do here

- Push the catalogue to TikTok directly — it is a **pull** feed (TikTok fetches the URL on its own cadence).
- Change the schema or refresh interval.

## Settings & fields

No fields of its own — see [[apps-tiktok-pixel-settings]] for the feed config (colour / size parameters, UTM, product filter).

## Business rules

- **Pull feed, regenerated every ~2 hours.** A background job rebuilds the feed (TikTok then re-fetches on its own Catalog-Manager cadence); it is served from S3 / CDN and paginated at **10,000 products per page**.
- **RSS 2.0 + Google `g:` schema** (reuses the Facebook / Google feed base), with TikTok-specific fields: `g:item_group_id` (= parent product id — all variants of a product share it), `g:gtin`, `g:mpn`, `g:color`, `g:size`, `g:custom_label_4`.
- **Variant colour / size come from mapped parameters.** The merchant maps which variant parameters represent colour / size (on the settings tab); those feed `g:color` / `g:size`.
- **Shipping weight uses TikTok-valid ASCII units.** The feed emits a numeric weight + `kg` or `lb` (per the store's unit system) — never a localized unit (e.g. Cyrillic "Кг."), which TikTok rejects; weight is omitted when a variant has none.
- **Product type has a fallback.** It uses the full category path (up to 3 levels); when the path is unavailable it falls back to the category name, so every product still carries a category hint.
- **Scope = products that have a price** (simple + variant products).

## Related

- [[apps-tiktok-pixel]] — TikTok Dynamic Ads hub (the Pixel / CAPI half).
- [[apps-tiktok-pixel-settings]] — feed settings (colour / size mapping, UTM, product filter).
- [[apps-xml-feed]] — the generic XML-feed framework this is built on.
- [[apps-facebook-pixel]] — the analogous Facebook Pixel + Catalog bundle.

## Open questions

- None.
