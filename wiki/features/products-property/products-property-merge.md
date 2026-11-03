---
type: feature
nav_path: "Products → Properties → Merge values"
route_name: category-property-values
route_path: /admin/products/property
aliases: ["Merge values", "Merge property values", "Consolidate property values", "Property value merge"]
tags: [products, properties, values, merge, taxonomy, irreversible]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[products-property]]. See the hub for the other aspects (list view, wizard, categories, values, business rules, programmatic access).

# Properties — merge values

## Purpose

The action that consolidates two or more property option values into a single survivor value. Used to clean up typos and duplicates ("Color: Red" + "Colour: Reds") and to collapse semantically equivalent values that drifted apart over time (e.g., legacy imports producing "16 GB" + "16GB" + "16gb").

The merge re-points every product currently tagged with a merged-out value to the survivor, deletes the merged-out value records, and fires a storefront search re-index. **The action is irreversible.**

## Where to find it

Sidebar → Products → **Properties** → click the **Values** count for a property → **Merge values** button. The button is on [[products-property-values]].

## What the merchant can do here

- Pick a **primary value** (the survivor).
- Pick **one or more values to be merged** into it.
- Merge across **different parent properties** — the merchant can collapse "Color: Red" and "Colour: Reds" (typo in another property) into a single survivor.

## Settings & fields

Opens as an `md`-sized modal.

| Field | Notes |
|---|---|
| **Select a primary value** | Required. The survivor. Single-select autocomplete sourced from `/admin/api/core/properties/{id}/values/merge-autocomplete`. |
| **Select values to merge** | Required, ≥ 1. Tag-mode multi-select from the same endpoint. These records are deleted after the merge. |

Help text: *"Select the values you want to be merged with the target value. After merging, the selected value(s) will be replaced with the target value."*

Footer buttons: **Cancel** + **Merge**. Merge stays disabled until both a primary and at least one merge value are picked.

## Business rules

### The merge is irreversible

Once committed, the merged-out values are gone — the merchant cannot undo without manually recreating the value records and reassigning products. This is the single most important rule to communicate before the merchant clicks **Merge**.

### Step-by-step effect (verified)

1. Re-points every product currently tagged with a merged-out value to the survivor.
2. If a product was tagged with **both** the survivor and a merged-out value, the platform deletes the merged-out tag (no duplicate per-product entries).
3. Carries over any external-integration metadata (e.g., the value's mapping in [[apps]] / OLX feeds) to the survivor — see [[apps-olx-parameters-values]] for the OLX side.
4. Deletes the merged-out value records.
5. Fires a search-engine re-sync for every affected product so the storefront filter immediately reflects the new value assignments — see [[products-property-api]] for the side-effect plumbing.

### Transactional — partial merges cannot occur

The entire sequence runs inside a database transaction. Either every step succeeds or the merge rolls back. So a failure mid-flow leaves the data exactly as it was before — there is no half-merged state to clean up.

### Cross-property merging is allowed

Both the **primary value** and the **values to merge** can come from different parent properties. This is intentional — it's the merchant's tool to fix taxonomy drift where the same physical attribute ended up under two properties (e.g., a legacy import created "Material" while a newer import created "Materials").

When the merge crosses properties, the resulting per-product values are attached to the **survivor's** parent property — products that referenced the merged-out value via the OTHER property are now tagged under the survivor's property instead.

### Deduplication when a product had both

If product X was tagged with the survivor AND a merged-out value, the merge does **not** create a duplicate per-product entry. The merged-out tag is dropped; the survivor stays.

## Related

- [[products-property]] — hub.
- [[products-property-values]] — the page that launches the merge.
- [[products-property-business-rules]] — broader irreversibility / data-flow rules.
- [[products-property-api]] — the same ES re-sync runs for API-initiated merges.
- [[apps-olx-parameters-values]] — OLX value mappings carried over on merge.
- [[products-products]] — products affected by re-pointing.

## Open questions

None.
