---
type: feature
nav_path: "Products → Properties → Create property wizard"
route_name: categories.property.create
route_path: /admin/category/property/create
aliases: ["Create property", "Add property", "Property wizard", "New property", "Edit property modal"]
tags: [products, properties, wizard, create, taxonomy]
plan_gates: ["category_properties"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-property]]. See the hub for the other aspects (list view, categories, values, merge, business rules, programmatic access).

# Properties — create wizard

## Purpose

The 3-step guided modal the merchant uses to define a new property end-to-end: property details (name + type + image) → categories to attach it to → option values. After step 3 the property is fully usable on products in the chosen categories and (if "Use as filter" is on) on the storefront filter sidebar.

The same field set — without the step indicator — drives the **Edit property modal** opened when the merchant clicks an existing property's name in the [[products-property-list-view|list]].

## Where to find it

Sidebar → Products → **Properties** → **+ Add property**. The wizard opens at `/admin/category/property/create` as an `lg`-sized popup over the list page. The X (close) button is **disabled while a save call is in flight**.

## What the merchant can do here

- Define a brand-new property in one guided pass.
- **Skip** the categories step (select zero categories — the API call is skipped and the wizard advances).
- **Skip** the values step (select zero values — the bulk-create call is skipped).
- **Cancel** between steps — each step's save call is independent; already-created records persist (so cancelling at step 2 leaves an empty property in the list that the merchant can edit later).
- Re-open the wizard from a category context — when launched from the per-category property-attach flow, the category ID is pre-populated in step 2.

## Settings & fields

The wizard has 3 steps + a success screen. Each step renders inside the same `lg` popup; the progress bar at the top reads "STEP 1 / 2 / 3" with labels *Property settings*, *Choose categories*, *Set property values*.

### Step 1 — Property settings

Two cards. **General settings** card:

| Field | Notes |
|-------|-------|
| **Property name** | Required. Free text. Max **191 characters** (server-side). |
| **Option type** | Visual radio cards — **Checkbox** or **Range** — with inline SVG previews. Locked after create (see [[products-property-business-rules]]). |
| **Range decimal places** (Range only) | Integer 0–5. Controls how the slider displays decimals (1 → 5.0–7.0; 2 → 5.00–7.00). Defaults to 2 when null at read time. Slider step auto-derives: `0.01` for 2, `0.1` for 1, `1` for 0. No manual step override exposed. |

**Advanced settings** card:

| Field | Notes |
|-------|-------|
| **URL** (URL handle) | URL slug for the filter parameter. Prefixed with `{host}/category/{category_url}?` on screens > 992 px wide. Must be unique across properties. |
| **Category Property Image** | Optional logo-section uploader with a Delete button. Some themes display this image next to the property name on the filter sidebar. |

Only a **Next** button at the bottom (no Back — it's step 1). The save call POSTs `multipart/form-data` with `name`, `type`, `url_handle`, `dec_points` (if Range), and `image` (if uploaded).

### Step 2 — Choose categories

Single tag-mode multi-select labelled *"Add categories to which the property is applied"* — searches `/admin/api/core/product-categories/search` as the merchant types.

Info banner: *"You can add or remove categories later from the respective category list for this property."*

**Back** and **Next** buttons. Selecting zero categories is allowed — the API call is skipped and the wizard advances.

### Step 3 — Set property values

A `createOption=true` tag-mode select labelled *"Type and press enter to create one or multiple options"*. The merchant types each value and presses Enter to chip it.

Info banner: *"You can add, remove and setup more details like image, description and advanced SEO settings for each value from the values list for this property."*

For Range-type properties this step still appears but the merchant typically skips it (Range filters use min/max from product data at runtime — see [[products-property-business-rules]]).

**Back** and **Save** buttons. Saving zero values is allowed.

### Success screen

A confirmation panel. On dismiss the list page invalidates and the new property appears in the table.

## Business rules

- **Each step's save is independent.** A cancelled wizard at step 2 leaves an "empty" property in the list — the merchant can re-edit it later from [[products-property-list-view]].
- **Wizard local state is preserved within a page lifecycle** — closing and reopening the wizard on the same list page restores the current step, property ID, selected categories, and draft values.
- **Plan-gated entry.** The wizard URL `/admin/category/property/create` is access-gated by the `category_properties` plan-feature key. Without it, the merchant is redirected to `/admin/plan/feature/category_properties` for the per-feature upsell. The list page itself remains visible (existing properties stay manageable), but the **+ Add property** flow is the gated entry point. See [[products-property-api]] for the plan gate detail.
- **Property type is locked after creation.** To switch a property's type, the merchant must create a new property and migrate products. See [[products-property-business-rules]].
- **Edit property modal uses the same field set** — clicking a property name in the list opens an `xl`-sized **Edit property modal** with the same shape as step 1, no step indicator, fields pre-loaded from the property record. Title reads *"Edit property"* or *"Create new property"* when launched outside the wizard.

### Validation strings

- **Property name** max length: **191 characters** (server-side).
- **Image upload over plan storage cap**: *"You have reached your storage limit"* — the check counts the image size **twice** (original + generated thumbnail).
- **Range type with non-numeric existing values**: *"There are values to the property which are not a number"* — fires when converting an existing property to Range with non-numeric option values present (in practice this is only reachable via [[products-property-api]] since the wizard locks type at create).

## Related

- [[products-property]] — hub.
- [[products-property-list-view]] — the page that launches the wizard.
- [[products-property-categories]] — same Categories-search endpoint used in step 2.
- [[products-property-values]] — step 3 creates option values; the Values sub-page edits them.
- [[products-property-business-rules]] — type-lock, name length, image storage cap.
- [[products-property-api]] — plan gate, JSON-API v2 equivalent for create.
- [[products-categories]] — categories being attached.
- [[settings-files]] — property images stored here.
- [[plan-vs-feature-pack]] — pack-vs-upgrade decision when the gate redirects.

## Open questions

None.
