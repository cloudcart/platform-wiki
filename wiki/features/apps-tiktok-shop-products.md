---
type: feature
nav_path: "Apps → TikTok Shop → Products"
route_name: apps.tiktok_shop.products
route_path: /admin/apps/tiktok_shop/products
aliases: ["TikTok Shop Products", "TTS products", "TikTok product list"]
tags: [apps, social, tiktok, products, sync-status]
plan_gates: ["tiktok_shop_export"]
created: 2026-05-21
updated: 2026-05-28
source_count: 2
---
# TikTok Shop → Products

## Purpose

The **Products** tab is where the merchant manages which **CloudCart products are published to TikTok Shop** and tracks their per-product sync status. Architecturally similar to [[apps-google-shopping-products]] — list with sync status, retry actions, validation indicators.

For the full TikTok Shop feature set, see [[apps-tiktok-shop]].

## Where to find it

Sidebar → Apps → TikTok Shop → **Products tab**. Route: `/admin/apps/tiktok_shop/products`.

## What the merchant can do here

### Synced Products header

Top-row controls:
- **Upload Products** primary button — triggers a single bulk export job. Disabled while a job is in flight (spinner).
- **Stop Export** outline-danger button — appears ONLY while an export is running. Cancels the in-flight batch.

There is **no Add Product picker, no filter, no search, no per-row actions** on this tab — it's a status-display table only. The merchant either clicks one Upload button (which exports every eligible active product up to 500) or clicks Stop.

### Products data table (display only — no inline actions)

When the synced-products table has rows, a `b-table` shows the exported variants:

| Column | Source |
|---|---|
| **TikTok ID** (`tiktok_product_id`) | TikTok-side product identifier returned after upload. |
| **Product** (`product.name`) | CloudCart product name from the joined `Product` record. |
| **SKU** (`variant.sku`) | The CloudCart variant SKU pushed to TikTok (defaults to `CC-{variant_id}` if no SKU on the variant). |
| **Status** | `uploaded` (green) / `error` (red) / `pending` (yellow) badge — driven by the webhook-updated status column. |
| **Synced At** | When the row was created (local-time formatted client-side). |

There are **no inline buttons** — no per-row Re-sync, no per-row Remove, no per-row View on TikTok. The merchant cannot retry a single failed variant from this tab; the only retry path is to click Upload Products again (which re-exports everything).

### Empty state

When no products have been synced yet, the table is replaced with a single text card: *"No products synced yet. Click 'Upload Products' to start."* No empty-state CTA — the merchant uses the Upload Products button in the header.

### Polling progress indicator

After clicking Upload Products, the Vue component sets `uploading = true` (disabling the button + showing the spinner) and starts a **5-second poll** against `/admin/api/tiktok_shop/get-status`. When `working = false` is returned, polling stops and the products table reloads. The merchant sees only the in-flight spinner — no per-product progress count is rendered.

### Stop Export wipes progress

Clicking Stop Export hits `/admin/api/tiktok_shop/stop-export`, which resets `working = false` AND clears the total / complete / errors progress counters. The merchant cannot resume from where they stopped — the next Upload Products restarts at product 1.

### What the merchant CANNOT do here
- Edit product data inline — jump to [[products-products]] to fix.
- Bypass TikTok policy rejections — restricted categories are silently rejected by TikTok (and surface as `error` status on the row).
- Use TikTok Shop without an OAuth-connected account (the Settings tab must show `auth = true` first).
- Filter / search / sort the synced-products list — the table is unfiltered, ordered server-side by `synced_at DESC` only.
- Re-sync a single failed variant — must re-trigger the whole bulk export.

## Settings & fields

### Per-product TikTok state

| Field | Notes |
|---|---|
| **product_id** | CloudCart product. |
| **tiktok_product_id** | TikTok-side product ID after first push. |
| **tiktok_status** | Approved / Pending / Disapproved / Failed. |
| **last_pushed_at** | Most recent push timestamp. |
| **disapproval_reason** | TikTok's rejection reason. |

### Common TikTok rejection reasons
- Restricted category (alcohol, weapons, adult — varies by market).
- Missing required attributes (Brand, GTIN for electronics).
- Image quality issues.
- Price mismatch.
- Title / description policy violation.

## Business rules

### Async batch push (up to 500 per run)

Upload Products dispatches a single background batch that pushes every eligible active product, capped at 500 per run. The merchant can navigate away while it runs; a larger catalog needs the action repeated. The engine — modes, auto-cancel conditions, and the synced-products table — is documented in [[apps-tiktok-shop-export-sync]].

### Plan-gating

`tiktok_shop_export` feature key — without it, push attempts are blocked.

### Per push

Each product is pushed individually and its TikTok response is recorded; the row's Status updates as TikTok processes it. Only successful pushes create a synced-products row; failures are logged. Each variant becomes its own TikTok listing per [[apps-tiktok-shop-product-mapping]].

### Permission
Standard apps permission scope.

## Related

- [[apps-tiktok-shop]] — TikTok Shop hub.
- [[apps-tiktok-shop-settings]] — OAuth + shop config.
- [[apps-tiktok-shop-export-sync]] — the batch job, 500-cap, webhooks, and synced-products table behind this tab.
- [[apps-tiktok-shop-product-mapping]] — how each pushed variant is transformed into a TikTok listing.
- [[apps-tiktok-ads]] — sister app (advertising).
- [[apps-tiktok-pixel]] — sister app (tracking).
- [[products-products]] — source products.

## Open questions
