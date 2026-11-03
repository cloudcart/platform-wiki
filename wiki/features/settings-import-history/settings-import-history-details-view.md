---
type: feature
nav_path: "Settings → Import history → Details tab"
route_name: product-list-details
route_path: /admin/settings/import-history/items/:id
aliases: ["Import history details tab", "Import history per-record view", "Import history records", "Per-job records"]
tags: [settings, import, history, details, records]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---

> Part of [[settings-import-history]]. See the hub for the other aspects (List tab, change-log modal, action states, storage / retention).

# Import history — Details tab

## Purpose

The Details tab opens when the merchant clicks any row (or per-action count cell) on the [[settings-import-history-list-view|List tab]]. It shows every individual record that the selected import job touched, the action applied per record, a compare-summary of which fields changed, and a per-row indicator into the field-by-field [[settings-import-history-change-log-modal|change-log modal]]. This is where the *"which products did the latest sync update?"* and *"why did SKU X fail?"* questions get answered at row resolution.

## Where to find it

Open from the [[settings-import-history|Settings → Import history]] hub by clicking any row on the List tab. The route is `/admin/settings/import-history/items/:id` where `:id` is the job identifier. Cells in the List tab that link here will additionally pre-populate the Action filter chip — clicking the *Errors* count opens this tab with `Action = Error` already set.

## What the merchant can do here

- See every record touched by the selected import, one row per record.
- Read the per-record action badge — see [[settings-import-history-action-states]] for the five action values.
- Open the per-record [[settings-import-history-change-log-modal|change-log modal]] for a field-by-field before/after diff.
- Filter by action (Created / Updated / Skip / Error / Pending / `processed`).
- Search across record name, compare-value, and the raw payload — see *Search scope* below.
- Save the current filter set under the `import-history / records` namespace.
- Paginate server-side through a job's records — scales to 100,000+ entries per job without loading the whole set into the browser.

What the merchant **cannot** do here:

- Retry a single failed row — there is no retry affordance.
- Edit the record's data — the merchant must navigate to the actual entity (product, category, customer, etc.) and edit there.
- Delete a row from history — see [[settings-import-history-storage-and-retention]].

## Settings & fields

### Per-record columns

| Column | What it shows |
|--------|---------------|
| **Name** | Product (or other entity) name plus thumbnail. Renders even for rows where the importer never matched an existing entity (the placeholder *"No name"* may appear — see [[settings-import-history-action-states]] for what that means). |
| **Action** | Badge: Created / Updated / Skip / Error / Pending. See [[settings-import-history-action-states]] for the full taxonomy. |
| **Compare info** | Summary of which fields changed for an Updated row, or which validation failed for an Error row. |
| **Change log** | Indicator that opens the [[settings-import-history-change-log-modal|change-log modal]] for the field-by-field diff. |

### Filter chips

The Details tab carries a filter bar above the table (`:filters="true"`). Three chip kinds:

- **Action** — multi-select chip with values `Created`, `Updated`, `Skip`, `Error`, `Pending`, `Processed`. `Processed` is synthetic: it returns *everything that is NOT Pending*. Pre-populated when the merchant clicks a per-action count cell on the List tab.
- **Search** — free text. Scope detailed below.
- **Save Filter** — the standard table-affordance to persist a chip combination. Scoped to `module: import-history, filter: records` — saved filter sets here will not bleed into unrelated table contexts.

### Search scope — richer than it looks

The search input scans more fields than just the visible Name. Specifically, the query matches against:

- The record's `name`.
- The `compare_value` — typically the import key (e.g. the SKU used to match against existing products).
- The raw payload's `data.name`, `data.app_import`, `data.variant.sku`, `data.variant.barcode`, `data.variants.sku`, `data.variants.barcode`.

Practical implication: a merchant chasing *"why did SKU X fail to import?"* can paste the SKU directly into the search box and find the row — **even when the importer never matched the SKU to an existing product**. A pending or errored row that has no `name` still exposes the SKU through the payload-fields search.

### Saved-filter namespace

The Details tab persists its saved filters under `module: import-history, filter: records`. The sister List tab uses `filter: tasks`. So the two tabs have independent saved-filter sets even though they live under the same module — saving a "show only errors" filter on the Details tab will not surface as a saved filter back on the List tab.

### Per-job action filter — the triage workflow

Combining Action = Error + a free-text search of the failing SKU + server-side pagination is enough to triage a six-figure import where most records succeeded but a handful need attention. The merchant doesn't need a separate query tool — Details is built for this triage path.

## Business rules

### Detail records live in a separate logging database

Per-record entries are stored in a separate logging database, not the main store database — see [[settings-import-history-storage-and-retention]] for why. Practical consequence: filtering and search apply server-side at the database level and remain responsive even on imports with 100,000+ records.

### Pagination is server-side

Both the List and Details tabs paginate at the DB level. A 100,000-record job does NOT return all entries to the browser — the Details tab loads one page at a time using the standard `Grid` page-size control.

### Pending rows appear only during in-flight imports

A record will show the `Pending` badge while the importer has reserved a placeholder row but has not yet processed it. On the next page refresh after the importer finishes, the row flips to its final action — see [[settings-import-history-action-states]] for the three-signal detection rule.

### No retry affordance

The Details tab is read-only audit. There is no per-row retry, no bulk-retry of failed records, and no in-page edit. To re-process records the merchant must fix the source data and re-run the import from the originator app — corrected CSV file, fixed XML feed, fixed ERP mapping, etc.

## Related

- [[settings-import-history]] — hub.
- [[settings-import-history-list-view]] — the tab that links here.
- [[settings-import-history-change-log-modal]] — the per-record drill-down opened from the Change log column.
- [[settings-import-history-action-states]] — the action badge taxonomy + how Pending is detected.
- [[settings-import-history-storage-and-retention]] — separate logging database + pagination scaling rationale.

## Open questions

None.
