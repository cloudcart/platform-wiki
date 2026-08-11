---
type: feature
nav_path: "Apps → XML Sync → Tasks list"
route_name: apps.xml_sync.settings
route_path: /admin/apps/xml_sync
aliases: ["XML Sync tasks", "XML Sync list", "Xml Sync settings"]
tags: [apps, imports, xml, sync, recurring, tasks, list]
plan_gates: ["xml_sync_limit"]
created: 2026-05-21
updated: 2026-05-27
source_count: 4
---
# XML Sync → Tasks list (Settings)

## Purpose

The **Tasks list** is where the merchant manages their XML Sync tasks — create new ones, edit, monitor, delete. Each task represents one **recurring** XML source: a feed URL + mapping + operation rules + interval. The interval is the key differentiator from [[apps-xml-import-settings]] — sync tasks rerun on schedule.

For the full feature set, see [[apps-xml-sync]].

## Where to find it

Sidebar → Apps → XML Sync → **Settings tab** (default empty path). Route: `/admin/apps/xml_sync`.

## What the merchant can do here

### Tasks data table

Standard table with per-row data (same column structure as [[apps-xml-import-settings]] plus a **Next execution** column):

| Column | Source |
|---|---|
| **Name** | Task name / source identifier. |
| **Statistics** | Created / Updated / Deactivated / Failed counts from the last run. |
| **Date and time** | Last execution. |
| **Next execution** | When the task is next scheduled (recurring). |
| **Switch** | Active / Inactive toggle. |
| **Actions** | Edit, Delete, View status. |

- **+ Add task** opens the AddOrEdit (Step 1) modal → 3-step wizard ([[apps-xml-sync-step2]] / [[apps-xml-sync-step3]]). See "AddOrEdit (Step 1) wizard" below for its fields.
- **Click a row** opens the wizard pre-filled (name, source URL, mapping, rules).
- **Switch toggle** flips Active / Inactive per row. Inactive tasks don't run on schedule but the config is preserved.
- **Delete** removes the task with confirmation (see the verified cascade below).

### Draft status — task setup not finished

A newly-created sync task starts in **Draft** (`draft = 1`) — it exists but its setup wizard isn't finished (the final field-mapping / operations step hasn't been saved). A Draft task:

- **Does not run** — the recurring pipeline processes only completed tasks (`draft = 0`); Draft tasks are skipped by both the scheduled tick and any manual trigger.
- Shows a **"Draft"** label in the Active column instead of the on/off toggle, and its statistics are blank.
- Is matchable via the `draft` list filter.

Completing the wizard (saving the final mapping / operations step — [[apps-xml-sync-step3]]) flips the task to `draft = 0`; only then is it active-eligible and syncs on the next tick. A task stuck in Draft was started in the wizard but never finished — so it never syncs.

### What the merchant CANNOT do here
- Add more sync tasks than the `xml_sync_limit` plan feature allows.
- Set a per-task interval — cadence is plan-wide (see below).
- Bypass plan gating.

## Settings & fields

### Per-task data

| Field | Notes |
|---|---|
| **id** | Task ID. |
| **name** | Merchant identifier. |
| **source** | Feed URL (HTTP/HTTPS only — see [[apps-xml-sync]]). |
| **active** | Boolean. |
| **last_execution** | When last run completed. |
| **next_execution** | When next scheduled run is. |
| **statistics** | Counts. |
| **mapping** + **operations** | Saved Step 2 + Step 3 output. |

There is no per-task `interval` field — cadence is plan-wide (see "How it works" below).

## Business rules

### Plan-gated count

`xml_sync_limit` plan feature caps the number of sync tasks. Lower plans = fewer tasks (typically 1-3); higher plans = many.

### Inactive preserves config

Toggling Inactive halts the recurring schedule but preserves everything for later re-activation. Recurring behaviour (vs one-time XML Import) and the full pipeline live on [[apps-xml-sync]].

### Permission
Standard apps permission scope.

## Related

- [[apps-xml-sync]] — XML Sync hub.
- [[apps-xml-sync-overview]] — Overview tab.
- [[apps-xml-sync-step2]] — wizard mapping step.
- [[apps-xml-sync-step3]] — wizard operations step.
- [[apps-xml-sync-status]] — per-task progress + run history.
- [[apps-xml-sync-features]] — features documentation.
- [[apps-xml-import-settings]] — parallel page in one-time XML Import.

