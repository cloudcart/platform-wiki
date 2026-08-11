---
type: feature
nav_path: "Apps → Size Chart"
route_name: apps.size_chart.overview
route_path: /admin/apps/size_chart
aliases: ["Size Chart", "Sizing guide", "Sizes table", "Размерна таблица", "no enable disable button", "app has no active toggle"]
tags: [apps, others, apparel, sizing, content]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# Size Chart

## Purpose

**Size Chart** integration — adds a clickable **"Size Chart" button** to product pages (typically apparel / footwear products) that opens a modal with the sizing reference table. Used by merchants selling clothing, shoes, accessories — where size standards vary by brand / region (EU vs US vs UK shoe sizes; clothing size charts per gender / region).

The merchant defines named size charts (e.g., "Adult shoes EU/US", "Women's tops"), adds conditions ([[apps-size-chart-conditions]]) that determine which products show which chart.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **chart** — each one has its own Active / Inactive status, see the status-flag rule below.

## Where to find it

Sidebar → Apps → install → **Size Chart**. Two sub-pages:

| Sub-page | Purpose |
|----------|---------|
| Overview | App management. |
| Conditions ([[apps-size-chart-conditions]]) | Rules mapping products → charts. |

## What the merchant can do here

- Create named size charts with table content (rich HTML).
- Define conditions per chart (which products / categories trigger it).
- Activate / deactivate.

### What the merchant CANNOT do here
- Auto-fit sizes based on customer measurements (no AI / fit assistant).
- Customer-specific saved measurements.

## Settings & fields

Manager exposes:
- `getMigrationsPath` — DB migrations.
- `appInfo` — App Store metadata.

The integration creates DB tables (`@app_size_chart` + `@app_size_chart_conditions`) holding chart definitions + rules.

## Business rules

### Condition-driven matching

Each size chart has CONDITIONS attached. When a customer views a product:
1. The platform checks which conditions match (category, brand, tag, etc.).
2. Picks the matching chart.
3. Renders the Size Chart button on the product page.

If multiple charts match, priority rules apply (verify).

### Charts can be reused across products

One chart covers many products (e.g., "Men's t-shirts" chart applies to all t-shirt SKUs).

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-size-chart-conditions]] — conditions sub-page.
- [[products-products]] — products where chart appears.
- [[products-categories]] — common condition field.

## How it works (verified against backend)

### Charts are CMS Pages, not a separate chart editor

A "size chart" inside this app is just a pointer to an existing CMS page (`@pages` → see **Content → Pages**). The size-chart record in `@app_size_chart` stores:

- `condition_name` — the **internal** title (admin-side only — e.g. "Adult shoes EU/US").
- `condition_name_front` — the **public** label shown on the storefront button (e.g. "Size chart").
- `page_id` — the CMS page that contains the actual sizing table content.

So the chart's HTML content (the actual table of sizes) is authored in the **Content → Pages** editor — the merchant uses the full Page Builder or the standard rich-text page editor, with image upload, multi-column layouts and everything else available to a normal CMS page. There is no separate "size chart editor" inside this app.

### Multi-language follows the underlying CMS Page

Because the chart is a CMS Page, multi-language behaviour matches whatever the Pages feature supports for that storefront — the merchant translates the page once and every product that maps to it shows the translated version. There is no per-condition language override.

### Conditions are category and optional vendor pairs

Each condition row in `@app_size_chart_conditions` is `(category_id, optional vendor_id)`. The merchant picks **one or more categories** and **zero or more vendors**:

- With vendors selected, the spinner creates one condition per (category × vendor) pair.
- Without vendors, the condition matches any vendor in that category.

There is no condition on individual products, no tag-based condition, and no condition on tags.

### Match resolution: deepest category wins, vendor narrows

When a customer opens a product page, the platform:

1. Collects the product's category plus all its **parent categories** (so a sub-category match counts).
2. Sorts these by depth descending (most-specific first).
3. Looks for a size-chart condition that matches any of these categories.
4. If `vendor_id` is set on the condition, the product's vendor must also match.

The **first** condition that matches is the one used — so the chart attached to the deepest matching category wins. If no condition matches, **no size chart button is shown** — there is no default fallback chart.

### Per-variant overrides not supported

The size chart is resolved at product level, not variant level. A shoe SKU with EU / US / UK variants gets one chart for the whole product. To present multiple sizing systems, the merchant builds them all into the single CMS page.

### Storefront rendering: link to the page

The storefront templates render a link with the `_product-details-size-chart` class that points to the CMS page (`route('page', $url_handle)`) and opens in a side-panel (the `data-ajax-panel` attribute) or new tab depending on theme. The "open in popup" admin setting toggles between in-page modal and dedicated page view. Because it's a normal CMS page, the layout responds to mobile / desktop based on the theme's existing page styling — there is nothing size-chart-specific about the modal.

### Status flag per chart

Each chart row has a `status` column (active / inactive). Toggling a chart off disables it without deleting — the button stops appearing on matched products until the merchant re-activates it.

### Lookup logic: collect parent categories, sort descending, vendor-narrow
The `getSizes($category_ids, $vendor_id)` helper:
1. For each category the product belongs to, walks all parent categories via the platform code.
2. Deduplicates the resulting list of category IDs.
3. Reverse-sorts the IDs so the highest-numbered (typically most recently created) categories come first — this is a proxy for "deepest" since CloudCart category IDs tend to grow with subcategory creation order.
4. Queries `@app_size_chart` joined with `@app_size_chart_conditions` filtering by those category IDs, optionally filtered by vendor ID.
5. Orders the result by `category_id` DESC and returns the FIRST match.

So the resolution depends on category ID ordering rather than explicit category-depth metadata. Re-organising the category tree can shift which chart wins for ambiguous products.

### No SizeChart manager logic beyond getSizes
The `SizeChartManager` only ships `install`-related migrations + the `getSizes` lookup helper. There's no per-product override, no caching, no rendering logic — the storefront theme is responsible for calling `getSizes` and rendering the result.

## Open questions

