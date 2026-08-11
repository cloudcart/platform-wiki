---
type: feature
nav_path: "Apps → XML Import → Tasks list"
route_name: apps.xml_import.settings
route_path: /admin/apps/xml_import
aliases: ["XML Import tasks", "XML Import list", "Xml Import settings"]
tags: [apps, imports, xml, tasks, list, plan-gated]
plan_gates: ["xml_import_limit", "xml_import_total_products"]
created: 2026-05-21
updated: 2026-06-10
source_count: 4
---
# XML Import → Tasks list (Settings)

## Purpose

The **Tasks list** (named "Settings" in the route map but actually the import-tasks list view) is where the merchant manages their XML Import tasks — create new ones, edit existing, monitor status at a glance, toggle Active, delete.

Each task represents one configured XML source: a publicly-fetchable feed URL (file upload is NOT supported — for non-URL sources use [[apps-csv-import]]) with a defined field mapping. The merchant can have multiple tasks (one per supplier) up to the plan's `xml_import_limit` cap.

For the full feature set, see [[apps-xml-import]]. This page covers only the list grid; the create/edit flow lives in [[apps-xml-import-wizard]] and per-task progress in [[apps-xml-import-status]].

## Where to find it

Sidebar → Apps → XML Import → **Settings tab** (the default — empty path child of `apps.xml_import`). Route: `/admin/apps/xml_import`.

## What the merchant can do here

### Tasks data table

Standard table with per-row data:

| Column | Source | Notes |
|---|---|---|
| **Name** (`TableColumns/Name`) | Task name / source identifier. | A red `fa-exclamation-circle` icon is suffixed when the task has a captured `error`; hover shows the full text ("URL return status code: 404", "CURL: Could not resolve host", etc.). 3 consecutive errors auto-deactivate the task — see [[apps-xml-import-fetch-transport]]. |
| **Statistics** (`TableColumns/Statistics`) | Two **live** counters queried at render time: **Remaining** (`records_count` — parsed but not yet inserted) and **Imported** (`imported_count` — products joined via `xml_import_id`). | Blank for tasks still in `draft` state. Progress is visible without drilling into Status. |
| **Date and time** (`TableColumns/DateAndTime`) | `last_cron_update` (last execution), formatted date + time; reads "Never" if NULL. | |
| **Switch** (`TableColumns/Switch`) | Active / Inactive toggle (controls whether the task can be triggered). | Re-checks the plan cap on activate — see Business rules. |
| **Actions** | Edit, Delete, View status. | |

The grid supports sorting on `id, name, records_count, imported_count, last_cron_update` (default: `id`, oldest first), a free-text `query` filter across the main columns, and filters `active` (boolean), `draft` (boolean), `last_cron_update` (date range, operators is/gt/gte/lt/lte/between/not_between).

### Draft status — task setup not finished

A newly-created task starts in **Draft** (`draft = 1`) — it exists but its setup wizard isn't finished (the final field-mapping / operations step hasn't been saved). A Draft task:

- **Does not run** — the background pipeline processes only completed tasks (`draft = 0`); Draft tasks are skipped by both the scheduled tick and any manual trigger.
- Shows a **"Draft"** label in the Active column instead of the on/off toggle, and its Remaining / Imported statistics are blank.
- Is matchable via the `draft` list filter.

Completing the wizard (saving the final mapping / operations step — [[apps-xml-import-step3]]) flips the task to `draft = 0`; only then is it active-eligible and runs on the next tick. A task stuck in Draft was started in the wizard but never finished — so it never imports anything.

### Add new task

**+ Add task** button → opens the 3-step wizard (Step 1/2/3). See [[apps-xml-import-wizard]] for the full field inventory and validation, and [[apps-xml-import-step2]] / [[apps-xml-import-step3]] for the per-screen detail.

### Edit existing task

Click a row → reopens the wizard pre-filled with the task's saved configuration (name, source URL, mapping, operation rules). Saving an edit clears the feed hash and forces a re-parse on the next tick — see [[apps-xml-import-wizard]].

