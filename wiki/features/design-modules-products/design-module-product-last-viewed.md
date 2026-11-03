---
type: feature
nav_path: "Design → Modules → Products → Last viewed products"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/lastViewed
aliases: ["Last viewed products module", "lastViewed module", "product.lastViewed", "Recently viewed module", "Модул последно видени продукти"]
tags: [design, modules, products, lastviewed, personalisation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Last viewed products (`product.lastViewed`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Last viewed products** module (instance name `lastViewed`, type `product.lastViewed`) renders a row of products the CURRENT shopper has recently viewed, sourced from a browser cookie (`cc_latest_viewed`). It is a passive personalisation tool: there are no curation controls — the platform fills the row from the shopper's own clicks. First-time visitors see an empty row (the module self-hides).

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab → card labelled **"Last viewed products"** (or theme-specific equivalent).

Edit-panel URL: `/admin/storefront/widgets/lastViewed`.

Slot placement is theme-controlled — typically homepage, cart sidebar, or product detail page. Some themes render multiple slots.

## What the merchant can do here

- Title the row (e.g., "You recently viewed").
- Set how many products to show (cap).
- Pick a section-header colour and icon (theme-dependent decoration).
- Master enable / disable toggle.

## What the merchant cannot do here

- Cannot bias what shows up — the list comes from the shopper's cookie, in the order they were viewed.
- Cannot filter by category, vendor, tag, or anything else.
- Cannot force the row to show for new visitors — without a cookie history, the row is empty and self-hides.
- Cannot exceed 30 products in the row.
- Cannot show fewer than 2 products in the row.

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `enabled` | toggle | `true` | on / off | — | freeform | Master on/off |
| `title` | string | `""` | any string | 0-100 chars | `char:0,100` | Section title |
| `products` | int | `4` | 2-30 | 2-30 | `int:2,30` | Cap on products in the row |
| `color` | colour string | `""` | hex / preset | — | freeform | Section-header decoration colour (theme-dependent) |
| `icon` | image select | `""` | uploaded image | — | freeform | Section-header decoration icon (theme-dependent); save derives `icon_data` |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| `products` out of 2-30 | Field-level integer-range error |

## All themes vs theme-specific

| Setting | All themes | Theme-specific notes |
|---------|-----------|----------------------|
| `enabled`, `title`, `products` | yes | Universal |
| `color`, `icon` | depends | Only on themes that advertise decorated section headers (e.g., a theme that ships it) |

## Business rules

### Cookie-driven, not server-stored

Source is the `cc_latest_viewed` cookie. The cookie is a JSON array of product IDs maintained client-side. The module reads the cookie at render time, deduplicates and filters to existing products, and renders up to `products` of them. No server-side history is kept.

### Crawler requests skip the source

Search-engine crawlers do not have shopper cookies, so the module returns an empty list for crawler requests. The row self-hides for crawlers regardless of merchant configuration.

### Hard upper bound is 30

The runtime caps the list at 30 even if the merchant somehow sets a higher number; the form restriction itself caps at 30.

### Order preserves browsing sequence

Products render in the order the shopper viewed them (most-recent-first by cookie insertion order). The merchant cannot override this order.

### Reset republishes shared `Configuration`

`product.lastViewed` writes its merged settings into a shared `Configuration` group (`last.viewed`). Reset deletes the per-instance row AND re-publishes the type-level defaults to the group. The save handler also regenerates the storefront JS apps bundle to refresh the cookie-handling code.

### Empty row hides

If the shopper has no cookie or all cookie IDs no longer exist as products, the row self-hides.

## Related

- [[design-modules-products]] — hub.
- [[products-products]] — products that get tracked.
- [[design-module-product-related]] — alternative recommendation row (matched server-side).
- [[design-module-product-showcase]] — for non-personalised homepage rows.

## How it works (verified against backend)

### Restrictions

`enabled=false (toggle), title=char:0,100, products=int:2,30, color=false (freeform), icon=false (freeform)`. The `enabled` and `icon` restrictions being `false` in the map means they are unconstrained at the schema layer — they are validated separately by the save handler.

### Defaults

`enabled=true, title="", products=4, color="", icon=""`.

### Save pipeline regenerates apps JS

The save handler casts `enabled` to bool, derives `icon_data` if `icon` is set, persists the settings, publishes the `last.viewed` Configuration group, then runs the `js:apps-generate` artisan command to rebuild the storefront apps bundle for the site. This is heavier than most module saves because the personalisation logic lives in JS.

### Cookie limit

The runtime slices the cookie array to the configured `products` count before fetching products.

## Open questions

- 📡 **Cookie TTL.** How long `cc_latest_viewed` persists in the shopper's browser is a JS-side setting — verify against the storefront JS or by inspecting a live cookie.
- 📡 **Cross-device personalisation.** None — without server-side history, viewing on mobile does not surface on desktop. A future feature could rely on customer-account history.
