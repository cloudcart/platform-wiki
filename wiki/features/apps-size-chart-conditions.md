---
type: feature
nav_path: "Apps → Size Chart → Conditions"
route_name: apps.size_chart.settings
route_path: /admin/apps/size_chart/conditions, /admin/apps/size_chart/conditions/create, /admin/apps/size_chart/conditions/edit/:id
aliases: ["Size Chart Conditions", "Size Chart rules", "Size Chart-to-product mapping"]
tags: [apps, others, size-chart, conditions, mapping]
plan_gates: []
created: 2026-05-21
updated: 2026-10-21
source_count: 1
---
# Size Chart → Conditions

## Purpose

The **Conditions** view is where the merchant defines **which products get which size chart** — each condition links a size-chart page (an ordinary page from Content → Pages) to one or more categories and, optionally, manufacturers. See [[apps-size-chart]] for the full feature set.

The DB stores conditions in `@app_size_chart_conditions` (per [[apps-size-chart]]) which links `condition_id` to specific size-chart `id`.

## Where to find it

Sidebar → Apps → Size Chart → **Conditions tab**. Route: `/admin/apps/size_chart/conditions`.

## What the merchant can do here

### Conditions data table

Per row:

| Column | Notes |
|---|---|
| **Title** | The internal title; click it to edit the condition. |
| **Title on website** | The link text shown on the product page. |
| **Page** | The size-chart page, linking to its editor. |
| **Status** | Active / inactive switch. |
| (delete) | Deletes the condition. |

### Add condition

**Create new** opens the condition form:
1. **Title (For internal use)** — required.
2. **Title (Will be Visible in the Store)** — required; the link text on the product page.
3. **Page** — required; the size-chart page.
4. **Category** — one or more, required.
5. **Manufacturers** — optional, one or more.
6. Save.

### When several conditions match

There is no priority setting — the platform picks one condition by category (see *How it works* below).

### What the merchant CANNOT do here
- Define the size chart content here — it is an ordinary page, edited under Content → Pages.
- Have a product with NO matching condition show any chart (in that case, no button appears).

## Settings & fields

Each condition holds an internal title, a store title, a page, a status, and its category × manufacturer combinations (see *How it works* below).

## Business rules

### Permission
Standard apps permission scope.

## Related

- [[apps-size-chart]] — hub.
- [[products-categories]] — categories as match values.
- [[products-vendors]] — vendors as match values.

## How it works (verified against backend)

### Categories + optional vendors are the only match keys

The condition form has exactly two match inputs:

- **Categories** — required, multi-select.
- **Vendors / manufacturers** — optional, multi-select (comma-separated in the request).

There is no priority field, no tag-based match, no per-product match, and no per-variant match. The Vue form lets the merchant pick multiple categories and zero or more vendors; the backend then writes one row to `@app_size_chart_conditions` for each (category × vendor) combination, or one row per category if no vendors are picked.

### Required fields and error messages

- *"You have not entered a condition name"* — internal title is required.
- *"You have not selected categories"* — at least one category is required.
- *"You have not selected a page"* — a target CMS page is required.
- *"You already have conditions created with the selected categories and manufacturers"* — when every category-vendor pair already exists, the platform refuses to create the duplicate condition and aborts.
- *"You now have conditions created with the selected categories"* — same duplicate error when no vendors are selected.

### Match resolution: by category, no priority field

When a customer opens a product page, the platform collects the product's categories and all their parent categories, and picks the matching condition whose category was created most recently — usually, but not always, the most specific one. There is no merchant-visible priority field. Manufacturers work like this: for a product that has a manufacturer, only conditions that list that manufacturer match (a condition without manufacturers does not); for a product without a manufacturer, any condition on its categories can match.

### Internal vs storefront title

Each condition stores two titles:

- **Title (for internal use)** — what the merchant sees in the admin list.
- **Title (visible in store)** — what shows as the storefront button label ("Size chart", "Размерна таблица", "View sizes", ...).

The storefront title can be edited per condition, so the same underlying CMS page can be exposed as different button text in different categories.

### Status toggle

Each condition has a status (active / inactive) switch in the list. The storefront's size-chart lookup does not read it, so switching a condition off does not hide its link on matching products; deleting the condition does.

### No bulk import, no CSV

Conditions are created one at a time through the **Create new** form. There is no CSV-import endpoint and no batch tooling in this app.

### Editing reuses the create form

Editing a condition deletes the existing `@app_size_chart_conditions` rows for that condition and re-inserts them based on the form's new (categories × vendors) selection. The condition's `id` (and therefore any URL or admin link) is preserved.

### No default / fallback chart

If a product does not match any condition, no size-chart button is shown. There is no global "default chart" setting and no behaviour for "show this chart when nothing else matches".

## Open questions

