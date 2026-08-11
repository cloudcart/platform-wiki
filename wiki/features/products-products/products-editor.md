---
type: feature
nav_path: "Products → Products → Editor"
route_name: products-edit.new
route_path: /admin/products/products-new/edit/:id
aliases: ["Product editor", "Edit product", "Product edit form", "Edit page", "Product details page", "Редактор на продукт", "Редактиране на продукт"]
tags: [catalog, products, editor, form, details]
plan_gates: ["products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-products]]. See the hub for the other aspects (list view, variants, bulk actions, etc.).

# Products — Editor

## Purpose

The single-product **Edit view** is a two-column form for every aspect of one product — the structural data the merchant writes (name, descriptions, prices, images, variants, categories, SEO) in the main area, plus the metadata controlling where and when it surfaces (publish state, vendor, tags, smart collections, sorting, discounts) in the aside. Route `products-edit.new`, at `/admin/products/products-new/edit/:id`. Breadcrumb: "Products → `<product name>`".

## Where to find it

- From [[products-list-view]] — click any row.
- From the create-product popup — after Create, auto-navigated here with `?new=true`.
- From cross-cutting admin links (search results, change-log drill-down).

## What the merchant can do here

### Main area sections

- **Details** — name, short description, full description (rich-text editor), price, SKU, barcode, weight, dimensions; plus the AI description trigger (Cloudio bar) — see [[products-ai-content]].
- **Media** — drag-and-drop image gallery; first image is the thumbnail.
- **Variants** — variant parameters (Color, Size, etc.) and the resulting matrix; each variant has its own SKU, barcode, price, quantity. See [[products-variants-matrix]] and [[products-variants-options]].
- **Categories** — primary + additional categories (multi-select from [[products-categories]]); properties from [[products-property]] for the chosen categories appear here.
- **Brand and Model** (Brand-Model app) — brand + model.
- **Suppliers** (Suppliers app) — supplier info, cost prices, SKU.
- **SEO configuration** — title, description, URL handle (default `/product/<slug>`).
- **Linked products** — manual cross-sell list (see Business rules).
- **Required Apps** — apps the product depends on (see Business rules).

### Aside (right column)

- **Dates** (visible when set) — scheduled activation / expiry (set via the Publish later modal).
- **Publish** — Active / Draft / Hidden toggle + "Save and publish" button.
- **Vendor** — manufacturer.
- **Tags** — tag autocomplete.
- **Smart Collections** — [[products-smart-collections]].
- **Sorting** — manual sort-order override for category pages.
- **Discounts** — discounts currently applying (read-only — see Business rules).

### Header action menu

- **Duplicate** ghost button — duplicates the product, opens the copy in a new tab. See [[products-known-issues]].
- **Preview** ghost button (only when Active + not Draft) — opens the storefront `/product/<url_handle>` URL.
- Options dropdown (kebab): **Duplicate** (mobile only), **Embed on a website** (`/admin/buy-button/builder/<id>`, only when Active + not Draft), **Change log** (see [[products-change-log-link]]), **Create checkout link**.

### Checkout link modal

**Create checkout link** opens a modal listing every variant with its own `<host>/checkout-link/<variant_id>` deep link (clicking copies it); products without variants get one product-level link.

### Postponed publishing modal — "Save and publish later"

When Active is ON, a **Publish later** button opens a popup with two toggle + date-picker rows: **Publish on specific date** (saved as Draft, published automatically then) and **Active till** (auto-unpublishes then). Save commits the dates (shown afterward on the aside Dates card); the main Save is still required.

### What the merchant CANNOT do here

Edit multiple products side-by-side (use [[products-list-view]] + [[products-bulk-actions]]); import categories / vendors / tags (separate import flows); drag-reorder the storefront category-page list (the per-product **Sort number** field and Smart Collections settings drive ordering); or create/assign a discount (Discounts aside is read-only).

## Settings & fields

### Save and publish behaviour

The bottom **Save and publish** button commits in one action — no separate "Save as draft"; a "Discard changes" prompt appears when navigating away unsaved. A Draft product → saves AND publishes (Active, Draft cleared); an Active product → saves only. Toggle Active OFF before saving to keep a draft unpublished.

### Validation on save — what's enforced

- **Mandatory:** category required unless saved as Draft; products with variants need at least one parameter and one combination, with duplicate (`v1`, `v2`, `v3`) combinations rejected; shipping-required physical products need a positive weight (max 10,000,000 units).
- **Stock-tracking guards:** *"Continue selling when sold out"* and the low-stock threshold can be set only with stock tracking on; the threshold must be a positive integer.
- **Length / pricing limits:** `sku`, `barcode`, and variant parameter name max 191 chars each (parameter name min 1 char); per-variant price is a currency amount up to 10 decimal places, and an empty price falls back to the base price.
- **Digital products:** cannot have variants — blocked at save with a *"digital file cannot have multiple variants"* error; file-type ones need at least one uploaded file before publishing (not for draft).

### URL handle generation rules

With no URL handle supplied, it is slugified from the product name, trimmed to 180 characters, and suffixed `-1`, `-2`, ... on duplicates (a 6-digit random number for very large catalogs). The **old URL handle is automatically saved to the redirect history** — editing a slug on a published (non-draft) product 301-redirects the old slug to the new one, so a URL change doesn't break inbound search or external links.

### Product image upload

An uploaded image appears immediately in the admin; the first becomes the primary thumbnail. Renditions are generated on demand at `/image/product/{product_id}/{size}` when the storefront first requests each size (not at upload), then CDN-cached; the dimensions cap is platform-managed.

- **Maximum upload size**: 1024 MB per file (`files_max_size = 1024 MB`).
- **Allowed image formats**: `bmp`, `gif`, `png`, `jpg`, `jpe`, `jpeg`, `tif`, `tiff`, `svg`, `webp`.

**Bulk-upload from URL** — images added via *"Upload from URL"* (ERP imports, bulk migrations) download in the background; the save returns immediately, the image appears seconds later. For 50+ images, storefront display can take 5–10 minutes.

### Storefront URL pattern

The storefront URL is `/product/{slug}/{cart_key?}`. The `/product/` prefix is **fixed** — no URL-prefix setting, so the merchant CANNOT change it to `/p/`. The legacy `/products/{id}` (plural, numeric ID) 301-redirects to `/product/{slug}`, even for inactive products.

## Business rules

### Discounts panel is read-only

The Discounts aside LISTS the discounts currently applying; it does NOT create or assign them. To add one targeting this product, the merchant uses the separate Discounts feature.

### Linked products are NOT auto-derived

The Linked products cross-sell list is 100 % merchant-curated — no smart suggestion; the merchant picks each one manually (or uses a smart collection).

### Required Apps — explicit dependency surface

Some product types depend on apps being installed (a digital-download product needs the Digital Files app; a subscription product needs the Subscriptions app). If a required app is missing or uninstalled, the merchant sees a warning + a CTA to install it from [[apps]].

### Default-variant auto-assignment and Price From / Price To

For a multi-variant product the platform auto-picks the **cheapest variant** as the *"default"* (not picked manually) — its price is the storefront card's headline. After every variant save the default, **Price From** (cheapest), and **Price To** (most expensive) are recalculated, so a new cheapest variant updates the headline. Cards show Price From – Price To.

## Related

- [[products-products]] — hub.
- [[products-variants-matrix]] — per-SKU manage modal.
- [[products-ai-content]] — Cloudio bar description panel.
- [[products-change-log-link]] — Change log modal.
- [[products-categories]] — Categories + category-property mapping.
- [[products-property]] — category-bound properties.
- [[products-smart-collections]] / [[products-vendors]] — assigned / picked in the aside.
- [[products-variants-options]] — variant parameter / option screen.
- [[products-statuses]] — Inventory card.
- [[settings-cart]] — `order_status_for_quantity_decrease`, `product_threshold` (drive the stock-tracking guards).
- [[apps]] — install / re-install for Required Apps.

## Open questions

None.
