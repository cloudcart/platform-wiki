---
type: feature
nav_path: "Apps → TikTok Shop"
route_name: apps.tiktok_shop.overview
route_path: /admin/apps/tiktok_shop
aliases: ["TikTok Shop", "TikTok Marketplace", "TikTok products", "TikTok commerce", "no enable disable button", "app has no active toggle"]
tags: [apps, social, tiktok, marketplace, products, plan-gated]
plan_gates: ["tiktok_shop_export"]
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# TikTok Shop (marketplace product export)

## Purpose

**TikTok Shop** integration — publishes the merchant's products to **TikTok Shop**, TikTok's in-app marketplace. When configured, customers can discover + buy the merchant's products directly inside the TikTok app (without leaving). Equivalent to [[apps-google-shopping]] for the TikTok ecosystem.

Used by merchants who:
- Run TikTok influencer / live-stream marketing and want one-tap checkout from videos.
- Target Gen-Z customers who shop in-app rather than via search engines.
- Cross-list catalog to multiple marketplaces (CloudCart storefront + Google Shopping + TikTok Shop).

Plan-gated under the `tiktok_shop_export` feature. Architecturally similar to [[apps-google-shopping]]: OAuth + batch upload + per-product approval cycle — the merchant's mental model carries over.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What governs whether products flow is the **TikTok Shop connection** (connect / disconnect), see [[apps-tiktok-shop-oauth-connection]].

## Where to find it

Sidebar → Apps → install → **TikTok Shop**.

Two UI sub-tabs:

| Sub-tab | Purpose |
|---------|---------|
| Settings ([[apps-tiktok-shop-settings]]) | OAuth connect + configuration. |
| Products ([[apps-tiktok-shop-products]]) | Products + their TikTok sync status. |

## Sub-pages (in this cluster)

The backend mechanics are split into three aspect pages. Drill into the one that matches the question.

- [[apps-tiktok-shop-oauth-connection]] — OAuth connect, the per-shop `shop_cipher`, automatic token refresh (1h before expiry), region inheritance, the silent null-client behaviour, and disconnect.
- [[apps-tiktok-shop-product-mapping]] — how a CloudCart product becomes a TikTok listing: one product per variant, main-image-only URL hot-link, title/description trimming, weight/dimension conversion, barcode-type auto-detection, SKU fallback, `external_product_id`.
- [[apps-tiktok-shop-export-sync]] — the background batch job (500-product cap), auto-cancel conditions, create/update/delete modes, auto-sync on change, stock/price re-push, the synced-products table, the inbound webhook receiver, and one-way order flow.

## What the merchant can do here

- **Connect** via *Sign in with TikTok* on the Settings tab — see [[apps-tiktok-shop-oauth-connection]].
- **Upload Products** — a single button on the Products tab triggers the bulk export job (every active product, up to 500). A **Stop Export** button appears while a job is in flight.
- **Watch sync status** — a read-only table shows TikTok ID, Product name, SKU, Status badge (`uploaded` / `error` / `pending`), and Synced At, polled every 5 seconds.
- **Enable auto-sync** — turning on `update_products` pushes product changes automatically; see [[apps-tiktok-shop-export-sync]].

What the merchant CANNOT do here:

- Retry a single failed variant from the Products tab — there is no per-row action; the merchant re-pushes the product. See [[apps-tiktok-shop-products]].
- Use without a TikTok Shop merchant account, or push products that break TikTok's content policy (restricted categories rejected).
- Use without the `tiktok_shop_export` plan feature.

## Settings & fields

App key: `tiktok_shop`. Plan-feature key: `tiktok_shop_export`.

Top-level settings live on the [[apps-tiktok-shop-settings]] tab; the detailed field tables are on the aspect pages:

- **Connection** (`app_key`, `app_secret`, `shop_cipher`, `shop_name`, tokens) — see [[apps-tiktok-shop-oauth-connection]].
- **Auto-sync** (`update_products`) and export state (`batch_id`, the `@tiktok_shop_products` table) — see [[apps-tiktok-shop-export-sync]].
- **Field transforms** (SKU, image, dimensions, barcode, `external_product_id`) — see [[apps-tiktok-shop-product-mapping]].

## Business rules

- **OAuth is required for every operation.** A missing or expired token makes the API client null, so pushes silently succeed with empty results rather than erroring — see [[apps-tiktok-shop-oauth-connection]].
- **One TikTok listing per variant.** A 5-variant CloudCart product becomes 5 TikTok products, each with its own SKU — see [[apps-tiktok-shop-product-mapping]] (mirrors the per-variant stock model in [[inventory-variant-model]]).
- **Export is a background batch capped at 500 products.** Pausing a plan or entering maintenance mode silently stops a running push mid-batch — see [[apps-tiktok-shop-export-sync]].
- **Sync is mostly one-way.** Products flow CloudCart → TikTok; orders placed on TikTok stay on TikTok and are NOT imported into [[orders]]. Inbound webhooks update product status only — see [[apps-tiktok-shop-export-sync]].
- **TikTok content policy compliance.** TikTok rejects products in restricted categories (weapons, alcohol in some markets, adult content); rejections surface as a per-product status (via webhook).
- **Permission.** Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-tiktok-shop-settings]] — Settings sub-tab (UI).
- [[apps-tiktok-shop-products]] — Products sub-tab (UI) + sync status.
- [[apps-tiktok-pixel]] — sister TikTok app (tracking); shares product IDs for attribution.
- [[apps-tiktok-ads]] — sister TikTok app (advertising).
- [[apps-google-shopping]] — architecturally similar (Google Merchant Center).
- [[products-products]] — products synced.
- [[inventory-tracking]] — stock model that drives auto re-push.
- [[plan-gates]] — plan-gating concept.

## Open questions

None.
