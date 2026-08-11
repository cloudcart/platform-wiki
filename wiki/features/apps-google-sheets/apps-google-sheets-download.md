---
type: feature
nav_path: "Apps → Google Sheets → Download"
route_name: apps.google_sheets.tasks
route_path: /admin/apps/google_sheets/tasks
aliases: ["Google Sheets download", "Sheets import products", "Sheets to CloudCart", "Sheets pull edits"]
tags: [apps, google, sheets, download, import, sync]
plan_gates: ["google_sheets"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Google Sheets → Download

> Part of [[apps-google-sheets]]. See the hub for related aspects (upload, sync pipeline, OAuth, columns & filters).

## Purpose

The **Download** task pulls the merchant's edits **out of the spreadsheet and back into CloudCart** (Sheets → CloudCart). This is the powerful half of the bidirectional sync: a non-technical user edits product names, prices, descriptions, brands, categories, and tags in a familiar spreadsheet, then commits all the changes at once. Download is also how the merchant **creates** brand-new products by adding rows.

## Where to find it

Sidebar → Apps → Google Sheets → **Tasks tab** → **Download** button (`/admin/apps/google_sheets/tasks`, down-arrow icon). The button UI is on [[apps-google-sheets-tasks]]; queue mechanics on [[apps-google-sheets-sync-pipeline]].

## What the merchant can do here

- Pull all spreadsheet edits back into the matching CloudCart products in one click.
- Add new products by adding rows with an empty Product ID.
- Add products into brand-new categories / brands just by typing the names — they're auto-created.

### What the merchant CANNOT do here

- Run a Download before at least one successful Upload (the sheet must have the right columns first).
- Cancel an in-progress Download from the UI (the batch supports cancellation internally, but no button is exposed — see [[apps-google-sheets-sync-pipeline]]).
- Expect CloudCart-side edits made after the last Upload to survive — the spreadsheet wins (below).

## Settings & fields

Download has no settings of its own; it reads whatever is currently in the configured worksheet. The column meanings come from the catalogue on [[apps-google-sheets-columns-filters]].

## Business rules

### Download requires a prior successful upload

A Download is only allowed once at least one Upload has completed successfully. This guarantees the sheet has the correct column structure before the import maps rows back. Error: *"You need at least one successful upload, before you can start a download task!"*

### Parallel batch pipeline (50-product chunks)

The Download path runs as a parallel background batch on the inbound (import) queue (see [[apps-google-sheets-sync-pipeline]]):

1. **`sheets_download`** (the read step) — pulls the entire spreadsheet from Google Sheets, groups rows by `Product ID`, stages all rows, then chunks them by 50 and creates **one parallel import task per chunk**.
2. **`sheets_import`** (the parallel importer) — runs concurrently for each chunk; takes 50 staged rows and syncs them into CloudCart products with deadlock-resilient saves and per-product retry.
3. The finalisation step — runs after the batch; marks the task `STATUS_COMPLETED` (or `STATUS_FAILED`) and cleans up the remaining staged rows.

### Conflict resolution: the spreadsheet wins

Download **overwrites** matching CloudCart products with whatever is in the spreadsheet. If the merchant edited a product in CloudCart admin between the last Upload and the Download, the spreadsheet's value wins — the spreadsheet is the working copy and the Download is treated as the "commit". (This is also why a prior Upload is mandatory: the sheet must carry the correct columns for a safe overwrite.) Re-running a Download is allowed with no idempotence guard — each run just refreshes CloudCart with the sheet's current state.

### Product-ID grouping + new-product creation

Rows are grouped by the `Product ID` column, so multiple variant rows for the same parent product collapse into one logical record on import. A row with an **empty Product ID** gets a synthetic `new-{uniqid}` ID, which triggers a **CREATE** — so the merchant adds products simply by adding rows with no Product ID.

### Category auto-creation from a `>`-separated path

If a row's `Category` cell holds a path like "Apparel > Shirts > T-Shirts", the platform splits it and creates each level that doesn't yet exist. The merchant can drop a product into a brand-new category just by typing the path — the integration builds the category tree.

### Vendor (Brand) auto-creation

A `Brand` value that matches no existing vendor creates a new vendor; existing names are matched and reused (no duplicates).

### Tags overwrite on download

When tags are supplied in the sheet, the platform **deletes the product's existing tags first**, then re-creates them from the sheet's comma-separated list. The spreadsheet is therefore the canonical tag source on every Download — tags present in CloudCart but absent from the sheet get removed.

### CloudCart CDN image URLs are skipped

When parsing image URLs, the platform **skips any URL containing `cdncloudcart.com`** — those images are already on CloudCart's CDN (from the prior Upload), so they aren't re-downloaded. Only NEW image URLs (e.g. external URLs the merchant pasted) are fetched and attached. Image downloads happen **after** the product is saved, so a slow download never holds up the save; if an image fails, the rest of the product still saves.

## Related

- [[apps-google-sheets]] — hub.
- [[apps-google-sheets-upload]] — the prerequisite forward direction.
- [[apps-google-sheets-sync-pipeline]] — the parallel-batch + live-progress mechanics.
- [[apps-google-sheets-columns-filters]] — the meaning of each column being imported.

## Open questions

(None currently outstanding for this page.)
