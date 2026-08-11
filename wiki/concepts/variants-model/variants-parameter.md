---
type: concept
nav_path: "Concept → Variants model → Parameter"
aliases: ["Variant Parameter", "Parameter entity", "Parameter definition", "Параметър", "Атрибут на вариант"]
tags: [catalog, variants, parameters, options, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[variants-model]]. See the hub for the other aspects (Option, matrix generation, pricing, inventory link, image mapping, known issues).

# Variants model — Parameter

## Definition

A **Parameter** is a **store-wide attribute definition** that names one customisation dimension of the catalogue — for example "Colour", "Size", "Material", "Voltage", "Storage". Parameters are catalogue dictionary entries, not per-product fields: one "Colour" Parameter is reused by every T-shirt, hoodie, and mug that uses colour. Created and managed from [[products-variants-options]] (Products → Variants in the admin sidebar).

A Parameter does NOT carry any sellable data — no SKU, no stock, no price. It only defines the dimension along which the catalogue can split into Variants. The sellable data sits on the per-product [[variant|Variant]] rows (see [[variants-matrix-generation]]).

## Scope

Covered here:

- The Parameter fields (name, display type, Active, sort priority, "Show in listing" premium).
- The 6 display types and the **locked-after-creation** rule.
- The deletion guard ("This parameter is used by products. Remove the products first.").
- Cascade renames — Parameter name changes propagate to every Variant denormalised label.
- The Active flag — soft-hide, preserves Variant data.

Not covered here:

- The **values** belonging to a Parameter — see [[variants-option]].
- How Parameters combine into per-product SKU rows — see [[variants-matrix-generation]].
- The 3-Parameter hard cap mechanics — see [[variants-matrix-generation]].
- The `variants.listing` plan-gated feature in depth — see [[plan-gates]].

## Contrasts

- **Parameter vs Option** — a Parameter is the dimension definition ("Colour"); an [[variants-option|Option]] is a value of that dimension ("Red"). Both are catalogue-level, but the Parameter contains the Options.
- **Parameter vs Property** — Parameters split SKUs (Variant); [[products-property|Properties]] are category-scoped descriptive specs that don't split SKUs. See the contrast section on [[variants-model]].
- **Parameter Active OFF vs deletion** — Active OFF hides the picker from storefront and product editors but **preserves** the Variant data on every product using it. Re-activating restores the picker without re-attaching Variants. Deletion is blocked while any product references the Parameter.

## Where it applies

Parameters surface on:

- [[products-variants-options]] — list view with name, Values count, Products count, Active toggle, Sort priority, Delete action. The Values count drills into the per-Parameter [[variants-option|Options]] sub-page.
- The product editor on [[products-products]] — flat picker to attach 1, 2, or 3 Parameters to that product. A 4th selection is rejected (see [[variants-matrix-generation]] for the cap).
- The storefront product detail page — each attached Parameter renders as a picker in its configured display type.
- The storefront category page — the storefront filter chips read from active Parameters.

### Merchant-controlled fields

| Field | Behaviour |
|-------|-----------|
| **Name** | "Colour", "Size", "Material", … 1–191 chars (validation: *"parameter must be between 1 and 191 characters long"*). Cascade-renames every Variant's denormalised `v1` / `v2` / `v3` label catalogue-wide. |
| **Display type** | One of 6 — Select option (dropdown), Radio button, Image sample, Colour sample, 2D schema, Numeric alpha. **Locked after creation.** |
| **Active** | yes / no. When `no`, the Parameter disappears from product editors and storefront pickers. Variants already using it keep their data. |
| **Sort priority** | integer. Controls the picker order on both the product editor and the storefront product page. |
| **Show in listing** (premium) | yes / no. Plan-gated by `variants.listing` — see [[plan-gates]]. When ON, each [[variant|Variant]] of products using this Parameter appears as a separate storefront category card. |

### The 6 display types

The Parameter's display type decides **three things at once**: what the customer sees on the storefront detail page, what fields appear on the Option-value form in admin, and which Value-name validation rules apply. The full reference (admin form per type, storefront DOM shape per type, CSS classes, examples) lives on [[products-variants-types]]. Short summary:

| Type | Customer-facing UI | Best for | Option fields |
|------|---------------------|----------|----------------|
| **Select option** (`select`) | Dropdown menu | Many values (10+), countries, languages | name only |
| **Radio button** (`radio`) | Row of radio buttons | 2–5 distinct options | name only |
| **Image sample** (`image`) | Row of image tiles | Patterns, fabrics, designs | name + image upload per Value |
| **Colour sample** (`color`) | Row of colour swatches | Colours | name + hex code per Value |
| **2D schema** (`2d`) | 2D `<table>` (X cols × Y rows) | Clothing measurements, room layouts | name + 2D coords per Value |
| **Numeric alpha** (`numeric_alpha`) | 2D `<table>` (X cols × Y rows) | Sizes with width+length axes (`36A`, `40B`) | name; pattern `<digits><letters>` enforced |

The display type is **locked after creation**. Switching from Select to Colour sample on a Parameter already attached to 50 products requires creating a new Parameter, re-adding its [[variants-option|Options]], detaching the old Parameter from every product, attaching the new one, re-setting Options on every Variant row, then deleting the old Parameter — a multi-hour migration. The merchant should pick the type carefully on first creation. The full per-type DOM, CSS classes, value-form fields, and validation rules are on [[products-variants-types]].

### Deletion guard

A Parameter cannot be deleted while any product still references it. The error reads *"product.parameters.parameter_used"* (merchant-facing message: *"This parameter is used by products. Remove the products first."*). Bulk-delete with some-used / some-unused entries deletes only the unused ones; used entries surface in the error.

### Cascade rename — name change propagates everywhere

When the merchant edits a Parameter's name (e.g., "Colour" → "Color"), the platform updates the denormalised column header on every product editor + every storefront product page + every Variant's denormalised label. The rename is atomic on save and **cannot be partial** — there is no per-product override of the Parameter name.

### Parameter Active OFF — soft hide

Setting Active = OFF removes the Parameter from storefront variant pickers and the product editor. Variants on every product that uses it remain intact — their data is preserved. Re-activating restores the picker without re-attaching Variants. Useful during a Parameter-type migration: hide the old Parameter while populating the new one without destroying historical Variant data.

## Related

- [[variants-model]] — hub.
- [[variants-option]] — values belonging to one Parameter.
- [[variants-matrix-generation]] — how Parameters combine into per-product Variant rows + the 3-Parameter cap.
- [[products-variants-types]] — full reference for the 6 display types: admin form per type + storefront DOM shape per type + CSS classes + cross-Parameter limits.
- [[products-variants-options]] — the catalogue-wide management screen.
- [[products-products]] — the product editor that attaches Parameters to a product.
- [[product-detail]] — the storefront detail page where each Parameter's picker renders in its configured type.
- [[products-property]] — Properties (descriptive, NOT a Variant Parameter).
- [[products-options-overview]] — Product Options (customer-input customisations, NOT a Variant Parameter).
- [[plan-gates]] — `variants.listing` premium feature.

## Open Questions

None.
