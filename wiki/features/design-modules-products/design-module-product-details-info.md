---
type: feature
nav_path: "Design → Modules → Products → Product details info"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/productsDetails
aliases: ["Product details module", "Product detail page module", "productsDetails module", "product.productsDetails", "Detail information for product", "Модул детайли на продукта", "Product page fields module"]
tags: [design, modules, products, product-detail]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Product module — Product details info (`product.productsDetails`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Product details info** module (instance name `productsDetails`, type `product.productsDetails`) is the single most impactful product module — it controls which fields, badges, and actions appear on the product detail page. Price, Buy button, stock-status badge, SKU, vendor, category, characteristics, gallery, compare, wishlist, quantity selector, description, short description, page-link block, and a few variant-handling tweaks all live here. Almost every merchant question of the form "how do I show / hide X on the product page?" routes to this module.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab → card labelled **"Detail information for product"** (or theme-translated equivalent).

Edit-panel URL: `/admin/storefront/widgets/productsDetails`.

The module controls every product detail page on the storefront.

## What the merchant can do here

- Toggle visibility for every field on the product page (price, status, SKU, vendor, category, characteristics, gallery, tags, descriptions, social-share) — see Settings & fields for the full list of toggles.
- Show or hide the exact stock quantity inside the status badge.
- Show or hide the BUY button, QUANTITY selector, COMPARE and WISHLIST actions.
- Link to a static page (e.g., "Delivery info") from the product page; optionally render the link as a side-panel popup.
- Include characteristic images (e.g., colour swatches) in the category-characteristics table.
- Append the selected variant value to the product H1, and pre-select the first variant on page load.

## What the merchant cannot do here

- Cannot pick WHERE each field renders on the page — slot placement is theme-controlled.
- Cannot show the exact stock quantity (`show_product_quantity_in_status`) without first turning on `show_product_status`.
- Cannot link to multiple static pages — `details_page_id` is a single page ID.
- Cannot disable the H1 product name — only fields BESIDES the name are toggleable.
- Cannot hide the product images entirely (only the GALLERY toggle — the main image still renders).

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `show_price` | toggle | `true` | on / off | — | freeform | Price block |
| `details_show_buy` | toggle | `true` | on / off | — | freeform | BUY / Add-to-cart button |
| `show_product_status` | toggle | `true` | on / off | — | freeform | In-stock / out-of-stock badge |
| `show_product_quantity_in_status` | toggle | `false` | on / off | — | freeform | Exact stock number in the badge ("3 in stock") |
| `show_SKU` | toggle | `true` | on / off | — | freeform | SKU field |
| `show_brand` | toggle | `true` | on / off | — | freeform | Vendor / brand link |
| `show_category` | toggle | `true` | on / off | — | freeform | Category link |
| `show_categories_characteristics` | toggle | `true` | on / off | — | freeform | Category-characteristics table (specs) |
| `show_categories_characteristics_with_images` | toggle | `false` | on / off | — | freeform | Render characteristic values with images (swatches) |
| `show_images_in_gallery` | toggle | `true` | on / off | — | freeform | Show all product images in the gallery |
| `show_compare` | toggle | `true` | on / off | — | freeform | Add-to-compare action |
| `show_wishlist` | toggle | `true` | on / off | — | freeform | Add-to-wishlist action |
| `choose_quantity` | toggle | `true` | on / off | — | freeform | Quantity selector |
| `show_product_description` | toggle | `true` | on / off | — | freeform | Full description block |
| `short_product_description` | toggle | `true` | on / off | — | freeform | Short description block |
| `social_media_share` | toggle | `true` | on / off | — | freeform | Social-share buttons |
| `choose_display_pages` | toggle | `true` | on / off | — | freeform | Per-page settings (theme-specific) |
| `show_page` | toggle | `false` | on / off | — | freeform | Show a link to a static page |
| `details_page_id` | int | `0` | any existing CMS page ID | 1-2 000 000 | `int:1,2000000` | Page to link to when `show_page=on`; page from [[marketing-landing-pages]] |
| `show_link_as_popup` | toggle | `true` | on / off | — | freeform | Render the page link as a side-panel popup instead of nav-away |
| `pre_selected_variant` | toggle | `true` | on / off | — | freeform | Pre-select the first variant on load |
| `hide_tags` | toggle | `false` | on / off | — | freeform | Hide tag chips |
| `variant_in_name` | toggle | `false` | on / off | — | freeform | Append selected variant to the H1 product name |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| `details_page_id` out of 1-2 000 000 | Field-level integer-range error |

All toggles above are universal — every theme that ships a product detail page reads them. Only the SLOT (where each field renders, and styling such as a heart icon vs a button for wishlist) is theme-controlled; the merchant controls visibility, not placement.

## Business rules

### `productsDetails` is auto-injected even when missing from the theme

`productsDetails` is a SYSTEM module: even when the active theme does not declare it, the platform injects it so the card always appears on the Modules screen and the merchant can always tune the product detail page.

### `show_product_quantity_in_status` requires `show_product_status`

The exact-quantity hint renders INSIDE the status badge. Turning `show_product_status` off hides the whole badge, so the quantity has nowhere to show. The merchant must enable both for "Only 3 left" to appear.

### Static page link supports popup mode

When `show_page=on`, the merchant picks a static / dynamic page from [[marketing-landing-pages]]. `show_link_as_popup=on` renders that page as a side panel instead of navigating away — useful for "Delivery info" or "Returns policy" snippets.

### Variant handling

`pre_selected_variant=on` pre-selects the first variant on page load instead of requiring the shopper to pick; turn it off when each variant materially changes price / availability. `variant_in_name=on` appends the chosen variant to the H1 (e.g., "T-Shirt — Red, M"); off keeps the H1 as the product name. Useful for SEO when each variant is a meaningfully distinct product.

### Save rebuilds the storefront

Saving stores every toggle and rebuilds the storefront apps. Allow up to a few minutes for the product page to fully reflect the new settings. Save / reset also clear the per-site cache.

## Related

- [[design-modules-products]] — hub.
- [[products-products]] — product editor where field VALUES are entered.
- [[products-categories]] — category record that supplies characteristics.
- [[marketing-landing-pages]] — pages that `details_page_id` can link to.
- [[design-module-product-related]] — sibling row that appears below the product detail.
- [[design-module-product-in-bundles]] — sibling row showing bundles the product belongs to.
- [[design-module-product-linked]] — sibling row of merchant-pinned linked products.

## Open questions

- 📡 **Per-theme slot overrides.** Themes can re-order or re-style each visibility region; a per-theme audit could map slot positions if needed.
- 📡 **`choose_display_pages` behaviour.** Its visible effect is theme-specific. Verify which themes consume it.
