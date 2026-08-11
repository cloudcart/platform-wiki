---
type: feature
nav_path: "Invoices → Download → Sync vs async"
route_name: admin.core.export
route_path: /admin/api/core/export-import/download_invoices
aliases: ["Invoice download sync vs async", "Invoice download threshold", "Invoice download chunking", "Invoice download email link", "Invoice download failure mode"]
tags: [orders, invoices, download, async, queue, zip]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---
# Invoices bulk download — sync vs async

> Part of [[orders-invoices-download]]. See the hub for related aspects (entry point, scope, rendering, permissions/plan).

## Purpose

Documents how the bundle is delivered: small bundles synchronously in the browser, large bundles asynchronously by emailed link. Covers the synchronous threshold, the async chunk size, email delivery, bundle retention, and the failure behaviour. The merchant does not choose — the count of in-scope invoices decides.

## Where to find it

Delivery is automatic after the merchant triggers a download from the **Download** button on [[orders-invoices]] (see [[invoices-download-entry-points]]). The count is the store's whole invoiced-order set — the filter is **not** applied to the download (see [[invoices-download-scope]]).

## What the merchant can do here

### Receive the result

| In-scope volume | Delivery |
|-----------------|----------|
| Up to **10 invoices** | Synchronous — the ZIP downloads directly in the browser (`type: zip`). |
| Over **10 invoices** | Asynchronous — split into chunks, processed in the background, and emailed when complete (`type: queue`). Toast: *"The export is being processed. You will receive an email with the download link."* |

### What the merchant CANNOT do here

- Choose sync vs async — the in-scope count decides.
- Resume a failed async job — a failed download must be re-triggered (see Business rules).
- Receive an async bundle without a working admin email — async delivery is by email link (and a matching alert in the admin).

## Settings & fields

### Threshold + chunk size

| Control | Current value | Meaning |
|---------|---------------|---------|
| Synchronous threshold | **10 invoices** | At or below this, the bundle is built inline and returned to the browser. |
| Asynchronous chunk size | **50 invoices per chunk** | Above the threshold, the work is split into chunks of this size and queued. |

There is a single **Download** entry point, so these are the only limits — there is no per-entry-point limit table. (The threshold and chunk size are platform defaults; the current UI does not override them.)

## Business rules

### Synchronous path (≤ 10) — bundle returned in the response

At or below the threshold the ZIP is assembled on the server, returned in the action's JSON response as a `type: zip` payload, and the browser saves it. Nothing is persisted server-side. The synchronous archive is named `invoices-YYYY-MM-DD-HH-MM-SS.zip` (a single archive). Per-invoice naming is covered in [[invoices-download-rendering]].

### Asynchronous path (> 10) — chunked background batch

Above the threshold the action returns `type: queue` (the toast) and queues the work as a background batch on the export queue. The in-scope invoices are split into chunks of 50; each chunk renders its slice of PDFs. When all chunks finish, the platform assembles them into one ZIP. Job status is visible in [[settings-queue-view]].

### Delivery — email link + admin alert

When the async bundle is ready, the platform delivers it two ways: an **email** to the admin with the download link, and a success **alert** in the admin panel carrying a *"download here"* link plus a link to the file in the store's Files area. The merchant must have a valid admin email for the email link to arrive.

### Bundle retention

The asynchronous bundle is stored as a file in the store's Files area (with a CDN URL) and persists until manually deleted — so the emailed / alert link keeps working. The synchronous bundle, by contrast, is never persisted server-side.

### Failure handling — no auto-retry

The platform does NOT auto-retry a failed download on the merchant's behalf. If a download fails, the merchant re-triggers it from the **Download** button. For very large invoice volumes or flaky conditions, narrowing the filter (a tighter **Date** range — see [[invoices-download-scope]]) reduces the amount of work per run and the chance of a failure.

## Open questions

(none.)

## Related

- [[orders-invoices-download]] — hub.
- [[invoices-download-scope]] — the in-scope count that drives the sync-vs-async choice.
- [[settings-queue-view]] — async job status for large bundles.
- [[orders-invoices]] — parent invoices list.
- [[invoice]] — entity page.
