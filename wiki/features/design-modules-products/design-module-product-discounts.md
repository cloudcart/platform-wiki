---
type: feature
nav_path: "Design → Modules → Products → Discounts row"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/discounts
aliases: ["Discounts module", "Products on sale module", "discounts module", "product.discounts", "Sale products row", "Модул промоции"]
tags: [design, modules, products, discounts, sale]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Discounts row (`product.discounts`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Discounts** module (instance name `discounts`, type `product.discounts`) renders a row of SALE products from the SAME category as the currently viewed product — picked randomly. It is a contextual cross-sell on the product detail page: "here are some other discounted items in this category". The row is theme-specific — only themes that ship a `discounts` instance expose the card.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab — card labelled per theme (often **"Products on sale"** or **"Sale products"**); appears only when the active theme declares a `discounts` instance.

Edit-panel URL: `/admin/storefront/widgets/discounts`.

Renders on the product detail page only — slot is theme-controlled.

## What the merchant can do here

- Master enable / disable toggle.
- Title the row.
- Set how many products to show (cap).

## What the merchant cannot do here

- Cannot pick which products surface — the list is `sale=true` AND same category as the current product, with the current product excluded.
- Cannot sort — the row is randomly ordered on every request.
- Cannot filter by vendor, tag, or any other criterion.
- Cannot show more than 30 products.
- Cannot show fewer than 1 product.
- Cannot use this module on themes that do not ship the `discounts` instance.

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `enabled` | toggle | `true` | on / off | — | freeform | Master on/off |
| `title` | string | `""` | any string | 0-100 chars | `char:0,100` | Section title |
| `products` | int | `4` | 1-30 | 1-30 | `int:1,30` | Cap on products in the row |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| `products` out of 1-30 | Field-level integer-range error |

## All themes vs theme-specific

| Setting | All themes | Theme-specific notes |
|---------|-----------|----------------------|
| `enabled`, `title`, `products` | only when present | The module INSTANCE itself is theme-specific — a theme that ships it ships `discounts`, many older themes don't |
| Slot rendering | theme | Renders only where the theme has placed a `discounts` slot |

Themes confirmed to ship a `discounts` instance: a theme that ships it. Older themes typically omit it.

## Business rules

### Source is same-category SALE products

The runtime queries products WHERE `category_ids` contains the current product's category AND `sale=true` AND `id != current product`. The result is randomly ordered, capped at `products`.

### Random order on every request

The module uses random sort, so the row content reshuffles on every page view. The merchant cannot enforce a stable order.

### Empty row hides

If the current category has no other sale products, the row self-hides — no empty header.

### No product detail context = empty row

The module only runs on pages with a "current product" in the rendering context (i.e., product detail pages). On other pages the module renders an empty row.

### Reset is per-instance

Per-instance JSON; reset clears only the instance.

### Cache invalidation on save / reset

Standard — save / reset bump the per-site cache key.

## Related

- [[design-modules-products]] — hub.
- [[products-categories]] — category that the current product belongs to.
- [[marketing-discounts]] — discount rules that put products on sale.
- [[design-module-product-related]] — sibling row not restricted to sale products.
- [[design-module-product-showcase]] — for homepage sale rows (uses `filter=sale` or `sale=yes`).

## How it works (verified against backend)

### Restrictions

`enabled=false (toggle), title=char:0,100, products=int:1,30`.

### Defaults

`enabled=true, title="", products=4`.

### Source query

Listing driver with `category_ids = [current.category_id]`, `sale = true`, `item_id != current.id`, sort `random-asc` or `random-desc` (coin-flipped), limit `products`.

### Save pipeline

Casts `enabled` to bool. No shared `Configuration` group — per-instance only.

### No category context = empty

If the registry has no `product.view` (i.e., the module is invoked outside a product detail page), the runtime returns an empty collection without querying.

## Open questions

- 📡 **Same-category scope.** The query checks the product's PRIMARY category. Behaviour with multi-category products (where the product belongs to several categories) needs verification — likely only the primary is used.
- 📡 **Discount expiry filtering.** Whether the SALE flag respects discount validity windows or just the `sale` denormalised column needs verification.
