---
type: feature
nav_path: "Design → Modules → Products → Linked products"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/linkedProducts
aliases: ["Linked products module", "linkedProducts module", "product.linked", "Модул свързани продукти ръчно", "Linked products row"]
tags: [design, modules, products, linked]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Linked products (`product.linked`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Linked products** module (instance name `linkedProducts`, type `product.linked`) renders the row of products that the merchant has EXPLICITLY linked from the product editor — see [[products-products]] for how the linked-product list is built per product. Unlike [[design-module-product-related]], which derives its list at render time via category / vendor / tag matching, this module shows ONLY the products the merchant manually pinned to the current product.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab → card labelled **"Linked products"**.

Edit-panel URL: `/admin/storefront/widgets/linkedProducts`.

Renders on the product detail page; the exact slot is theme-controlled. The module displays the current product's `linked_products_ids` minus the product itself.

## What the merchant can do here

- Title the row.
- Toggle whether to show the row title, image, price, buy button, and quick-view link.
- Pick how many products per row on desktop and on mobile.
- Pick a render position — variant / recommended / section_recommended (theme slot key).
- Cap the maximum number of card title lines.

## What the merchant cannot do here

- Cannot set which products link to which — that is per-product on the product editor in [[products-products]] (Linked products tab).
- Cannot exceed 6 products per row on desktop or 4 on mobile.
- Cannot allow more than 5 title rows on a card.
- Cannot filter / sort the linked products — they always render in the order they were pinned on the product editor.

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `enabled` | bool | `true` | on / off | — | `bool` | Master on/off |
| `title` | string | `""` | any string | 0-100 chars | `char:0,100` | Section title |
| `show_title` | bool | `true` | on / off | — | `bool` | Show the section title |
| `show_image` | bool | `true` | on / off | — | `bool` | Show product image on each card |
| `show_price` | bool | `false` | on / off | — | `bool` | Show price on each card |
| `show_buy_btn` | bool | `false` | on / off | — | `bool` | Show Buy button on each card |
| `show_as_quick_view` | bool | `false` | on / off | — | `bool` | Open product in quick-view modal instead of full nav |
| `per_row_desktop` | int | `3` | 1-6 | 1-6 | `int:1,6` | Cards per row on desktop |
| `per_row_mobile` | int | `2` | 1-4 | 1-4 | `int:1,4` | Cards per row on mobile |
| `position` | enum | `variant` | `variant`, `recommended`, `section_recommended` | — | `in:variant,recommended,section_recommended` | Slot identifier the theme uses to place the row |
| `max_title_rows` | int | `2` | 1-5 | 1-5 | `int:1,5` | Maximum lines for the card title |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| `per_row_desktop` out of 1-6 | Field-level integer-range error |
| `per_row_mobile` out of 1-4 | Field-level integer-range error |
| `position` not in enum | Field-level enum error |

## All themes vs theme-specific

| Setting | All themes | Theme-specific notes |
|---------|-----------|----------------------|
| Core fields | yes | Every theme that ships product detail pages |
| `position` slot rendering | theme | The string is forwarded to the theme; if the theme does not recognise the slot key, the row renders in the default slot or not at all |

## Business rules

### Source is explicit linking, not matching

The module reads `linked_products_ids` on the current product record. The merchant builds this list inside the product editor (Linked products tab). Adding / removing a product on the editor changes what this module renders for that product.

### Order is preserved

The runtime fetches the linked products by IDs, then re-orders them to match the order in `linked_products_ids`. So the merchant controls the row sequence by drag-reorder on the product editor.

### Empty list hides the row

If the product has no linked products (or only itself), the row self-hides — no empty header is shown.

### `position` controls theme slot

The `position` value (`variant`, `recommended`, `section_recommended`) is a slot identifier the theme template reads to decide WHERE on the product page to render the row. Themes that do not recognise the value fall back to the default slot. This is the merchant's only control over WHERE the row appears (vs WHAT it contains).

### Quick view mode

When `show_as_quick_view=on`, clicking a card opens the product in a side-panel modal instead of navigating to the product page. The card itself still links to the product page; only the click handler changes.

### Cache invalidation on save / reset

Standard — save / reset bump the per-site cache key.

## Related

- [[design-modules-products]] — hub.
- [[products-products]] — product editor where linked products are pinned.
- [[design-module-product-related]] — auto-matched row (vs this explicit-linking row).
- [[design-module-product-bundle-showcase]] — for grouped-product packages.

## How it works (verified against backend)

### Restrictions

`enabled=bool, title=char:0,100, show_title=bool, show_image=bool, show_price=bool, show_buy_btn=bool, show_as_quick_view=bool, per_row_desktop=int:1,6, per_row_mobile=int:1,4, position=in:variant,recommended,section_recommended, max_title_rows=int:1,5`.

### Defaults

`enabled=true, title="", show_title=true, show_image=true, show_price=false, show_buy_btn=false, show_as_quick_view=false, per_row_desktop=3, per_row_mobile=2, position=variant, max_title_rows=2`.

### Source resolution

The module pulls `linked_products_ids` from the current product, removes the current product's own ID, batch-loads the remaining IDs from the listing driver, then re-orders by the original ID sequence to preserve merchant-defined order.

## Open questions

- 📡 **Theme support for `position=section_recommended`.** Not every theme honours the value — per-theme audit needed.
- 📡 **Linked-product limit per product.** The module renders all linked IDs (no `products` cap field). If a merchant links 100 products, the row gets very long — verify whether the storefront paginates or trims.
