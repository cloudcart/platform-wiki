---
type: feature
nav_path: "Design → Modules → Products → Brand showcase"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/showcaseBrand
aliases: ["Brand showcase module", "Vendor showcase module", "showcaseBrand module", "showcaseBrands1 module", "showcaseBrands2 module", "product.showcase vendor", "Витрина с марки", "Showcase with stamps"]
tags: [design, modules, products, brand, vendor, showcase]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Brand showcase (`product.showcase` with `type=vendor`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Brand showcase** module (type `product.showcase`, instance names `showcaseBrand`, `showcaseBrands1`, `showcaseBrands2`) renders a row of brand / vendor tiles (logo + name) that link to the vendor's product listing. Used to drive shoppers into curated brand pages from the homepage or any theme slot the brand showcase has been placed in. Some themes ship multiple instances — typically one big "all brands" row plus 1-2 themed sub-rows.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab — cards labelled **"Showcase with stamps"**, **"Showcase with stamps 1"**, **"Showcase with stamps 2"**, etc.

Edit-panel URL: `/admin/storefront/widgets/{instance-name}` (e.g., `/admin/storefront/widgets/showcaseBrand`).

Renders as a homepage row (or theme-placed slot). Vendor LOGO comes from the vendor record — see [[products-vendors]].

## What the merchant can do here

- Master enable / disable toggle.
- Header text for the row.
- Toggle whether each tile shows the vendor NAME.
- Toggle whether each tile shows the vendor DESCRIPTION (short).
- Pick the vendors to surface (multi-select autocomplete; drag to reorder).
- Toggle slider mode (carousel) with arrow / pagination indicators.
- Pick arrow position (top / center).
- Pick tiles per row (1-12).

## What the merchant cannot do here

- Cannot pick more than 40 vendors in a single showcase (`_max_filter_value_items = 40`).
- Cannot upload tile-specific images — the vendor's stored LOGO is what renders. Edit the logo on the vendor record in [[products-vendors]].
- Cannot mix vendors and categories — `type=vendor` is fixed for this instance. Use [[design-module-product-showcase-categories]] for categories.
- Cannot exceed 12 tiles per row.

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `enabled` | bool | `true` | on / off | — | `bool` | Master on/off |
| `header` | string | `""` | any string | 0-100 chars | `char:0,100` | Row header text |
| `type` | enum | `vendor` (for brand instances) | `category`, `vendor` | — | `in:category,vendor` | Fixed by the theme JSON for brand instances |
| `show_name` | bool | `true` | on / off | — | `bool` | Show vendor name on each tile |
| `show_description` | bool | `true` | on / off | — | `bool` | Show vendor short description |
| `showcase` | multi-select | `[]` | vendor IDs (drag-reorder) | up to 40 entries | freeform; existence-validated | Which vendors to surface |
| `per_row` | int | `3` | 1-12 | 1-12 | `int:1,12` | Tiles per row |
| `enable_slider` | toggle | off | on / off | — | freeform | Render as a carousel |
| `enable_arrows` | bool | `true` | on / off | — | `bool` | Show next/prev arrows (slider mode) |
| `enable_pagination` | bool | `false` | on / off | — | `bool` | Show pagination dots (slider mode) |
| `arrows_position` | enum | `top` | `top`, `center` | — | `in:top,center` | Slider arrow position |
| `amount` | int | `4` | (default-content placeholder) | — | freeform | Used only for the "no-content yet" placeholder; not a customer-facing cap |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| Picked > 40 vendors | *"More than {count} vendors"* (i18n key `module.product.showcase.err.more_than_20_vendors`) |
| Picked an unknown vendor ID | *"One or more vendors no longer exist."* |
| `per_row` out of 1-12 | Field-level integer-range error |
| `header` longer than 100 chars | Field-level char-range error |

## All themes vs theme-specific

| Setting | All themes | Theme-specific notes |
|---------|-----------|----------------------|
| Core fields (`enabled`, `header`, `show_name`, `show_description`, `showcase`, `per_row`, slider settings) | yes | Universal across themes that ship a brand showcase slot |
| Number of brand showcase instances | varies | a theme that ships it typically ships 1; older themes may ship `showcaseBrands1` + `showcaseBrands2`; many themes omit entirely |
| Tile styling | theme | Logo dimensions, border, hover effect are all theme-controlled |

## Business rules

### Tile content comes from the vendor record

Each tile renders the vendor's stored LOGO + name + (optional) short description. To change a tile, edit the vendor record in [[products-vendors]] — the module just lays them out.

### Order preserved from picker

Vendor IDs are stored in the order the merchant picked them in the autocomplete. The runtime preserves that order using `ORDER BY FIELD(id, ...)`. Drag-reorder controls the row sequence.

### Cap at 40 vendors

The save handler hard-caps the vendor list at 40. Picking more triggers the error message. For very large brand catalogues, use multiple `showcaseBrand` instances (`showcaseBrands1` + `showcaseBrands2`) instead of trying to cram everything in one.

### Empty showcase + enabled = renders placeholder

When `enabled=on` AND `showcase=[]`, the module renders a placeholder (using default content images) so the merchant can see where the row will appear. Disabling the module OR filling `showcase` removes the placeholder.

### Slider mode swaps template

`enable_slider=on` switches the rendered template from `showcase` to `showcaseSlider` — same data, carousel layout.

### Cache invalidation on save / reset

Standard — save / reset bump the per-site cache key.

## Related

- [[design-modules-products]] — hub.
- [[products-vendors]] — vendor records that supply tile logos.
- [[design-module-product-showcase-categories]] — same module TYPE with `type=category` for category tiles.
- [[design-module-product-showcase]] — separate module for hand-picked / smart-collection PRODUCT rows.

## How it works (verified against backend)

### Restrictions

`enabled=bool, show_name=bool, show_description=bool, header=char:0,100, type=in:category,vendor, showcase=false (freeform; existence-validated), per_row=int:1,12, enable_slider=false, enable_arrows=bool, enable_pagination=bool, arrows_position=in:top,center`.

### Defaults

`enabled=true, amount=4, show_name=true, show_description=true, header="", type=category, showcase=[], per_row=3, enable_slider="", enable_arrows=true, enable_pagination=false, arrows_position=top`.

### Save pipeline

`enable_slider` cast to 0/1. `showcase` exploded from CSV if string. Cap at 40 enforced by `_max_filter_value_items`. Existence validated via the platform code for `type=vendor`. Empty showcase + disabled allowed; empty + enabled triggers default-content placeholder.

### Vendor query preserves order

the platform codeid`, csv-ids)'), 'asc')` — preserves the merchant-defined sequence.

### Template dispatch

`enable_slider=on` → the platform code (or global fallback). Off → the platform code.

## Open questions

- 📡 **Vendor description length on tiles.** The "show_description" toggle shows the SHORT description from the vendor record. Verify there is no separate per-tile override.
- 📡 **Vendor logo dimensions.** Themes constrain tile sizes — verify the recommended logo dimensions per theme.