### Switch toggle

Per-row Switch flips between Active / Inactive. Inactive tasks remain fully configured but cannot be triggered.

### Delete

Per-row delete with confirmation. Removes the task record and cancels its pending parsed-records queue. Historical imported products are NOT decremented from the `xml_import_total_products` counter — see [[apps-xml-import-side-effects]].

### What the merchant CANNOT do here
- Add or activate more tasks than the plan's `xml_import_limit` cap (the Add button / activate toggle returns HTTP 402 — see Plan gates).
- See the **next-run** time — it isn't exposed on the list; only the per-task [[apps-xml-import-status]] page shows it. Because one shared parser queue (`xml_import_parse`, every 12h) serves all tasks, the next-run timestamp would be identical for every row anyway.
- See per-task historical run details — drill into [[apps-xml-import-status]] for that.

## Settings & fields

### Per-task data shown on the list

| Field | Notes |
|---|---|
| **id** | Task ID (referenced in step2/step3/status routes). |
| **name** | Merchant-friendly identifier. |
| **source** | The feed URL. |
| **active** | Boolean flag (Switch). |
| **last_cron_update** | Last run timestamp (UPDATE — includes no-op runs). Distinct from `last_cron` (last successful fetch + parse); a row with `last_cron_update` set but no `last_cron` was touched by the parser but produced no records (typically an unreachable URL). |
| **records_count / imported_count / total_products / error** | Live per-run counters surfaced in the Statistics column. |
| **mapping / operations** | The configured field mapping + rules (wizard output). |

## Business rules

### Plan-gated task count

`xml_import_limit` caps the number of **active** tasks. Both *+ Add task* and turning a parked task's Active switch ON run the same plan-cap check; over cap returns HTTP 402 with *"You can have maximum {max} active tasks"*. Inactive tasks don't count against the cap, so a merchant can keep many parked tasks as templates and activate one at a time — see [[apps-xml-import-plan-gates]].

### Inactive tasks preserve state

Toggling a task to Inactive doesn't delete its mapping / operations — it just disables triggering, and clears its pending parsed-records queue. The merchant can re-enable later.

### Permission

Standard apps permission scope. Permission failures return the normal CloudCart auth error, not the 402 upsell.

## Plan gates

The Tasks list (Settings) screen enforces two of the app's plan-features (see [[plan-gates]], [[plan-vs-feature-pack]]):

| Mapping | Shape | What it controls on this screen |
|---|---|---|
| `xml_import_limit` | Numeric (max concurrent active tasks) | Caps how many tasks can be created / active. *+ Add task* and the per-row Active switch (ON) both run the plan-cap check — over cap returns HTTP 402 with *"You can have maximum {max} active tasks"*. |
| `xml_import_total_products` | Numeric (cumulative product cap) | Total products imported across all tasks (deletes don't decrement). Not enforced on the grid itself, but the per-row counts feed this global cap, surfaced on [[apps-xml-import-status]]. |

The app-install gate (`xml_import`) doesn't apply here — by the time the merchant reaches this list the app is installed. Full gating behaviour (402 modal, downgrade, feature-pack extension) lives in [[apps-xml-import-plan-gates]].

## Related

- [[apps-xml-import]] — XML Import hub.
- [[apps-xml-import-overview]] — Overview tab.
- [[apps-xml-import-wizard]] — the 3-step create/edit flow (Step 1 field inventory + validation).
- [[apps-xml-import-step2]] — wizard step 2 (mapping).
- [[apps-xml-import-step3]] — wizard step 3 (operations / rules).
- [[apps-xml-import-status]] — per-task progress, next-run, history.
- [[apps-xml-import-features]] — feature docs.
- [[apps-xml-import-fetch-transport]] — fetch rules + consecutive-error auto-deactivation.
- [[apps-xml-import-plan-gates]] — full 402 / cap behaviour.
- [[apps-xml-import-side-effects]] — delete / disable-missings side-effects.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.

## Open questions

_None._
