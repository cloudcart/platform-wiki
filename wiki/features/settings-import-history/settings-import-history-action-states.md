---
type: feature
nav_path: "Settings → Import history → Action states"
route_name: import-history.settings
route_path: /admin/settings/import-history
aliases: ["Import history action states", "Created updated skip error pending", "Pending state import", "Processed synthetic filter", "Import action taxonomy"]
tags: [settings, import, history, actions, states, pending]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---

> Part of [[settings-import-history]]. See the hub for the other aspects (List tab, Details tab, change-log modal, storage / retention).

# Import history — Action states

## Purpose

Every record processed by every importer (CSV, XML, JSON, ERP) ends up in one of **five** action states, plus a synthetic *Processed* filter value that means "everything but Pending". These are the values the merchant sees on the badge column of the [[settings-import-history-details-view|Details tab]] and the count columns of the [[settings-import-history-list-view|List tab]]. Understanding the five states (especially Pending, which is the most misunderstood) lets the merchant interpret a running import correctly and use the page as a live-progress indicator.

## Where to find it

The action states appear in two surfaces of the [[settings-import-history|Settings → Import history]] page:

- As **count columns** on the List tab (one per state — Created, Updated, No action, Errors; Pending is not its own column but contributes to Total).
- As **badges** in the Action column of the Details tab, and as the values of the *Action* filter chip.

## What the merchant can do here

- Read the per-record action badge on the Details tab to know what the importer did to each record.
- Filter Details by any single action — Created, Updated, Skip, Error, Pending — or by the synthetic *Processed* (everything but Pending).
- Watch the Pending count tick down as a manual progress indicator while a job runs — see *Pending* below.
- On the List tab, click any of the four count cells (Created / Updated / No action / Errors) to deep-link into Details pre-filtered to that action — see [[settings-import-history-list-view]].

What action states **don't** let the merchant do:

- They are not a workflow — the merchant cannot move a row between states or "retry from Error to Created".
- They are not editable — the importer assigns each row's action at processing time and never re-evaluates it.

## Settings & fields

### The five action states

| State | What it means | Filter chip value |
|-------|---------------|--------------------|
| **Created** | Record didn't exist before, importer added it. Counted in the Created column on the List tab. | `Created` |
| **Updated** | Record existed, at least one field differed, importer wrote the new values. Counted in the Updated column. | `Updated` |
| **No action / Skip** | Record existed and the payload was identical to the current state — nothing to do. Counted in the No action column on the List tab; badge label is *Skip* on the Details tab. | `Skip` |
| **Error** | Importer couldn't apply this record. Reason is captured in the [[settings-import-history-change-log-modal|change-log modal]] (e.g. *"SKU already exists"*, *"Required field missing"*, *"VAT validation failed"*). Counted in the Errors column. | `Error` |
| **Pending** | Importer has *seen* the record (inserted a placeholder row in the log) but has not yet processed it. Appears only while the import job is in flight. | `Pending` |

Plus one synthetic value used only in the filter chip, never as a badge:

- **`Processed`** — synthetic shortcut meaning *everything that is NOT Pending*. Filters Details down to all rows the importer has actually touched, regardless of outcome.

### Total = processed + pending

The List tab's Total column is `processed + pending`. While an import runs, `processed < total` and `pending > 0`. Once the importer finishes, `processed = total` and `pending = 0`. There is no separate Pending count column on the List tab — pending is implicit in the gap between Total and the sum of the four visible columns.

### How Pending is detected — three-signal rule

The Details view identifies a record as Pending when **all three** of these conditions hold simultaneously:

1. `method = 'nothing'` — the importer hasn't decided yet whether the row will be Created / Updated / Skip / Error.
2. `relation_id` is empty — no underlying entity is linked yet.
3. `name = "No name"` — the platform's placeholder text used when the importer hasn't read enough of the payload to set a real name.

When all three are true the row is relabelled `pending` in the API response. On the next page refresh after the importer finishes the row, all three signals get rewritten with the real values and the badge flips to its final action.

### How the counts stay accurate while a job runs

Each importer bumps the running totals on the job row atomically as it processes each record — one increment per record into the matching counter (`created`, `updated`, `nothing`, `error`), plus a single increment of `total` if the row is new. These increments are guaranteed not to lose updates even when several workers process the same job in parallel. Practical consequence: the counts the merchant sees on the List tab are real-time accurate, not eventually-consistent estimates.

## Business rules

### Pending is real, not a UI quirk

A common merchant misunderstanding is treating Pending as an error or a stuck state. It is not. Pending simply means *the importer has reserved a row but hasn't processed it yet*. On a long import the Pending population shrinks as the worker grinds through the file. On a finished import there are no Pending rows.

### Skip is a success outcome

A Skip row means the importer scanned the record, compared the payload to the current state, found no differences, and correctly chose to do nothing. **Skip is not an error.** It indicates the importer is idempotent — running the same import twice the second run will be all-Skip.

### Action is assigned once, never re-evaluated

The importer writes the action when it processes the record. The platform does not later re-check whether an Error row would now succeed, or whether a Skip row would now have a diff. The state is historical. To check current state the merchant must re-run the import.

### `processed` chip vs Pending chip — opposite slices

The `Processed` synthetic chip and the `Pending` chip are complementary — together they cover the whole record set. There is no overlap and no gap. Selecting both at once is equivalent to clearing the Action filter.

### Re-running an import does NOT amend prior history

Re-running an import after fixing the source data creates a **new** history job with its own counts and per-record entries. The previous job's Pending / Error rows stay as they were. The merchant tracks "did we fix it?" by inspecting the new job's row counts, not by waiting for the old job's badges to change.

## Related

- [[settings-import-history]] — hub.
- [[settings-import-history-list-view]] — count columns that aggregate by action.
- [[settings-import-history-details-view]] — badge column + Action filter chip.
- [[settings-import-history-change-log-modal]] — where the per-row failure reason appears for Error states.
- [[settings-import-history-storage-and-retention]] — separate logging database; why the counts update atomically and why support cannot easily edit historical action values.
- [[settings-queue-view]] — sister page; while Pending shrinks on this view, the underlying worker is what [[settings-queue-view]] surfaces as a live process.

## Open questions

None.
