---
type: feature
nav_path: "Settings → Import history → Storage & retention"
route_name: import-history.settings
route_path: /admin/settings/import-history
aliases: ["Import history retention", "Import history the analytics store storage", "Import history cleanup", "Import history mapping codes", "Import history permission", "Import history pagination"]
tags: [settings, import, history, retention, the analytics store, storage, permission]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---

> Part of [[settings-import-history]]. See the hub for the other aspects (List tab, Details tab, change-log modal, action states).

# Import history — Storage and retention

## Purpose

Where Import history data lives, how long it is kept, why the merchant cannot delete rows from the UI, how the cross-importer view aggregates CSV / XML / JSON / ERP jobs into one table, and what permission scope gates access. The operational / housekeeping aspect — relevant to *"can we clean up old imports?"*, *"why is my history so long?"*, or *"why can't moderators see only their own imports?"* questions.

## Where to find it

The behaviours documented here are platform-wide and apply to the whole [[settings-import-history|Settings → Import history]] page — every row on every tab is governed by these rules. There is no separate sub-screen.

## What the merchant can do here

- See years of accumulated import history without any auto-cleanup.
- Filter and paginate through unbounded history (server-side, scales to 100k+ records per job).
- Recognise the source app of any past import via the **Name** column — the platform writes a human-readable name like *"Szamlazz - Daily sync"* rather than the internal `mapping` code.
- Read every staff member's imports — the history is store-scoped, not staff-scoped.

What the merchant **cannot** do:

- Delete a history row from the UI — there is no delete affordance anywhere on the page.
- Set a retention policy — there is no auto-cleanup config.
- Restrict moderators to "only my imports" — there is no per-staff filter.
- Restrict moderators to "only CSV imports" — there is no per-importer permission.

## Settings & fields

### Storage layer — a separate logging database

Both the per-job summary and the per-record detail entries live in a **separate logging database**, not in the main store database. Each import keeps one job-summary record plus one detail record per imported row. Two practical consequences:

1. The Details tab scales to 100,000+ records per import without bloating the main store database — see [[settings-import-history-details-view]] for the pagination rationale.
2. CloudCart support **cannot** clean up history rows with the standard store-database tooling — they must operate on the separate logging database directly.

### Retention — indefinite, no auto-cleanup

There is **no scheduled cleanup, no retention TTL, no expiration policy** on this surface. Past import jobs and their per-record detail rows accumulate **forever** — a merchant who has run daily imports for years sees years of history. Server-side pagination handles browse-time size; the storage footprint grows monotonically.

### No UI delete — an API route exists but is unexposed

A delete endpoint exists behind the scenes (`DELETE /admin/api/history/import/list/{id}`), but **no UI surface invokes it**. The merchant cannot delete history rows from any tab, modal, or contextual menu. All visible actions on the import-history surface are reads (index, list-by-type, listing, all-imports-type, view).

To prune old history a merchant must contact CloudCart support, who can either operate on the separate logging database directly or invoke the unexposed `DELETE` endpoint from an internal tool.

### Cross-importer aggregation — one table, many sources

All importer types share this history view. The platform tags each task with a `mapping` field identifying which importer produced it:

| `mapping` value | What it means |
|------------------|---------------|
| `xml_import` | XML feed import (one-shot upload). |
| `xml_sync` | XML feed sync (recurring). |
| `erp_imports` + `erp_imports_execute` | ERP integration imports (Szamlazz, FGO, FlixFacts, SmartBill, Profics, etc.). |
| `products_import_csv`, `customers_import_csv`, `blog_import_csv` | CSV bulk imports. |
| `products_import`, `customers_import`, `blog_import`, `redirects_import` | Programmatic / app-driven bulk imports. |

The **Name** column the merchant sees on the [[settings-import-history-list-view|List tab]] is **not** the raw `mapping` value — it's a display name computed from the linked app (e.g. *"Szamlazz - Daily sync"*, *"CSV products import 2026-05-20"*). The internal `mapping` code is hidden from the UI.

### Permission gate — standard Settings scope

There is **no per-importer permission and no per-staff permission** on this page. Access is governed by the merchant's general Settings permission scope. If a moderator can see the Settings menu and the Import History sub-page, they see ALL imports regardless of which originator app produced them (CSV, XML, ERP, etc.) and regardless of which staff member kicked them off.

**Per-staff isolation is not possible at this surface.** Merchants relying on per-staff accountability should restrict access at the originating app's screen instead (e.g. permission-gate CSV import per-staff). The history is a shared audit trail by design.

### Auto-refresh — none

Unlike [[settings-queue-view]], this page does **not** auto-refresh. The merchant manually reloads to see newly-completed imports. To watch progress live the merchant either reloads periodically or switches to [[settings-queue-view]] for the live queue view.

### Pagination — server-side, scales unbounded

Both the List view and the per-job Details view paginate server-side using the standard `Grid` page-size control with default sort `created_at desc`. A job with 100,000 record-level entries does not return all rows to the browser; the detail tab loads one page at a time. Filtering and search also apply at the DB level so they remain responsive on years-long histories.

## Business rules

### No staff filter — store-wide audit trail

Because the platform does not record which specific staff member ran a given import, every staff member with Settings permission sees the same shared history. Moderators cannot filter to *"only my imports"*. Merchants needing per-staff accountability must record initiator information externally (e.g. a note on the imported entities, or external workflow tracking).

### History never blocks new imports

Unbounded history accumulation has no effect on the merchant's ability to run new imports — no throttle by history count, no quota. The only practical cost of indefinite retention is logging-database storage on CloudCart's infrastructure, invisible to the merchant.

### Cleanup is a support-side operation

If a merchant explicitly wants old history removed (e.g. for a data-protection request, or because the table is unwieldy to browse), the only option is a CloudCart support ticket. Support can prune by date range, importer type, or job ID via direct operations on the logging database or the unexposed `DELETE` endpoint.

### The `mapping` code is the platform-internal identifier

Support and engineering use the `mapping` value to distinguish importer sources when diagnosing issues. The merchant sees only the friendlier display name. A ticket that says *"the XML sync isn't working"* should reference the **Name** as shown in the UI; support translates that to the underlying `mapping` value (`xml_sync`) internally.

### Permission applies to the page, not to rows

Once a staff member has access to the Settings → Import history page, they see **every row** in it. The permission is binary: whole history or none. There is no per-row, per-importer, or per-staff row-level filtering.

## Related

- [[settings-import-history]] — hub.
- [[settings-import-history-list-view]] — where the *Name* column surfaces the importer display name.
- [[settings-import-history-details-view]] — where logging-database-backed pagination + filtering scales to 100k+ records per job.
- [[settings-import-history-change-log-modal]] — per-record diff also stored in the separate logging database.
- [[settings-import-history-action-states]] — atomic count increments in the logging database keep the counts accurate during in-flight imports.
- [[settings-queue-view]] — sister page for live-running jobs; this is the surface that auto-refreshes.
- [[apps-csv-import]], [[apps-xml-import-settings]], [[apps-json-import]] — the importer screens whose `mapping` codes appear here.

## Open questions

None.
