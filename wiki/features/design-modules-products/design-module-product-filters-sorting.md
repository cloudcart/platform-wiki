---
type: feature
nav_path: "Design → Modules → Products → Product Catalog Settings → sorting"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/filters
aliases: ["Listing sort", "Default product order", "Default sort", "Sort number vs default sort", "Manual sort", "Подреди по", "Посока на подреждане", "Добави опции за 'подреди по'", "Ръчно сортиране", "Подреждане на продуктите в категория"]
tags: [design, modules, products, catalog, sorting, listing]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

# Product Catalog Settings — how listings are sorted

> Part of [[design-modules-products]]. The card itself is [[design-module-product-filters]].

## Purpose

How the order of products on category, brand, smart-collection, tag and all-products pages is decided: the default sort set on the **Product Catalog Settings** card, the sort options the shopper can pick, and when the per-product **Sort number** counts.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab (*Продукти*) → card **Product Catalog Settings** (*Настройки на продуктов каталог*), edit panel `/admin/storefront/widgets/filters`. The Sort number is a field in the product editor ([[products-editor]]) and a bulk action ([[products-bulk-actions]]).

## What the merchant can do here

- Tick the sort options shoppers may choose.
- Pick the default sort and its direction.
- Order products by hand with the Sort number, by choosing **Ръчно сортиране** as the sort.

## Settings & fields

| Field (Bulgarian admin label) | Key | What it does |
|---|---|---|
| **Добави опции за 'подреди по'** — checkboxes | `order_by_options` | The sort options shown to shoppers. At least one must stay ticked. |
| **Подреди по** — dropdown | `order_by` | The default sort. |
| **Посока на подреждане** — **Възходящ** / **Низходящ** | `order_direction` | The default direction. |

Both lists offer the same six options, always in this order:

| Admin label | Key | Sorts by |
|---|---|---|
| Разпродажба | `sale` | Products on sale first, then Featured ones (the basic engine lists newest first) |
| Препоръчан | `featured` | Products marked Featured first |
| Дата | `id` | Date added (product ID): ascending = oldest first, descending = newest first |
| Име | `name` | Product name |
| Цена | `price_from` | Lowest price of the product |
| Ръчно сортиране | `sort_order` | The per-product Sort number |

The card's defaults are **Дата**, **Възходящ** (oldest first), with all six options ticked. When no default sort is saved at all, listings show newest first.

## Business rules

### The default must be one of the shopper options

The **Подреди по** dropdown enables only the options ticked under **Добави опции за 'подреди по'**; the others are greyed out. Unticking the option that is the current default switches the default to the first ticked option. So a dropdown that offers only **Дата** and **Цена** means only those two are ticked.

### What the shopper sees

The storefront sort dropdown lists only the ticked options. **Дата**, **Име** and **Цена** appear twice, ascending and descending; Sale, Featured and manual sort appear once. The shopper labels come from the storefront translations, which the theme can change; the defaults are "Подреди по дата", "Подреди по име", "Подреди по цена", "Sale", "Препоръчан" and "По подразбиране" (manual sort). The shopper's choice is kept in the page address, and the search results page has its own relevance-first options instead (see [[storefront-search-new]]).

### When the Sort number counts

The Sort number orders products **only while the listing is sorted by Ръчно сортиране**, as the default or as the shopper's choice. With any other sort it is ignored. **Посока на подреждане** decides the direction: **Възходящ** puts the smallest number first, **Низходящ** the largest. A shopper who picks manual sort gets the saved direction.

Under manual sort, products with the same number are ordered Featured first, then oldest first.

### Blank Sort number vs 0

A blank Sort number is stored as "no number", and 0 is a number. Where they land depends on the store's listing engine ([[apps-listing-engine]]):

- **Indexed engine:** products with no number come after all numbered products, in both directions.
- **Basic database engine:** with **Възходящ** they come before 0; with **Низходящ** after all numbered products. (verify which engine a store runs)

To control the order, give every product a number.

### Sold-out products last

The switch to put products without stock at the end of the listing comes before every sort, see [[design-module-product-filters]].

## Related

- [[design-module-product-filters]] — the card and its other settings.
- [[design-module-product-filters-sidebar]] — the filter sidebar.
- [[products-editor]] — the Sort number field.
- [[products-bulk-actions]] — setting the Sort number on many products.
- [[products-known-issues]] — product-order quirks.
- [[apps-listing-engine]] — indexed vs basic engine.

## Open questions

- Bulgarian labels of the product editor's Sort number field (translations database).
