---
type: feature
nav_path: "Design → Modules → Products"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Product modules", "Product showcase module", "Related products module", "Last viewed module", "Product details module", "Bundle products module", "Add-to-cart module", "Витрина с продукти", "Свързани продукти", "Последно видени продукти", "Детайли на продукта"]
tags: [design, modules, products]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---
# Storefront Modules — Products

## Purpose

The **Products** tab on the [[design-modules]] screen groups every module that DRIVES product discovery on the storefront — the product-detail field controls, the related / linked / last-viewed product rows, the homepage / category showcase rows, the brand showcase, the bundle blocks, and the static product-details text block. Tuning these modules is how the merchant decides which information appears on the product page, what kinds of recommendations the shopper sees, and how the homepage product strips are sourced.

The module catalogue on this tab is controlled by the **active theme** ([[design-themes]]) — switching themes can swap which product-module instances appear. The module TYPES are platform-wide; the named INSTANCES vary per theme.

This page is the navigation hub. Drill into the aspect page that matches the question rather than reading every aspect.

## Sub-pages (in this cluster)

- [[design-module-product-filters]] — `filters` instance / `product.filters`. The **Product Catalog Settings** card — master settings module for EVERY product-listing page (per-page, per-row, sort, filter chips, price ranges, out-of-stock, card visuals).
- [[design-module-product-listing]] — `productsListing` instance / `product.listing`. Legacy sibling of `filters` — sort + per-page + price range; older themes only.
- [[design-module-product-details-info]] — `productsDetails` instance / `product.productsDetails`. Master product-detail-page field visibility (price, BUY, status, SKU, brand, category, characteristics, gallery, compare, wishlist, quantity, description).
- [[design-module-product-showcase]] — `showcaseProducts*` instances / `product.productShowcase`. Homepage product rows (Featured / Bestsellers / Promotions / Smart-collection / hand-picked).
- [[design-module-product-related]] — `productsRelated*` instances / `product.related`. Related / Top / Match-with rows on product detail (category / vendor / tag matching).
- [[design-module-product-linked]] — `linkedProducts` instance / `product.linked`. Explicit merchant-pinned linked-products row.
- [[design-module-product-last-viewed]] — `lastViewed` instance / `product.lastViewed`. Cookie-driven recently-viewed-products row.
- [[design-module-product-in-bundles]] — `productInBundles` instance / `product.productInBundles`. "Product in packages" row on product detail.
- [[design-module-product-discounts]] — `discounts` instance / `product.discounts`. Same-category SALE products row on product detail (theme-specific).
- [[design-module-product-showcase-brand]] — `showcaseBrand` / `showcaseBrands1` / `showcaseBrands2` instances / `product.showcase` with `type=vendor`. Brand tile rows.
- [[design-module-product-showcase-categories]] — `showcaseCategories` instance / `product.showcase` with `type=category`. Category tile rows.
- [[design-module-product-bundle-showcase]] — `bundleShowcase` instance / `product.bundleShowcase`. Hand-picked bundle row (theme-specific).

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab.

Each card on the Products tab opens an edit panel with three buttons at the top: **Save module**, **Reset module** (confirmation: *"Are you sure you want to reset this module?"*), and **Cancel**. Saves regenerate the storefront cache automatically — the new settings are live on the next request. Success messages: *"Module successfully edited"* / *"Module successfully reset"*.

## What the merchant can do here

- Pick the module for the surface they want to tune — the Products tab covers EVERY product-discovery surface on the storefront.
- Open each module card to a side panel with its own form fields (see the aspect page).
- Save / Reset / Cancel — standard actions across every editable module.
- Enable / disable the master toggle on modules that support it.

## What the merchant cannot do here

- Cannot ADD a new product module instance — the catalogue is fixed by the active theme. Page-builder placement of module blocks lives in [[marketing-landing-pages]] (Dynamic pages).
- Cannot RENAME or DELETE a module instance — disable via the master toggle.
- Cannot configure modules that the theme has flagged `editable: no` — the card does not appear.
- Cannot configure plan-gated modules without the matching plan feature — see [[plan-gates]]. (None of the product modules in this category are currently plan-gated.)

## Settings & fields

Field tables live in the aspect pages. Pick the right aspect from the sub-pages list above.

## Business rules

### Cards are theme-defined

The cards visible on this tab are the theme's declared `modules` block filtered to the **Products** tab. Switching themes swaps the catalogue.

### Settings are stored per INSTANCE name

Each module instance has its own JSON blob keyed by instance name (e.g., `showcaseProducts1` vs `showcaseProducts2`). The same module TYPE can be instanced multiple times with independent settings.

### `productsDetails`, `filters`, `productInBundles` are SYSTEM modules

These three are auto-injected by the module helper even when the theme JSON does not declare them — the merchant always sees the cards and can always tune the product detail page, the catalog, and the bundles row. See [[design-module-product-details-info]], [[design-module-product-filters]], [[design-module-product-in-bundles]].

### Reset can re-seed a SHARED Configuration group

Five module groups share defaults across all their instances on Reset: `product.related`, `product.filters`, `product.listing`, `product.productsDetails`, `product.lastViewed`. Resetting one instance in such a group re-seeds the group defaults, so the change can look store-wide rather than per-instance — e.g. resetting any `productsRelated*` instance ALSO resets every other `product.related` instance. All other product modules reset per-instance only. See [[design-module-product-related]] for the surprise.

### Cache invalidation is automatic

Save and Reset bump the per-site cache key — storefront sees changes on the next request. No manual cache clear is needed.

### Disabled cards return 404

A module the theme flags `editable: no` does not appear on the tab, and opening its edit URL directly returns HTTP 404.

### Unknown fields are silently dropped

Save validates the submitted form against the module's declared field schema. Any field not in that schema is silently discarded rather than stored.

### Plan gating

None of the product modules are plan-gated at the module level (only `extra.videoSlider` in [[design-modules]] is). Page-builder blocks (`product-showcase`, `add-to-cart`, `bundle-products`) used on Dynamic pages require the `storefront_builder` plan feature on the Page Builder URL, not on the module itself.

### Localization

Module text fields (`title`, `header`, `text` on `productText`) are stored as a single string per instance by default. Per-language storage requires the multi-language app — see [[apps-multilang-settings]].

## Related

- [[design-modules]] — parent module editor (lists ALL modules and the full module-type catalogue).
- [[design-modules-engagement]] — sibling category page (contact form, contact info, Google map, newsletter, embedded forms, product reviews).
- [[design-modules-navigation]] — sibling category page (header / footer / menu / navigation links).
- [[design-modules-content]] — sibling category page (text, banner, carousel, slider).
- [[design-modules-utility]] — sibling category page (filters, social, footer text, system modules).
- [[design-themes]] — theme picker that controls which product-module instances appear on this screen.
- [[design]] — parent Design pillar.
- [[marketing-landing-pages]] — Dynamic pages use the page-builder, which exposes the same product-showcase, add-to-cart, and bundle-products blocks.
- [[products-smart-collections]] — Smart Collections power the `filter=selection` source for product-showcase rows.
- [[products-categories]] — category records supply tile images for the category showcase.
- [[products-vendors]] — vendor records supply tile logos for the brand showcase.
- [[apps-bundles-overview-new]] — bundles must exist before they can be surfaced via the bundle modules.

## Open questions

- 📡 **Per-language text fields.** With `multylang`, showcase `title` / `header` and `productText` accept per-language entries via the language switcher.
- 📡 **Bundle module app key.** `product.bundleShowcase` and `product.productInBundles` require the Bundles app installed; without it, the picker is empty and the row stays hidden.
