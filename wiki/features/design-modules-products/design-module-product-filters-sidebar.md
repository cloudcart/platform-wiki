---
type: feature
nav_path: "Design → Modules → Products → Product Catalog Settings → filter sidebar"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/filters
aliases: ["Listing filter sidebar", "Filter sidebar", "Hide the filters", "Turn off filters", "Categories filter block", "Sidebar categories", "Настройки за показване на филтри", "Настройки за подредба на филтрите", "Позиция на филтрите", "Филтри в категория", "Покажи филтри"]
tags: [design, modules, products, catalog, filters, sidebar, listing]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

# Product Catalog Settings — the filter sidebar

> Part of [[design-modules-products]]. The card itself is [[design-module-product-filters]].

## Purpose

What decides the filter sidebar on category, brand, smart-collection, tag and all-products pages: which filter blocks the merchant switches on, how to hide the sidebar, what each block lists, and which categories the **Categories** block shows.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab (*Продукти*) → **Product Catalog Settings** (*Настройки на продуктов каталог*), `/admin/storefront/widgets/filters`. The same settings apply to every listing page; there is no per-category or per-page version.

## What the merchant can do here

- Tick which filter blocks show in the sidebar.
- On themes that support it, set the order of the blocks and the sidebar's position.
- Switch on product counts next to filter values.

## Settings & fields

### Filter blocks — box *Настройки за показване на филтри*

The theme decides which checkboxes appear. Labels in the Bulgarian admin:

| Label | Key | Block |
|---|---|---|
| Подреждане | `sort` | Sort dropdown, see [[design-module-product-filters-sorting]] |
| На страница | `per_page_filter` | Products-per-page picker |
| Категории | `categories` | Categories block |
| Производители | `vendors` | Brands |
| Цени | `price_ranges` | Price ranges or price slider |
| Разновидности | `variants` | Variant values (size, colour…) |
| Нови | `new` | New products |
| Разпродажба | `sale` | Products on sale |
| Препоръчан | `featured` | Featured products (only where the theme lists it) |
| Марка и Модел | `brand_model` | Brand & Model app filter |

**Покажи бройки продукти на филтрите** (`show_facet_counts`) adds a product count next to each value.

### New themes only

- **Настройки за подредба на филтрите** — a number per block; the smaller the number, the higher the block.
- **Позиция на филтрите** (`list`) — where the filters sit, from the theme's own list. The themes that offer it list **Ляво** (left), **Отгоре** (top) and **Дясно** (right).

## Business rules

### Hiding the whole sidebar

There is no separate on/off switch. Untick every checkbox under *Настройки за показване на филтри* and save: the sidebar and the mobile "show filters" button disappear. Two blocks have no checkbox and still show when they have values:

- **category characteristics** — on category pages, the category's characteristics that are Active and have **Use as filter** on ([[products-property-list-view]]), drawn by the theme's characteristics module ([[design-modules-utility-system]]; verify per theme);
- **Марка и Модел** on themes whose checkbox list does not include it.

A block with nothing to list is not drawn either, so an empty sidebar does not leave an empty frame.

### What the filters can list

The listing engine builds filter values for categories, brands, category characteristics, variant values, price, Brand & Model, and the New / On sale / Featured flags, from the products in the current listing.

### Turning off one value

- **Variant values** have an **Active** switch of their own on the variant's values list. An inactive value, or an inactive variant type, drops out of the filter.
- **Characteristic values** have no switch of their own. The whole characteristic leaves the sidebar when it is made inactive or **Use as filter** is turned off.

### Which categories the Categories block lists

Most themes build the block from the current listing: it lists every category that holds at least one product of the listing, plus that category's parent categories. The category being browsed does not narrow it, but a smart collection, brand or tag page and any selected filter do. So:

- on a **smart-collection page** (`/selection/...`) only categories with products in that collection show;
- on a **category page** the block shows every category that has listable products, so it usually looks like the whole tree.

Some older themes list the whole category tree instead. (verify per theme)

Either way, a category with no active, published product in it or its subcategories is not shown. Categories have no hidden / published switch of their own. How many levels are expanded, and whether only the current branch opens, is drawn by the theme's template. (verify per theme)

The category setting **Display subcategories** does not change this block; it only controls the subcategory tiles at the top of the category page (see [[category-entity-business-rules]]).

## Related

- [[design-module-product-filters]] — the card.
- [[design-module-product-filters-sorting]] — sorting.
- [[products-property-list-view]] — Use as filter on characteristics.
- [[storefront-category]] — the category page.
- [[selection]] — the smart-collection page.
- [[apps-listing-engine]] — the engine that builds the filter values.

## Open questions

- Bulgarian label of the **Use as filter** column and of the variant values' Active switch (translations database).
- Which themes still list the whole category tree in the Categories block.
