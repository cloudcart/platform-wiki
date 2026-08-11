---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Product"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Product module", "Product detail block", "Single product block", "Модул продукт"]
tags: [design, modules, page-builder, product, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Product block (`product`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Product** block renders a full product detail view inline on a Dynamic page — image gallery, title, price, variants, description, and (when configured) detailed product information. Used for single-product landing pages, flash-sale launch pages, and campaign pages where the merchant wants the product detail surfaced without sending the customer to the product's own URL.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Product** from the block picker.

## What the merchant can do here

- Pick the product the block surfaces (autocomplete search by name / SKU) via the `filter_value` picker.
- Pick a theme-shipped colour highlight (when the theme advertises `functions.product_showcase.color.status`).
- Pick a theme-shipped icon (when the theme advertises `functions.product_showcase.icon.status`).
- Configure the product-details panel below the main view (merged in from the global product-details module settings).
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot bind the block to a customer-picked product — the product is fixed at design time.
- The merchant cannot change the gallery layout, button placement, or variant picker style — those are controlled by the active theme.
- The merchant cannot disable specific sections (gallery / description / reviews) per-block — the surfaces are theme-defined.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `filter_value` | product picker (autocomplete) | `null` | Product ID the block surfaces. Source: `admin.autocomplete.products` route. |
| `color` | text input (hex) | `''` | Theme-shipped colour highlight. Only renders when theme advertises `functions.product_showcase.color.status`. |
| `icon` | select | `''` | Theme-shipped icon overlay. Only renders when theme advertises `functions.product_showcase.icon.status`. |

The block ALSO merges in the global product-details module restrictions and defaults — meaning the side panel may include extra fields (e.g., "show short description", "show reviews count", etc.) sourced from the global `product.productsDetails` module. The exact list depends on what the global module exposes.

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Product is fixed at design time

The bound product (`filter_value`) is picked when the merchant builds the page. To swap to a different product, the merchant edits the block. There is no runtime / customer-driven product selection.

### Inherits product-details settings

The Product module's `_default_settings` and `_restrictions` are merged at construct time with the global `product.productsDetails` module — so settings like "show short description" or "show vendor" are available here even though they live on the global module by default. This keeps the inline block visually consistent with the standalone product detail page.

### Sets the product-details module context

When the block renders on the storefront (non-sitecp namespace), the module call also pushes its `_settings` into the platform code global context — so any product-details sub-renders pick up the same settings as the parent block.

### Helper card when no product is picked

If the merchant hasn't picked a product yet, the block renders a helper card with a link to the product create flow — `getHelperData` returns the helper title / text / action URL.

### Theme dependencies for colour / icon

Some themes ship per-block colour / icon options (highlighted ribbon, icon overlay). The block only renders those rows when the theme's `theme_config` advertises them. On themes without those features, the colour / icon fields are hidden.

### Variants render based on the bound product

When the bound product has variants, the variant picker renders inside the block — the customer picks variant attributes (size, colour, etc.) and the price / stock updates accordingly. The merchant doesn't pre-select a variant from the block settings.

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-add-to-cart]] — sibling: minimal product-bound add-to-cart button.
- [[design-module-pb-bundle-products]] — sibling: bundle showcase block.
- [[products-products]] — product catalogue (the bound product source).
- [[variants-model]] — variant model (how attribute pickers work).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Full field list.** The block merges in `product.productsDetails` settings — the exact merged catalogue depends on the global module's restrictions. (verify against the global module)
- 📡 **Out-of-stock behaviour.** When the bound product is out of stock, does the block hide the add-to-cart button, render disabled, or show a "notify me" toggle? (verify per theme)
