---
type: feature
nav_path: "Apps → CSV Import"
route_name: apps.csv_import.overview
route_path: /admin/apps/csv_import
aliases: ["CSV Import", "Csv Import", "Bulk product import", "Spreadsheet import", "Excel import", "no enable disable button", "app has no active toggle"]
tags: [apps, imports, csv, products, plan-gated]
plan_gates: ["csv_import"]
created: 2026-05-22
updated: 2026-08-06
source_count: 5
---

# CSV Import

## Purpose

**CSV Import** integration — imports product / catalog data from a **CSV / Excel-exported** file uploaded by the merchant. It is one of the tools for **loading a catalog IN from an external source**, alongside [[apps-xml-import]] (URL-fed XML) and the API (developer route) — spreadsheet-based, which makes it more accessible for non-technical merchants.

> ## 🔴 CSV Import CREATES products — it does NOT update existing ones
>
> **A CSV import always loads the file as NEW products. It is not an update / upsert tool for a catalog that is already in the store.** Re-importing a product that already exists **creates a duplicate**, it does not modify the original.
>
> In particular, **putting a product's CloudCart ID (the number in the admin URL, e.g. `583`) into the mapped `product.id` column does NOT update product 583** — it creates another product. The `product.id` column is the **file's own identifier**, used to group the file's variant rows into products; it is not a reference to an existing CloudCart product. See [[apps-csv-import-mapping-fields]].
>
> **To change products that are already in the store**, use one of:
> - the **[[apps-google-sheets|Google Sheets]] app** — the one-click round-trip (Upload → edit in the sheet → Download), the recommended way to mass-edit prices / texts / weights / any attribute;
> - the **product editor** / the products list **bulk actions** for a small number of products.
>
> Treat CSV / XML import as the **load-in** path only (bringing a catalog IN for the first time).

Used for:

- **Bootstrap** — a new store with an existing catalog in a spreadsheet file.
- **Migration** — from a competitor platform that exports CSV.
- **Periodic refresh** — from supplier-provided CSV files.

The integration uses modern Vue (CcDomain) and supports background processing for large files. Imports run asynchronously row-by-row; the merchant can leave the page and return to see results.

The integration is **plan-gated** through the `csv_import` plan-feature mapping and ALSO inherits the merchant's per-plan **products numeric cap** — see [[apps-csv-import-plan-gates]].

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> There is nothing to keep "running" either — each import is a task the merchant starts by hand and it ends on its own.

## Where to find it

