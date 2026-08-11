---
type: feature
nav_path: "Design → Modules → Products → Product showcase"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/showcaseProducts
aliases: ["Product showcase module", "showcaseProducts module", "product.productShowcase", "Homepage product row", "Витрина с продукти", "Promotions row", "Best sellers row"]
tags: [design, modules, products, showcase, homepage]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Product module — Product showcase (`product.productShowcase`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Product showcase** module (type `product.productShowcase`) renders a horizontal row of products on the homepage, on a page-builder Dynamic page, or wherever the theme has placed the slot. Instance names are theme-declared (e.g. `showcaseProducts`, `showcaseProductsFirst`–`showcaseProductsFourth`, `showcaseBestSellersProducts`, `Promotions`). It is the workhorse for "Featured", "New arrivals", "Bestsellers" and "Promotions" strips — it decides what products appear in each homepage row.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab. Each named instance appears as its own card; the display name is the theme-declared label (e.g. **"Products Showcase - First Row"**, **"Promotions"**).

Edit-panel URL: `/admin/storefront/widgets/{instance-name}` (e.g. `/admin/storefront/widgets/showcaseBestSellersProducts`).

Position on the storefront is theme-controlled — typically the first numbered variant renders highest and later variants stack below.

## What the merchant can do here

- Title the row.
- Pick a product source — all products, category, vendor, hand-picked list, tag list, or a Smart Collection.
- Filter the source by the **New**, **Sale**, **Featured** flags (independent toggles), and by product type (all, physically, digital, bundle).
- Set how many products to fetch and how many per row.
- Switch the row to a slider (carousel) and pick arrow position (top / center).
- Set spacing between cards on desktop and mobile, and a color and icon for the section header (theme-dependent).
- Sort by id, name, or random, and pick the direction.
- Save / Reset / Cancel.

## What the merchant cannot do here

- Cannot fetch more than 96 products in a single showcase, or more than 6 per row.
- Cannot sort by price, sale-discount, or featured weight — only `id`, `name`, `rand` on this module. (Sort by price is on `product.filters` for listing pages, not showcases.)
- Cannot mix multiple sources — `filter` is single-valued. Need two rows? Use two instances.
- Cannot leave `filter_value` empty when `filter` is `category` / `vendor` / `product` / `tag` / `selection` — the save is rejected.

## Settings & fields

| Setting key | Type | Default | Allowed values | Validation rule | Notes |
|---|---|---|---|---|---|
| `enabled` | toggle | `true` | on / off | freeform | Master on/off |
| `enable_slider` | toggle | off | on / off | freeform | Render as a carousel instead of a static grid |
| `title` | string | `""` | 0-100 chars | `char:0,100` | Section title above the row |
| `products` | int | `4` | 1-96 | `int:1,96` | Number of products to fetch |
| `per_page` | int | `9` | hidden | freeform | Used for listing-mode dispatch on the dedicated `/showcase/{name}` page |
| `order_by` | enum | `id` | `id`, `name`, `rand` | `in:id,name,rand` | Sort field |
| `order_direction` | enum | `desc` | `asc`, `desc` | `in:asc,desc` | Sort direction; hidden when `order_by=rand` |
| `new` | enum | `both` | `yes`, `no`, `both` | `in:yes,no,both` | Filter on the New flag |
| `sale` | enum | `both` | `yes`, `no`, `both` | `in:yes,no,both` | Filter on the Sale flag |
| `featured` | enum (not always shown) | — | `yes`, `no`, `both` | `in:yes,no,both` | Filter on the Featured flag |
| `filter` | enum | `all` | `all`, `category`, `vendor`, `product`, `tag`, `selection` | `in:all,category,vendor,product,tag,selection` | Product source |
| `filter_value` | autocomplete | `[]` | category / vendor / product / selection IDs, or tag strings | freeform | Required when `filter` ≠ `all`; existence-validated |
| `type` | enum | `all` | `all`, `physically`, `digital`, `bundle` | `in:all,physically,digital,bundle` | Product type filter |
| `per_row` | int | `3` | 1-6 | `int:1,6` | Products per row |
| `space_between` | int | `0` | 0-40 | `int:0,40` | Desktop gap in px (theme-dependent) |
| `space_between_mobile` | int | `0` | 0-40 | `int:0,40` | Mobile gap in px (theme-dependent) |
| `arrows_position` | enum | `top` | `top`, `center` | `in:top,center` | Slider arrow position (when `enable_slider=on`) |
| `color` | colour string | `""` | hex / colour preset | freeform | Section-header decoration colour (theme-dependent) |
| `icon` | image select | `""` | uploaded image / icon | freeform | Section-header decoration icon (theme-dependent) |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| Save with `filter=category` and empty `filter_value` | *"Value is required."* |
| Save with `filter=product` and an unknown product ID | *"One or more products no longer exist."* |
| Save with `filter=vendor` and an unknown vendor ID | *"One or more vendors no longer exist."* |
| Save with `filter=tag` and an unknown tag | *"One or more tags no longer exist."* |
| Save with `filter=selection` and a deleted Smart Collection | *"Some product no longer exists."* |

## All themes vs theme-specific settings

Core fields are on every theme that ships a showcase row: `enabled`, `enable_slider`, `title`, `products`, `per_row`, `order_by`, `order_direction`, `new`, `sale`, `filter`, `filter_value`, `type`, `arrows_position`. Theme-dependent fields: `space_between` / `space_between_mobile` (a theme that ships it and a few modern themes), `color` / `icon` (themes with decorated section headers), and the `featured` filter (some legacy themes omit it).

Instance count also varies: a theme that ships it has four numbered rows (`showcaseProductsFirst`–`showcaseProductsFourth`) plus a `Promotions` instance; `delicious` and `happydreams` usually have two (`showcaseProducts1`, `showcaseProducts2`); many older themes have one (`showcaseProducts`).

## Business rules

### The row is fetched live on every visit

The list is rebuilt on each storefront visit from the configured `filter` source, so new matching products appear automatically. Leaving `filter_value` empty is accepted with `filter=all` but rejected with any other `filter`.

### Hand-picked order is preserved

When `filter=product`, the row renders in exactly the order of the chosen IDs — drag-reorder the autocomplete to control the sequence.

### `filter_value` is existence-validated on save

For every non-`all` filter, every chosen ID must still exist. A deleted product / vendor / category / tag / Smart Collection makes the save fail with the matching error message; remove the dangling ID before saving.

### Reset is per-instance

Each instance has its own saved settings. Reset clears one instance without touching the others. (Unlike `productsRelated`, this module does NOT share settings across instances.)

### Cache invalidation on save / reset

Save and Reset make the new layout live on the next storefront request.

### Bundle filter is independent of "in bundles" module

Setting `type=bundle` shows only bundle-type products in the row. This is DIFFERENT from [[design-module-product-in-bundles]], which shows the bundles that contain a specific product on the product detail page, and from the bundle-only [[design-module-product-bundle-showcase]] variant. For a related-products row on product detail (different fields), see [[design-module-product-related]].

### Smart Collection is the most powerful source

`filter=selection` reads from [[products-smart-collections]] — define a rule-based product set there once, then surface it as a homepage row without manually picking IDs. Smart Collections re-evaluate each request, so new matching products auto-appear.

## Related

- [[design-modules-products]] — hub.
- [[products-smart-collections]] — source for `filter=selection`.
- [[products-products]] — products that the row surfaces.
- [[products-categories]] — source for `filter=category`.
- [[products-vendors]] — source for `filter=vendor`.
- [[products-tags]] — source for `filter=tag`.
- [[marketing-landing-pages]] — page-builder uses the same module for Dynamic pages.

## Open questions

- 📡 **`featured` field availability per theme.** The field is allowed but only rendered on some themes — a per-theme audit would confirm.
- 📡 **`space_between` units.** Likely raw pixels — verify against the rendered storefront.
- 📡 **`icon` source.** The image picker pulls from store assets — confirm whether it allows external URLs.
