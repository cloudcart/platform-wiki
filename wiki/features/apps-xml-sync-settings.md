---
type: feature
nav_path: "Apps → XML Sync → Tasks list"
route_name: apps.xml_sync.settings
route_path: /admin/apps/xml_sync
aliases: ["XML Sync tasks", "XML Sync list", "Xml Sync settings", "XML Sync interval", "XML Sync every 20 minutes"]
tags: [apps, imports, xml, sync, recurring, tasks, list]
plan_gates: ["xml_sync_limit", "xml_sync-interval"]
created: 2026-05-21
updated: 2026-11-09
source_count: 5
---
# XML Sync → Tasks list (Settings)

## Purpose

The **Tasks list** is where the merchant manages their XML Sync tasks — create new ones, edit, monitor, delete. Each task represents one **recurring** XML source: a feed URL + mapping + operation rules. The run interval is store-wide, not per task (see "How it works").

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
- **Switch toggle** turns one task on or off (toast *Published* / *Unpublished*); a draft shows *Draft* instead.
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


## Business rules

### Plan-gated count

`xml_sync_limit` plan feature caps the number of active sync tasks.

### Inactive preserves config

An off task is skipped by the schedule and keeps its settings; its queued, not-yet-imported rows are dropped.

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

The cadence is the store's `xml_sync-interval` value (seconds, from the plan or a feature pack), shared by ALL sync tasks; the default is 12h. There is **no per-task interval picker**. The platform sets no lower limit, but a task read less than **1 hour** ago is skipped, so the same task re-syncs at most about hourly (never every 20 minutes). Per-plan values live in the plan catalogue (verify). Pipeline: [[apps-xml-sync-job-pipeline]].

### Manual trigger paths from the list

There is no "Run now" button. Two list-page side-effects force the next sync ASAP without waiting for the interval:
1. **Switch toggle** — flipping Active OFF → ON enqueues the parser at once, but a task read under an hour ago still waits for the 1-hour gate.
2. **Editing the task** — any update re-initialises the parser queue + clears the feed hash, so the next queue tick re-parses this task.

### Sortable list with active + last-run filters

Sorting on `id, name, records_count, imported_count, last_cron_update`. Filters: `query` (free text), `active` (boolean), `draft` (boolean), `last_cron_update` (date range).

### Delete cascade

Per-row delete drops the task plus its sync-import linkage rows. When no active task remains (after a delete or a switch-off), the sync schedule is removed; activating a task restores it.

### Statistics column: imported is DERIVED, not stored

The `imported_count` on each row is computed as `MAX(0, total_products - records_count)` — total products from the last successful parse, minus the live count of parsed-but-not-yet-inserted records. Tasks that haven't run yet (or produced zero records) show 0 imported.

### Error icon + tooltip surface the last failure inline

Tasks with a captured `error` (failed fetch, parse, or insert) get a red `fa-exclamation-circle` icon next to the name; hovering shows the text. Combined with 3-strike auto-deactivate (see [[apps-xml-sync]]), red icons turn into "Unpublished" rows after consecutive failures.

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

Unlike XML Import, XML Sync has NO Action picker (it only updates matched variants and never creates products), no "Publish imported products" toggle, no "Track inventory" / "Continue selling" toggles, and no Supplier / Parent / Task ID number fields.

**"Missing products" card (revealed after Validate XML):** two switches — **Disable missing products** (`meta.disable_missings`) and **Enable exists products** (`meta.active_disabled`), each with an optional **XML import** multi-select (`import_ids` / `import_active_ids`) that scopes the logic to products from linked XML Import tasks only (preventing cross-supplier deactivation/reactivation). Full discontinued + re-activation semantics are on [[apps-xml-sync-step3]].

Common errors surfaced inline at Validate: *"Unable to find search tag"*, *"Document is empty or is not valid XML"*, *"Unable to open url"*, plus the plan-cap message *"You can have maximum {max} active tasks"*.

## Open questions

_None._
