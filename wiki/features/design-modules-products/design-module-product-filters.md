---
type: feature
nav_path: "Design → Modules → Products → Product Catalog Settings"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/filters
aliases: ["Product Catalog Settings module", "Filters module", "filters module", "product.filters", "Product listing settings", "Catalog module", "Модул настройки на продуктов каталог", "Настройки на продуктов каталог", "Модул филтри"]
tags: [design, modules, products, catalog, filters]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Product module — Product Catalog Settings (`filters`)

> Part of [[design-modules-products]]. See the hub for the other product modules.

## Purpose

The **Product Catalog Settings** card (instance `filters`, type `product.filters`) is the master settings module for every product-listing page on the storefront — category, search, vendor, smart-collection, and wishlist pages. It controls per-page count, products per row, sort options, filter-sidebar visibility, price ranges, card visuals, out-of-stock handling, and the card-display toggles. There is no per-page override.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab → card labelled **"Product Catalog Settings"** (instance `filters`, type `product.filters`). Edit-panel URL: `/admin/storefront/widgets/filters`.

It drives the layout and filter sidebar of every product-listing page: `/category/...`, `/vendor/...`, `/search`, `/collection/...`, `/wishlist`.

## What the merchant can do here

- Set the default products-per-page and the per-page picker options shown to the customer.
- Set the default sort + direction and the sort picker the customer can switch.
- Pick products-per-row on desktop and mobile.
- Toggle which filter chips appear in the sidebar (categories / vendors / sale / new / variants / per-page / sort / sort direction / price ranges).
- Define pre-set price ranges OR (slider mode) set the price slider step.
- Toggle card icons + actions (wishlist, compare, buy, price, quick view) and out-of-stock visibility, badge, and push-to-end ordering.
- On new themes: pick a card template (`_list-one` / `_list-two` / `_list-horizontal`) + horizontal-size variant, and toggle second-image-on-hover, vendor-logo overlay, variant pickers, category-property facets, and facet counts.
- Save / Reset / Cancel — as on every editable module.

The merchant **cannot** override settings for one specific listing page — the same settings apply to all listings; per-page customisation needs a Dynamic page, see [[marketing-landing-pages]].

## Settings & fields

| Setting key | Default | Allowed values / range | Notes |
|---|---|---|---|
| `per_row` | `3` | 1-5 | Products per row on desktop |
| `per_row_mobile` | `1` | 1-2 | Products per row on mobile |
| `per_page` | `15` | int 2-100 | Default; must be present in `per_page_options` |
| `per_page_options` | `[15, 30, 50]` | 2-10 entries, each 2-100 | Per-page picker options |
| `order_by` | `id` | `id`, `name`, `price_from`, `sale`, `new`, `featured`, `sort_order` | Default sort |
| `order_by_options` | `['sale','featured','id','name','price_from','sort_order']` | 2-20 entries from `featured`, `id`, `name`, `price_from`, `sale`, `sort_order` | Sort options shown to the customer |
| `order_direction` | `asc` | `asc`, `desc` | Default direction |
| `products_price_ranges` | `[]` | 1-2 rows of `{from,to}` (verify) | Price-range chips (when NOT in slider mode) |
| `price_range_step` | — | positive int | Slider step (only with `mode: range_slider`) |
| `hide_sale` | `false` | on / off | Hide the SALE badge on cards |
| `hide_featured` | `false` | on / off | Hide the FEATURED badge on cards |
| `filters_options` | `['sort','sort_direction','categories','price_ranges','vendors','per_page_filter','variants','new','sale']` | 0-20 entries from `sort`, `sort_direction`, `categories`, `price_ranges`, `vendors`, `per_page_filter`, `variants`, `new`, `sale`, `featured`, `brand_model`, `category_properties` | Filter chips shown in the sidebar |
| `listing_show_compare` | `true` | on / off | Compare icon on the card |
| `listing_show_wishlist` | `true` | on / off | Wishlist heart icon on the card |
| `listing_show_buy` | `true` | on / off | Buy button on the card |
| `listing_show_price` | `true` | on / off | Price on the card |
| `show_quick_view` | `true` | on / off | Quick-view link on hover |
| `enable_category_properties` | `false` | on / off | Enable category-property facets |
| `category_properties_limit` | `3` | 0-100000 | Max category-property facets shown |
| `show_short_description` | `false` | on / off | Short description on the card |
| `show_out_of_stock_products` | `false` | on / off | Include out-of-stock products in the listing |
| `mark_out_of_stock_products` | `false` | on / off | Show OUT-OF-STOCK badge (when above is on) |
| `order_latest_out_of_stock` | `false` | on / off | Push out-of-stock products to the END |
| `list` | `lists/list-one.tpl` | theme-defined template paths | Filter-sidebar position template |
| `list_class` | `_list-one` | `_list-one`, `_list-two`, `_list-horizontal` | Card-template class |
| `list_horizontal_size` | `_list-horizontal-normal` | `_list-horizontal-small`, `_list-horizontal-normal`, `_list-horizontal-large` | Only when `list_class=_list-horizontal` |
| `second_image_show` | `false` | on / off | Swap to the second image on hover |
| `manufacturer_logo_show` | `false` | on / off | Brand-logo overlay on the card |
| `color_product_variants` | `[]` | colour parameter IDs | Colour variants to surface on the card |
| `variants` | `false` | on / off | Variant pickers on the card |
| `filters_sort_numbers` | `{sort:1, brand_model:2, categories:3, vendors:4, new:5, price_ranges:6, category_properties:7, variants:8}` | int per filter key | Per-filter sort order in the sidebar |
| `show_facet_counts` | `false` | on / off | Count next to each facet ("Red (12)") |

