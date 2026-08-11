---
type: feature
nav_path: "Design → Modules → Products → Category showcase"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/showcaseCategories
aliases: ["Category showcase module", "showcaseCategories module", "showcaseCategory module", "product.showcase category", "Витрина с категории", "Category tile row"]
tags: [design, modules, products, category, showcase]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Category showcase (`product.showcase` with `type=category`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Category showcase** module (type `product.showcase`, instance name typically `showcaseCategories` or `showcaseCategory`) renders a row of category tiles (category image + name) that link to the category listing pages. Used on the homepage to direct shoppers into curated top-level categories. Visually a sister to [[design-module-product-showcase-brand]] — same module type, just `type=category`.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab — card labelled **"Category showcase"** or theme-specific equivalent.

Edit-panel URL: `/admin/storefront/widgets/{instance-name}` (e.g., `/admin/storefront/widgets/showcaseCategories`).

Renders as a homepage row (or theme-placed slot). Category IMAGE comes from the category record — see [[products-categories]].

## What the merchant can do here

- Master enable / disable toggle.
- Header text for the row.
- Toggle whether each tile shows the category NAME.
- Toggle whether each tile shows the category short DESCRIPTION.
- Pick the categories to surface (multi-select tree picker; drag to reorder).
- Toggle slider mode with arrows / pagination indicators.
- Pick arrow position (top / center).
- Pick tiles per row (1-12).

## What the merchant cannot do here

- Cannot pick more than 40 categories in a single showcase (`_max_filter_value_items = 40`).
- Cannot upload tile-specific images — the category's stored image is what renders. Edit the image on the category record in [[products-categories]].
- Cannot mix categories and vendors — `type=category` is fixed for this instance.
- Cannot exceed 12 tiles per row.
- Cannot pick non-existing categories — save validates existence.

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `enabled` | bool | `true` | on / off | — | `bool` | Master on/off |
| `header` | string | `""` | any string | 0-100 chars | `char:0,100` | Row header text |
| `type` | enum | `category` (for category instances) | `category`, `vendor` | — | `in:category,vendor` | Fixed by the theme JSON for category instances |
| `show_name` | bool | `true` | on / off | — | `bool` | Show category name on each tile |
| `show_description` | bool | `true` | on / off | — | `bool` | Show category short description |
| `showcase` | multi-select tree | `[]` | category IDs (drag-reorder) | up to 40 entries | freeform; existence-validated | Which categories to surface |
| `per_row` | int | `3` | 1-12 | 1-12 | `int:1,12` | Tiles per row |
| `enable_slider` | toggle | off | on / off | — | freeform | Render as a carousel |
| `enable_arrows` | bool | `true` | on / off | — | `bool` | Show next/prev arrows (slider mode) |
| `enable_pagination` | bool | `false` | on / off | — | `bool` | Show pagination dots (slider mode) |
| `arrows_position` | enum | `top` | `top`, `center` | — | `in:top,center` | Slider arrow position |
| `amount` | int | `4` | (default-content placeholder) | — | freeform | Placeholder count for empty-state default content |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| Picked > 40 categories | *"More than {count} categories"* (i18n key `module.product.showcase.err.more_than_20_categories`) |
| Picked an unknown category ID | *"One or more categories no longer exist."* |
| `per_row` out of 1-12 | Field-level integer-range error |
| `header` longer than 100 chars | Field-level char-range error |

## All themes vs theme-specific

| Setting | All themes | Theme-specific notes |
|---------|-----------|----------------------|
| Core fields | yes | Universal across themes that ship a category-showcase slot |
| Number of category showcase instances | varies | Usually one (`showcaseCategories`); some themes ship sub-rows |
| Tile styling (image / overlay / hover) | theme | All theme-styled |

## Business rules

### Tile content comes from the category record

Each tile renders the category's stored IMAGE + name + (optional) short description. To change a tile, edit the category record in [[products-categories]] — the module just lays them out.

### Order preserved from picker

Categories are saved in the order they were picked. The runtime fetches them and orders by the stored `order` column (category natural order) when the picker stores IDs — verify per-theme that the picker preserves drag-reorder.

### Cap at 40 categories

Hard-cap is 40. Picking more triggers the validation error. For deep navigation, link to category listing pages from elsewhere ([[design-navigation]]) rather than cramming.

### Empty showcase + enabled = renders placeholder

When `enabled=on` AND `showcase=[]`, the module renders default-content placeholder tiles ("Category title", "Category description" with stock images) so the merchant can see where the row will appear.

### Slider mode swaps template

`enable_slider=on` switches the rendered template from `showcase` to `showcaseSlider` — same data, carousel layout.

### Cache invalidation on save / reset

Standard — save / reset bump the per-site cache key.

## Related

- [[design-modules-products]] — hub.
- [[products-categories]] — category records supplying tile images.
- [[design-module-product-showcase-brand]] — same module TYPE with `type=vendor` for brand tiles.
- [[design-module-product-showcase]] — separate module for product rows.

## How it works (verified against backend)

### Restrictions

Same as [[design-module-product-showcase-brand]] — `type` switch picks the picker, but the schema is identical: `enabled=bool, show_name=bool, show_description=bool, header=char:0,100, type=in:category,vendor, showcase=false, per_row=int:1,12, enable_slider=false, enable_arrows=bool, enable_pagination=bool, arrows_position=in:top,center`.

### Defaults

`enabled=true, amount=4, show_name=true, show_description=true, header="", type=category, showcase=[], per_row=3, enable_slider="", enable_arrows=true, enable_pagination=false, arrows_position=top`.

### Save pipeline

`enable_slider` cast to 0/1. `showcase` exploded from CSV if string. Cap at 40 enforced by `_max_filter_value_items`. Existence validated via the platform code for `type=category`. Empty + enabled renders placeholder.

### Category query

the platform code — orders by the category natural `order` column.

### Template dispatch

`enable_slider=on` → the platform code (or global fallback). Off → the platform code.

## Open questions

- 📡 **Picker drag-reorder vs category natural order.** Some pickers preserve the drag order; the runtime orders by the category's `order` column. Verify whether the merchant's picker order is honoured per theme.
- 📡 **Nested categories.** Whether the picker allows sub-categories and how nested tiles render — verify per-theme.
