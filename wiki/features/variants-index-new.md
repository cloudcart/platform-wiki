---
type: feature
nav_path: "Products → Variants"
route_name: variants-index.new
route_path: /admin/products/variants
aliases: []
tags: [products, variants]
plan_gates: ["multi_variants", "variants.listing"]
created: 2026-05-21
updated: 2026-05-27
source_count: 8
---
# Variants

## Purpose

The Vue-based modern variants screen — same feature as [[products-variants-options]] but on the newer route (`/admin/products/variants` vs the legacy `/admin/products/parameters`). The legacy route (`admin.parameters.list`) now permanently redirects to this modern Vue route.

See **[[products-variants-options]]** for the full feature page covering:

- Variant parameter list + create wizard
- Six variant types (select, radio, image, color, 2d, numeric_alpha)
- Per-parameter values screen + Merge action
- Active toggle behaviour
- "Show as separate product in listing" paid feature + 24-hour throttle
- Hard cap of 3 parameters per product / 500 variants per product
- Validation rules (parameter names, numeric_alpha pattern, hex colour pattern)
- Delete protection, sort priority, rename cascade rules
- Side effects on save (search re-index, storefront cache flush)

## Where to find it

Products → Variants

## What the merchant can do here

See [[products-variants-options]] for the full feature description. This page is a pointer to the canonical documentation.

## Settings & fields

See [[products-variants-options]] — same backend, same fields.

## Business rules

See [[products-variants-options]] — same backend, same rules.

## Sub-screens

Distinct routes within this feature, captured from `vuejs-sitecp/` route files.

| Label | Route name | Route path |
|-------|------------|------------|
| Variants | `variants-index.new` | `/admin/products/variants` |
| Variants | `variants-list.new` | `/admin/products/variants` |
| Options | `variants-options.new` | `/admin/products/variants/options/:id` |

## Plan gates

Same gates as [[products-variants-options]] (this is the modern Vue surface of the same backend):

| Mapping | Shape | What it controls |
|---|---|---|
| `multi_variants` | Boolean | Whether variants are available on the plan. The `/admin/products/variants` URL is access-gated — without the feature the merchant cannot open the screen or the wizard. |
| `variants.listing` | Boolean | The "Show each variant as a separate product in the product listing" toggle. Without the feature, the toggle is locked behind the per-feature upsell. |

Behaviour: both gates redirect to plan-upgrade / pack-purchase panels (see [[plan-vs-feature-pack]], [[plan-features]]). See [[products-variants-options]] for the full feature description.

## Modern Vue surfaces — verified

### Main wrapper (`ProductsVariantsMainPage.vue`)

The page is a `CcSettingsWrapper` with:

- Header icon: `fas fa-sliders-v`.
- Header title: **Variants** + description *"Manage your variants"*.
- Single tab strip — **Variants** (always present) + **Values** (conditional, only when on `variants-options.new` route).
- Action button (top-right):
  - On `variants-list.new` → **+ Add variant** opens `ProductsVariantsWizard` modal.
  - On `variants-options.new` → **+ Add variant value** opens `ProductsVariantsOptionsCreateOrEditModal`.
- Layout is `large` on the list view, `medium` on the per-variant Values view.
- Sub-pages mount through `<router-view />`.

### Create-variant wizard (`ProductsVariantsWizard.vue` + 2 steps)

Clicking **+ Add variant** opens a large modal `CcPopup` titled "Create variant" with `ProductsVariantsWizardSteps` as the stepper. Two steps:

**Step 1 — `ProductsVariantsWizardCreateVariant.vue`** — General + Advanced settings.

| Section | Field | Notes |
|---|---|---|
| **General settings** (collapsible, open by default) | **Name** (`item.name`) | Required, column-style input. Validation comes from server (`errorStore.getError('name')`). |
| | **Option type** (`item.type`, radio) | Six types (per `useVariantParameterUi`): `select`, `radio`, `image`, `color`, `2d`, `numeric_alpha`. |
| | Info alert | *"Get more detailed information about creating product variants"* with help-article link. |
| **Advanced settings** (collapsible, closed by default) | **Show each variant as a separate product in the product listing** (`item.in_listing`, switch) | Paid feature. Toggle is DISABLED unless `feature.current` is truthy (= `variants.listing` plan-feature owned). When OFF (no feature), a **Paid** badge appears next to the label + a `CcWarning` block with *"See pricing"* button opens the `PlanFeature` upsell modal. |
| | **Include the variant name in the product title** (`item.show_label`, switch) | Only shown when `feature.current` is truthy (the slide-up wrapper). Visible only when the listing toggle is active. |
| | Warning text | *"... ensure that this option is enabled..."* — explains storefront implications of separate-listing. |

Bottom button: **Next** (saves the parameter via `apiVariants.create` / `apiVariants.update`, then advances to step 2). The Close button on the modal is disabled (`disableClose = true`) while the save is in flight.

**Step 2 — `ProductsVariantsWizardCreateOption.vue`** — set the variant's values.

Two branches by `data.type`:

- **`image` or `color`** → renders `ProductsVariantsWizardOptionRows` with a row-per-value editor where each row collects:
  - **Value Name** (`items[i].name`).
  - **Color sample** (HEX picker, default `#FFFFFF`) — only for `color` type.
  - **Image** (single image upload) — only for `image` type.
- All other types (`select`, `radio`, `2d`, `numeric_alpha`) → a `CcSelect` in **tags** mode with `create-option = true` — the merchant types option names and presses enter to commit each as a tag. Bound to `apiVariantOptions.autocomplete` for typeahead against the existing options of the parameter. No-results text: *"To add new start typing..."*.

Footer info alert: *"You can add or remove values later from the respective value list for this variant."*

Bottom buttons: **Back** (returns to step 1, parameter is already saved) + **Save** (POSTs the values via `apiVariantOptions(id).storeBulk` with FormData). On save, the wizard invalidates the variants list query so the row appears immediately. The wizard auto-closes 350 ms after save success (lets the success state render).

### Per-row inline edit modal (`ProductsVariantsCreateOrEditModal.vue`)

Clicking a row's **edit** action on the list opens a modal with the same field set as Step 1 of the wizard (Name + Option type radio + listing toggle + show_label toggle + paid feature warning). The edit modal is `CcModal` size `xl`, title **Edit** when editing or **Create new** when adding via this path. The Option Type radio is also editable here — changing the type after creation may have downstream consequences (see [[products-variants-options]] for type-change rules).

### Values screen — per-row delete + name edit

The `variants-options.new` route (`/admin/products/variants/options/:id`) renders the values list for one parameter. Uses table helper components:

| Helper | Renders |
|---|---|
| `ProductsVariantsTableName` | The value name (clickable to edit). |
| `ProductsVariantsTableBadgeType` | The variant type badge (Select / Radio / Image / etc.) shown on the parameter list. |
| `ProductsVariantsTableSwitch` | Per-row active toggle. |
| `ProductsVariantsTableButtonLink` | Per-row link out to per-parameter Values screen. |
| `ProductsVariantsTableDeleteRow` | Per-row delete. |

A **Merge values** flow (`ProductsVariantsMergeValues.vue`) is available for combining two values into one (preserves product links of both into the kept value). Full merge semantics: see [[products-variants-options]].

## Related

- [[products-variants-options]] — the canonical feature page (full content).
- [[products]] — parent hub.
- [[products-products]] — variant matrix lives on each product's edit page.
- [[plan-features]] — `variants.listing` paid-feature upsell modal.

## Open questions

(none — feature documented on [[products-variants-options]])
