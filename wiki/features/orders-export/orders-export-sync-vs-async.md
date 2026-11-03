---
type: feature
nav_path: "Orders → Export → Sync vs async"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_orders
aliases: ["Orders export async", "Orders export queue", "Export chunk limit", "50 order threshold", "Export sync threshold"]
tags: [orders, export, async, queue, chunks]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-export]]. See the hub for related aspects (trigger / 2FA, CSV schema, delivery, filter scope, permissions / plan).

# Orders export — synchronous vs asynchronous path

## Purpose

Documents the **50-order threshold** that splits the export into two paths: a synchronous browser download for small scopes, and a queued, chunked, ZIP-bundled async path for large scopes. This is the single most-asked merchant question about "why didn't my CSV download immediately."

## Where to find it

This is a backend behaviour, not a configurable UI. The merchant experiences it through the response to the [[orders-export-trigger-2fa]] modal submit:

- ≤ 50 orders in scope → CSV downloads directly in the browser.
- \> 50 orders in scope → toast *"The export is being processed. You will receive an email with the download link."* — see [[orders-export-delivery]].

## What the merchant can do here

Nothing directly — the threshold is fixed. The only lever the merchant has is the **filter scope**: narrowing the orders list to ≤ 50 rows forces sync mode (instant browser download), while leaving it broad routes through the queue.

## Settings & fields

### Chunk + limit configuration (fixed platform parameters)

| Parameter | Value | What it controls |
|-----------|-------|------------------|
| **limit** | `50` | Threshold below which the export runs synchronously (returns CSV directly). At or below 50 orders, no async queue. |
| **chunk** | `500` | Async chunk size — when going async, each background job processes 500 orders. |

These are fixed parameters for the orders-export action and are NOT exposed to the merchant for tuning.

### Validated parameter range

The platform validates the `chunk` and `limit` parameters submitted with the export request. Values **above 1000** are silently coerced to `50`. The platform-enforced range is **`1`–`1000`**. The merchant cannot force unusually large or small chunks via URL tweaks.

### Inner per-chunk iteration

The CSV writer iterates the order set in batches of **250 rows** using a chunked database read inside each queue job, regardless of the chunk-size parameter. The chunk-size parameter (`500` for orders) controls how the SQL pages are split across queue jobs; the inner 250-row iteration controls memory usage WITHIN one job. Merchants don't see this directly — it's a memory-bound safeguard for the worker process.

## Business rules

### Async threshold — 50 orders

When the filter scope returns more than 50 orders, the export goes async automatically. This is a hard threshold — the merchant cannot force synchronous mode for >50.

For very large exports (hundreds of thousands of orders), the queue splits the work into chunks of 500 per background job, processed in parallel where worker capacity allows.

### Sync path — JSON response with inline row array

For small exports (≤50 orders), the response payload is a JSON object with `type: csv`, `filename`, and a `data` array of rows. The frontend's CSV handler converts the array to a downloadable CSV file directly in the browser — no server-side file is persisted. The `cc.ajax.success` handler inspects the response `type`:

- `type=csv` → frontend CSVHandler triggers browser download.
- `type=zip` → frontend ZipHandler triggers browser download (rare on sync path).
- `type=queue` (or any other type) → toast *"The export is being processed. You will receive an email with the download link."*

### Async path — queue `export6`

Large exports route through the platform's queue system on the queue named **`export6`**. The orchestration job splits the work into chunks of 500 orders each. Each chunk job produces a CSV part. When all parts complete, a final batch step bundles them into a ZIP and notifies the merchant — see [[orders-export-delivery]].

The batch is tracked in the queue-monitoring system — accessible to CloudCart support for diagnostics via [[settings-queue-view]] but not directly to the merchant.

### Rapid-click behaviour — no dedup

When the merchant clicks Export multiple times in quick succession before the queue completes, each click enqueues a fresh batch — there is no dedup. The merchant will receive multiple emails with identical (or near-identical) CSV bundles. Best practice: click once, then wait for the email.

### Failure handling — partial completion blocked

If a chunk job fails mid-way, the platform retries per its standard queue retry policy. If all retries fail, the merchant does NOT receive a partial export — the batch's `finally` step requires successful completion to generate the bundle. The merchant must re-run the export.

### Filename pattern by path

- **Synchronous (small)**: `orders-YYYY-MM-DD-HH-MM-SS.csv` (single file).
- **Asynchronous (large)**: split into parts — `orders-YYYY-MM-DD-HH-MM-part_1.csv`, `part_2.csv`, etc., bundled into a single archive named `orders-YYYY-MM-DD-HH-MM-SS.zip` for the download link.

## Related

- [[orders-export]] — hub.
- [[orders-export-trigger-2fa]] — what produces the export request that hits the sync / async split.
- [[orders-export-csv-schema]] — what each chunk's CSV contains (also covers the BOM / CRLF differences between sync and async output).
- [[orders-export-delivery]] — how the async ZIP reaches the merchant.
- [[orders-export-filter-scope]] — the SQL snapshot that each async chunk reads against.
- [[settings-queue-view]] — async job status diagnostics for CloudCart support.
- [[background-queue-inventory]] — catalogue of all background processes.

## Open questions

None.
