---
type: feature
nav_path: "Products → Variants → Values → Merge values"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: ["Merge values", "Merge variant values", "Merge variant options", "Consolidate variant values", "Обединяване на стойности", "Обединяване на разновидности"]
tags: [products, variants, values, options, merge]
plan_gates: ["multi_variants"]
created: 2026-07-09
updated: 2026-07-09
source_count: 2
---

> Part of [[products-variants-options]]. See the hub for the other aspects (list table, values, wizard, types, listing toggle, data model, API).

# Variants — Merge values

## Purpose

**Merge values** consolidates two or more variant option values into a single survivor value, store-wide. It is the tool for cleaning up a duplicated or fragmented value list — collapsing "Red", "red" and "Reds" into one "Red", or unifying two sizing schemes into one. Unlike a rename, a merge **also rewrites past order history** and **deletes** the merged-away values, so it is a permanent catalogue-hygiene operation, not a cosmetic edit.

## Where to find it

Sidebar → Products → **Variants** → click the **Values** count on a parameter row → **Merge values** button at the top of the values table (opens the Merge values modal). See [[products-variants-values]] for the surrounding page.

## What the merchant can do here

- Consolidate two or more variant values into one survivor value, store-wide.
- Merge values that belong to **different parameters** — this re-parameterises the affected variants (see Business rules).
- Retire an in-use value that a plain delete would block, by merging it into a survivor.

## Settings & fields

The Merge values modal has two pickers, both autocompleting **store-wide across every parameter** (each result is labelled `Parameter: Value`, e.g. "Colour: Red", "Size: M"):

- **Primary / target value** (required, single-select) — the **survivor**. Everything merged collapses INTO this value.
- **Values to merge** (required, multi-select) — the values that will be reassigned to the survivor and then **deleted**. Each must be different from the target.
- Help text: *"Select the values you want to be merged with the target value. After merging, the selected value(s) will be replaced with the target value"*.

The **Merge** button enables only when a target and at least one value-to-merge are chosen. On success: toast *"Values merged successfully"*.

## How the merge works

For **each** value being merged into the survivor, the platform runs — in a transaction per value:

1. **Finds every variant** that uses the merged value — across any of the up-to-three variant axes a product can have.
2. **Reassigns those variants to the survivor** — the variant's value becomes the survivor value, and the product's parameter on that axis becomes the **survivor's parameter** (this is what makes cross-parameter merges possible — see Business rules).
3. **Rewrites past orders** — every historical order line that recorded the old parameter + value is updated to the survivor's parameter + value. A customer's old invoice will now show the survivor value.
4. **Re-syncs search** — the affected products are queued for a storefront search-engine reindex.
5. **Redirects external-integration mappings** — any external-metadata mapping for the merged value (e.g. a marketplace / feed integration that had mapped that option) is repointed to the survivor value.
6. **Deletes the merged value** — the old option is removed from the parameter.

If a single value fails partway, it is returned with an error naming that value; values already processed stay merged.

## Business rules

### Merging is permanent and rewrites order history

The merge is **irreversible**. Beyond reassigning live variants, it updates the parameter + value on **every past order line** that bought the merged value, so historical invoices and order-history reporting change retroactively. This is the deliberate difference from a rename: use **Merge** (not rename) when the goal is to retroactively unify a value across order history. The merged-away values are **deleted**, not hidden.

### Cross-parameter merge re-parameterises the variants

Because both pickers autocomplete **store-wide** (every parameter's values, labelled `Parameter: Value`), the survivor and the merged values can belong to **different parameters**. When they do, the merge doesn't only change the value — it **moves the affected variants onto the survivor's parameter**: a variant that was "Colour = Red" becomes "Shade = Crimson" if "Colour: Red" is merged into "Shade: Crimson". This is useful for consolidating two parameters that drifted apart, but it is easy to trigger by accident when the merchant picks a same-named value from the wrong parameter. **Confirm both sides are the intended parameter before merging.**

### Merge is the sanctioned way to remove an in-use value

A plain value delete is blocked while any variant still uses the value (see [[products-variants-data-model]]). Merge is the supported path to retire an in-use value: it reassigns the variants to the survivor first, then deletes the old value — so it succeeds where a direct delete is protected.

### Rename does NOT do what merge does

Renaming a value (or a parameter) via the edit modal cascades to live variants but does **not** touch past order lines and does **not** delete or consolidate anything. If the merchant only wants to relabel going forward, rename; if they want to collapse duplicates and fix history, merge. Same semantics as the property-value merge ([[products-property]]).

## Related

- [[products-variants-options]] — hub.
- [[products-variants-values]] — the values sub-page that hosts the Merge button.
- [[products-variants-data-model]] — value delete-protection that merge bypasses by reassigning first.
- [[products-variants-wizard]] — parameter edit / rename that (unlike merge) does not cascade to order history.
- [[products-property]] — sister system with the same merge semantics + "permanent" caveats.

## Open questions

None.
