---
type: concept
nav_path: "Concept → Import pipeline → Upsert & provenance"
aliases: ["Import upsert", "Import provenance tags", "Imported with filter", "app_import", "xml_import_id", "Per-record import tagging", "Import match by identifier"]
tags: [ops, imports, upsert, provenance, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[import-pipeline]]. See the hub for the other aspects (stages, concurrency lock, validation, plan gates + 2FA, history + recovery, XML Sync).

# Import pipeline — upsert & provenance

## Definition

Most importers in CloudCart operate in **upsert mode**: if a row's identifier matches an existing record, the existing record is **updated**; otherwise a **new** record is created. The match identifier varies by entity — `email` for customers, `sku` / `barcode` / `product.id` for products. Only mapped columns are touched on an update; unmapped fields keep their current values.

Every record created or updated by an importer is also tagged with **provenance** — a marker pointing back to the source task. Products carry `app_import = 'csv-{taskId}-<source>'` (CSV imports) or `xml_import_id` + `xml_import_product_id` + `xml_import_name` (XML imports); other entities carry similar source hints. The provenance enables the **"Imported with" filter** on [[products-products]] — the merchant's primary cleanup tool when a botched import needs to be reversed.

## Scope

Covered:

- Upsert match-by-identifier semantics per entity (customer email, product SKU / barcode / id).
- "Only mapped fields touched" rule on updates.
- Provenance fields written by each importer (`app_import`, `xml_import_id`, etc.).
- The "Imported with" filter on [[products-products]] for finding all records from a task.
- The asymmetry — provenance filtering exists for products, NOT for customers (verify).
- Field-mapping persistence: per-task only, no reusable presets.

Not covered here:

- The wizard step where columns are mapped — see [[import-pipeline-stages]].
- Per-field update policies on [[apps-xml-sync]] — see [[import-xml-sync-recurring]].
- How "no undo" interacts with provenance for cleanup — see [[import-history-and-recovery]].

## Contrasts

- **Upsert vs create-only vs update-only** — most importers do upsert. There is NO "update only" or "create only" toggle on most importers — the upsert is the default behaviour. Merchants who want to ONLY add new (skip existing) typically filter the source data to exclude existing identifiers before upload.
- **Per-task mapping vs reusable preset** — the column-to-field mapping is stored on the task row itself for resume support, but there is NO "save this mapping for next month's import" affordance. Each new import starts from scratch. Workaround: keep the source spreadsheet with the SAME column order across imports.
- **Products provenance vs customer provenance** — the "Imported with" filter is currently implemented on [[products-products]] only. Customers list does NOT have an equivalent one-click filter today (verify).

## Where it applies

Provenance and upsert apply during **Stage 4 — Background processing** ([[import-pipeline-stages]]). Each row is matched against the existing data set; if matched, fields are updated; if not, a new record is created with the provenance tag set.

### Match identifiers per entity

- **Customers** — email match (case-sensitive exact) updates the customer; otherwise creates new. Only mapped fields are touched; un-mapped fields keep their current values. So a partial CSV (just `email, note`) updates the note on matching customers and leaves everything else alone.
- **Products** — match column is configurable (`sku`, `barcode`, `product.id`); same upsert pattern. [[apps-xml-sync]] also offers per-field update policies (always update / update if delta < N% / never update) — see [[import-xml-sync-recurring]].
- **Other entities** — varies per importer; most match by a stable identifier (slug, external ID, etc.).

### Provenance fields per importer

- **Products via CSV** — `app_import = 'csv-{taskId}-<source>'` is set on each imported product.
- **Products via XML import / sync** — `xml_import_id` (the task ID), `xml_import_product_id` (the source-feed identifier), `xml_import_name` (the feed's product name) are set on each imported product.
- **Customers via CSV** — import-source fields are set on the customer record (verify per importer).
- **Other entities** — carry similar provenance hints depending on the importer.

### The "Imported with" filter

The "Imported with" filter on [[products-products]] takes a task ID (or task name) and returns all products created or last-updated by that task. The merchant uses it for:

- **Bulk cleanup** after a botched import: filter to the task ID, select-all, bulk-delete.
- **Verification** that the import created the expected products: filter and count.
- **Bulk re-edit** of imported products if the source data needs a follow-up change.

The filter is currently implemented on **[[products-products]] only** — not on the Customers list. Merchants who need to find / clean up imported customer records do so via the [[settings-import-history]] audit log (showing task details) plus manual customer-search criteria; there is no equivalent one-click "filter all customers from task X" surface on the Customers list today (verify).

### Field-mapping persistence — per-task only

The merchant's column-to-field mapping is stored on the task row itself, NOT as a reusable preset. Practical consequences:

- The merchant CAN re-open a paused import (modal closed mid-wizard) and the mapping is retained.
- The merchant CANNOT save the mapping as a template for future imports — each new task starts from scratch.
- **Workaround**: keep the source spreadsheet (CSV) with the SAME column order across imports. The mapping is then identical each time and the merchant only spends a few seconds re-picking it.

[[apps-xml-sync]] tasks are slightly different — once a sync task is configured, it reuses its mapping for every scheduled run; the merchant doesn't re-map every 12-hour pull. See [[import-xml-sync-recurring]].

### Update vs create — most importers do both

There is no "update only" or "create only" toggle on most importers — the upsert is the default behaviour. The merchant who wants to ONLY add new (skip existing) typically does it by filtering the source data to exclude existing identifiers before upload. Conversely, the merchant who wants to ONLY update existing typically maps just the fields they want to change and accepts that any new rows will be created (then deletes them via the "Imported with" filter).

### Example — re-running with corrected data

1. Merchant runs a 500-row product CSV import. 487 succeed, 13 fail with "category not found".
2. Merchant fixes the source CSV — corrects the category slugs on the 13 failing rows.
3. Merchant re-uploads the SAME 500-row CSV.
4. Upsert kicks in: the 487 previously-imported products match by `sku` and are updated (with the same data, so effectively no-op). The 13 previously-failed rows now match the corrected categories and are created.
5. Both runs are visible in [[settings-import-history]] with their own task IDs and `app_import` provenance markers.

## Related

- [[import-pipeline]] — hub.
- [[import-pipeline-stages]] — the Map step where columns are wired to identifier fields.
- [[import-xml-sync-recurring]] — per-field update policies and recurring upsert.
- [[import-history-and-recovery]] — recovery via the "Imported with" filter + bulk delete.
- [[products-products]] — hosts the "Imported with" filter for products.
- [[product]] — Product entity; carries `app_import` / `xml_import_id` provenance.
- [[customer]] — Customer entity; carries import-source metadata.
- [[import-task]] — entity page for the import-task record.

## Open Questions

- Confirm the exact customer-side provenance fields and whether a filterable surface exists on the Customers list.