## How it works (verified against backend)

### Cadence is plan-wide, not per-task

The recurring cadence comes from the `xml_sync-interval` plan feature applied to ALL the merchant's sync tasks (queue default 12h). There is **no per-task interval picker** and no Unix-cron entry anywhere in the list or wizard. The full pipeline (12h tick + per-task gate, shared `import1` queue, FIFO ordering, plan-priority) lives on [[apps-xml-sync]].

### Manual trigger paths from the list

There is no "Run now" button. Two list-page side-effects force the next sync ASAP without waiting for the interval:
1. **Switch toggle** — flipping Active OFF → ON enqueues the parser immediately.
2. **Editing the task** — any update re-initialises the parser queue + clears the feed hash, so the next queue tick re-parses this task.

### Sortable list with active + last-run filters

Sorting on `id, name, records_count, imported_count, last_cron_update` (same set as XML Import). Filters: `query` (free text), `active` (boolean), `draft` (boolean), `last_cron_update` (date range). Default sort is by `id`.

### Delete cascade

Per-row delete drops the task plus its sync-import linkage rows. The shared `xml_sync_parse` queue mapping stays in place — the next tick simply finds no active tasks (or only the surviving ones); the mapping is only torn down on app-level uninstall.

### Statistics column: imported is DERIVED, not stored

The `imported_count` on each row is computed as `MAX(0, total_products - records_count)` — total products from the last successful parse, minus the live count of parsed-but-not-yet-inserted records. Tasks that haven't run yet (or produced zero records) show 0 imported.

### Error icon + tooltip surface the last failure inline

Tasks with a captured `error` (failed fetch, parse, or insert) get a red `fa-exclamation-circle` icon next to the name; hovering shows the text. Combined with 3-strike auto-deactivate (see [[apps-xml-sync]]), red icons turn into "Unpublished" rows after consecutive failures — a breadcrumb back to root cause.

### AddOrEdit (Step 1) wizard — field inventory

The Add task / Edit task modal is the entry to the 3-step sync wizard. Three collapsible cards:

**"Create new XML job" card (always visible):**
| Field | Validation | Notes |
|---|---|---|
| **Job name** (`xml_sync.name`) | required | Merchant-friendly identifier. |
| **XML url** (`xml_sync.url`) | required, valid URL | Supplier feed URL. HTTP/HTTPS only — see [[apps-xml-sync]]. |
| **XML Product tag** (`xml_sync.product_tag`) | required | The repeating XML element wrapping a single product. |
| **Rows** (`xml_sync.lines`) | integer 20-1500 | Sample size for Step 2 structure detection. |
| **Validate XML and continue** button | — | Confirms URL reachability + tag presence and populates Step 2 dropdowns. |

**"Action" card (revealed after Validate XML succeeds):**
| Field | Options | Notes |
|---|---|---|
| **Compare by** (`xml_sync.product_map`) | `SKU` / `Barcode` / `Official ID` | Variant-match column. Must be NOT NULL on the variant — variants without it populated are silently skipped, even if their SKU is in the feed. |
| **Choose Fixed Discount type** (`xml_sync.discount_id`) | Optional select | Auto-apply a fixed-discount campaign to every synced product. |

Unlike XML Import, XML Sync has NO Action picker (sync is always update-existing + create-new), no "Publish imported products" toggle, no "Track inventory" / "Continue selling" toggles, and no Supplier / Parent / Task ID number fields.

**"Missing products" card (revealed after Validate XML):** two switches — **Disable missing products** (`meta.disable_missings`) and **Enable exists products** (`meta.active_disabled`), each with an optional **XML import** multi-select (`import_ids` / `import_active_ids`) that scopes the logic to products from linked XML Import tasks only (preventing cross-supplier deactivation/reactivation). Full discontinued + re-activation semantics are on [[apps-xml-sync-step3]].

Common errors surfaced inline at Validate: *"Unable to find search tag"*, *"Document is empty or is not valid XML"*, *"Unable to open url"*, plus the plan-cap message *"You can have maximum {max} active tasks"*.

## Open questions

_None._
