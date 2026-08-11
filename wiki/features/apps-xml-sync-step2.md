---
type: feature
nav_path: "Apps → XML Sync → Step 2 (Mapping)"
route_name: apps.xml_sync.step2
route_path: /admin/apps/xml_sync/step2/:id
aliases: ["XML Sync Step 2", "XML Sync mapping", "Xml Sync field mapping"]
tags: [apps, imports, xml, sync, mapping, wizard]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# XML Sync → Step 2 (Field Mapping)

## Purpose

The **Step 2** wizard page is the **field-mapping stage** of the XML Sync wizard — structurally identical to [[apps-xml-import-step2]]. The merchant:
- Identifies which XML tag represents a single product (repeating element).
- Maps each XML tag to its CloudCart product field.

The platform fetches a sample of the XML source, parses the structure, and presents a tree of detected XML groups + a per-field XML tag picker.

The `:id` URL parameter is the sync task ID.

For the full feature set, see [[apps-xml-sync]].

## Where to find it

Sidebar → Apps → XML Sync → wizard → Step 2. Route: `/admin/apps/xml_sync/step2/:id`.

## What the merchant can do here

### Sticky controls

- **Back** → returns to AddOrEdit (Step 1).
- **Save and go to step 3** → persists mapping + advances to [[apps-xml-sync-step3]].
- Loading spinner during save.

### Skeleton groups (collapsed cards)

Per-group `b-card` blocks (toggleable via `<details>`):
- **Group header** with title + expand/collapse toggle.
- **Within group**: field rows pairing CloudCart field + XML tag dropdown.

The `sortedSkeletons` data is grouped in stable order; per-group `maxHeight[index]` controls expansion state.

### Per-field mapping

Within a group, each row pairs:
- **CloudCart field** label (e.g., "Product name", "Price", "SKU").
- **XML tag picker** — dropdown of detected XML tags.

Row component variants (per the file structure: `Step2Item.vue`, `Step2Row.vue`, `OnlyRow.vue`, `Step2Header.vue`) handle different complexity:
- Single value (price, stock).
- Multi-value (categories, tags).
- Header (group title, non-mapped).

### What the merchant CANNOT do here
- Skip required mappings (name, SKU at minimum) — Step 2 won't save.
- Map one XML tag to multiple CloudCart fields without explicit duplicate-support.
- Define new CloudCart skeleton fields here.

## Settings & fields

### Persisted mapping

Saved on the task as `{ <cloudcart_field_key>: <xml_tag_path>, ... }` JSON. Used by the recurring sync job to extract values during each run.

### Sample parsing

When the merchant first lands on Step 2, the platform fetches a small sample of the source XML to populate the picker dropdowns. May take a few seconds for large feeds.

## Business rules

### Required-field validation

The CloudCart skeleton declares required fields (name, SKU, price at minimum). Step 2 won't save with unmapped required fields.

### Re-saving Step 2 may invalidate Step 3

When the merchant changes Step 2 mapping, the operation rules in [[apps-xml-sync-step3]] may reference fields that no longer exist — verify re-validation behaviour.

### Mapping persists across sync runs

Once saved, the same mapping is used for every recurring run. The merchant doesn't need to re-map on each sync.

### Permission
Standard apps permission scope.

## Related

- [[apps-xml-sync]] — XML Sync hub.
- [[apps-xml-sync-settings]] — task list (parent).
- [[apps-xml-sync-step3]] — next step (operations / rules).
- [[apps-xml-sync-status]] — per-task status.
- [[apps-xml-sync-features]] — features docs.
- [[apps-xml-import-step2]] — parallel step in one-time XML Import.

## How it works (verified against backend)

### Same XMLReader streaming parser as XML Import — handles huge feeds

The parser is shared between XML Import and XML Sync — it uses PHP's streaming XML reader to consume the feed node-by-node and stop after the requested sample size. The merchant controls the sample size via `lines` on Step 1 — validated `min:20, max:1500`. Even multi-GB feeds work because the parser never loads the whole document into memory.

### No auto-suggest, no presets, no clone-from-existing-task

Per the controller's `step2` method: when the merchant first opens Step 2 for a new task, ALL CloudCart fields start unmapped. The platform discovers XML paths in the sampled records and surfaces them in pickers — but there's **no name-matching heuristic** ("price" XML → CloudCart "price"), **no library of preset mappings** for known platforms (Woo / Shopify / BigCommerce), and **no "copy from existing task" action** in the UI. Editing an existing task preserves the prior mapping (it's stored serialized on the task row), so day-2 re-sync never re-maps.

### Variant pattern: two tabs, mutually exclusive

XML Sync's variant section exposes TWO patterns (vs three in XML Import — sync omits the "Our template" option):
- **Multiple variants** (`multilevel`) — nested `<options>` with name + values.
- **Single variant** (`singlelevel`) — flat per-product variant fields.

Choosing one drops the other from the saved mapping. Switching after save loses fields that belonged to the unchosen pattern.

### Save raises PHP's time limit to "no limit"

The Step 2 save endpoint runs `set_time_limit(0)` — long mapping payloads with many skeleton fields won't trip the 30-second PHP timeout. Useful when the merchant's task has 100+ category-property mappings (which the platform iterates serially during persist).

### "Update" checkbox = "this field can change on next sync"

The per-field Update checkbox (same UX as XML Import) marks which fields refresh on each recurring sync run. When NO field has Update checked, the task is `updatable = 0` — the next 12h tick still re-parses, but the importer treats it as create-only (existing matching products are left untouched). A common config: check Update on price + quantity + active, leave description / images unchecked → merchant's edits to product copy stick across syncs.

## Open questions

_None._
