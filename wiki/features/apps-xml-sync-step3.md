---
type: feature
nav_path: "Apps → XML Sync → Step 3 (Operations & Rules)"
route_name: apps.xml_sync.step3
route_path: /admin/apps/xml_sync/step3/:id
aliases: ["XML Sync Step 3", "XML Sync operations", "XML Sync rules"]
tags: [apps, imports, xml, sync, operations, rules, wizard]
plan_gates: []
created: 2026-05-21
updated: 2026-10-21
source_count: 3
---
# XML Sync → Step 3 (Operations & Rules)

## Purpose

The **Step 3** wizard page is the **operations + rules stage** of the XML Sync wizard. It is the same screen as [[apps-xml-import-step3]]: a list of rows, each picking a mapped field, one of the operations offered for that field, and the operation's value. What happens to products that disappear from the feed is not set here — it is the **Disable missing products** switch on Step 1 (see [[apps-xml-sync-discontinued]]).

The `:id` URL parameter is the sync task ID.

For the full feature set, see [[apps-xml-sync]].

## Where to find it

Sidebar → Apps → XML Sync → wizard → Step 3 (after Step 2). Route: `/admin/apps/xml_sync/step3/:id`.

## What the merchant can do here

### Sticky controls

- **Back** → returns to [[apps-xml-sync-step2]].
- **Save job** primary button → persists the operations, takes the task out of draft and returns to the task list. An active task is picked up by the next sync run.
- Loading spinner during save.

### Operations and Rules section

Beneath the *"Operations and Rules"* heading:

Each row has three parts:
- **Field** — one of the fields from [[apps-xml-sync-step2]] that has operations.
- **Operation** — one of the operations offered for that field (the same 7 as XML Import: Multiplication, Divided by, Increment, Decrement, Check value, Split, Yes / No).
- **Value** — the operation's own setting (for example the multiplier).

The ✕ at the end of a row removes it; **Add new row** appears once the last row is complete.

### What the merchant CANNOT do here
- Define new transformation operators (built-in set only).
- Run the task from this page — Save returns to settings list / status.
- Bypass plan-feature limits.

## Settings & fields

### Saved operations

The rows are saved on the task in the order shown and applied in that order on every sync run (see *How it works* below).

### Missing-product handling is on Step 1

Step 3 has no option for products that disappear from the feed. Step 1 has two switches, both off by default: **Disable missing products** (products missing from the feed are made inactive — never deleted) and **Enable exists products** (inactive products that are back in the feed with stock are made active again). See [[apps-xml-sync-discontinued]].

## Business rules

### Save job = task active for recurring sync

Clicking "Save job" persists the operations and takes the task out of draft; an active task is picked up by the next sync run. The merchant returns to [[apps-xml-sync-settings]] / [[apps-xml-sync-status]] to monitor.

### Step 3 references Step 2 mappings

Transformations / rules reference CloudCart fields by their Step 2 mapping. Changing Step 2 mappings may break Step 3 references — the platform does not check them (see *How it works* below).

### Side effects on save
- The task's operations are saved and the task leaves draft.
- The feed hash and the pending parsed records are cleared, so the next sync run processes the whole feed with the new operations.

### Permission
Standard apps permission scope.

## Related

- [[apps-xml-sync]] — XML Sync hub.
- [[apps-xml-sync-step2]] — preceding step (mapping).
- [[apps-xml-sync-settings]] — task list (parent).
- [[apps-xml-sync-status]] — per-task progress.
- [[apps-xml-import-step3]] — the same step in XML Import; this page is built on it.
- [[apps-xml-sync-discontinued]] — missing-product handling (Step 1).

## How it works (verified against backend)

### Missing-product default: KEEP (do nothing)

The merchant has a single binary opt-in flag `disable_missings` (Step 1, stored on the task's metadata). **Default is OFF** — products missing from a sync run are LEFT untouched in CloudCart. When the merchant enables it, missing-from-feed products are flipped inactive — only products that track stock and do not allow selling when out of stock, and only when none of their variants still in the feed has stock; quantities are not changed. There is **no built-in "Delete" mode**; the choice is Keep (default) or Deactivate.

### Same 7 fixed operations as XML Import — no custom code

The XML Sync module ships the same 7 operation types as XML Import — multiplication, partition, increment, decrement, has, split, yes/no. There is **no custom JavaScript / regex / PHP escape hatch**; the merchant picks one of the 7 per applicable field. See [[apps-xml-import-step3]] for the per-field availability table — XML Sync uses the identical operation set.

### No per-rule preview, no rule templates

Per the controller code: there is no preview endpoint that simulates a transformation on a sample row. The merchant tests by saving Step 3, letting the next scheduled (or manually-triggered) sync run, then inspecting affected products in [[apps-xml-sync-status]]. There's also no "save rule set as template" — operations are per-task.

### Save persists, next scheduled sync picks it up — Save toggle off+on triggers sooner

Save wraps the Step 3 update in a DB transaction and returns success. **No immediate-run side-effect**. However, the task's update hook clears the feed hash and re-initialises the parser queue, so the next queue tick re-parses this task even if the 12h timer hasn't elapsed. For a faster trigger the merchant flips the task's Active switch off and on from [[apps-xml-sync-settings]].

### Step 3 save is not validated — broken references silently no-op

Saving checks only that the task still exists; the rows are not validated (a row without a field is skipped, and a row whose operation the field does not offer is dropped). Operation rules pointing at fields not mapped in Step 2 are persisted but do nothing at runtime — the field has no source value, so the transformation is skipped.

### "Re-activate returned products" opt-in (`active_disabled`)

A separate task-metadata flag `active_disabled` enables a **second** sync-specific behaviour: when a product that was previously deactivated re-appears in the feed with quantity > 0, the importer flips it back to active. Off by default. When ON and the merchant has linked XML Import tasks via `imports_active`, the reactivation is scoped to products that originated from those linked imports only — preventing reactivation of products from a different supplier feed.

### Save Step 3 deletes pending records + resets timestamps

Same behaviour as XML Import: `editStep3` clears `xml_hash`, `last_cron_update`, `last_cron`, and the pending parsed-records queue (`records->delete`). The new operations apply from scratch on the next queue tick.

### No sample preview on screen

Opening Step 3 also reads up to 3 products from the start of the feed, but the screen does not show them — there is no sample preview. The merchant checks the result after the next sync run in [[apps-xml-sync-status]].

### Operations are evaluated in stored order, identical to XML Import

Operations persist as a serialised PHP array in the order the merchant entered them. The importer walks the array linearly per row. **Has** operations with `unsetRow` short-circuit the row entirely — dropped silently, not counted as failed. See [[apps-xml-import-step3]] for the per-field operation availability table; XML Sync uses the same set.

## Open questions

_None._
