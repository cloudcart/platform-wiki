---
type: feature
nav_path: "Apps → XML Import → Step 2 (Mapping)"
route_name: apps.xml_import.step2
route_path: /admin/apps/xml_import/step2/:id
aliases: ["XML Import Step 2", "XML Import mapping", "Xml Import field mapping"]
tags: [apps, imports, xml, mapping, wizard, plan-gated]
plan_gates: ["xml_import_limit"]
created: 2026-05-21
updated: 2026-05-28
source_count: 3
---
# XML Import → Step 2 (Field Mapping)

## Purpose

The **Step 2** wizard page is the **field-mapping stage** of the XML Import wizard. After Step 1 (AddOrEdit), where the merchant configured the source XML feed URL + basic metadata, this page is where they identify:
- Which XML tag represents a single product (the "repeating element").
- Which XML tags inside it correspond to CloudCart product fields (name, price, SKU, description, image URL, category, etc.).

The platform fetches a sample of the XML, parses it to discover the structure, and presents a tree of detected XML groups. The merchant maps each group to a CloudCart skeleton field. The result is a complete field-mapping JSON saved on the task.

The `:id` URL parameter is the task ID.

For the full feature set, see [[apps-xml-import]].

## Where to find it

Sidebar → Apps → XML Import → click on / create task → Step 2. Route: `/admin/apps/xml_import/step2/:id`.

## What the merchant can do here

### Sticky controls header

At the top, a sticky element (visible while scrolling) hosts:
- **Back** button → returns to AddOrEdit (Step 1).
- **Save and go to step 3** primary button → persists the mapping + advances to [[apps-xml-import-step3]].
- Loading spinner during save.

### Skeleton groups

Fields are organised into collapsible groups (e.g., "Product data", "Variants", "Properties"), collapsed by default and expanded individually. Each group lists its fields in a stable order.

### Per-field mapping

Within a group, each row pairs a **CloudCart field** label (e.g., "Product name", "Price", "SKU", "Stock quantity") with an **XML tag picker** — a dropdown of detected XML tags; the merchant picks the tag whose value should populate that field. Rows come in a few shapes: single value (price, stock), multi-value (categories list, tag list), and non-mapped header rows (group titles).

### What the merchant CANNOT do here
- Skip mandatory mappings — XML import refuses to save Step 2 with unmapped REQUIRED fields (e.g., product name, SKU).
- Map one XML tag to multiple CloudCart fields without explicit duplicate-support.
- Define new CloudCart skeleton fields here — the skeleton is platform-defined.

## Settings & fields

- **Persisted mapping** — saved on the task as a JSON mapping object (`{ <cloudcart_field_key>: <xml_tag_path>, ... }`), reused by the import pipeline on every run.
- **Sample parsing** — landing on Step 2 fetches and parses a sample of the feed to populate the tag dropdowns (may take a few seconds for large feeds); see [[apps-xml-import-mapping-fields]].
- **Step navigation** — Back returns to AddOrEdit (Step 1); Forward goes to [[apps-xml-import-step3]].

## Business rules

### Required fields validation

The CloudCart skeleton declares which fields are REQUIRED (typically: name, SKU, price). The merchant must map these or Step 2 won't save.

### Re-saving Step 2 invalidates Step 3

When the merchant changes the field mapping in Step 2, the operation rules in Step 3 may reference fields that no longer exist — the merchant typically re-validates Step 3 after major Step 2 changes.

### Side effects on save
- Task's mapping JSON is updated; Step 3 becomes accessible (or refreshes with new context).
- The feed hash + pending records are reset so the new mapping applies on the next parser tick — the full edit-clears-hash flow is in [[apps-xml-import-wizard]].
- Standard apps permission scope applies.

## Plan gates

The create-time `xml_import_limit` gate is enforced upstream (the task must already exist to reach Step 2). Flipping the task to Active later re-checks that cap — see [[apps-xml-import-settings]] — and the full product-import cap (`xml_import_total_products`) is enforced at the importer insert stage, not on Step 2 save. See [[plan-gates]], [[plan-vs-feature-pack]] for the gating model.

## Related

- [[apps-xml-import]] — XML Import hub.
- [[apps-xml-import-settings]] — task list (parent).
- [[apps-xml-import-step3]] — next step (operations / rules).
- [[apps-xml-import-status]] — per-task status after wizard completion.
- [[apps-xml-import-features]] — features docs.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.
- [[apps-xml-sync-step2]] — parallel step in XML Sync app.

## How it works (verified against backend)

This section covers only what is **specific to the Step 2 screen** — how detected XML paths are surfaced in the pickers. The deeper mechanics (which fields exist, the three variant patterns, category auto-creation, custom-field slots, the per-field Update strategy, image handling) live in [[apps-xml-import-mapping-fields]]; the create/edit flow that frames the three steps is [[apps-xml-import-wizard]].

### How the tag pickers are populated

When the merchant first lands on Step 2 the platform reads a preview window of the feed (the Step 1 `lines` field, `min:20`, `max:1500`) and parses the sampled rows into a flat list of XML path strings (e.g., `Product > Title`, `Product > Image[url]`). These paths populate the picker dropdowns. **There is no name-matching auto-suggest** — every CloudCart field starts unmapped and the merchant picks each path manually. Editing an existing task pre-fills the previously-saved mapping instead. The `lines` value is a structure-detection sample, **not** a cap on the import (the full feed is processed later — see [[apps-xml-import-mapping-fields]]).

### Path display rules in the picker

The picker renders each detected path with display conventions the merchant needs to recognise:
- **Preview text** — each path shows a value snippet found at that path, capped at **20 characters per occurrence** and deduplicated, so the merchant can confirm "yes, this is the title tag".
- **Repeated children collapsed** — numerically-suffixed siblings (`item_1`, `item_2`, `item_3`) collapse into a single `item_(1-n)` entry, so feeds that bind images as `image_1`, `image_2` map to the multi-value image field without 50 separate options.
- **Namespaces surfaced separately** — feeds using namespaces (Atom, Google Merchant) list each declared namespace combination as its own option, so a Google Merchant `<g:price>` appears as `g:price`.
- **Attribute bracket notation** — attributes appear as `[bracketed]` path segments (`Product[id]`). Common names (`name`, `id`, `title`, `type`, `currency`) also get a second option with the value inline (`Product[type=variant]`), letting the merchant filter on attribute value, not just existence.

### Choices on this screen that feed the rest of the wizard

Two Step 2 choices change later behaviour:
- **Variant pattern tabs are mutually exclusive** — the "Variants" group offers Multiple variants (`multilevel`) / Single variant (`singlelevel`) / Our template (`template`); choosing one drops the other two from the saved mapping, and switching tabs after a save loses the unchosen pattern's fields. What each pattern means is in [[apps-xml-import-mapping-fields]].
- **Per-field Update checkbox** — set here, it governs whether each field is refreshed on later parse ticks; the full update strategy (and the `updatable = 0` "load and forget" case) is in [[apps-xml-import-mapping-fields]]. The multi-value separator is **not** set here — it's a Split transform configured in [[apps-xml-import-step3]].

## Open questions

_None._
