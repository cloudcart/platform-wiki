---
type: feature
nav_path: "Apps → Size Chart → Conditions"
route_name: apps.size_chart.settings
route_path: /admin/apps/size_chart/conditions
aliases: ["Size Chart Conditions", "Size Chart rules", "Size Chart-to-product mapping"]
tags: [apps, others, size-chart, conditions, mapping]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Size Chart → Conditions

## Purpose

The **Conditions** view is where the merchant defines **which products get which size chart** — rules mapping categories / brands / tags to specific size charts. See [[apps-size-chart]] for the full feature set.

The DB stores conditions in `@app_size_chart_conditions` (per [[apps-size-chart]]) which links `condition_id` to specific size-chart `id`.

## Where to find it

Sidebar → Apps → Size Chart → **Conditions tab**. Route: `/admin/apps/size_chart/conditions`.

## What the merchant can do here

### Conditions data table

Per row:

| Column | Notes |
|---|---|
| **Size chart** | Which named chart this condition references. |
| **Match type** | Category / Brand (vendor) / Tag / Product. |
| **Match value** | The specific entity (e.g., category "T-shirts", brand "Adidas"). |
| **Priority** | When multiple conditions match a product, which applies first. |
| **Actions** | Edit, Delete. |

### Add condition

`+ Add condition` modal:
1. Pick a size chart.
2. Pick match type (category / brand / tag / product).
3. Pick the specific match value.
4. Set priority.
5. Save.

### Priority handling

When multiple conditions match a product (e.g., it's in T-shirts category AND has Brand X), the highest-priority condition's chart is shown. The merchant orders conditions intentionally.

### What the merchant CANNOT do here
- Define the size chart content here — that's the parent app's chart-CRUD.
- Have a product with NO matching condition show any chart (in that case, no button appears).

## Settings & fields

Per [[apps-size-chart]] data model: conditions table links charts (`@app_size_chart`) to products via category / brand / tag / product matches.

## Business rules

### Default chart fallback

When the merchant defines a default chart (without specific conditions), it applies to ALL products as fallback (verify).

### Permission
Standard apps permission scope.

## Related

- [[apps-size-chart]] — hub.
- [[products-categories]] — categories as match values.
- [[products-vendors]] — vendors as match values.
- [[products-tags]] — tags as match values.

## How it works (verified against backend)

### Categories + optional vendors are the only match keys

The condition form (the platform code / `update`) accepts exactly two inputs:

- **Categories** — required, multi-select.
- **Vendors / manufacturers** — optional, multi-select (comma-separated in the request).

There is no priority field, no tag-based match, no per-product match, and no per-variant match. The Vue form lets the merchant pick multiple categories and zero or more vendors; the backend then writes one row to `@app_size_chart_conditions` for each (category × vendor) combination, or one row per category if no vendors are picked.

### Required fields and error messages

- *"You have not entered a condition name"* — internal title is required.
- *"You have not selected categories"* — at least one category is required.
- *"You have not selected a page"* — a target CMS page is required.
- *"You already have conditions created with the selected categories and manufacturers"* — when every category-vendor pair already exists, the platform refuses to create the duplicate condition and aborts.
- *"You now have conditions created with the selected categories"* — same duplicate error when no vendors are selected.

### Match resolution: closest category wins, no priority field

When a customer opens a product page, the platform resolves which chart applies by walking the product's category and all its parents (most-specific first) and returning the **first** matching condition. There is no merchant-visible priority field — order is determined automatically by category depth (deeper / more-specific categories override broader ones). Vendor narrows the match: a condition with a vendor only fires when the product's vendor matches.

### Internal vs storefront title

Each condition stores two titles:

- **Title (for internal use)** — what the merchant sees in the admin list.
- **Title (visible in store)** — what shows as the storefront button label ("Size chart", "Размерна таблица", "View sizes", ...).

The storefront title can be edited per condition, so the same underlying CMS page can be exposed as different button text in different categories.

### Status toggle

Each condition has a status (active / inactive) — the merchant can switch a condition off without deleting it, in which case the matched products stop showing the button.

### No bulk import, no CSV

Conditions are created one at a time through the modal. There is no CSV-import endpoint and no batch tooling in this app.

### Editing reuses the create form

Editing a condition deletes the existing `@app_size_chart_conditions` rows for that condition and re-inserts them based on the form's new (categories × vendors) selection. The condition's `id` (and therefore any URL or admin link) is preserved.

### No default / fallback chart

If a product does not match any active condition, no size-chart button is shown. There is no global "default chart" setting and no behaviour for "show this chart when nothing else matches".

## Open questions

