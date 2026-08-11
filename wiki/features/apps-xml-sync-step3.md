---
type: feature
nav_path: "Apps → XML Sync → Step 3 (Operations & Rules)"
route_name: apps.xml_sync.step3
route_path: /admin/apps/xml_sync/step3/:id
aliases: ["XML Sync Step 3", "XML Sync operations", "XML Sync rules"]
tags: [apps, imports, xml, sync, operations, rules, wizard]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# XML Sync → Step 3 (Operations & Rules)

## Purpose

The **Step 3** wizard page is the **operations + rules stage** of the XML Sync wizard. Structurally similar to [[apps-xml-import-step3]] but with **additional options for recurring-sync behaviour**:
- What HAPPENS when a product is found in the feed.
- What HAPPENS when a product DISAPPEARS from the feed (was synced before, now missing).
- Conditional rules + transformations + default values.

The `:id` URL parameter is the sync task ID.

For the full feature set, see [[apps-xml-sync]].

## Where to find it

Sidebar → Apps → XML Sync → wizard → Step 3 (after Step 2). Route: `/admin/apps/xml_sync/step3/:id`.

## What the merchant can do here

### Sticky controls

- **Back** → returns to [[apps-xml-sync-step2]].
- **Save job** primary button → persists the operations + finalizes the task. The recurring sync becomes active per the configured interval.
- Loading spinner during save.

### Operations and Rules section

Beneath the *"Operations and Rules"* heading:

**Per-product operations**:
- **On match (existing SKU/ID)**: Update / Skip.
- **On new product**: Create / Skip.
- **On missing in feed [SYNC-SPECIFIC]**: Deactivate / Delete / Keep — the recurring-sync-only option for products that DISAPPEARED from the feed (supplier removed the SKU).

**Conditional rules**: same as XML Import Step 3 — filter conditions for which XML rows are processed.

**Per-field transformations**: same operators (string, numeric, date, conditional value mappings).

**Image handling**: same options (download vs hot-link, format filtering, duplicate detection).

**Default values**: same.

### What the merchant CANNOT do here
- Define new transformation operators (built-in set only).
- Run the task from this page — Save returns to settings list / status.
- Bypass plan-feature limits.

## Settings & fields

### Operations JSON structure

Saved on task:
```
{
  "on_match": "update",
  "on_new": "create",
  "on_missing": "deactivate", // sync-only
  "filters": [...],
  "transformations": {...},
  "image_handling": {...},
  "defaults": {...}
}
```

### Sync-specific options

| Option | Use case |
|---|---|
| **on_missing = deactivate** | Default — when supplier removes a SKU, the corresponding CloudCart product becomes inactive (hidden from storefront but data retained). |
| **on_missing = delete** | Permanently remove the product from CloudCart (aggressive cleanup). |
| **on_missing = keep** | Do nothing on disappearance (merchant's own data is preserved). |

This is the key strategic decision for recurring syncs. Most merchants choose `deactivate` to preserve order history while hiding out-of-stock items.

## Business rules

### Save job = task active for recurring sync

Clicking "Save job" persists the operations + activates the task at the configured interval. The merchant returns to [[apps-xml-sync-settings]] / [[apps-xml-sync-status]] to monitor.

### on_missing semantics matter

The `on_missing` choice has significant operational impact:
- **Deactivate** — safe default; preserves history.
- **Delete** — irreversible; only for trusted feeds where deletion is intentional.
- **Keep** — strict additive sync; the merchant manages removals separately.

### Step 3 references Step 2 mappings

Transformations / rules reference CloudCart fields by their Step 2 mapping. Changing Step 2 mappings may break Step 3 references — the platform should validate.

### Side effects on save
- Task's operations JSON is persisted.
- Task becomes triggerable on the configured interval.

### Permission
Standard apps permission scope.

## Related

- [[apps-xml-sync]] — XML Sync hub.
- [[apps-xml-sync-step2]] — preceding step (mapping).
- [[apps-xml-sync-settings]] — task list (parent).
- [[apps-xml-sync-status]] — per-task progress.
- [[apps-xml-import-step3]] — parallel step in one-time XML Import (no on_missing option).

## How it works (verified against backend)

### Missing-product default: KEEP (do nothing)

The merchant has a single binary opt-in flag `disable_missings` (Step 1, stored on the task's metadata). **Default is OFF** — products missing from a sync run are LEFT untouched in CloudCart. When the merchant enables it, missing-from-feed products are flipped inactive (and their variants zeroed out). There is **no built-in "Delete" mode**; the choice is Keep (default) or Deactivate.

### Same 7 fixed operations as XML Import — no custom code

The XML Sync module ships the same 7 operation types as XML Import — multiplication, partition, increment, decrement, has, split, yes/no. There is **no custom JavaScript / regex / PHP escape hatch**; the merchant picks one of the 7 per applicable field. See [[apps-xml-import-step3]] for the per-field availability table — XML Sync uses the identical operation set.

### No per-rule preview, no rule templates

Per the controller code: there is no preview endpoint that simulates a transformation on a sample row. The merchant tests by saving Step 3, letting the next scheduled (or manually-triggered) sync run, then inspecting affected products in [[apps-xml-sync-status]]. There's also no "save rule set as template" — operations are per-task.

### Save persists, next scheduled sync picks it up — Save toggle off+on triggers sooner

Save wraps the Step 3 update in a DB transaction and returns success. **No immediate-run side-effect**. However, the task's update hook clears the feed hash and re-initialises the parser queue, so the next queue tick re-parses this task even if the 12h timer hasn't elapsed. For a faster trigger the merchant flips the task's Active switch off and on from [[apps-xml-sync-settings]].

### Step 3 validates only `id` + `name` — broken references silently no-op

The only enforced validation at save is `id` and `name` required. Operation rules pointing at fields not mapped in Step 2 are persisted but do nothing at runtime — the field has no source value, so the transformation is skipped.

### "Re-activate returned products" opt-in (`active_disabled`)

A separate task-metadata flag `active_disabled` enables a **second** sync-specific behaviour: when a product that was previously deactivated re-appears in the feed with quantity > 0, the importer flips it back to active. Off by default. When ON and the merchant has linked XML Import tasks via `imports_active`, the reactivation is scoped to products that originated from those linked imports only — preventing reactivation of products from a different supplier feed.

### Save Step 3 deletes pending records + resets timestamps

Same behaviour as XML Import: `editStep3` clears `xml_hash`, `last_cron_update`, `last_cron`, and the pending parsed-records queue (`records->delete`). The new operations apply from scratch on the next queue tick.

### Step 3 fetch shows 3 sample products for verification

The Step 3 view fetches the feed and shows the merchant **3 sample parsed products** with their values mapped per the Step 2 mapping. The merchant can verify "yes, this is the data I expect" before saving the operations. The samples come from the start of the feed — not random — so dynamic feeds (newest-first) show the most recent products.

### Operations are evaluated in stored order, identical to XML Import

Operations persist as a serialised PHP array in the order the merchant entered them. The importer walks the array linearly per row. **Has** operations with `unsetRow` short-circuit the row entirely — dropped silently, not counted as failed. See [[apps-xml-import-step3]] for the per-field operation availability table; XML Sync uses the same set.

## Open questions

_None._
