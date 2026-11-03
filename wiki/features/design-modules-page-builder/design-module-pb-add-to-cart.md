---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Add to cart"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Add to cart module", "Add-to-cart block", "Buy button block", "Модул добави в количка"]
tags: [design, modules, page-builder, add-to-cart, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Add to cart block (`add-to-cart`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Add to cart** block renders a standalone "Add to cart" button bound to a specific product. The customer clicks it and the product is added to the cart without leaving the page. Useful on landing pages where the merchant wants a single product hero with a direct purchase CTA (e.g., a flash-sale page, a single-product launch page, a campaign landing page).

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Add to cart** from the block picker.

## What the merchant can do here

- Pick the product the button adds to the cart (autocomplete search by name / SKU).
- Pick the button colour (theme-shipped colour variants).
- Pick the button size (small / normal / large; depends on theme support).
- Pick the button position (left / center / right).
- Toggle full-width.
- Set an override text (custom button label) — if blank, the global "Add to cart" translation is used.
- Add custom HTML attributes (`data-*`, `id`, etc.) for analytics / styling hooks.
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot bind the block to a customer-picked product — the product is fixed at design time.
- The merchant cannot adjust the global "Add to cart" translation here — that lives in [[settings-translations]] / [[settings-general]].
- The merchant cannot add VAT / quantity selectors from this block — it's a single-click add only. Use the full Product block ([[design-module-pb-product]]) for variant pickers.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `filter_value` | product picker (autocomplete) | `null` | Product ID the button adds to the cart. Source: `admin.autocomplete.products` route. |
| `color` | image-preview select | `_button` | Theme-shipped colour variant — applied via CSS class on the button. |
| `size` | select | `''` | Theme-shipped size variant. |
| `position` | select | `text-center` | Horizontal position: `text-left` / `text-center` / `text-right`. |
| `full_width` | toggle | `''` | When ON, the button stretches to the row width. |
| `override_text` | text input | `''` | Custom button label — overrides the global "Add to cart" translation when set. |
| `text` | text input | `''` | (verify — set via override) |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]] for the builder's save flow (auto-save + history).

## Business rules

### Product is fixed at design time

The bound product (`filter_value`) is picked when the merchant builds the page. If the merchant later wants a different product, they edit the block. There is no dynamic / runtime product selection here.

### Picks up global button radii

The block uses the same `<a class="_button...">` HTML as every other button on the storefront — meaning it inherits the global button corner-radius from [[design-module-buttons-settings]] and the theme's button colour palette.

### Helper: empty product = helper card

If the merchant hasn't picked a product yet (or the merchant has no products at all), the block renders a helper card pointing to the product create flow — `getHelperData` returns the helper title / text / action URL. This keeps the builder from rendering a broken button.

### Falls back to global "Add to cart" translation

When `override_text` is blank, the button label uses the global `sf.product.add_to_cart` translation. The merchant can override per-language via [[settings-translations]] if they want a custom label without using `override_text`.

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-button]] — sibling: generic Button block with a custom link (not bound to a product).
- [[design-module-pb-product]] — sibling: full Product detail block (with variant pickers, gallery, description).
- [[design-module-buttons-settings]] — global button radii applied to this block.
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.
- [[products-products]] — the product the button binds to.

## Open questions

- 📡 **Variant handling.** When the bound product has variants, the block may default to the first variant or require the customer to pick on the cart page. Confirm exact behaviour. (verify)
- 📡 **Out-of-stock UX.** When the bound product is out of stock, does the block hide itself, render disabled, or render with an "out of stock" label? (verify)
