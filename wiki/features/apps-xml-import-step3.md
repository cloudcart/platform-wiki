---
type: feature
nav_path: "Apps → XML Import → Step 3 (Operations & Rules)"
route_name: apps.xml_import.step3
route_path: /admin/apps/xml_import/step3/:id
aliases: ["XML Import Step 3", "XML Import operations", "XML Import rules"]
tags: [apps, imports, xml, operations, rules, wizard, plan-gated]
plan_gates: ["xml_import_limit"]
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---
# XML Import → Step 3 (Operations & Rules)

## Purpose

The **Step 3** wizard page is the **operations + rules stage** of the XML Import wizard. After [[apps-xml-import-step2]] mapped XML tags to CloudCart fields, this page attaches **per-field transformations** — markup math, conditional replace, value-split, yes/no coercion — chosen from a fixed built-in operator set (e.g. "multiply price by 1.2 for markup", "skip the row when price = 0"). The output is saved on the task; when the import runs, each parsed XML row passes through these operations in order.

The `:id` URL parameter is the task ID. For the full feature set, see [[apps-xml-import]].

## Where to find it

Sidebar → Apps → XML Import → wizard → Step 3 (after Step 2). Route: `/admin/apps/xml_import/step3/:id`.

## What the merchant can do here

### Sticky controls header

At the top, sticky controls:
- **Back** → returns to [[apps-xml-import-step2]].
- **Save job** primary button → persists the operations + finalizes the task. The task becomes runnable.
- Loading spinner during save.

### Operations and Rules section

The main page section header is *"Operations and Rules"* — beneath, the merchant attaches **per-field transformations** chosen from a fixed set of built-in operators (markup math, conditional replace, value-split, yes/no coercion). Each operator targets one CloudCart field mapped in [[apps-xml-import-step2]]; the exact vocabulary and which operators each field type allows are in *How it works* below. The per-product Create / Update / Skip behaviour and the "deactivate products no longer in the feed" toggle are set earlier in the wizard, not here — see [[apps-xml-import-wizard]].

### What the merchant CANNOT do here
- Define new transformation operators beyond the platform's built-in set — there's no free-form regex, math expression, or custom script.
- Run the task from Step 3 — saving the job FINALIZES it; the merchant returns to [[apps-xml-import-settings]] (or [[apps-xml-import-status]]) to trigger / monitor.

## Settings & fields

The operations the merchant defines are persisted on the task as a serialised list and reused on every re-parse. Each entry binds one operator to one mapped field with its configurable parameter (multiplier, increment value, has-value, split character, etc.). The full operator vocabulary, per-field availability, and evaluation order are in *How it works* below.

## Business rules

### Save job = finalize task

Clicking "Save job" persists the operations + marks the task as ready-to-run. The merchant returns to [[apps-xml-import-settings]] to trigger or monitor. Saving also resets the feed hash and clears pending parsed records so the new operations apply from scratch on the next parser tick — the full edit-clears-hash flow is in [[apps-xml-import-wizard]].

### Step 3 references Step 2 mappings

Operations reference CloudCart fields by their mapping in [[apps-xml-import-step2]]. The only save-time validation is that the parent `id` and `name` are present — a rule pointing at a field that Step 2 no longer maps is stored silently and simply does nothing during the run (no source value to operate on).

### Permission
Standard apps permission scope.

## Plan gates

Step 3 has no plan-feature paywall of its own. It sits downstream of the create-time `xml_import_limit` gate, and the cumulative `xml_import_total_products` cap is enforced later at the importer insert stage when the parser runs — not on save. The full three-gate model is in [[apps-xml-import-plan-gates]].

## Related

- [[apps-xml-import]] — XML Import hub.
- [[apps-xml-import-step2]] — preceding step (mapping).
- [[apps-xml-import-settings]] — task list (parent).
- [[apps-xml-import-status]] — per-task status / trigger.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.
- [[apps-xml-sync-step3]] — parallel step in XML Sync app.

## How it works (verified against backend)

### Fixed operations vocabulary: 7 transformations

The platform ships **7 hard-coded operations** that the merchant chooses from per field:

| Operation | Behaviour | Configurable param |
|---|---|---|
| **Multiplication** | Multiplies a numeric value (markup, currency). | `multiplication` (default 1) |
| **Partition** ("Divided by") | Divides a numeric value (decimal/unit shift). | `partition` (default 1) |
| **Increment** | Adds a constant. | `increment` (default 0) |
| **Decrement** | Subtracts a constant. | `decrement` (default 0) |
| **Has** ("Check value") | On a value match, replace it / unset the field. | `has`, `has_action_complete` (replace/unset), `has_value` |
| **Split** | Splits a string into multiple values (tags, images). | `split` (default space) |
| **Yes / No** | Coerces yes/no/0/1/string into a boolean. | `has_action_yes_no`, `has_yes_no`, `yesno` |

### Per-field operation availability

The dropdown of operations is per-field — the platform restricts which operations apply to which field by data type:

| CloudCart field | Allowed operations |
|---|---|
| **Price** | multiplication, partition, has, increment, decrement |
| **Quantity** | has, increment, decrement |
| **Weight** | multiplication, partition, has, increment, decrement |
| **Tags** | has, split |
| **Images** | split, has |
| **Description / Text / SeoTitle / SeoDescription** | has |
| **Name / Newest / OnSale / Tracking / Shipping** | has, yesno (where boolean) |

So price gets math operations, tags/images get split + has, descriptions get conditional replace.

### No "save and run" button — Save persists, then the parser picks it up

The Save action persists Step 3 and returns success. **There is NO immediate-trigger side-effect on Save** — the parser job picks up the task on its next tick (12h base interval per [[apps-xml-import]]). Because saving Step 3 clears the feed hash and the pending parsed-records queue, the **next tick reprocesses the task even if the previous 12h window hasn't elapsed**, and the freshly-saved operations always apply from scratch — no stale operations from a prior save can hit already-parsed records. For an even faster trigger the merchant flips the Active toggle off and on from [[apps-xml-import-settings]]. The shared edit-clears-hash mechanic lives in [[apps-xml-import-wizard]].

### Existing operations are pre-filled on edit

When the merchant returns to Step 3 for an existing task, the platform returns the previously-saved operations payload. The form re-renders the same configuration the merchant left.

### No per-rule preview / no templates

There's no preview that returns "what would this row look like after this transformation". The merchant tests by saving Step 3, letting the parser re-run, then inspecting the resulting product. There's also no "save rule set as template" — operations live per-task and are not reusable across tasks.

### Operations are evaluated **in order** per row — first one wins for short-circuiting

Operations are stored in the order the merchant defined them, and the importer applies each one in that order while formatting a row. The **Has** operation can short-circuit the row entirely (dropping the product). So a "skip if price = 0" rule placed at the top of the list runs before any markup math — but if reordered later, the row could have its price multiplied first, never matching the original zero, and slipping through. Ordering matters.

### Dropped rows don't increment failed_count

When the **Has** operation drops a row, the row is **silently dropped, not counted as failed**. The merchant sees the row in the source XML but not in the imported catalog — and there's no error-log entry pointing at it. Useful for legit filters; surprising when a typo in the Has-value silently drops half the catalog.

## Open questions

_None._
