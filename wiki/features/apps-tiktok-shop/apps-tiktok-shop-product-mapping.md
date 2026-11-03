---
type: feature
nav_path: "Apps → TikTok Shop → Product mapping (field transforms)"
route_name: apps.tiktok_shop.products
route_path: /admin/apps/tiktok_shop/products
aliases: ["TikTok Shop product mapping", "TikTok Shop field mapping", "TikTok one product per variant", "TikTok Shop SKU", "TikTok Shop barcode type", "TikTok Shop image upload"]
tags: [apps, social, tiktok, products, mapping, plan-gated]
plan_gates: ["tiktok_shop_export"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-tiktok-shop]]. See the hub for the other aspects (OAuth / connection, export & sync).

# TikTok Shop — product mapping (how a CloudCart product becomes a TikTok listing)

## Purpose

This aspect documents the **field-by-field transformation** that turns a CloudCart product into one or more TikTok Shop listings: the one-product-per-variant rule, image handling, text trimming, weight/dimension conversion, barcode-type auto-detection, the seller SKU fallback, and the `external_product_id` that ties listings back to CloudCart for Pixel matching. It explains *what TikTok ends up showing* and *why* certain fields look different from CloudCart.

## Where to find it

The merchant never edits these mappings directly. They are applied automatically when the export runs from the **Products** tab — Sidebar → Apps → TikTok Shop → **Products** → *Upload Products*. See [[apps-tiktok-shop-products]] for the tab itself and [[apps-tiktok-shop-export-sync]] for the export mechanics.

## What the merchant can do here

- **Set product SKUs** so the TikTok-side seller SKU is meaningful rather than a CloudCart internal fallback.
- **Set a main image** — only the main image is published.
- **Set weight + full dimensions** (width / height / depth) so shipping data flows to TikTok.
- **Set a barcode** — its type is auto-detected; the merchant does not pick EAN/UPC/etc. manually.

What the merchant CANNOT do here:

- Choose additional / gallery images — only the main image is sent.
- Override the auto-detected barcode type.
- Map a multi-variant product to a single TikTok listing — each variant becomes its own listing (see Business rules).

## Settings & fields

The transform reads these CloudCart product/variant fields:

- **Variant** → one TikTok product each (title, single SKU sized to that variant, price, stock).
- **`sku`** → TikTok seller SKU; falls back to `CC-{variant_id}` when blank.
- **Main image** → TikTok product image, sent as a URL (hot-linked, not re-uploaded).
- **Description** → HTML-stripped, entity-decoded, whitespace-collapsed, truncated to **5000** chars.
- **Title** → truncated to **255** chars.
- **Weight** → grams → kilograms (3 decimal places).
- **Width / height / depth** → mm → cm (1 decimal). Omitted entirely if any dimension is missing.
- **Barcode** → type auto-detected by digit count (see Business rules).
- **Product ID** → sent as `external_product_id` (string) for Pixel correlation.

## Business rules

### Variant model — one TikTok product per variant

Each active variant of a CloudCart product is formatted as a **separate** TikTok product entry, each with a single SKU sized to that variant. So a CloudCart product with 5 size variants becomes 5 separate TikTok Shop products. This mirrors CloudCart's own per-variant stock model — see [[inventory-variant-model]] for why the Variant (not the Product) is the unit of stock and SKU.

### Image handling — main image only, hot-linked via URL

Only the product's main image is published. Images are sent as URLs, not re-uploaded — TikTok fetches them from CloudCart. No automatic resize / format conversion happens before sending.

### Description trimmed to 5000 chars; title to 255

The description is HTML-stripped, entity-decoded, whitespace-collapsed, and truncated to 5000 characters. The title is truncated to 255 characters. Long rich-text descriptions therefore arrive at TikTok as plain text, possibly cut off.

### Weight + dimensions auto-converted

Weight is converted from CloudCart grams → kilograms (3 decimal places). Width/height/depth are converted from mm → cm (1 decimal). **If any one dimension is missing, dimensions are not sent at all** — TikTok receives no package size for that listing.

### Barcode type auto-detected (EAN / UPC / GTIN / ISBN)

The barcode digits are counted to choose the TikTok barcode type: 14 = GTIN; 13 starting with `978` = ISBN; 13 = EAN; 12 = UPC; 10 starting with `0` = ISBN; everything else defaults to EAN. The merchant does not pick the type manually.

### Seller SKU defaults to `CC-{variant_id}` when the variant has no SKU

If a CloudCart variant has no `sku` set, the integration defaults the seller SKU to `CC-{variant_id}` (literal `CC-` prefix + the internal variant ID). Products without SKUs still get a TikTok-side identifier, but it is CloudCart's internal ID — merchants who want consistent SKU mapping across systems should always set product SKUs.

### `external_product_id` ties TikTok products to CloudCart products for Pixel matching

When pushing a product, CloudCart sets `external_product_id` to the CloudCart product ID (as a string). TikTok uses this to correlate Pixel events (with `content_id = product.id`) to TikTok Shop product listings — so the same product ID flows through both the Pixel and Shop integrations. This is why having the same product IDs across both apps is critical for full-funnel attribution. See [[apps-tiktok-pixel]].

### Content-policy compliance affects what survives mapping

A well-mapped product can still be rejected by TikTok if it falls in a restricted category (weapons, alcohol in some markets, adult content). Rejections do not change the mapping; they surface as a status on the listing — see [[apps-tiktok-shop-export-sync]] for how rejection status reaches the synced-products table via webhook.

## Related

- [[apps-tiktok-shop]] — hub.
- [[apps-tiktok-shop-products]] — the Products tab that triggers the mapping.
- [[products-products]] — where the merchant sets SKU, image, weight, dimensions, barcode.
- [[inventory-variant-model]] — per-variant SKU / stock model that the one-product-per-variant rule mirrors.
- [[apps-tiktok-pixel]] — consumes the same product IDs for attribution.
- [[apps-google-shopping]] — architecturally similar feed mapping.

## Open questions

None.
