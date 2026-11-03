---
type: feature
nav_path: "Apps → CSV Import → Upload + mapping wizard"
route_name: apps.csv_import.create
route_path: /admin/apps/csv_import (upload + mapping steps)
aliases: ["CSV Import wizard", "CSV Import — upload step", "CSV Import — column mapping", "CSV Import — publish defaults", "CSV Import — has_header_line", "CSV Import — staging table", "CSV Import — delimiter detection"]
tags: [apps, imports, csv, wizard, mapping]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-csv-import]]. See the hub for the other aspects (task detail, row pipeline, final statuses, mapping fields, side effects, plan gates).

# CSV Import — upload + mapping wizard

## Purpose

The wizard is how the merchant turns a raw spreadsheet into a queued import task. It accepts a file, auto-detects delimiter and line ending, stages every row in a temporary table, and walks the merchant through the per-task publish defaults plus a column-to-field mapping. The wizard's output is a saved task record that the row pipeline picks up immediately.

This page covers what's accepted, what's auto-detected, the publish-default toggles, the staging table, and the sample-row preview. For what's mappable see [[apps-csv-import-mapping-fields]]; for what happens after save see [[apps-csv-import-row-pipeline]].

## Where to find it

Apps → CSV Import → upload step (drag-and-drop or file picker). The wizard supports five import types — products, customers, subscribers, redirects, blog — captured at upload time and used to filter the field picker on the mapping step. See [[apps-csv-import-mapping-fields]].

## What the merchant can do here

### Upload — CSV / TXT only

The upload validation requires a file with extension `csv` or `txt`. **Excel formats (`.xls`, `.xlsx`) are rejected at upload time** with:
> *"Please select a valid file type (csv, txt)."*

The merchant exports their spreadsheet to CSV before uploading. Excel itself does the export; the wizard doesn't try to parse `.xlsx` directly.

### Delimiter + line-ending auto-detection

