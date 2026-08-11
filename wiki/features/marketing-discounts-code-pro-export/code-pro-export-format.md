---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Export → File format"
route_name: discounts-code_pro-list
route_path: /admin/marketing-new/discounts/code-pro/:id
aliases: ["Code PRO export file format", "Export CSV encoding", "UTF-8 BOM export", "Streamed CSV export", "Export filename discount-codes-pro.csv"]
tags: [marketing, discounts, code-pro, export, csv]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-code-pro-export]]. See the hub for the other aspects (overview, columns, business rules).

# Code PRO export — file format & encoding

## Purpose

This aspect documents the **file-format mechanics** of the Code PRO codes export: the filename and HTTP headers, the UTF-8 BOM that keeps Excel happy, the leading-space trick on the `Code` column, the UTC date formatting, and the streamed-in-chunks delivery that makes very large exports memory-safe and timeout-free.

## Where to find it

These mechanics apply to the `discount-codes-pro.csv` file produced by the "Export" toolbar anchor on the [[marketing-discounts-code-pro]] codes list — `GET /admin/api/core/discounts/code-pro/{id}/export`. The merchant never configures any of this; the format is fixed (see [[code-pro-export-overview]]).

## What the merchant can do here

- **Open the file directly in Excel-on-Windows** without character corruption, thanks to the UTF-8 BOM.
- **Keep leading zeros** on all-numeric codes — the leading-space prefix stops the spreadsheet auto-casting them to integers.
- **Export tens of thousands of codes** in one file — streaming + chunking + the disabled time limit mean huge exports complete without truncation.
- **Re-interpret the UTC dates** into local time inside the spreadsheet (the file stores everything in UTC).

## Settings & fields

### Output filename and headers

| Aspect | Value |
|--------|-------|
| **Filename** | `discount-codes-pro.csv` |
| **Content-Type** | `text/csv` |
| **Encoding** | UTF-8, with BOM prefix (`EF BB BF`) for spreadsheet-tool compatibility |
| **Cache headers** | `must-revalidate, post-check=0, pre-check=0`, `Expires: 0`, `Pragma: public` |
| **Response type** | Streamed |
| **Time limit** | `set_time_limit(0)` — no PHP timeout (large exports won't truncate) |
| **Chunk size** | 500 codes per DB chunk |

## Business rules

### UTF-8 BOM for Excel compatibility

The first 3 bytes written to the response are the UTF-8 byte-order mark (`EF BB BF`). Without it, Excel-on-Windows opens UTF-8 CSVs as ASCII and mangles non-ASCII characters (Cyrillic / accented Latin). The BOM tells Excel to read the file as UTF-8.

### Code value is prefixed with a space

The `Code` column writes a leading single space before the code string (` <code>`). This is a deliberate trick to prevent Excel from auto-parsing all-numeric codes (e.g., `0001234`) as integers, which would strip leading zeros. Spreadsheet tools render the leading space as visually-empty cell text, preserving the exact code string. (This column is documented in full on [[code-pro-export-columns]].)

### Time zone — UTC for `date_start` / `date_end`

Both date columns are converted to UTC and written as ISO 8601 strings (`startOfDay` for `date_start`, `endOfDay` for `date_end`). This is intentional: ISO 8601 UTC is the most-portable date format and avoids confusion when sharing the CSV across time zones. The merchant's local-time interpretation must be derived by re-formatting the UTC value in their spreadsheet.

### Memory-safe via chunking

The output is streamed and the codes are read in chunks of 500. This means even a Code PRO discount with tens of thousands of codes won't blow up server memory — each chunk is written to the response and freed before the next is read. Keyset pagination (`id > last_id`) rather than offset-based pagination keeps the read performant on large tables.

### `set_time_limit(0)` — no PHP timeout

The exporter explicitly disables the PHP execution-time limit, so very large exports (50,000+ codes) finish without hitting the default 30 / 60-second timeout. The bottleneck on huge exports becomes the database read throughput, not PHP.

### Conditions hydrated per chunk, not per code

Each chunk of 500 codes is loaded with its conditions' related records (product names, category names, vendor names, smart-collection names, geo-zone name) eager-loaded — so each row's full condition info is hydrated in a handful of SQL statements per chunk, not per code. For a 50,000-code export this means roughly 100 query batches total instead of one query set per code.

## Related

- [[marketing-discounts-code-pro-export]] — hub.
- [[code-pro-export-columns]] — the `Code` column and the date columns documented here in column context.
- [[marketing-discounts-code-pro]] — the codes being exported.
- [[apps-csv-import]] — CSV import surface (different direction; the export is one-way out).

## Open questions

No outstanding questions.
