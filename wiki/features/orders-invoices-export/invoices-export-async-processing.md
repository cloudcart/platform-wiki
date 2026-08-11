---
type: feature
nav_path: "Invoices → Export → Async processing"
route_name: admin.core.export
route_path: /admin/api/core/export-import/export_invoices
aliases: ["Invoice export async", "Large invoice export", "Invoice export ZIP", "Invoice export email delivery", "Асинхронен експорт на фактури", "Голям експорт на фактури"]
tags: [orders, invoices, export, csv, async, queue]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-07-29
source_count: 7
---

> Part of [[orders-invoices-export]]. See the hub for the other aspects (trigger & delivery, column schema, credit-note rows).

# Invoices export — async processing

## Purpose

Covers what happens when the export exceeds the synchronous threshold (more than 10 invoices): the 500-per-chunk background jobs, the ZIP-of-parts bundle, email-only delivery, the CRLF + UTF-8-with-BOM encoding, the lack of incremental tracking, and file retention.

## Where to find it

There is no separate screen — async mode is triggered automatically by the **Export** header button on [[orders-invoices]] when the filtered list holds more than 10 invoices (see [[invoices-export-trigger]] for the threshold and the toast). Job status can be watched on [[settings-queue-view]].

## What the merchant can do here

- Trigger a large export and receive a ZIP archive of CSV parts by email when it completes.
- Re-assemble the multi-part CSV by concatenating the parts (and discarding repeated header lines) — most spreadsheet tools open multi-part CSV directly.

What the merchant CANNOT do:

- Resume or cancel a running async export job.
- Receive the async result anywhere other than the emailed download link.
- Get an incremental ("only since last export") file — every run is a fresh full export of the filtered scope.

## Settings & fields

| Parameter | Value | What it controls |
|-----------|-------|------------------|
| **limit** | 10 | At or below this, the export runs synchronously in the browser (see [[invoices-export-trigger]]). Over it → async. |
| **chunk** | 500 | Each background job processes 500 invoices' worth of CSV rows. |

### Delivery

Async exports are delivered ONLY by email link. The merchant must have a valid admin email — if the email is broken, the file is generated but not delivered.

### Filenames

Async parts are named `invoices-export-YYYY-MM-DD-HH-MM-part_1.csv`, `part_2.csv`, etc., and bundled into one ZIP archive named `invoices-YYYY-MM-DD-HH-MM-SS.zip`.

## Business rules

### Async batch processing

When async mode triggers, the platform spawns a background batch containing chunked aggregation jobs. Each chunk processes 500 invoices' worth of CSV rows. Each chunk emits its OWN CSV part (`part_1`, `part_2`, …), and the final batch step bundles the parts into a single ZIP archive and emails the merchant the download link. The merchant receives ONE ZIP containing N CSV parts; re-assembling the CSV is the merchant's responsibility.

### CSV uses CRLF line endings + UTF-8 with BOM

Async-generated CSVs emit Windows-style CRLF (`\r\n`) line endings to keep Microsoft Excel (Windows + locale-defaulted viewers) from collapsing the file onto one line, and a UTF-8 BOM is added during upload to the file store. Synchronous CSVs (≤10 invoices) use the same CRLF endings. Merchants opening the file in Unix-style tools (`grep`, `awk`, `cut`) should expect CRLF endings.

### Modern sync path uses OpenSpout, not Maatwebsite/Excel anymore

The modern sync path uses the OpenSpout library (chunked at 250 rows from the DB). A legacy Maatwebsite/Excel version of this exporter exists in the codebase but is marked deprecated — that older variant additionally converts the output to CP1251 Windows-Cyrillic encoding. Modern stores producing exports via the current admin always get UTF-8 output. Merchants whose tooling broke after a recent platform update should NOT need a CP1251 conversion any more.

### No incremental export

The platform does NOT track which invoices were previously exported. Each export run produces a fresh CSV from scratch covering the filtered scope. For incremental exports (only invoices issued since last export), the merchant must apply a **Date** filter manually to exclude already-exported records.

### Retention

Async export files are stored in the platform Filemanager with no auto-purge — the CDN download URL persists (same retention behaviour as [[orders-export]]). The emailed link continues to work until the file is manually removed.

### Side effects

- Queues background jobs on the `export6` queue; each chunk produces a CSV part; the final batch step bundles them into a ZIP and emails the download link.
- The sync path (≤10 invoices) does NOT queue anything — it builds the CSV in memory and returns rows in JSON for the browser to download. No server-side persistence on the sync path.

## Related

- [[orders-invoices-export]] — hub.
- [[orders-invoices]] — parent invoices list.
- [[invoices-export-trigger]] — the threshold + toast that lead into async mode.
- [[invoices-export-columns]] — the CSV schema each part contains.
- [[orders-export]] — orders export; same Filemanager retention behaviour.
- [[settings-queue-view]] — async job status for large exports.

## Open questions

(none — retention answer is the same as orders-export: Filemanager-stored, no auto-purge, CDN URL persists.)
