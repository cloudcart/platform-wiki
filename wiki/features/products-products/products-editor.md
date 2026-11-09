---
type: feature
nav_path: "Products → Products → Editor"
route_name: products-edit
route_path: /admin/products/edit/:id
aliases: ["Product editor", "Edit product", "Product edit form", "Edit page", "Product details page", "Product Statuses card", "Show also in", "Applied discounts", "Publish later", "Extend functionality by", "Add new tab", "Редактор на продукт", "Редактиране на продукт"]
tags: [catalog, products, editor, form, details]
plan_gates: ["products"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[products-products]]. See the hub for the other aspects (list view, variants, bulk actions, etc.).

# Products — Editor

## Purpose

The single-product **Edit view** is a two-column form — the structural data the merchant writes in the main area, plus the metadata controlling where and when it surfaces in the aside. Route `products-edit`, at `/admin/products/edit/:id`. The page title is the product's name with its first image beside it, and a **Draft** badge while it is a draft.

## Where to find it

- From [[products-list-view]] — click a product's name.
- From the create-product popup — after Create, auto-navigated here with `?new=true`.
- From other admin screens that link to a product.

## What the merchant can do here

### Main area sections

- **Details** — **Product title** and a rich-text editor with a row of tabs: **Description** (can be renamed), **Files** (files shown on the product page), and extra tabs from **Add new tab**, which can be renamed, removed and dragged into order. Tabs belong to one product: no bulk action, CSV or Google Sheets column fills them; **Duplicate** copies them, and the Admin GraphQL API adds one tab per call. **Add short description** reveals the **Short description** editor. The AI bar sits under the editors — see [[products-ai-content]].
- **Media** — image gallery: drag to reorder, first image is the thumbnail. **Add image**, **Add video** (one YouTube link per product: [[products-editor-video]]) and **Add 360° image** (up to 36 images; one per product). Selecting images enables **Tools**: **Set as primary** (one image) and **Delete**. Dropping more than 36 images keeps the first 36, with *"You can upload up to 36 images only!"*
- **Product setup** (digital products) — the download files or the pages, with pricing and inventory. See [[products-digital]].
- **Product type settings** (other products) — the **Simple Product** / **Product with variants** toggle, **Pricing**, the variants and the **Inventory** card. See [[products-variants-matrix]] and [[products-variants-options]].
- **Categories** — the main category, picked from a flat, searchable list (no tree view) where each entry shows its full path, `Parent > Child`, in creation order (verify); typing matches any part of the path, so a parent's name also lists its subcategories. With **Create new category** and *Edit "<name>" category*, both opening a category window (a category's Metafields card is on the window from [[products-categories]]). **Show also in**: up to 5 additional categories, one picker each, where the product appears on the storefront; discounts, widgets and automated selections go by the main category only. Below, the category properties from [[products-property]], with **Manage category properties** and **Create new property**.
- **Metafields** — right below Categories: the pinned definitions in order, then *Show all*, saved with the page's save bar. See [[metafields-definitions]].
- **Brand and model** (Brand-Model app) — models related to the product, with **Add new brand** and **Add new model**.
- **Suppliers** (Suppliers app) — *"Link suppliers to this product and compare the supplier price to the one in your store."*, with **Add supplier to this product**.
- **Imos3d** (Imos3d app) — **Catalogue**, **Product**, **indFile**.
- **SEO Configuration** — collapsible Google preview with title, description, URL handle (default `/product/<slug>`), and the AI bar.
- **Linked products** — manual cross-sell list of published products (see Business rules).
- **Extend functionality by:** — apps not yet installed (see Business rules).

### Aside (right column)

- **Active and publish dates** (visible when set) — **Publish date** / **Active until** (set via the Publish later window).
- **Product Statuses** — **Published** switch (while on, **Postponed publishing** with a **Publish later** button), **Mark as new**, **Mark as featured**, **Hide from store**. When the plan's `hidden_products` limit is reached, **Hide from store** opens the plan-upgrade window and the switch goes back off.
- **Vendors** — pick a manufacturer; typing a new name offers to create it, as does **Add new vendor**.
- **Tags** — tag autocomplete; new tags are accepted, and a comma-separated paste adds several.
- **Smart Collections** — [[products-smart-collections]]: search to add the product to a collection, or **Create new collection**. Collections it joined by their rules carry a **By criteria** badge linking to the collections screen; the ones added by hand can be removed here.
- **Sort number** — counts only under **Ръчно сортиране**, in the saved direction ([[design-module-product-filters-sorting]]).
- **Applied discounts** (visible when any apply) — read-only — see Business rules.

### Header action menu

- **Duplicate** button — duplicates the product, shows *"Product duplicated successfully"* and opens the copy in a new tab. See [[products-known-issues]].
- **Preview** button (only when Published + not Draft) — opens the storefront `/product/<url_handle>` URL.
- Options dropdown (kebab): **Duplicate** (mobile only), **Embed on a website** (`/admin/buy-button/builder/<id>`, only when Published + not Draft), **Change log** (see [[products-change-log-link]]), **Create checkout link**.

### Checkout link modal

**Create checkout link** opens the **Create a checkout link** side window, listing every variant with its own `<host>/checkout-link/<variant_id>` deep link (clicking copies it); a product without variants shows one link. A variant not saved yet shows *"To generate a checkout link, you need to save your product first"*.

### Postponed publishing window — "Save and publish later"

