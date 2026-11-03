---
type: feature
nav_path: "Apps → Google Sheets → Upload"
route_name: apps.google_sheets.tasks
route_path: /admin/apps/google_sheets/tasks
aliases: ["Google Sheets upload", "Sheets push products", "CloudCart to Sheets", "Sheets export"]
tags: [apps, google, sheets, upload, export, sync]
plan_gates: ["google_sheets"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Google Sheets → Upload

> Part of [[apps-google-sheets]]. See the hub for related aspects (download, sync pipeline, OAuth, columns & filters).

## Purpose

The **Upload** task pushes the merchant's product catalog **out of CloudCart and into the auto-created spreadsheet** (CloudCart → Sheets). This is the forward direction of the bidirectional sync, and it must run at least once before the merchant can run a [[apps-google-sheets-download|Download]] (the sheet needs the correct column structure first). Upload is how the merchant gets their catalog into spreadsheet form for bulk editing or sharing.

## Where to find it

Sidebar → Apps → Google Sheets → **Tasks tab** → **Upload** button (`/admin/apps/google_sheets/tasks`, up-arrow icon). The button UI is documented on [[apps-google-sheets-tasks]]; the queue mechanics are on [[apps-google-sheets-sync-pipeline]].

## What the merchant can do here

- Push all (or a filtered subset of) products into the spreadsheet with one click.
- Re-run Upload any time to refresh the sheet with the current CloudCart catalog (it's a full overwrite each time).
- Pick which products and which columns are written — via the Settings tab; see [[apps-google-sheets-columns-filters]].

### What the merchant CANNOT do here

- Append to the existing sheet — every Upload **clears and rewrites** the worksheet.
- Upload while another sync task is unfinished (one task at a time — see [[apps-google-sheets-sync-pipeline]]).
- Reorder columns or transform values in the written rows (the platform writes the raw column values).

## Settings & fields

Upload reads the settings saved on the Settings tab — `filter_group` + `filter_group_value` (which products) and `allowed_columns` (which columns). No Upload-specific fields exist. See [[apps-google-sheets-columns-filters]] for the catalogue and the filter-mode caveats.

## Business rules

### Upload replaces sheet contents (no append-only mode)

Each Upload clears the worksheet and rewrites the header row + all matching products from CloudCart. There is no merge / append knob — Upload is a full overwrite of the worksheet. A subsequent Download reads back whatever the merchant has since edited.

### Two-phase upload pipeline

A successful Upload runs as two distinct queue jobs (both on the `export1` queue — see [[apps-google-sheets-sync-pipeline]]):

1. **`sheets_upload`** (the seeding job) — runs **once**: clears the sheet, writes the **header row**, queries the **total product count**, stores `total_count` on the job row, then dispatches the first export iteration.
2. **`sheets_export`** (the chunk writer) — runs **repeatedly**: reads up to **500 products at a time**, formats them as rows, appends them to the sheet, then re-dispatches itself with the last product's ID as the cursor. Terminates when no more products are returned and marks the job `STATUS_COMPLETED`.

This explains why a 50,000-product upload can take many minutes — each chunk is one Sheets API append plus a new queue-job dispatch, so progress is gradual. The merchant watches it advance via *"Uploaded products: X of Y"* in the Status Message column.

### Discount column is conditional

The Discount column is written only when the merchant has selected a `discount_id` in Settings; without one, the column is dropped from the allowed-columns list at save time. Only `fixed`-type discount campaigns are eligible — see [[apps-google-sheets-columns-filters]].

### Plan / maintenance gating applies

If the site's plan is expired or it's in maintenance mode, the Upload job silently skips without writing — the merchant must clear the restriction and queue a fresh task. See [[apps-google-sheets-sync-pipeline]].

## Related

- [[apps-google-sheets]] — hub.
- [[apps-google-sheets-download]] — the reverse direction (Sheets → CloudCart).
- [[apps-google-sheets-sync-pipeline]] — queue routing + concurrency for this job.
- [[apps-google-sheets-columns-filters]] — which columns / products get written.
- [[apps-google-sheets-tasks]] — the Upload button + progress UI.

## Open questions

(None currently outstanding for this page.)
