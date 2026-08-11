---
type: feature
nav_path: "Apps → Bundles → Settings (modern)"
route_name: apps.bundles.settings.new
route_path: /admin/products/bundles-new
aliases: ["Bundles Settings (modern)", "Bundles config new"]
tags: [apps, administration, bundles, settings, modern-vue]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 4
---
# Bundles → Settings (modern Vue)

## Purpose

The modern Vue version of Bundles Settings — store-wide bundle defaults plus the bundle create/edit editor, built on CloudCart's current design system (CcSettingsBox / CcCard) with better mobile UX and live validation feedback.

For the full Bundles feature set, see [[bundles-list]] and [[apps-bundles-overview-new]].

## Where to find it

Sidebar → Apps → Bundles → **Settings tab**. Route: `/admin/products/bundles-new` (the same path as the Overview hub — `apps.bundles.settings.new` is registered at the Bundles parent route, with `bundles-list.new`, `bundles-add.new`, and `bundles-edit.new/:id` as children).

## What the merchant can do here

- Configure store-wide bundle display defaults (show savings on bundle pages, show constituent prices, stock model Strict / Partial, customer-facing label localisation).
- Create and edit individual bundles via the bundle editor (see Settings & fields).
- Set per-constituent-product visibility and pricing overrides.

### What the merchant CANNOT do here
- Browse the existing bundle catalogue — that's [[bundles-list]] or [[apps-bundles-overview-new]].

## Settings & fields

### Bundle editor — five collapsible sections

The create/edit page renders these five sections, in order:

| Section | Heading | Fields |
|---|---|---|
| Bundle details | **Bundle details** | Name (required, max 191 chars); Short description; Logo (image upload — jpg/jpeg/jpe/gif/png/svg/webp, max 10 MB); Display photo in detailed page (`meta.show_image` switch); Mark as new (`new`); Mark as featured (`featured`); Hide from store (`hidden`). |
| Show in category | **Show in category** | Category (single select, clearable — a bundle can stay uncategorised). |
| Select products | **Select products** | Pricing type radio (Price vs Percent); the constituent-products list with per-product flags (below); Products per row (1–6 dropdown, default 3). |
| Date range | **Date range** | Publish date (`publish_date`); Active to (`active_to`); Active till switch (`activeTill`); Show timer in products listing (`meta.timer_list`); Show timer in product details page (`meta.timer_details`). Both timer switches are disabled while Active to is empty. |
| Advanced SEO settings | **Advanced SEO settings** | SEO title (`seo_title` — defaults to the bundle name if left empty); SEO description (`seo_description`, no auto-fallback); URL handle (`url_handle`). |

### Pricing type (per bundle)

- **Price** — a fixed bundle price (the `price` value).
- **Percent** — a percentage discount (the `percent` value) applied to whatever the constituents resolve to at checkout.

The merchant never types the bundle's *displayed* price range — it is derived by summing the constituents' `price_from` and `price_to` (respecting any per-product quantity override). A bundle shows a single price if no constituent has variants, otherwise a price range.

### Per-product flags (per constituent product)

Each product added to a bundle has its own toggles, giving fine-grained control over what shoppers see for that item across the product page, cart, and order receipt:

- `optional` — shopper can opt this item in or out.
- `individual_price_enabled` — override this item's price (then a price is required).
- `individual_qty_enabled` — override this item's quantity (then a quantity ≥ 1 is required).
- `visible_product_details` / `visible_cart` / `visible_order_details` — show this item on the product detail page / in the cart / in order details.
- `price_visible_product_details` / `price_visible_cart` / `price_visible_order_details` — show this item's price in each of those places.
- `hide_thumb` — hide this item's thumbnail.
- `override_title` — replace the product title in the bundle context (then a title is required).
- `override_short_description` — replace the short description in the bundle context (then a short description is required).

## Business rules

### Fixed price is blocked for bundles with variant products

If the merchant picks the **Price** (fixed) pricing type and adds a constituent that has price variants (its price varies per variant), the save is rejected with:
*"Fixed price is not allowed when the bundle contains products with variants"*

This is a hard stop. To include variant-priced products, the merchant must use the **Percent** pricing type, which applies the discount to whatever price each variant resolves to.

### Minimum to save: name + one product

Before saving, the editor only enforces two things:
- Name must be non-empty — otherwise the inline error reads *"Field is required"*.
- At least one product must be added — otherwise the error reads *"You have to choose products to be added into the bundle"*.

Everything else (category, SEO, date window, description) is optional. Note: although the rule is "at least one product", some server messages still say "at least two" — a wording holdover, not an extra requirement.

### Timer switches auto-clear when the Active to date is removed

If the merchant clears the **Active to** date, both timer switches (`meta.timer_list` and `meta.timer_details`) are forced off and disabled — preventing a countdown timer with no end date.

### Drag order sets the storefront display order

Reordering the constituent-products list by drag-and-drop sets each item's `sort_order` from its position, so the storefront shows products in the same order the merchant arranged them. No separate save step is needed for the order.

### Deleting a bundle clears it from shoppers' carts

When a bundle is deleted, any copies of it sitting in shoppers' carts are removed too — a shopper won't see a phantom bundle in their cart after the merchant deletes it.

### Permission
Standard apps permission scope.

## Related

- [[bundles-list]] — the bundle catalogue list.
- [[apps-bundles-overview-new]] — the Bundles overview hub (modern).

## Open questions

_None — all questions answered above._
