---
type: feature
nav_path: "Products → Products → List view"
route_name: products-index
route_path: /admin/products
aliases: ["Products list", "Product list view", "Product table", "Product filters", "Search and Filter", "Product list columns", "Списък с продукти"]
tags: [catalog, products, list, filters, table]
plan_gates: ["products"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[products-products]]. See the hub for the other aspects (editor, variants matrix, bulk actions, etc.).

# Products — List view

## Purpose

The default mode of [[products-products]] is the **List view** — a paginated, filterable, multi-select table of every product, and where merchants spend most of their catalog time: finding a product, filtering to a slice (e.g. *"every Draft without a vendor"*), running a bulk action, and entering the editor.

## Where to find it

Sidebar → Products → **Products**. URL `/admin/products` (the default route renders the List). Clicking a product's name opens `/admin/products/edit/:id` — see [[products-editor]].

## What the merchant can do here

### Header

The header shows the **counts** (*"Products: `<count>` / `<plan-allowed-max>`"*, *"Variants: `<count>`"*; tooltip *"Number of products you can create"*) with a green progress bar when the plan has a hard limit. **Add product** and **Import** (cloud-upload icon) open their popups (see "Settings & fields").

### Search and filters

Above the table, the **Search and Filter** box takes a keyword (Enter) and opens a **Filters** list: pick a filter, set it, **Apply filter**. Applied filters show as tags in the box, and **All results** clears them. A combination can be kept with **Save filter**; it then sits under **Saved filters** and can be pinned as a tab.

**Yes / No flags:** **New**, **Draft** (unpublished work-in-progress), **Published** (visible to customers), **Featured**, **Hidden** (hidden from storefront, still in admin), **Tracking** (stock tracking enabled), **Digital** (vs physical), **Imported** (came in via an importer), **Has image**, **Has variants**.

**Other filters:**

| Filter | Options |
|--------|---------|
| **Quantity** / **Price** | Numeric / currency: Exactly / Not equal to / More than / Less than |
| **SKU** / **Barcode** | Free-text contains |
| **Tagged with** | Tag search, one tag |
| **Manufacturer** | Multi-select, Includes / Does not include — searches [[products-vendors]] |
| **Variant** | Single-select of a variant parameter (e.g. "Color") |
| **Variant with parameter** | Pair: parameter + option (e.g. "Color" + "Red") — finds a specific variant value |
| **Category** | Multi-select, Includes / Does not include — searches [[products-categories]] |
| **Product** | Single-product search (Includes / Does not include) |
| **Brand** + **Brand model** | Brand-Model app — pair search for brand + model |
| **Suppliers** | Suppliers app — single-select from supplier list |
| **Category property** + **Category property option** | For category-bound properties ([[products-property]]) — property + option |
| **Imported with** | Multi-select of import sources (CSV / apps), Includes / Does not include |

Filters combine; the table reloads when one is applied.

### List columns

| Column | What it shows |
|--------|---------------|
| **Product** | Thumbnail, name (opens the editor), *By `<vendor>`* (click to filter the list by that vendor), star rating with review count linking to the reviews (Product Reviews app), and a badge with the import source for imported products. The thumbnail of a published product opens its storefront page in a new tab (tooltip *"View in store"*). |
| **Variants** | A button with the number of combinations; it opens a read-only list of the parameters and their values. |
| **Qty** | With tracking on, the quantity across variants, with the unit when all variants share one. With tracking off, an infinity sign. |
| **Sort** | The product's sort number. |
| **Added** / **Updated at** | Dates. |
| **Actions** | Inline per-row quick actions (see below). |

The list opens newest first, 25 rows per page; **Product**, **Qty**, **Sort**, **Added** and **Updated at** sort on click. **Modify columns** adds or removes columns (**Product** and **Actions** always stay). Selecting rows via the checkboxes enables the **Tools** button with the bulk actions — see [[products-bulk-actions]].

### Per-row inline actions

The actions cell gives quick toggles without entering Edit mode, as icons with tooltips. On screens from 769 to 1350 px wide they fold into a **⋯** menu.

- **Hide product / Show product** (eye) — flips Hidden.
- **Mark as featured / Unmark as featured** (thumbs-up) and **Mark as new / Unmark as new** (flame).
- **Publish / Unpublish** (arrow) — flips Published. On a draft the icon is a pen, labelled **Draft**.
- **Change log** — opens the modal on [[products-change-log]]; the icon is purple when there's an entry, greyed and not clickable when empty. See [[products-change-log-link]].
- **Delete** (trash) — small confirmation *"Delete row?"*. Permanent (no soft-delete or trash); see [[products-known-issues]] for the cascade.