While **Published** is on, the **Publish later** button opens a popup with two toggle + date-picker rows: **Publish on specific date** (saved as Draft, published automatically then) and **Active till** (auto-unpublishes then). Its **Save** saves the whole product straight away, and the dates then show on the **Active and publish dates** card. A date the server refuses reopens the popup with the error on the field.

### What the merchant CANNOT do here

Edit several products at once (use [[products-bulk-actions]]); drag-reorder a category page (**Sort number** drives it); or create a discount (**Applied discounts** is read-only).

## Settings & fields

### Save and publish behaviour

The bottom bar (*"You have unsaved changes"*) carries **Save and publish**, which commits in one action — no separate "Save as draft" — and **Discard changes**. Leaving unsaved asks *"Do you want to save your changes first?"* with **Stay on page**, **Leave without saving** and **Save changes**.

The product's state follows the **Published** switch: with it on, the save publishes the product and clears Draft; with it off, the save leaves the product unpublished, and a draft stays a draft. A product opened from the create popup starts with the switch on, so turn it off before the first save to keep it unpublished.

### Validation on save — what's enforced

- **Mandatory:** every save needs a main category, otherwise *"You have not selected a main category for the product. Please select a main category for the product"* and the page scrolls to the Categories card; products with variants need at least one parameter and one combination, with duplicate (`v1`, `v2`, `v3`) combinations rejected; shipping-required physical products need a positive weight (max 10,000,000 units).
- **Stock-tracking guards:** *"Continue selling when sold out"* and the low-stock threshold can be set only with stock tracking on; the threshold must be a positive integer.
- **Length / pricing limits:** `sku`, `barcode`, and variant parameter name max 191 chars each (parameter name min 1 char); per-variant price is a currency amount up to 10 decimal places, and an empty price falls back to the base price.
- **Digital products:** cannot have variants — blocked at save with a *"digital file cannot have multiple variants"* error; **Downloadable files** ones need at least one file on every save, otherwise *"The type digital field is required for digital products"*.

### URL handle generation rules

With no URL handle supplied, it is slugified from the product name, trimmed to 180 characters, and suffixed `-1`, `-2`, ... on duplicates (a 6-digit random number for very large catalogs). The **old URL handle is automatically saved to the redirect history** — editing a slug on a published product 301-redirects the old slug for **30 days**, with no row on [[marketing-seo-301-redirects]].

### Product image upload

An uploaded image appears immediately in the admin; the first becomes the primary thumbnail. Renditions are generated on demand at `/image/product/{product_id}/{size}` when the storefront first requests each size (not at upload), then CDN-cached; the dimensions cap is platform-managed.

- **Maximum upload size**: 1024 MB per file (`files_max_size = 1024 MB`).
- **Allowed image formats**: `gif`, `png`, `jpg`, `jpe`, `jpeg`, `svg`, `webp`. Another file shows *"Only images are allowed"*.
- **Storage full**: the Media card shows *"Storage space at 100%, you cannot upload any more files"* with **Upgrade storage space**.

**Bulk-upload from URL** — images added by URL (ERP imports, migrations) download in the background, so they appear a little after the save.

### Storefront URL pattern

The storefront URL is `/product/{slug}/{cart_key?}`. The `/product/` prefix is **fixed** — no URL-prefix setting, so the merchant CANNOT change it to `/p/`. The plural address `/products/{id}` (numeric ID) 301-redirects to `/product/{slug}`, even for inactive products.

## Business rules

### Applied discounts card is read-only

The **Applied discounts** card lists the discounts applying now, each with a link, an **Amount** or **Percent** badge, its dates and *Visible to*. Discounts are created in the Discounts feature.

### Linked products are NOT auto-derived

The Linked products list is picked by hand from published products; nothing is suggested. Each row has a **Two way connection** switch (on when added), a drag handle for the order, and a remove action (*"Remove linked product?"*).

### "Extend functionality by:" — apps that add cards

This card lists the apps from this set that the store doesn't have yet: Product Reviews, Suppliers, Brand-Model, Imos3d, Grocery store and Membership. **Install app** installs one, after checkout if it is paid, and the page scrolls to the card it adds. Installed apps add their cards to the page, marked **Extended**. See [[apps]].

### Default-variant auto-assignment and Price From / Price To

For a multi-variant product every save makes the **cheapest variant** the *"default"*; there is no picker. When all variants share one price and at least two have different sale prices, the one with the lowest sale price wins instead. **Price From** (cheapest) and **Price To** (most expensive) are recalculated with it.

## Related

- [[products-products]] — hub.
- [[products-variants-matrix]] — **Product type settings**, the per-SKU window and the Inventory card (with the **Not for parcel lockers** switch, [[shipping-provider-mech-locker-fit]]).
- [[products-ai-content]] — the AI bar and its side panel.
- [[products-change-log-link]] — Change log modal.
- [[products-categories]] — Categories + category-property mapping.
- [[products-property]] — category-bound properties.
- [[products-smart-collections]] / [[products-vendors]] — assigned / picked in the aside.
- [[products-variants-options]] — variant parameter / option screen.
- [[products-digital]] — the **Product setup** card.
- [[metafields-definitions]] — the **Metafields** card.
- [[products-statuses]] — Inventory card.
- [[settings-cart]] — `order_status_for_quantity_decrease`, `product_threshold` (drive the stock-tracking guards).
- [[apps]] — install / re-install for the apps on **Extend functionality by:**.

## Open questions

None.
