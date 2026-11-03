---
type: feature
nav_path: "Design → Modules → Products → Product listing"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/productsListing
aliases: ["Product listing module", "productsListing module", "product.listing", "Product list view config", "Модул продуктов списък"]
tags: [design, modules, products, listing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Product listing (`productsListing`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Product listing** module (instance name `productsListing`, type `product.listing`) is a SIBLING of the `filters` module — it holds the pagination, sort, and price-range defaults for the storefront product-listing pages on themes that ship a separate listing module. On most modern themes the same job has migrated to the [[design-module-product-filters]] module; older themes still expose `productsListing` as the canonical settings card. Tuning this module controls the same listing pages (category, search, vendor, smart collection) but with a smaller field set.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab → card labelled per the theme (commonly **"Products listing"** or **"Catalog settings (legacy)"**).

Edit-panel URL: `/admin/storefront/widgets/productsListing`.

Only themes that declare a `productsListing` instance in their theme JSON expose the card. Modern themes (e.g., a theme that ships it, `themex`, another custom theme) skip the instance and rely on `filters` instead.

## What the merchant can do here

- Set the default products-per-page and the customer-pickable per-page options.
- Set the default sort field and direction, plus the customer-pickable sort options.
- Define pre-defined price-range chips (when not in slider mode) or the slider step.
- Toggle which filter chips appear in the sidebar (categories / vendors / sort / per-page / price ranges).

## What the merchant cannot do here

- Cannot change the storefront card visuals (price / buy / wishlist toggles) — those live on [[design-module-product-filters]] or `product.related`-style siblings, not here.
- Cannot pick out-of-stock visibility, second-image hover, or any of the other card display options — those are `filters`-only.
- Cannot pick the `featured` / `sort_order` sort option — the listing module restricts sorting to `id`, `name`, `price_from`, `sale`, `new` (narrower than `filters`).

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `per_page` | int | `15` | any int 2-100 | 2-100 | `int:2,100` | Default products-per-page; must be in `per_page_options` |
| `per_page_options` | array of int | `[15, 30, 50]` | each entry 2-100 | 2-10 entries | `array:2,10\|int:2,100` | Per-page picker options on the storefront |
| `order_by` | enum | `id` | `id`, `name`, `price_from`, `sale`, `new` | — | `in:id,name,price_from,sale,new` | Default sort |
| `order_by_options` | array of enum | `['id','name','price_from','sale']` | values include `id`, `name`, `price_from`, `sale` | 2-20 entries | `array:2,20\|in:id,name,price_from,sale` | Customer-visible sort options |
| `order_direction` | enum | `asc` | `asc`, `desc` | — | `in:asc,desc` | Default sort direction |
| `products_price_ranges` | repeater of `{from,to}` | `[]` | each row two ints | 1-2 rows (verify) | `array:1,2` | Pre-defined price-range chips |
| `price_range_step` | int | — | any positive int | — | freeform | Slider step (when theme uses slider mode) |
| `filters_options` | array of enum | `['sort','sort_direction','categories','price_ranges','vendors','per_page_filter']` | values: `sort`, `sort_direction`, `categories`, `price_ranges`, `vendors`, `per_page_filter` | 0-20 entries | `array:0,20` | Which filter chips show in the sidebar |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| Reset confirmation | *"Are you sure you want to reset this module?"* |
| `per_page` out of range | Field-level integer-range error |
| `per_page_options` length out of 2-10 | Field-level array-length error |
| `order_by` value not in enum | Field-level enum error |

## All themes vs theme-specific

| Theme | `productsListing` instance present | Notes |
|-------|-----------------------------------|-------|
| a theme that ships it, `themex`, another custom theme | NO | Replaced by `product.filters` |
| Older `delicious`, `happydreams`, similar | YES | Card visible; sole listing-settings module |

Themes that ship BOTH (`filters` AND `productsListing`) are rare; if present, treat `filters` as authoritative and `productsListing` as the legacy duplicate.

## Business rules

### Sister module to `filters`

`product.listing` and `product.filters` are intentionally similar — `filters` is the modern superset and `listing` is the trimmed legacy. Both write into the same `Configuration` group (`list.product`), so a save on one is visible to the other.

### `per_page` must match an entry in `per_page_options`

Same constraint as on `filters` — the default must be a customer-pickable option.

### Cache invalidation on save / reset

Save and Reset bump the per-site cache key, so storefront changes are visible on the next request.

### Reset re-publishes the shared `Configuration`

Because the module uses a shared `Configuration` group, Reset deletes the per-instance row AND re-publishes the type-level defaults. Other consumers of `list.product` see the reset immediately.

## Related

- [[design-modules-products]] — hub.
- [[design-module-product-filters]] — modern superset; prefer when present.
- [[design-modules]] — parent module editor.
- [[products-categories]] — listing pages this module drives.
- [[marketing-landing-pages]] — Dynamic pages for per-page overrides.

## How it works (verified against backend)

### Restrictions are a narrower subset of `filters`

`product.listing` declares fewer sort options (`id`, `name`, `price_from`, `sale`, `new`) and fewer filter-chip values than `product.filters` (`sort`, `sort_direction`, `categories`, `price_ranges`, `vendors`, `per_page_filter` only — no `variants`, `new`, `sale` chips).

### Shared `Configuration` group

`product.listing` and `product.filters` both publish into the `list.product` Configuration group on save. The runtime reads merged settings from the group, so the two modules coordinate when both are present.

## Open questions

- 📡 **Which themes still ship `productsListing` as primary.** Most current themes have migrated to `filters`. A per-theme audit would establish which themes still surface the legacy card.
- 📡 **Settings carry-over when migrating from `productsListing` to `filters`.** Because they share `Configuration`, settings should transfer cleanly — verify on a real migration.