When the merchant uploads a file the platform reads the first **10 KB** and counts candidate delimiters: `,` (comma), `;` (semicolon), `\t` (tab), `|` (pipe), `:` (colon — auto-disabled when URLs are detected so `https://...` doesn't break parsing). The most-frequent character wins. Line endings (`\r\n`, `\n\r`, `\n`, `\r`) are detected the same way.

**The merchant does NOT pick the delimiter manually** — it just works for the common spreadsheet exports.

### Encoding — UTF-8 expected (no detection layer)

There is no explicit encoding-detection layer; the platform reads CSVs using PHP's standard CSV reader. UTF-8 files (the default modern export) parse correctly. **Windows-1251 / non-UTF-8 files MAY produce mangled Cyrillic** depending on PHP's locale — the merchant should save as UTF-8 before uploading.

### `has_header_line` toggle (default OFF)

The merchant explicitly tells the platform whether the first row contains column headers via a toggle in the import wizard. **It is NOT auto-detected**; the merchant must set it correctly. When ON, the first row is skipped as headers; when OFF, all rows are treated as data.

### Per-task publish defaults (products only)

For `products` type, the merchant sets defaults at upload time. These apply uniformly to every row in the imported CSV — they are NOT per-row overrides. To vary, the merchant must map a CSV column to the corresponding product field.

| Setting | Values | Default | What it controls |
|---|---|---|---|
| `has_header_line` | 0 / 1 | 0 (no) | Skip the first row as headers. |
| `publish_as_active` | yes / no | no | Imported products start active or as drafts. |
| `publish_as_featured` | 0 / 1 | 0 | Auto-mark as featured. |
| `publish_as_new` | yes / no | no | Auto-tag as "New". |
| `require_shipping` | yes / no | no | Default for whether tracking weight is needed. |
| `quantity_tracking` | yes / no | yes | Track inventory per product (per-product master switch — see [[inventory-variant-model]]). |
| `continue_sell` | yes / no | no | Allow ordering when stock = 0 (see [[inventory-oversell]]). |

### Column mapping — sample row preview

When the merchant lands on the mapping screen, the platform fetches the FIRST data row from the staging table and shows the value next to each column index. This helps the merchant identify which column holds which value — useful when the CSV doesn't have a header line. The same first-row sample is later shown on the task-detail page's column-mapping card (see [[apps-csv-import-task-detail]]).

The mapping itself is documented on [[apps-csv-import-mapping-fields]].

## Settings & fields

The wizard writes to a single `csv_tasks` row. Key fields it captures:

| Field | Source | What it does |
|---|---|---|
| `type` | Upload | products / customers / subscribers / redirects / blog. |
| `filename` | Upload | Original file name (shown on task detail). |
| `delimiter` + line-ending | Auto-detected | Stored on the task. |
| `has_header_line` | Wizard toggle | Skip first row. |
| `publish_as_active` / `publish_as_featured` / `publish_as_new` / `require_shipping` / `quantity_tracking` / `continue_sell` | Wizard publish defaults | Applied per row at insert time. |
| `mapping` | JSON column | The column-to-field map. Saved per task; not reusable across tasks. |

## Business rules

### CSV → staging table, one column per CSV column

On upload the platform creates a temporary table named `csv_import_{timestamp}` with one **longtext** column per CSV column (named `0`, `1`, `2`, …) plus an auto-incrementing `row_id`. The CSV is streamed into this table in **batches of 500 rows**. The mapping step then reads from this staging table by column index. **The table persists until the merchant manually deletes the task** — it survives the actual product-create run, useful for retries or post-import inspection.

### Mapping persists per task — not reusable across tasks

The mapping is stored as a JSON column on the task row in the `csv_tasks` table. **There is no clone-mapping-from-prior-task action**. Each new import requires fresh mapping. The mapping IS preserved if the merchant deletes the file mid-import and re-uploads (the task row survives until manually cleared).

### Variant rollup collapses CSV rows by `variant.parent_id`

If the merchant's CSV has 100 rows but they're for 25 products × 4 variants each, the formatter detects the shared `variant.parent_id` and collapses to 25 records (not 100). This is one of the reasons the `total < CSV rows` final-status outcome appears — see [[apps-csv-import-final-statuses]]. Useful but can surprise merchants; the wizard does not warn about the collapse before save.

### No standalone "Download template" on this app

The standalone CSV Import app pages (list / task / settings) do NOT expose a "Download template" button — on this surface the merchant figures out the column mapping from the wizard's column-name suggestions. (There is no product-catalogue CSV export to reverse-engineer columns from; to get current catalogue data into a spreadsheet the merchant uses an [[apps-xml-feed|XML product feed]] or the [[apps-google-sheets|Google Sheets app]].)

**However**, the modern CSV import wizard launched from the Products list header (cloud-upload icon → "Import with CSV file") DOES expose a **"CSV Template"** download button that fetches a sample `sitecp/docs/product-template.csv` from the asset host. Merchants who want a starter template should use the in-Products wizard rather than the standalone app. See [[products-products]] § "CSV import wizard".

### REQUIRED fields per import type

Each import type has its own required-field validation. For `products` the wizard requires at minimum `product.id` + `product.name` mapped; variant rows additionally require `variant.parent_id`. For `redirects` the wizard requires `redirect.old_url` + `redirect.new_url`. See [[apps-csv-import-mapping-fields]] for the per-type required-field catalogue.

## Related

- [[apps-csv-import]] — hub.
- [[apps-csv-import-mapping-fields]] — what fields can be mapped + per-type required fields.
- [[apps-csv-import-row-pipeline]] — what happens after the wizard is saved.
- [[apps-csv-import-task-detail]] — the post-save view that surfaces the saved mapping.
- [[apps-csv-import-final-statuses]] — the variant-rollup-driven `total < CSV rows` outcome.
- [[products-products]] — in-Products CSV wizard with a Download-template button.
- [[inventory-variant-model]] — `quantity_tracking` + `continue_sell` per-product master switches.
- [[inventory-oversell]] — what `continue_sell = yes` does after import.

## Open questions

_None._