### Validation strings the merchant may see

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| Reset confirmation | *"Are you sure you want to reset this module?"* |
| Out-of-range `per_page` / `per_row` / `category_properties_limit` | Field-level integer-range error |
| `per_page_options` length out of 2-10 | Field-level array-length error |
| `filter` / `order_by` / `list_class` value not in its allowed enum | Field-level enum error |

### Which fields appear depends on the theme

The core fields (everything except the rows below) render on every theme with a listing page. These render **only on new themes**: `list`, `list_class`, `list_horizontal_size`, `second_image_show`, `manufacturer_logo_show`, `color_product_variants`, `variants`, `filters_sort_numbers`, `show_facet_counts`. The category-property facet (`enable_category_properties`, `category_properties_limit`) renders only when the theme also ships a `categoryProperties` system module — see [[design-modules-utility-system]]. `price_range_step` appears only with `mode: range_slider` (see Business rules).

Themes confirmed to ship the new-theme settings: a theme that ships it, another custom theme, `themex`, `echappe` (verify per-store). Older themes (e.g., `delicious`, `happydreams`) expose only the core fields.

## Business rules

### `per_page` must be inside `per_page_options`

The default `per_page` must be one of the values in `per_page_options`. If the merchant replaces the options with `9`, `18`, `36` but `per_page` is still `15`, the next save requires updating `per_page` to an allowed value.

### Price ranges OR slider step — never both

When the theme sets `"mode": "range_slider"` for the `filters` instance, the form shows `price_range_step` and hides `products_price_ranges`; otherwise it shows the price-ranges repeater. The mode is theme-controlled — not switchable from this form.

### Cache invalidation on save / reset

Save and Reset both refresh the storefront cache, so the new layout is live on the next storefront request — no manual clear required.

### Out-of-stock layering

The three out-of-stock toggles compose: `show_out_of_stock_products` OFF filters out-of-stock products out of every listing; ON shows them (with the "OUT OF STOCK" badge only if `mark_out_of_stock_products` is also ON); adding `order_latest_out_of_stock` ON pushes them to the END of the listing regardless of the sort.

### Card-template change typically requires `per_row` adjustment

Switching `list_class` from `_list-one` to `_list-two` typically pairs with a different `per_row` (e.g., 4 not 3) — otherwise cards may overflow or crowd. Tune both together.

### Reset restores defaults for all listings

Reset clears the saved values and re-publishes the defaults, restoring the shared listing layout.

## Related

- [[design-modules-products]] — hub.
- [[design-modules]] — parent module editor.
- [[design-themes]] — theme controls which fields render here.
- [[products-products]] — products that flow into the listings.
- [[products-categories]] — category pages this drives.
- [[products-smart-collections]] — smart-collection pages this drives.
- [[marketing-landing-pages]] — Dynamic pages for per-page overrides.
- [[design-modules-utility-system]] — `categoryProperties` module that pairs with `enable_category_properties`.

## Open questions

- 📡 **`color_product_variants` source.** The select pulls from colour-flagged parameter values — confirm the exact list on a real store.
- 📡 **`category_properties_limit` with deep trees.** The limit applies to the flat list — exact behaviour with grouped/nested properties needs verification on a real store.
