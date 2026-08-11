---
type: feature
nav_path: "Orders → Ordered Products → Export → Sync vs async"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders_products
aliases: ["Ordered Products export async", "Products by orders export chunking", "Aggregated product export threshold", "Order products export ZIP", "Ordered Products export filename"]
tags: [orders, products, export, csv, async, queue, zip]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-ordered-products-export]]. See the hub for related aspects (trigger / 2FA, CSV schema, filter scope, delivery, permissions / plan).

# Ordered Products export — sync vs async

## Purpose

Documents **how the export decides between a direct in-browser download and a queued background job**, the row threshold, the chunk parameters, how the queue assembles the final ZIP, and the resulting filename patterns. The merchant has no control over this — it is driven purely by the pivot's row count.

## Where to find it

There is no UI for this. The path is chosen automatically when the merchant clicks **Export** on [[orders-ordered-products]] (after 2FA — see [[ordered-products-export-trigger-2fa]]). The result delivery differs by path — see [[ordered-products-export-delivery]].

## What the merchant can do here

- Trigger the export and let the platform pick the path.
- Track a large async export's progress on [[settings-queue-view]].

The merchant CANNOT force sync mode for a large pivot, force async for a small one, change the chunk size via URL manipulation, or resume / cancel a running job.

## Settings & fields

### Chunk + limit configuration

| Parameter | Value | What it controls |
|-----------|-------|------------------|
| **limit** | 50 | Threshold below which the export runs synchronously. At or below 50 product rows, CSV returns directly. |
| **chunk** | 1000 | Async chunk size — when going async, each background job processes 1000 product rows. |

The header button on the page sets `chunk=1000` for this export action — different from the orders export, which uses `chunk=500` (see [[orders-export-sync-vs-async]]).

## Business rules

### Async threshold — 50 product rows

Pivots over 50 product rows go async automatically. For very large catalogues (thousands of variants ordered), the export queues with `chunk=1000` per background job, processed in parallel. The merchant gets the bundle by email when complete — see [[ordered-products-export-delivery]].

| Volume | Delivery |
|--------|----------|
| Up to **50 product rows** | Synchronous — CSV downloads directly in the browser. |
| Over **50 product rows** | Asynchronous — split into chunks of **1000** rows per background job, processed in parallel. Email + in-app alert when complete. |

### Async chunk size — capped at 1000 by validation

The platform validates the `chunk` parameter to ensure it is between 1 and 1000. Values above 1000 silently fall back to 50. The header button sends `chunk=1000` (the maximum), so each job processes 1000 product rows. Merchants cannot force larger or smaller chunks.

### Iteration in 250-row inner chunks

Inside each queued chunk job (which receives up to 1000 product rows), the CSV writer further iterates rows in batches of 250 using `chunkById`. This is a memory safeguard for the worker process — it does not load all 1000 rows into memory at once.

### Click-time SQL snapshot

The async path serialises the pivot query at click time and the queue worker reuses that exact query for each chunk. If orders / ordered-product lines change between Export-click and queue completion, the export reflects the **click-time snapshot**, not the current state. Chunks are guaranteed to be internally consistent. The filter parity that makes this snapshot match the page is covered in [[ordered-products-export-filter-scope]].

### ZIP assembly streamed to S3-compatible storage

For large pivots, each chunk CSV is uploaded as a Filemanager file first, then a final step streams all the chunk CSVs into a single ZIP at a server-side temp location, then uploads the assembled ZIP to S3-compatible storage (Hetzner Object Storage) via multipart upload (5 MB parts, retryable). Once the ZIP is stored and the Filemanager row saved, the individual chunk CSV files are deleted automatically.

### Filename pattern

- Synchronous: `orders-products-YYYY-MM-DD-HH-MM-SS.csv` (single file).
- Asynchronous: split into parts — `orders-products-YYYY-MM-DD-HH-MM-part_1.csv`, etc., bundled into a ZIP named `orders-products-YYYY-MM-DD-HH-MM-SS.zip`.

### Runs on the export6 queue

Async jobs run on the `export6` queue — the same queue the orders export uses. See [[background-queue-inventory]] for the catalogue of background processes and how to tell when an export switched to queued.

## Related

- [[orders-ordered-products-export]] — hub.
- [[ordered-products-export-trigger-2fa]] — the click that starts either path.
- [[ordered-products-export-delivery]] — how each path's result reaches the merchant.
- [[ordered-products-export-filter-scope]] — the click-time filter snapshot the async path reuses.
- [[orders-export-sync-vs-async]] — the orders export equivalent (chunk `500` instead of `1000`).
- [[settings-queue-view]] — async job status for large exports.
- [[background-queue-inventory]] — `export6` queue + background-process catalogue.

## Open questions

None.
