---
type: feature
nav_path: "Apps → TikTok Shop → Export & sync (batch job, webhooks)"
route_name: apps.site.tiktok.shop.webhook
route_path: /admin/apps/tiktok_shop/products
aliases: ["TikTok Shop export", "TikTok Shop sync", "TikTok Shop batch upload", "TikTok Shop auto-sync", "TikTok Shop webhook", "TikTok Shop synced products table", "TikTok Shop 500 cap"]
tags: [apps, social, tiktok, products, export, webhooks, background-job, plan-gated]
plan_gates: ["tiktok_shop_export"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-tiktok-shop]]. See the hub for the other aspects (OAuth / connection, product mapping).

# TikTok Shop — export & sync (batch job, auto-sync, webhooks)

## Purpose

This aspect covers **how products actually move to TikTok and stay in sync**: the background batch export job and its 500-product cap, the conditions that silently cancel it mid-run, the create/update/delete modes, automatic re-push when stock or price changes, what the synced-products table records, the inbound webhook receiver, and the fact that orders flow only one way (TikTok keeps its own orders — CloudCart does not import them).

## Where to find it

Sidebar → Apps → TikTok Shop → **Products** tab → *Upload Products* (and *Stop Export* while a job is in flight). Status is polled every 5 seconds. See [[apps-tiktok-shop-products]] for the tab UI; this page documents the engine behind it.

## What the merchant can do here

- **Trigger a bulk export** — *Upload Products* dispatches the batch job (up to 500 active products).
- **Stop an in-flight export** — *Stop Export* cancels the running batch.
- **Enable auto-sync** — turning on the `update_products` setting makes product create/update changes push automatically.
- **Watch status** — the synced-products table shows TikTok ID, product name, SKU, status badge, and Synced At.

What the merchant CANNOT do here:

- Retry a single failed variant from the tab — there is no per-row retry; the merchant re-pushes the product (see Business rules).
- Import TikTok-side orders into CloudCart — orders are not pulled (see order-flow direction).
- Export more than 500 products in one click — the action is repeated for larger catalogs.

## Settings & fields

- `update_products` — auto-sync toggle. When ON, product create/update fires an automatic TikTok push; when OFF, the merchant must push manually.
- `batch_id` — stores the current export batch ID so progress is visible in the status endpoint.
- `@tiktok_shop_products` table — one row per **successfully** uploaded variant: `(variant_id, tiktok_product_id, product_id, status, synced_at)`.
- Webhook route `apps.site.tiktok.shop.webhook` — inbound endpoint for TikTok event callbacks.

## Business rules

### Single background job; create / update / delete modes

One queued background task orchestrates the full product-push flow. Its batch upload supports three modes: `'create'` (default, new listing), `'update'` (refresh an existing listing), and `'delete'` (remove a listing). Each call returns per-item outcomes for granular error tracking. Items are handled **one at a time** (per-product API calls) — unlike [[apps-google-shopping]]'s single bulk request. This is slower for large batches but gives easier per-product error handling. The push is mapped per the rules in [[apps-tiktok-shop-product-mapping]].

### Bulk export caps at 500 products per dispatch

The dispatcher queries up to 500 active products into one export batch. Stores with more than 500 catalog items repeat the action — there is **no UI pagination button**; the merchant just clicks *Upload Products* again after the first batch completes. The batch runs on the export queue and persists its batch ID under the `batch_id` setting so progress shows in the status endpoint.

### Background job auto-cancels on cancelled batch, expired plan, or maintenance

The export job checks for: a cancelled batch, a missing site, an expired plan, the store in maintenance mode, the app not installed, or the app not active. Any one of those returns immediately and stops processing. So pausing a plan or putting the store in maintenance during a push **silently stops the job mid-batch** — surviving items are not retried automatically.

### Auto-sync on product create / update / delete

When the merchant enables `update_products`, CloudCart fires the TikTok push automatically when a product is created, updated, or its variants change. **Deletes always propagate** (no `update_products` gate). Without `update_products` enabled, the merchant must manually trigger pushes from the Products tab.

### Stock and price auto-update — TikTok stays in sync with CloudCart

When a variant's stock or price changes, the integration immediately triggers an `update` upload, so TikTok Shop reflects the change without merchant intervention. This rides on CloudCart's per-variant stock model — see [[inventory-tracking]] for when stock actually changes.

### Synced-products table stores only successful uploads, indexed by variant_id

The `@tiktok_shop_products` table stores one row per successfully-uploaded variant, with `tiktok_product_id`, `product_id`, `status='uploaded'`, and `synced_at`. **Failures do NOT create a row** — they only increment a failure counter (`errors`) in the per-batch export progress. To recover from a failed upload, the merchant re-pushes that product from the Products tab; there is no row to "retry" from. The client null-guard means an expired token makes the whole push "succeed with empty results" rather than fail loudly — see [[apps-tiktok-shop-oauth-connection]].

### Disapproval / rejection — no rejection-reason capture from the push side

The integration tracks per-batch responses and logs failures to system logs. There is no per-product disapproval-reason surface in the synced-products table from the push itself — only `status='uploaded'` on success. Rejection details must be inspected in TikTok Seller Center (but see the webhook below, which can flip the status).

### Webhook receiver handles 3 event types — order status, product status, return status

The integration exposes `apps.site.tiktok.shop.webhook` for inbound TikTok webhooks. It validates the HMAC-SHA256 signature against the merchant's `app_secret` using the request body, then routes by event type: **type 1** = order status change (logged only), **type 2** = product status change (updates the `status` column of the synced-products row matching `tiktok_product_id`), **type 3** = return / refund status change (logged only). Unknown types are logged as warnings. **All responses return `code: 0`** even on failure, to prevent TikTok from retrying.

### Webhook product-status update — TikTok-driven status reaches the synced-products table

Per the type-2 handling: when TikTok changes a product's status on their side (listing approved → live, or product violated policy → rejected), it pushes the change to CloudCart's webhook endpoint and CloudCart updates the `status` column on the matching synced-products row. So unlike the original push (which records only `uploaded`), webhooks DO surface TikTok-side approval/rejection back into the table — but only if TikTok actually fires the webhook.

### Order-flow direction — TikTok → CloudCart is NOT supported

The integration is **product-export-only** — there is no inbound order-pull. Orders placed on TikTok Shop stay on TikTok; CloudCart does not import them into the [[orders]] list. Stock decrement on TikTok-side sales is handled by TikTok internally, not reflected back into CloudCart inventory.

## Related

- [[apps-tiktok-shop]] — hub.
- [[apps-tiktok-shop-products]] — the Products tab that triggers and displays the export.
- [[apps-tiktok-shop-oauth-connection]] — why an expired token makes a push silently no-op.
- [[apps-tiktok-shop-product-mapping]] — the field transform applied to each pushed item.
- [[inventory-tracking]] — when stock changes (driving auto re-push).
- [[settings-hooks]] — webhook concept (signature validation, idempotency).
- [[orders]] — order list that TikTok orders do NOT enter.
- [[apps-google-shopping]] — contrast: single bulk request vs per-product calls.

## Open questions

None.
