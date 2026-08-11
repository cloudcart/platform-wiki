---
type: feature
nav_path: "Products → Properties"
route_name: categories.property
route_path: /admin/products/property
aliases: ["Properties", "Category properties", "Filters", "Specifications", "Спецификации", "Характеристики", "Филтри"]
tags: [products, properties, filters, specifications, taxonomy]
plan_gates: ["category_properties"]
created: 2026-05-21
updated: 2026-06-10
source_count: 12
---

# Properties

## Purpose

The screen where the merchant defines **category-bound product properties** — the structured specifications that describe products in a category (Color, Size, Material, RAM, Screen size, etc.). Each property is created once, attached to one or more categories, and given a set of allowed values. When a product is later assigned to one of those categories, the property appears on the product editor — the merchant picks the value, and the property becomes a customer-facing **filter** in the storefront category sidebar (when the property has "Use as filter" enabled).

Two property types are exposed in the admin UI:

- **Checkbox** — discrete categorical options (e.g., Color: Red / Blue / Green / Yellow). Customers see filter checkboxes.
- **Range** — continuous numeric values (e.g., Screen size: 5.0–7.0 inches). Customers see a slider with min/max; the merchant configures the slider's decimal precision via `dec_points`.

First-time creation is guided through a 3-step wizard (property details → categories → values); existing properties are edited directly from the table. Properties have no time-windowed visibility — the merchant toggles `active` on / off manually.

## Where to find it

Sidebar → Products → **Properties**. The page's breadcrumb reads "Products → Properties". The route is `/admin/products/property`. The header icon is the sliders icon.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[products-property-list-view]] — list mode: columns, inline toggles (`is_visible`, `active`), drag-drop reorder, per-row Delete, bulk actions, entry points to wizard / categories / values.
- [[products-property-wizard]] — 3-step create wizard (property settings → choose categories → set values) + the Edit property modal that shares step 1's field set.
- [[products-property-categories]] — per-property Categories sub-page: attach / detach categories; orphan-value behaviour on detach.
- [[products-property-values]] — per-property Values sub-page: option-value editor (name, description, image, SEO), drag-reorder, bulk-delete.
- [[products-property-merge]] — Merge values modal: cross-property consolidation, dedup, irreversibility, transactional behaviour, ES re-sync.
- [[products-property-business-rules]] — the cross-cutting rule catalogue: Active vs Use-as-filter, type-lock, range-numeric validation, delete-protection, URL handle uniqueness, primary-category JOIN, image dimensions per property, 191-char caps.
- [[products-property-api]] — JSON-API v2 endpoints, plan gate (`category_properties`), shared side effects (search re-index, URL-handle cache invalidation), the surface gap (`select` / `radio` exist in storage but not in the UI), field reference.

## What the merchant can do here

The list page is the entry point. From there:

- **Find / sort / filter** properties — see [[products-property-list-view]].
- **Create** a new property via the **+ Add property** wizard — see [[products-property-wizard]].
- **Edit** an existing property by clicking its name — see [[products-property-wizard]] (Edit property modal).
- **Manage attached categories** by clicking the Categories cell — see [[products-property-categories]].
- **Manage option values** by clicking the Values cell — see [[products-property-values]] (and [[products-property-merge]] for consolidation).
- **Toggle visibility** (`is_visible` / `active`) inline or in bulk — semantics on [[products-property-business-rules]].
- **Reach products** using a property by clicking the Products count — opens [[products-products]] pre-filtered.

## Settings & fields (top-level)

Field-by-field tables live on the aspect pages — they're the section the support LLM cites most. Quick map:

| What | Where |
|---|---|
| List columns + bulk actions | [[products-property-list-view]] |
| Create / Edit property fields (`name`, `type`, `dec_points`, `url_handle`, image) | [[products-property-wizard]] |
| Add categories modal field | [[products-property-categories]] |
| Add / Edit value modal fields (name, description, image, SEO) | [[products-property-values]] |
| Merge values modal fields | [[products-property-merge]] |
| Field-length caps + validation strings | [[products-property-business-rules]] |

## Business rules (cross-cutting)

Aspect-specific rules live on the relevant sub-page; full catalogue on [[products-property-business-rules]]. The rules that span every aspect:

- **Category-scoped, not store-wide.** A property only appears on products in categories it's attached to — see [[products-property-categories]].
- **Type locked after creation.** Checkbox vs Range can't be flipped in place — see [[products-property-business-rules]].
- **Delete-protection on in-use properties.** Single delete shows *"This property still has products and cannot be deleted"*; bulk-delete returns the list of blocked names. Active / Use-as-filter toggles are unrestricted.
- **Sort priority drives TWO surfaces** — storefront filter sidebar AND product editor's category-properties section. Drag-reorder on [[products-property-list-view]].
- **Saves trigger storefront search re-index** — same side effect runs from admin and [[products-property-api|JSON-API v2]] paths. The `categories_properties.keys.v1` cache invalidates on create / URL-handle change.
- **Primary-category JOIN on storefront product detail** — the Specifications table joins on the product's primary category only. Multi-category products surface only the properties whose attachment matches the primary category. See [[products-property-business-rules]].

### Permission

The Properties pages and actions require the `products` permission section. Moderators without it cannot see the Properties sidebar entry.

## Programmatic access

Full surface, plan gate (`category_properties`), and shared side effects live on [[products-property-api]]. The data this screen manages can be read / written via [[api-properties]] and [[api-property-options]]. **Same side effects** (search-index re-index, URL-handle cache invalidation) and **same validations** (type-lock, range-numeric, 191-char caps, delete-blocked-when-in-use) apply on the API path.

## Plan gates

`category_properties` (boolean) gates `/admin/category/property/create` — the wizard entry point. The list itself remains visible. Full details on [[products-property-api]].

## Related

- [[products]] — parent hub.
- [[products-products]] — products are assigned property values on their editor; clicking the Products count on the list opens [[products-products]] pre-filtered.
- [[products-categories]] — properties are attached to specific categories; the storefront filter sidebar appears on category landing pages.
- [[products-variants-options]] — distinct from properties — variants are physical SKU variations (different stock units); properties are descriptive specifications (no SKU split).
- [[apps-csv-import]] — bulk-create properties + values via CSV.
- [[settings-files]] — property + value images stored here.
- [[product]] / [[category]] — entity pages.
- [[api-properties]] / [[api-property-options]] — JSON-API v2 surface.
- [[json-api-v2]] — auth, rate limit, side-effects principle.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — plan-feature gating model.

## Open questions

None at the hub level. Aspect-specific open questions live on each sub-page.
