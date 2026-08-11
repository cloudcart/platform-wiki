---
type: feature
nav_path: "Apps → XML Import → Wizard"
route_name: apps.xml_import.create
route_path: /admin/apps/xml_import (Step 1 + Step 2 + Step 3)
aliases: ["XML Import wizard", "XML Import — create task", "XML Import — 3-step flow", "Field mapping wizard", "XML Import — Step 1", "XML Import — Step 2", "XML Import — Step 3"]
tags: [apps, imports, xml, wizard, mapping]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-xml-import]]. See the hub for the other aspects (job pipeline, fetch transport, mapping fields, plan gates, side effects).

# XML Import — the 3-step wizard

## Purpose

The XML Import wizard is how the merchant turns a raw supplier XML feed into a configured task. Three steps walk the merchant from "here is a URL" to "this is the field mapping that will run every parse cycle". The wizard's output is a **task record** with URL, structure pattern, field-to-tag mapping, per-field update flags, and a handful of operational toggles — everything the parse / insert pipeline needs to process the feed unattended thereafter.

This page covers what each step asks for, what's optional, and how the mapping persists between re-parses. For the actual tags the wizard can MAP TO see [[apps-xml-import-mapping-fields]]; for what happens after Step 3 is saved see [[apps-xml-import-job-pipeline]].

## Where to find it

Apps → XML Import → **+ New task** button. Existing tasks are edited from the Status list — Edit reopens the wizard pre-populated with the saved mapping.

## What the merchant can do here

### Step 1 — URL + import-level toggles

The merchant points the integration at the feed and picks operational defaults:

- **Feed URL** — required, must be a valid HTTP/HTTPS URL. File upload is NOT accepted in this app (use [[apps-csv-import]] for files). See [[apps-xml-import-fetch-transport]] for the fetch rules.
- **Import type** — new products / update existing / both.
- **Track inventory** (`track_inventory`) — whether the imported `quantity` field is written to Variant stock. ON = quantity from XML applied (missing-or-zero = 0 stock); OFF = quantity ignored, merchant manages stock manually. See [[inventory-variant-model]] for what `quantity` means on a Variant.
- **Continue selling** (`continue_selling`) — copied to every imported product. See [[inventory-oversell]].
- **Disable missings** (`disable_missings`) — opt-in: when ON, products that previously came from this task but are no longer in the feed get deactivated automatically. OFF by default — feed-shrink doesn't touch the catalog. The platform looks up by "product was imported by THIS task AND its task-row ID is no longer in the current feed" and queues a disable-missings job.
- **Fixed category** (`category_id`) — when set, the XML's category mapping is IGNORED and every imported product lands in the chosen category. When blank, the wizard's category mapping (Step 3) drives placement.

### Step 2 — XML tag mapping

The merchant identifies which XML tag is the "product" (the repeating element that wraps each row) and maps tags to CloudCart fields:

- The platform reads a preview window of XML rows to surface the structure (the `lines` field — validated `min:20`, `max:1500` — controls how many rows the wizard scans to discover structure). This is NOT a cap on the import itself; the full import processes every record.
- Variant structural pattern is chosen here — multilevel / singlelevel / template — and stored on the task. See [[apps-xml-import-mapping-fields]] for what each pattern means.
- Each mappable field has a per-field **Update** checkbox. Only fields the merchant explicitly marks as "updatable" overwrite on subsequent re-parses. Unmarked fields keep their existing CloudCart values. This is how the merchant says "refresh prices every parse, but don't trample my edited descriptions".

### Step 3 — finalisation

The wizard collects the remaining configuration before persisting the mapping:

- **Category mapping** — when no fixed `category_id` is set, the merchant maps the XML's category tag to CloudCart category placement (auto-create paths on `>` separator; see [[apps-xml-import-mapping-fields]]).
- **Default tax / vendor** — applied per product when the field is unmapped.
- **Custom field assignments** — category properties, description tabs, supplier metadata. See [[apps-xml-import-mapping-fields]].

Saving Step 3 commits the task. The mapping is then reused on every re-parse cycle — see [[apps-xml-import-job-pipeline]].

## Settings & fields

The wizard writes to a single task record. Key fields:

| Field | Source | What it does |
|-------|--------|--------------|
| `url` | Step 1 | The XML feed URL. |
| `import_type` | Step 1 | new / update / both. |
| `track_inventory` | Step 1 | Whether `quantity` is written. |
| `continue_selling` | Step 1 | Copied to every imported product. |
| `disable_missings` | Step 1 | Opt-in deactivation of products no longer in feed. |
| `category_id` | Step 1 | Fixed category override; when set, XML category mapping is bypassed. |
| `lines` | Step 2 | Preview-window size (20–1500) for structure detection. |
| Structure pattern | Step 2 | `multilevel` / `singlelevel` / `template` variant pattern. |
| Field mapping | Step 2 | Per-field tag bindings + Update checkbox flags. |
| Category / tax / vendor | Step 3 | Finalisation. |

## Business rules

### Mapping persists per task

Once configured, the same mapping is reused on every re-parse — the merchant doesn't re-map every 12 hours. The mapping skeleton and operation rules are stored on the task record.

### Editing the task clears the feed hash + records

Editing the task URL, parameters, name or any Step 1/2/3 field resets `xml_hash` to NULL and clears `last_cron_update` — guaranteeing the next queue tick re-parses the feed even if the content hasn't changed. **Pending parsed records are also deleted** so stale data from a previous mapping doesn't get inserted under the new mapping. This is also how the merchant can force a re-run without waiting for the 12h tick — save Step 3 again, or toggle Active off/on.

### Per-field Update checkbox is the update strategy

Only the fields the merchant ticks as "updatable" in Step 2 are overwritten on subsequent re-parses. Matching of an existing product to its row uses the task's import ID + a per-row task key stored on the product — so re-imports correctly find and update the right row instead of duplicating.

### Step 1 `category_id` overrides Step 3 mapping

When the merchant sets a fixed `category_id` in Step 1, the XML's category tag is ignored — every product from the feed lands in that one category regardless of what Step 3 maps. This is for "the supplier feed is one product line; I know it belongs in this one category" cases.

### `disable_missings` only deactivates this-task products

The opt-in lookup is scoped to products previously imported by THIS task. Products from other tasks (or from manual entry) are never touched even if they happen not to be in the feed. See [[apps-xml-import-side-effects]] for the deactivation side-effects.

## Related

- [[apps-xml-import]] — hub.
- [[apps-xml-import-step2]] — screen-level documentation for Step 2.
- [[apps-xml-import-step3]] — screen-level documentation for Step 3.
- [[apps-xml-import-mapping-fields]] — what fields and structures the wizard can map.
- [[apps-xml-import-job-pipeline]] — what happens after Step 3 is saved.
- [[apps-xml-import-fetch-transport]] — fetch rules for the configured URL.
- [[apps-csv-import]] — alternative for non-URL sources.
- [[inventory-variant-model]] — how `track_inventory` interacts with the per-Variant `quantity`.
- [[inventory-oversell]] — what `continue_selling` does on each imported product.

## Open questions

_None._