## Settings & fields

### Create product popup — multi-screen type picker

The **Add product** button opens a popup that walks through three screens. The address `/admin/products#add-product` opens it directly.

1. **Select your Product Type** — **Physical product** (always) and **Digital product** (when the plan supports it). Digital expands to **Downloadable files** (digital file delivery) and **Landing pages** (membership / private content; requires the Subscriptions app — if missing, the popup detours to a Required App install screen).
2. **Fill name + category** — **Name** + **Category** single-select with autocomplete against [[products-categories]]. With *"Want to add a new category? Type the category name to create it."*, typing a new name offers *Create "<name>" category*, which opens the category window with the name filled in. **Create** stays disabled until both fields are filled.
3. **Create** — creates the product and opens its Edit page (`/admin/products/edit/:id?new=true`). A back-arrow returns to the type-picker.

### Import products popup — 4 entry options

The **Import** button shows an **Import products** popup with 4 option cards:

| Option | Action |
|--------|--------|
| **Import with CSV file** | Opens the 3-step CSV wizard (below). |
| **XML Import app** | Routes to [[apps-xml-import]]. |
| **XML Sync app** | Routes to [[apps-xml-sync]]. |
| **API import** | Opens the CloudCart developer center API tools page in a new tab. |

### CSV import wizard — 3-step modal flow

The CSV option opens the **Import with CSV file** side window: three steps and a success screen. It feeds the same import pipeline as the CSV Import app ([[apps-csv-import]]).

| # | Step | What the merchant does |
|---|---|---|
| **1** | **Upload file** | Drag-and-drop or select a CSV; another file type shows *"Invalid file type, please upload a valid csv file."* A **"CSV Template"** button downloads a sample CSV to fill in offline. **Next** without a file shows a "Please upload a CSV file" error. |
| **2** | **CSV file settings** (**General settings** + **Advanced settings** cards) | **General settings:** header-line toggle (`has_header_line`); *"The sign that splits the names of the categories"* (e.g. `>` makes `Apparel > Shirts` nested); *"Task ID number"* (`import_key`) — optional; it chains nothing, since a later upload never matches an earlier task's products (re-uploading duplicates); fixed-discount picker with a **Generate discount code** link. **Advanced settings:** *Publish imported products* (`publish_as_active`), *Publish products as featured* (`publish_as_featured`), *Publish products as new* (`publish_as_new`), *All imported products require shipping* (`require_shipping`), *The quantity of each imported product must be tracked* (`quantity_tracking`), *Continue selling* (`continue_sell`). |
| **3** | **Mapping** | For each product / variant field, pick the matching CSV column. Required: `product.name`, `product.id`, `variant.parent_id`. The button reads **Submit** — clicking it queues the import. If an earlier import is blocking this one, a recovery button appears beside **Back**; it clears the block and submits again. |
| _(success)_ | **Import task created** | Success screen: *"The file was successfully uploaded and the products import task was added to the queue. If you wish, you could track the uploading in the queued jobs."* with a **Track importing progress** button → CSV Import task list (`apps.csv_import.settings`) in a new tab. |

A Back button is on steps 2 and 3; refreshing mid-wizard resets to step 1.

### "Imported" and "Imported with" — origin tracking

Products created via imports (CSV, XML, JSON, ERP) carry an Imported flag plus an import-source identifier, shown as a badge in the **Product** column. The **Imported with** filter finds all products from a specific import (e.g. from Szamlazz) — useful for reversing a bad import.

## Business rules

### Moderator restrictions

A moderator with restricted access (per [[settings-staff]] → Access permissions / Restrictions) may only edit products in certain categories. The list view filters their visible products automatically; they cannot reach hidden categories' products via the search bar either.

### Plan-cap on create

When the plan's `products` quota is exhausted, **Add product** and **Import** open the plan-upgrade window with *"You have reached the maximum number of products you can create ({used} out of {current}). You must upgrade your plan to continue."* See "Plan gate" on [[products-products]].

## Related

- [[products-products]] — hub.
- [[products-categories]] — Category filter + create-product category picker.
- [[products-vendors]] — Vendor filter.
- [[products-property]] — Category-property filter pair.
- [[apps-csv-import]] — backend for the CSV wizard launched here.
- [[apps-xml-import]] / [[apps-xml-sync]] — the other two Import-popup destinations.
- [[settings-staff]] — moderator restrictions that filter the visible list.

## Open questions

None.
