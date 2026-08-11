---
type: entity
nav_path: "Entity → Product Option"
aliases: ["Product Option", "Custom option", "Per-product option", "Customisation option", "Customization option", "Cart-add option", "Engraving option", "Gift-wrap option", "Опция на продукт", "Персонализация", "Допълнителна опция"]
tags: [catalog, products, options, customisation, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---

# Product Option

## Identity

A **Product Option** is a per-product customisation field that the customer fills in at the cart-add / product-detail stage and that **does NOT split the product into separate SKUs**. The merchant uses Options to capture customer input that personalises the same underlying stock unit — typical examples: *"Type the engraving text"* on a piece of jewellery, *"Choose a font"* for a printed mug, *"Pick a delivery date"* on a perishable, *"Upload your logo"* for a print-on-demand T-shirt, or a *"Gift wrap (+5 BGN)"* toggle. The submitted value is **stored on the order line**, so when the merchant fulfils the order they see exactly what each customer asked for — without ever multiplying the catalog with one SKU per possible customisation. Product Options live behind the **Product Options** app and are managed on [[products-options-overview]]; per-app configuration is on [[apps-product-options-settings-new]].

A Product Option is intentionally **distinct from a [[variant|Variant]]** and from a **[[category-property|Category Property]]** — see [[variants-model]] for the full three-way contrast. Briefly: a **Variant** (the *Parameter → Option → Variant* chain) splits the product into separate SKUs with their own stock, price, barcode, and weight — a "Red T-shirt size M" Variant has a different inventory count from a "Blue T-shirt size L" Variant, and the customer must pick a Variant before adding to cart. A **Category Property** is a category-scoped descriptive specification (e.g., *"Has Bluetooth: yes/no"* on Electronics) that doesn't split SKUs and isn't customer-input — the merchant fills it in once per product to drive the storefront filter sidebar. A **Product Option** is none of those: same SKU regardless of the customer's input, no per-Option stock, no per-Option filter — it is purely a customer-fill personalisation slot whose value lives on the order line.

The Product Options app installs into the store from the App Store under the `product_options` app identifier. When the app is NOT installed, the Options sidebar entry is hidden and the underlying tables are inert.

## Aliases

- **Product Option** / **Custom option** — the canonical merchant-facing terms in the admin sidebar ("Products → Options") and on [[products-options-overview]].
- **Per-product option** — emphasises the per-product scope (compared with the store-wide Parameters that drive Variants).
- **Customisation option** / **Customization option** — used in support docs and the App Store description.
- **Cart-add option** — informal phrasing reflecting where the customer fills the value (on the product page or in the cart, depending on theme).
- **Engraving option** / **Gift-wrap option** — informal merchant phrasing tied to the two most common use cases.
- **Опция на продукт** / **Персонализация** / **Допълнителна опция** — Bulgarian terms used across the Products → Options screens.

## Key Attributes

The Product Option is a multi-faceted entity split across **four well-scoped aspects**. The Assistant should drill into the aspect that matches the question, not read every page.

- [[product-option-entity-attributes]] — the full merchant-controlled field schema (Name, Input type, Required, possible values, Storefront name override, per-Option / per-value symbols, `customer_modify`, `system`) + the complete supported input-type list (`text`, `textarea`, `select`, `radio`, `checkbox`, `file`, `image`, `length`, `weight`, `square` — no `date`, no `multi-checkbox`).
- [[product-option-entity-pricing]] — the price-modifier model (`amount_type` flat / percent, `per_item` per-quantity flip, `apply_over_price_type` before / after discount, `allow_negative` credits, per-value modifiers, additive stacking on Checkbox, parent-product tax class, `min_square`, the forced `per_item = 1` on measurement types).
- [[product-option-entity-order-storage]] — how the customer-submitted value snapshots onto the `orders_products_options` order-line table, why renames are immutable on historical orders but re-render in live carts, and the File-upload value → [[file-asset]] reference.
- [[product-option-entity-scoping-and-edge-cases]] — the four attachment scopes (`product` / `category` / `vendor` / `selection`), the File-upload-delete cart cascade, file-upload caps inherited from [[settings-files]], and the Bundle Required-Option bypass.

## Where it appears

- [[products-options-overview]] — the master management screen where the merchant creates, edits, and deletes Option definitions (Sidebar → Products → Options).
- [[apps-product-options-settings-new]] — the app-level settings sub-page that configures app-wide behaviour for the Options system.
- [[product]] — each Product's editor has an Options section where the merchant attaches one or more Option definitions to that specific Product. The Option appears on the storefront product page in the configured input type.
- [[cart]] — the customer's selected / typed Option values are carried on the cart line as they shop.
- [[order]] — when the cart converts, the Option values snapshot onto the order line items so the merchant can see them when fulfilling. Editing the Option definition LATER does NOT retroactively update orders already placed — see [[product-option-entity-order-storage]].
- [[file-asset]] — File-upload Option values reference uploaded files stored in the file manager. The merchant downloads the customer's upload from the order details when fulfilling print-on-demand work.
- Storefront product detail page — the Options are rendered as a form (one section per Option) above or below the Add to cart button, depending on theme.

## Related

### Related entities

- [[product]] — Options are attached per-product; one Product can carry many Option definitions.
- [[variant]] — DISTINCT concept; Variants split SKUs (per-Variant stock, price, barcode), Product Options do NOT.
- [[category-property]] — DISTINCT concept; Properties are category-scoped descriptive metadata filled by the merchant once per product, not customer-input.
- [[file-asset]] — File-upload Option values reference uploaded assets stored in the file manager.
- [[cart]] — customer Option values live on the cart line during shopping.
- [[order]] — customer Option values snapshot onto the order line at checkout; the merchant reads them when fulfilling.
- [[discount]] — line-level discounts apply to the line total *including* any Option price modifiers (the merchant should account for surcharges when planning promotions).

### Cross-cutting concepts

- [[variants-model]] — the canonical three-way contrast page (Parameter / Option / Variant vs. Property vs. Product Option). Use this page when deciding which mechanism to use.
- [[checkout-flow]] — Required Options block the Add to cart button until filled; Option values flow into the cart and order via this pipeline.
- [[multi-language]] — Option names + possible values can be translated per-locale on multilang stores so the customer reads the input in their language.

### Settings & feature pages

- [[products-options-overview]] — primary admin screen for managing Option definitions.
- [[apps-product-options-settings-new]] — app-level configuration sub-page.
- [[products-products]] — per-product attachment (the product editor's Options section).
- [[apps]] — App Store; the Product Options integration is installed from here.

## Open Questions

No outstanding questions — all items resolved or distributed to sub-pages.
