---
type: feature
nav_path: "Products → Products → List view"
route_name: products-index.new
route_path: /admin/products/products-new
aliases: ["Products list", "Product list view", "Product table", "Product filter sidebar", "Product list columns", "Списък с продукти"]
tags: [catalog, products, list, filters, table]
plan_gates: ["products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-products]]. See the hub for the other aspects (editor, variants matrix, bulk actions, etc.).

# Products — List view

## Purpose

The default mode of [[products-products]] is the **List view** — a paginated, filterable, multi-select table of every product, and where merchants spend most of their catalog time: finding a product, filtering to a slice (e.g. *"every Draft without a vendor"*), running a bulk action, and entering the editor.

## Where to find it

Sidebar → Products → **Products**. URL `/admin/products/products-new` (the default route renders the List). Clicking any row navigates to `/admin/products/products-new/edit/:id` — see [[products-editor]].

## What the merchant can do here

### Header

The header shows a **product count chip** (*"Products: `<count>` / `<plan-allowed-max>`"* + a Variants count) with a green progress bar when the plan has a hard limit. **+ Add product** and **Import** (cloud-upload icon) open their popups (see "Settings & fields"); a **Draft** badge marks the currently-being-edited product if it's still a draft.

### Filter sidebar — extensive

Every column the merchant cares about is filterable:

**Yes / No flags:** **New** (the "🔥 NEW" badge), **Draft** (unpublished work-in-progress), **Published** (visible to customers), **Featured**, **Hidden** (hidden from storefront, still in admin), **Tracking** (stock tracking enabled), **Digital** (vs physical), **Imported** (came in via an importer), **Has image**, **Has variants**.

**Other filters:**

| Filter | Options |
|--------|---------|
| **Quantity** / **Price** | Numeric / currency: Exactly / Not equal to / More than / Less than |
| **SKU** / **Barcode** | Free-text contains |
| **Tagged with** | Multi-select tag search |
| **Manufacturer / Vendor** | Multi-select, Includes / Does not include — searches [[products-vendors]] |
| **Variant** | Single-select of a variant parameter (e.g. "Color") |
| **Variant with parameter** | Pair: parameter + option (e.g. "Color" + "Red") — finds a specific variant value |
| **Category** | Multi-select, Includes / Does not include — searches [[products-categories]] |
| **Product** | Single-product search (Includes / Does not include) |
| **Brand** + **Brand model** | Brand-Model app — pair search for brand + model |
| **Suppliers** | Suppliers app — single-select from supplier list |
| **Category property** + **Category property option** | For category-bound properties ([[products-property]]) — property + option |
| **Imported with** | Multi-select of import sources (CSV / apps), Includes / Does not include |

Filters combine; the table re-fetches on change.

### List columns

| Column | What it shows |
|--------|---------------|
| **Name** | Product name + thumbnail (when an image exists) + status badges (Draft, Hidden, New). Click to open Edit. |
| **Variants** | Per-variant info — quantity per variant, optionally clickable to manage. |
| **Quantity** | Aggregate or single-variant quantity. |
| **(actions)** | Inline per-row quick actions (see below). |

**Manage columns** adds or removes columns. Selecting rows via the checkboxes reveals the multi-select bulk-action menu — see [[products-bulk-actions]].

### Per-row inline actions

The actions cell gives quick toggles without entering Edit mode:

- **Publish / Unpublish** — flips Active. **Hide / Show** — flips Hidden.
- **Duplicate** — see [[products-known-issues]] for duplicate rules (Copy suffix, draft state).
- **Change log** — opens the modal on [[products-change-log]]; icon is green when there's an entry, greyed when empty. See [[products-change-log-link]].
- **Delete** — confirmation *"Are you sure you want to delete? Caution: This action cannot be undone."* Permanent (no soft-delete or trash); see [[products-known-issues]] for the cascade.

## Settings & fields

### Create product popup — multi-screen type picker

The **+ Add product** button opens a popup that walks through three screens:

1. **Pick product type** — **Physical product** (always) and **Digital product** (when the plan supports it). Digital expands to **Downloadable files** (digital file delivery) and **Landing pages** (membership / private content; requires the Subscriptions app — if missing, the popup detours to a Required App install screen).
2. **Fill name + category** — Name input (required) + Category single-select with autocomplete against [[products-categories]], including an inline *"Want to add a new category? Type the category name to create it."* quick-create. **Create** stays disabled until both fields are filled.
3. **Create** — creates the product and opens its Edit page (`/admin/products/products-new/edit/:id?new=true`). A back-arrow returns to the type-picker.

### Import products popup — 4 entry options

The cloud-upload icon shows an **Import products** popup with 4 option cards:

| Option | Action |
|--------|--------|
| **Import with CSV file** | Opens the 3-step CSV wizard (below). |
| **XML Import app** | Routes to [[apps-xml-import]]. |
| **XML Sync app** | Routes to [[apps-xml-sync]]. |
| **API import** | Opens the CloudCart developer center API tools page in a new tab. |

### CSV import wizard — 3-step modal flow

The CSV option opens a modal wizard with a **3-step progress bar** (STEP 1 *Upload file* / STEP 2 *CSV file settings* / STEP 3 *Mapping*) and a success screen. It feeds the same import pipeline as the legacy CSV-import page ([[apps-csv-import]]).

| # | Step | What the merchant does |
|---|---|---|
| **1** | **Upload file** | Drag-and-drop or select a CSV (accepts `.csv` only). A **"CSV Template"** button downloads a sample CSV to fill in offline. **Next** without a file shows a "Please upload a CSV file" error. |
| **2** | **CSV file settings** ("General" + "Advanced" cards) | **General:** header-line toggle (`has_header_line`); category-hierarchy separator character (e.g. `>` makes `Apparel > Shirts` nested); *"Task ID number"* (`import_key`) — optional ID to chain imports into one task; Fixed-discount picker. **Advanced toggles:** Publish imported products (`publish_as_active`), Publish as featured (`publish_as_featured`), Publish as new (`publish_as_new`), Require shipping (`require_shipping`), Track quantity (`quantity_tracking`), Continue selling (`continue_sell`). |
| **3** | **Mapping** | For each product / variant field, pick the matching CSV column. Required: `product.name`, `product.id`, `variant.parent_id`. The button reads **Submit** — clicking it queues the import. |
| _(success)_ | **Import task created** | Success screen: *"The file was successfully uploaded and the products import task was added to the queue."* with a **Track importing progress** button → CSV Import task list (`apps.csv_import.settings`) in a new tab. |

A Back button is on steps 2 and 3; refreshing mid-wizard resets to step 1.

### "Imported" and "Imported with" — origin tracking

Products created via imports (CSV, XML, JSON, ERP) carry an Imported flag plus an import-source identifier. The **Imported with** filter finds all products from a specific import (e.g. from Szamlazz) — useful for reversing a bad import.

## Business rules

### Moderator restrictions

A moderator with restricted access (per [[settings-staff]] → Access permissions / Restrictions) may only edit products in certain categories. The list view filters their visible products automatically; they cannot reach hidden categories' products via the search bar either.

### Plan-cap on create

When the plan's `products` quota is exhausted, **+ Add product** still opens the popup, but the final Create step fails with a plan-upgrade prompt. See "Plan gate" on [[products-products]].

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
