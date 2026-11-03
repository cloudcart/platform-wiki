---
type: feature
nav_path: "Apps → Google Sheets → Columns & filters"
route_name: apps.google_sheets.settings
route_path: /admin/apps/google_sheets/settings
aliases: ["Google Sheets columns", "Sheets column picker", "Sheets product filter", "Sheets allowed columns", "Sheets filter modes"]
tags: [apps, google, sheets, columns, filter, settings]
plan_gates: ["google_sheets"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Google Sheets → Columns & filters

> Part of [[apps-google-sheets]]. See the hub for related aspects (upload, download, sync pipeline, OAuth).

## Purpose

Documents **what data the sync moves** — which product attributes become spreadsheet columns and which products are included — plus the two important gotchas: the Discount column only supports one discount type, and the upload pipeline honours fewer filter modes than the Settings UI offers. The merchant controls both from the Settings tab.

## Where to find it

Sidebar → Apps → Google Sheets → **Settings tab** (`/admin/apps/google_sheets/settings`) → the **Allowed columns** and **Filter** boxes. The full field-level UI is on [[apps-google-sheets-settings]].

## What the merchant can do here

- Choose which product attributes appear as spreadsheet columns (`allowed_columns`).
- Choose which products are included (`filter_group` + `filter_group_value`).
- Optionally add a **Discount** column sourced from a fixed-type discount campaign.

### What the merchant CANNOT do here

- Reorder columns or transform values — the platform writes the raw column values in a fixed structure.
- Map an arbitrary CloudCart custom field as a column — only the built-in catalogue (+ the compact `Variations` column) is available.
- Effectively filter by `tag` or `selection` on Upload — those resolve for display only (below).

## Settings & fields

### The fixed column catalogue

The merchant picks any combination of these built-in columns:

- Product name
- Meta title
- Short description
- Description
- Meta description
- Brand
- Category
- Shipping
- Track quantity
- Continue selling
- Sort order
- Minimum quantity
- Variations
- Tags
- Images
- Url
- Discount (only when a `discount_id` is also chosen)

**App-conditional columns** (only when the corresponding app is installed):

- **Units** — only when [[apps-grocery-store-overview-new]] is installed.
- **Suppliers** — only when the Suppliers app is installed.
- **Stores** — only when [[apps-stores]] is installed.

**Default-checked columns at first install:** Product name, Variations, Images, Url. `allowed_columns` is required — the merchant cannot save an empty selection (*"You have not selected any columns to export"*).

### The 5 filter modes

`filter_group` decides WHICH products get pushed on Upload:

- `all` — all products.
- `category` — products in selected categories.
- `vendor` — products from selected vendors.
- `product` — specific products picked one-by-one.
- `tag` — products with specific tags.
- `selection` — products in smart collections (Product Selections).

The Settings UI resolves all five to human-readable chip labels (Category names, Vendor names, etc.) for display.

## Business rules

### The Discount column only supports `fixed`-type discounts

The Discount dropdown is populated **only with `fixed`-price discount campaigns**. Percent / bulk / quantity discounts never appear — so a merchant who only runs percent discounts has nothing to pick. If the Discount column is selected, a `discount_id` is required at save (*"You have not selected a discount"*); without a chosen discount, the Discount column is dropped from the allowed-columns list at save time. The chosen discount's discounted price fills the column on Upload.

### Upload honours only 3 filter modes (not 5)

This is the key gotcha. The Settings save endpoint **accepts** `category`, `vendor`, `product`, `tag`, and `selection`, and the UI shows chips for all of them — but the **upload job only branches on `category`, `vendor`, and `product`**. If the merchant picks `tag` or `selection`, the upload silently falls through to **"all products"** — the filter is effectively ignored. So in practice only **category, vendor, and the individual product picker** actually narrow the upload set.

### No column ordering or value transforms

The column picker is a multi-select against the fixed catalogue above. There is no UI to reorder columns in the spreadsheet or to transform values (uppercase, regex-replace, etc.) — the platform writes whatever each column's value is. The `Variations` column packs each variant's SKU / price / quantity / parameters into one compact cell.

## Related

- [[apps-google-sheets]] — hub.
- [[apps-google-sheets-settings]] — the Settings tab UI for these fields.
- [[apps-google-sheets-upload]] — where the column set + filter are applied on push.
- [[apps-google-sheets-download]] — where these same columns are read back in.
- [[apps-grocery-store-overview-new]] — gates the Units column.
- [[apps-stores]] — gates the Stores column.

## Open questions

(None currently outstanding for this page.)
