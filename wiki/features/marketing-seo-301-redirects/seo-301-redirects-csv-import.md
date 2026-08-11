---
type: feature
nav_path: "Marketing → Seo → 301 Redirects → CSV import"
route_name: seo-301-redirects
route_path: /admin/marketing-new/seo/301-redirects
aliases: ["Import 301 redirects from CSV", "Bulk import redirects", "ImportRedirects job", "Three-step import wizard", "Импорт на пренасочвания", "CSV пренасочвания"]
tags: [marketing, seo, redirects, csv, import, background-jobs]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-seo-301-redirects]]. See the hub for the other aspects (types, validation, middleware, wildcards, marketing pass-through, auto-tracking).

# 301 Redirects — CSV import

## Purpose

For a migration with hundreds or thousands of legacy URLs, the row-by-row inline editor on [[marketing-seo-301-redirects]] is impractical. The **Import redirects** button opens a three-step wizard that uploads a CSV, maps the columns to the redirect fields, and enqueues a background `ImportRedirects` job to insert the rows in chunks.

The import is **idempotent by `old_url`** — re-running the same CSV deletes the previously-imported duplicates and re-inserts them (last-write-wins per `old_url`). This makes it safe to iterate on the source spreadsheet without ending up with stale dupes.

## Where to find it

The **Import redirects** button sits in the table header on [[marketing-seo-301-redirects]]. Clicking it opens the wizard modal. The wizard is the standard CloudCart 3-step importer used across product / customer / category imports.

## What the merchant can do here

- Upload a CSV file (`.csv` extension only) into the Filemanager-style drop zone.
- Tick "Check this if your file has a header line explaining the columns" so the importer skips the first row.
- Bind each CSV column to one of the expected redirect fields: `redirect.old_url` and `redirect.new_url` (both required).
- Submit the mapping and have the import run in the background while the merchant continues working.
- See the import status from [[settings-queue-view]] (the `ImportRedirects` job appears on the `import` queue) and from the standard CloudCart imports dashboard.

### What the merchant CANNOT do here

- Pick the redirect **type** during the import — the importer auto-types every row as `external` (when the value starts with `http://` / `https://`) or `manual` (everything else). Entity-typed rules cannot be created via CSV.
- Import to a specific `item_id` (Product / Category / Vendor / Page / Blog / Article ID) — see above; CSV is for free-form rules only.
- Pause / cancel the running job from this screen — the merchant has to use [[settings-queue-view]] to inspect or cancel the background job.

## Settings & fields

### The 3-step wizard

| Step | What happens | Required input |
|------|--------------|----------------|
| **1. Upload CSV file** | Drop zone accepts a single `.csv` file. Toggle for "has header line" controls whether the first row is skipped. | `.csv` file. |
| **2. Column mapping** | The importer shows a preview of the columns and asks the merchant to bind each one to a redirect field. | Map column → `redirect.old_url` AND column → `redirect.new_url`. Both required. |
| **3. Submit** | The mapping is POSTed; the import is enqueued as a background `ImportRedirects` job on the `import` queue; the modal closes and toasts *"The import started"*. | Click Submit. |

### What gets stored per row

For each CSV row, the importer:

1. Reads `old_url` and `new_url` from the mapped columns.
2. Auto-types the row: `external` if `new_url` starts with `http://` / `https://`; `manual` otherwise.
3. Deletes any existing rule with the same `old_url` (idempotent re-import).
4. Inserts the new row in chunks of 100 (batched for DB efficiency).
5. After all chunks, drops the temp DB table that held the upload, and recomputes the `has_301_redirects` site setting (see [[seo-301-redirects-middleware]]).

## Business rules

### Idempotent re-import — last-write-wins per `old_url`

Duplicates by `old_url` are deleted-then-reinserted. Re-importing the same CSV with one column changed produces one row per `old_url` with the latest values. This is by design for migrations where the merchant iterates on the spreadsheet several times before getting the final shape right.

The duplicate detection is across **all** redirect rows in the store, not just CSV-imported ones — so a CSV row whose `old_url` matches a previously merchant-created manual rule will OVERWRITE the manual rule (replacing its `new_url` and resetting its type to `external` or `manual`). Support pattern: "my hand-crafted entity-type redirect was replaced after a CSV import" → check whether the `old_url` was in the CSV.

### Auto-type heuristic — `external` vs `manual`

`http://` or `https://` prefix → `external` (the redirect points off-store). Anything else → `manual` (the redirect is on-store, with `new_url` as a relative path).

The auto-type means **entity-typed redirects cannot be created via CSV**. A merchant who wants `product` redirects (which would auto-follow product renames — see [[seo-301-redirects-types]]) has to create them manually via the inline editor or via [[api-redirects]]. The CSV path is for "preserve the old URL → land on a fixed URL" migrations.

### Background job + queue visibility

The import enqueues an `ImportRedirects` job on the `import` queue. The merchant can:

- Watch the queue from [[settings-queue-view]] to see when the job finishes.
- See the import history under the standard imports dashboard, with row counts.
- Receive a notification when the import completes (depends on store notification settings).

For inventory of all background jobs the platform runs and how to verify they finished, see [[background-queue-inventory]].

### Required 2FA on import

The CSV import surface MAY be gated by the `required_2fa` flag returned in the import meta — meaning the merchant must have 2FA enabled before they can run the import. This is a security measure: bulk URL rewriting can break SEO across an entire site if the wrong file is uploaded, so the platform requires a higher auth bar than the inline editor. Verify the flag against the merchant's import-meta response if a merchant reports the Import button is missing.

### Permission

The CSV-import endpoints (`/admin/api/core/imports/*/redirects`) sit behind the standard import permission group, separate from the `marketing.seo` permission that gates the inline editor on [[marketing-seo-301-redirects]]. Staff with import permission but no `marketing.seo` permission can still import — but cannot then edit / delete the imported rows from the inline editor (verify).

## Related

- [[marketing-seo-301-redirects]] — hub.
- [[seo-301-redirects-types]] — what gets stored differs by type; CSV is `external` / `manual` only.
- [[seo-301-redirects-validation]] — validation runs on each imported row; duplicate `old_url` triggers delete-then-reinsert rather than error.
- [[seo-301-redirects-middleware]] — `has_301_redirects` is recomputed after the import finishes.
- [[seo-redirect-csv-import]] — entity-side documentation of the CSV import (data-model view).
- [[settings-queue-view]] — watch the `import` queue for the `ImportRedirects` job.
- [[background-queue-inventory]] — full catalogue of background jobs.

## Open questions

- Maximum CSV row count per import (verify against the import-meta `max_rows` limit).
- Whether import-permission-only staff (no `marketing.seo` permission) can edit imported rows after the import (verify).