Sidebar → Apps → install → **CSV Import**.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[apps-csv-import-task-detail]] — the task-detail page: header summary, interrupted card + Cancel button, live progress card with 5-second polling, failed-records table, column-mapping table; back-navigation to the list view.
- [[apps-csv-import-wizard]] — upload + mapping wizard: accepted file types (csv / txt — XLS / XLSX rejected), delimiter / line-ending auto-detection, encoding, `has_header_line` toggle, per-task publish defaults (active / featured / new / shipping / tracking / continue-sell), staging-table mechanics, first-row sample preview, mapping-persistence semantics.
- [[apps-csv-import-row-pipeline]] — async row processing: `working` concurrency lock (one import per store), batched dispatcher, the 3-flag `finalizeIfComplete` gate that protects against premature finalisation, polling cadence, queue context.
- [[apps-csv-import-final-statuses]] — the 4 deterministic final-status outcomes (`total = 0` → failed, `failed_count > 0` → completed-with-failures, `total < CSV rows` → completed-with-collapse, otherwise → success), the orphaned-task finaliser for plan-quota interruption, persisted `imported_count` / `failed_count` on `csv_tasks`.
- [[apps-csv-import-mapping-fields]] — what fields can be mapped: product columns, variant columns (`variant.parent_id` REQUIRED, three option groups `v1`/`v2`/`v3`), required-field validation per import type, comma-separated image URLs downloaded into media library, multi-column mapping (multiple CSV columns into one field), the 5-type multi-pipeline (products / customers / subscribers / redirects / blog).
- [[apps-csv-import-side-effects]] — the search index async sync via `MakeSearchable` on `searchable-import4` (#1 source of "I imported and don't see it" tickets); webhook ordering (`product.created` / `product.updated` fires before search-index sync); no built-in rollback / undo; `app_import = 'csv-{taskId}-…'` tag for bulk cleanup via the products-list filter `import=csv-{taskId}-`.
- [[apps-csv-import-plan-gates]] — the `csv_import` plan-feature mapping (install gate); inheritance of the merchant's per-plan **products numeric cap** (interrupts the task with a plan-quota message); concurrent-imports serialisation is at the manager level (independent of plan).

## What the merchant can do here

- Upload a CSV / TXT file (drag-and-drop or file picker) — see [[apps-csv-import-wizard]].
- Map CSV columns to CloudCart product / variant / customer / subscriber / redirect / blog fields — see [[apps-csv-import-mapping-fields]].
- Configure per-task publish defaults (active / featured / new / shipping / tracking / continue-sell) — see [[apps-csv-import-wizard]].
- Set a per-task **import key** and a **category delimiter** — see [[apps-csv-import-wizard]]. (There is **no** "update strategy" / create-vs-update choice — every task creates products; see the callout above.)
- Track import progress with live per-row counts and a 5-second polling cadence — see [[apps-csv-import-task-detail]].
- Cancel a running task mid-flight via the **Cancel import** button — see [[apps-csv-import-task-detail]].
- See per-row failures (first error summarised on the task; full list queryable from the failed-records table) — see [[apps-csv-import-final-statuses]].
- Filter the products list by `import=csv-{taskId}-` to find every product the task created — useful for bulk cleanup since there is no rollback. See [[apps-csv-import-side-effects]].

What the merchant **cannot** do here:

- Upload Excel `.xls` / `.xlsx` directly — they're rejected at upload. The merchant exports to CSV first. See [[apps-csv-import-wizard]].
- Run multiple imports in parallel — the `working` lock serialises imports per store. See [[apps-csv-import-row-pipeline]].
- Roll back / undo an import — there is no built-in undo. See [[apps-csv-import-side-effects]].
- Clone the mapping from a prior task — every task requires fresh column mapping. See [[apps-csv-import-wizard]].
- Pick the delimiter manually — it is auto-detected from the file's first 10KB. See [[apps-csv-import-wizard]].

## Settings & fields

App key: `csv_import`. The integration honours the plan-feature gate of the same name plus the merchant's per-plan **products numeric cap**. Field-by-field configuration is documented per aspect — wizard fields on [[apps-csv-import-wizard]], mapping fields on [[apps-csv-import-mapping-fields]], live-task fields on [[apps-csv-import-task-detail]], gate fields on [[apps-csv-import-plan-gates]].

## Business rules

Each aspect documents its own rules. The cluster-level invariants:

- **One concurrent import per store** — the `working` lock blocks a second import while one is in progress. See [[apps-csv-import-row-pipeline]].
- **Async row processing** — every row queues as a background job; the merchant can navigate away and return. See [[apps-csv-import-row-pipeline]].
- **3-flag finalisation gate** — declared done only when (a) dispatcher completes, (b) no pending rows remain, (c) progress ≥ total. Protects against the "momentary zero" race between batches. See [[apps-csv-import-row-pipeline]].
- **Storefront lags behind admin** — the search index sync runs through `MakeSearchable` on `searchable-import4` *after* the import row finishes; the storefront catches up product-by-product. This is the most common "I imported and don't see it" support ticket. See [[apps-csv-import-side-effects]].
- **No rollback / undo** — every import tags its products with `app_import = 'csv-{taskId}-…'` for later filter-and-delete cleanup. See [[apps-csv-import-side-effects]].
- **Standard apps permission scope** for who can install / configure.

## Related

- [[apps]] — App Store.
- [[apps-google-sheets]] — **recommended for mass-editing existing products** (one-click Upload → edit → Download round-trip, no file handling). Prefer this over CSV for updating prices / texts / attributes.
- [[apps-xml-import]] — XML alternative (URL-fed, not file).
- [[apps-xml-sync]] — recurring sync alternative.
- [[apps-blog-csv-import]] — CSV import for blog articles (sibling app routed through `BlogCsvImportManager`).
- [[customers-import]] — customer-records CSV variant.
- [[products-products]] — products created / updated; the in-Products CSV wizard with a **Download template** button.
- [[settings-queue-view]] — background queue that processes rows.
- [[settings-import-history]] — historical import audit.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.
- [[background-queue-inventory]] — catalogue of all background processes; covers the product CSV-import queue, how rows are processed in chunks, and how to spot a stalled import.
- [[storefront-architecture]] — the search index read-side (why the storefront can lag after the import finishes).
- [[inventory-variant-model]] — `quantity_tracking` / `continue_sell` publish defaults map to the per-Variant stock model.

## Open questions

_None._
