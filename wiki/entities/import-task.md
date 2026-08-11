---
type: entity
aliases: ["Import task", "Import job", "Bulk import", "Background import", "CSV import job", "XML sync run", "Импорт", "Импорт задача", "Качване от файл", "Масов импорт"]
tags: [settings, ops, imports, csv, xml, entity, background-jobs]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---
# Import Task

## Identity

An **Import Task** is the per-import audit record + background-processing state for a single bulk-data load the merchant kicked off — uploading a CSV of products / customers / redirects / blog articles / subscribers, configuring or running an XML supplier feed sync, pushing data via JSON, or letting an ERP integration (Szamlazz, FGO, SmartBill, Profics, FlixFacts, Frisbo, etc.) pull a batch of records into the store. Every Import Task carries the **type** (which entity is being imported), the **source filename** or feed URL, the merchant's **field-mapping** (which CSV column → which CloudCart field), a **status** that walks the task through queue → processing → done, **per-record action counts** (Created / Updated / No-action / Errors / Total), and the **creator** (which admin user launched it).

An Import Task is the merchant's **single source of truth for "what happened during my import"** — both while it runs (live progress in [[settings-queue-view]]) and forever afterwards (historical audit on [[settings-import-history]] with per-record drill-in and a "View detailed change log" modal showing before/after values for every field that changed). The platform tags every record it creates / updates from the Task with a **provenance hint** so the merchant can later filter the affected entities via the **"Imported with"** filter on [[products-products]] / [[customers]] / etc. — this is the merchant's primary cleanup tool after a botched import because there is **NO undo / rollback** for any import.

An Import Task is distinct from the in-admin **bulk actions** (e.g., bulk-archive on [[orders]], bulk-update on [[products-inventory]]) that act on EXISTING records and run synchronously — those don't produce Import Tasks. It is also distinct from data **EXPORT** operations (the opposite direction, also async but tracked separately).

## Aliases

- **Import task** — the canonical platform term used in the admin UI, support tickets, and queue diagnostics.
- **Import job** — informal phrasing used in [[settings-queue-view]] tooltips and merchant-facing docs.
- **Bulk import** / **Background import** — emphasises the async + queue-based nature.
- **CSV import job** / **XML sync run** — type-specific phrasings.
- Bulgarian: **Импорт** (standard), **Импорт задача**, **Качване от файл**, **Масов импорт** — used interchangeably in the BG admin.

## Key Attributes

The Import Task is a multi-faceted record split across **six well-scoped aspects**. The AI Assistant should drill into the aspect that matches the question, not read every page.

## Sub-pages (in this cluster)

- [[import-task-attributes]] — the full per-field schema: type, source filename / feed URL, field mapping (per-Task, NOT reusable), status enum, processed-rows counter, action counts (Created / Updated / No-action / Errors), Started-at / Finished-at timestamps, Created-by user, queue, wizard-step persistence for resume, provenance tag written on every imported record.
- [[import-task-lifecycle]] — the six statuses (Pending-wizard, Pending-queued, Processing, Completed, Failed, Cancelled), the store-wide single-import lock that blocks parallel imports, HTTP 409 *"There cannot be more than {N} imports running simultaneously."*, what happens after completion (indefinite retention, no auto-cleanup), and the lack of a "retry failed rows" affordance.
- [[import-task-types-and-queues]] — the importer families (customer CSV, product CSV, product XML one-time, XML sync recurring, JSON, blog CSV, multilang, ERP / app-specific like Szamlazz / FGO / SmartBill / Profics / FlixFacts / Frisbo) + their dedicated queues (`import1`, `import2`, app-specific) + plan-feature gates (`customer_import`, `xml_import_limit`, `xml_sync_limit`, `xml_sync-interval`) + customer CSV's 2FA requirement.
- [[import-task-processing-model]] — chunked 500-row processing (50-row sub-chunks for ERP customer CSV), upsert-by-default behaviour (no "create only" / "update only" toggle), validation handling matrix (silent skip vs counted error vs abort), file-format constraints (csv / txt only, delimiter auto-detect, UTF-8 expected, header-row toggle, plan-capped row limit).
- [[import-task-provenance-and-recovery]] — the provenance tag written on every imported record (`app_import` for CSV products, `xml_import_id` / `xml_import_product_id` / `xml_import_name` for XML, app-specific fields for other integrations), the **"Imported with"** filter on [[products-products]] / [[customers]], and the three recovery paths after a botched import (bulk-delete via filter, restore from [[backups-and-restore]], run a corrective Task) — there is NO undo button.
- [[import-task-history-and-webhooks]] — indefinite retention on [[settings-import-history]] (no TTL, no auto-cleanup, no DELETE endpoint), Site-scoped shared history (every staff sees every Task, NO per-staff filter), the absence of `import.completed` / `import.failed` webhook events, and per-record webhook fan-out (`product.updated` / `customer.created` etc. fire on every row).

## Where it appears

- [[settings-queue-view]] — live in-flight queue progress; the Task's `processing` rows are visible here.
- [[settings-import-history]] — historical audit trail; per-Task aggregate counts + per-record drill-in + change-log modal.
- [[customers-import]] — source screen for customer CSV Tasks (2FA-gated).
- [[apps-csv-import]] — source screen for product CSV / Excel Tasks.
- [[apps-xml-import]] — source screen for one-time product XML import Tasks.
- [[apps-xml-sync]] — source screen for recurring product XML sync Tasks.
- [[apps-json-import]] — source screen for JSON-format Tasks.
- [[apps-blog-csv-import]] — source screen for blog-article CSV Tasks.
- [[products-products]] — "Imported with" filter finds all products tagged with a specific Task ID.
- [[customers]] — equivalent filter for customers from a specific Task.
- [[apps-multilang]] — multilang sync Tasks (translation + copy) run as Import Tasks too.

## Related

### Related entities

- [[product]] — most imports target products; imported products carry `app_import` / `xml_import_id` provenance.
- [[customer]] — customer CSV Tasks create / update customers; 2FA-gated.
- [[variant]] — product imports map onto variants too (per-SKU stock / price / barcode).
- [[subscriber]] — subscriber CSV imports create subscriber records.
- [[blog-article]] — blog CSV imports.
- [[site]] — Tasks are Site-scoped; the single-import lock is per-Site.
- [[staff-member]] — the admin who launched the Task (recorded but not filterable).
- [[queue-job]] — the underlying queue infrastructure that runs the Task.

### Cross-cutting concepts

- [[import-pipeline]] — the platform-wide bulk-import pipeline this Task belongs to. Single-import lock, chunked processing, validation handling, provenance tagging, indefinite retention — all live there.
- [[backups-and-restore]] — last-resort recovery when an import goes wrong.
- [[plan-gates]] — `customer_import`, `xml_import_limit`, `xml_sync_limit`, `xml_sync-interval` plan-features gate which Task types are available.
- [[notification-delivery]] — `file_download` admin alerts surface on related aggregate downloads (export side).
- [[settings-hooks]] — per-record webhooks fire as each row is processed (no Task-level events).

## Open Questions

Distributed to aspect pages. See:

- [[import-task-lifecycle]] — the exact behaviour when a merchant cancels a Task mid-flight: rows already processed appear to be KEPT, but the merchant-visible state of the temp table (cleaned up vs orphaned) needs verifying.
- [[import-task-provenance-and-recovery]] — whether the "Imported with" filter on [[products-products]] is granular to the Task ID or the source-app type — affects how usefully the merchant can scope cleanup.
