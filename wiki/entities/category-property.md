---
type: entity
aliases: ["Category Property", "Property", "Product property", "Category-bound property", "Specification", "Spec", "Filter (category)", "Категорийна характеристика", "Спецификация", "Характеристика", "Филтър"]
tags: [catalog, products, properties, filters, specifications, taxonomy, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 4
---

# Category Property

## Identity

A **Category Property** is a category-scoped descriptive specification — a structured attribute (e.g., *"Has Bluetooth: yes/no"*, *"Screen size: 5.0–7.0 inches"*, *"Material: Cotton / Polyester / Wool"*) that the merchant attaches to one or more [[category|Categories]] so it **auto-applies to every [[product|Product]] in those categories**. Each Property carries a name and a type (Checkbox for discrete categorical values, Range for continuous numeric ones); Checkbox types also carry a set of allowed option values. Once attached to a Category, the Property appears on the product editor for every Product in that Category; the merchant fills in the value per product (picks a Checkbox option, or types a Range number). That value then drives (a) the **storefront product detail specs table** so customers see the full specification list and (b) — when the Property's *"Use as filter"* toggle is ON — the **storefront category-page filter sidebar** where customers narrow the listing by Property values. Properties are managed on [[products-property]] (Sidebar → Products → Properties) via a 3-step wizard (details → categories → values).

A Category Property is intentionally **distinct from a [[variant|Variant]]** and from a **[[product-option|Product Option]]** — see [[variants-model]] for the full three-way contrast. It does **NOT split SKUs** (Bluetooth: yes and Bluetooth: no on one model are still one SKU), it's **filled by the merchant once per product** (not by the customer at cart-add), and it's **scoped per-Category**. Its main customer-facing role is the category-page filter sidebar.

This entity is split into **five aspect pages** (below). Drill into the aspect that matches the question rather than reading every page.

## Sub-pages (in this cluster)

- [[category-property-attributes]] — the full per-field schema (`name`, `type`, `options_list`, `dec_points`, Categories M2M, `is_visible`, `active`, `sort`, `url_handle`, image + dimensions, per-product value, `products_count`, URL-handle cache).
- [[category-property-types]] — the two merchant-creatable types (Checkbox / Range), the two data-layer-only types (`select` / `radio`), type-locked-after-create, Range retro-conversion blocked when non-numeric values exist, `dec_points` default + slider step derivation.
- [[category-property-business-rules]] — primary-category JOIN scope for the specs table, delete-blocked-while-in-use (whole Property + per-option), bulk-delete partial block, detach-does-not-delete orphan values, field-length caps, transactional multi-property value merge.
- [[category-property-storefront]] — where Property values surface for the customer: the category-page filter sidebar (gated on *Use as filter*), the product detail specs table (always), value images / colour swatches, the `active` master-hide toggle.
- [[category-property-api]] — JSON-API v2 read / create / update / delete via [[api-properties]] + [[api-property-options]], the identical side-effects + validations on the API path, the type-surface gap, the transactional merge endpoint.

## Aliases

- **Category Property** / **Property** — the canonical merchant-facing terms in the admin sidebar ("Products → Properties") and on [[products-property]].
- **Product property** — used in the product editor's Category section where the merchant fills in the per-product value.
- **Category-bound property** — emphasises the per-Category scope (vs. store-wide Parameters).
- **Specification** / **Spec** — informal phrasing for the customer-facing spec list.
- **Filter (category)** — informal phrasing for the most-used customer-facing role (the filter sidebar).
- **Категорийна характеристика** / **Спецификация** / **Характеристика** / **Филтър** — Bulgarian terms across the Products → Properties area.

## Key Attributes

The Category Property record is documented field-by-field on [[category-property-attributes]]. In brief, the Property definition carries: a **name** (required, max 191 chars, translatable), a **type** (`checkbox` or `range`, locked after creation), an **options list** (Checkbox only), **decimal places** (`dec_points`, Range only), an **M2M Categories** attachment, a **Use as filter** toggle (`is_visible`), an **Active** toggle (`active`, master hide), a drag-reorderable **sort priority**, a unique **URL handle**, optional **image** + **dimensions**, and a read-only **products count**.

The **per-product value** (the Checkbox option picked or Range number typed) is set on the [[products-products]] product editor and stored separately from the Property definition. The record has **no time-windowed visibility** and **no `created_at` / `updated_at` audit columns** surfaced in the UI.

## Why it matters to the merchant

Five high-impact behaviours (detail on the aspect pages):

- **Type is locked after creation.** Switching Checkbox ↔ Range means creating a new Property and migrating products. See [[category-property-types]].
- **A Property in use cannot be deleted** (HTTP 422); clear every per-product value first. See [[category-property-business-rules]].
- **The specs table only shows Properties on the product's PRIMARY category** — secondary-category specs do not surface on the detail page. See [[category-property-storefront]].
- **Detaching a Category leaves orphan per-product values** that reappear if the Category is re-attached, with no UI to clean them. See [[category-property-business-rules]].
- **Only Checkbox + Range are creatable in admin.** The data layer also accepts `select` / `radio`, but the wizard never exposes them. See [[category-property-types]].

## Where it appears

- [[products-property]] — the master management screen (Sidebar → Products → Properties): 3-step creation wizard, then per-row inline edit / toggle / delete / drag-reorder.
- [[category]] — Properties are attached per-Category via M2M (many-to-many both ways).
- [[product]] / [[products-products]] — every Product inherits the Properties of its assigned Categories; the per-product value is entered on the editor's Categories section (separate from the Variants matrix).
- Storefront — the filter sidebar (Use as filter = ON) + product detail specs table. See [[category-property-storefront]].
- [[apps-csv-import]] — bulk-create Properties + values via CSV.
- JSON-API v2 — programmatic read / write via [[api-properties]] + [[api-property-options]]. See [[category-property-api]].

## Related

### Related entities

- [[product]] — Properties auto-apply to every Product in their assigned Categories; the per-product value is set on the product editor.
- [[category]] — Properties are attached per-Category; the M2M attachment determines which Products see the Property.
- [[variant]] — DISTINCT concept; Variants split SKUs (per-Variant stock + price + barcode), Properties do NOT. A laptop with RAM as a Variant has separate SKUs per RAM size; as a Property it has one SKU with RAM as a spec.
- [[product-option]] — DISTINCT concept; Product Options are per-product customer-input fields filled at cart-add, not merchant-filled category-scoped metadata.
- [[file-asset]] — value images (e.g., colour swatches) reference uploaded assets stored in the file manager.

### Cross-cutting concepts

- [[variants-model]] — the canonical three-way contrast page (Parameter / Option / Variant vs. Property vs. Product Option). The classic decision rule: *"Does this dimension determine a separate SKU and price?"* → Variant Parameter; *"Is this dimension purely descriptive / informational?"* → Property.
- [[multi-language]] — per-locale translation of Property names + option value names on multilang stores.

### Settings & feature pages

- [[products-property]] — primary admin screen for managing Property definitions, attaching Categories, and managing values.
- [[products-categories]] — the Categories that Properties attach to. Categories are required for a Property to exist (the wizard step 2 forces selection).
- [[products-products]] — per-product Property value entry.
- [[apps-csv-import]] — bulk-create Properties + values from CSV.
- [[settings-files]] — Property images and value images live in the file manager.

## Open Questions

Distributed to aspect pages. See:

- [[category-property-attributes]] — whether the per-Property image dimensions (`width`, `height`, `max_thumb_size`) are hard-enforced on upload or merely advisory.
- [[category-property-types]] — Range slider min/max is auto-computed at runtime from the actual per-product values present (no merchant-set fixed bounds, per code paths).
