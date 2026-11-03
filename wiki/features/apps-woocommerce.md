---
type: feature
nav_path: "Apps → WooCommerce Importer"
route_name: apps.woocommerce.settings
route_path: /admin/apps/woocommerce
aliases: ["WooCommerce", "WooCommerce Importer", "Migrate from WooCommerce", "Migrate from WordPress"]
tags: [apps, migration, woocommerce, wordpress, import, competitor-platform, csv]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 1
---
# WooCommerce Importer

## Purpose

**WooCommerce Importer** is a one-way migration tool from a **WooCommerce** (WordPress-based) store to CloudCart. Unlike [[apps-magento]] (which uses live API credentials), WooCommerce migration is **CSV-based** — the merchant exports their WooCommerce products to a CSV file in WordPress admin, then uploads that file here.

This approach decouples the migration from API access — useful for merchants who:
- Lack admin / developer access to their WooCommerce backend.
- Are migrating from a managed WordPress host without exposed APIs.
- Want full control over the data subset being moved (they can edit the CSV).

## Where to find it

Sidebar → Apps → install → **WooCommerce Importer**.

The route is `/admin/apps/woocommerce`. The Vue route currently renders a placeholder; the legacy flow handles the upload.

## What the merchant can do here

### Install (Header: "WooCommerce Importer installation")
Help text: *"With this tool you will be able to import products from WooCommerce."* Capabilities:
- *"With WooCommerce Importer you will be able to: import products from WooCommerce in your online shop."*

### Configure (Header: "WooCommerce Importer settings")
Help text: *"Set up the settings below in order to configure correctly your online store with WooCommerce."*

The single key field:
- **File to import products from** (`label.file`) — CSV file upload.

Errors:
- *"Invalid csv file"* (`error.invalid.file`) — surfaces when the uploaded file isn't a valid CSV.

### What the merchant CANNOT do here
- Pull data directly via WooCommerce REST API — WooCommerce Importer is CSV-only.
- Migrate orders / customers (the lang file documents only products).
- Two-way sync (one-shot import).
- Upload anything other than CSV (other formats rejected).

## Settings & fields

| Field (lang key) | Required | Validation |
|---|---|---|
| File to import products from (`label.file`) | Yes | Must be a valid CSV (`error.invalid.file`) |

The lang file (`/lang/en/woocommerce.php`) currently exposes only these strings; no API credentials, no fetch-mode, no progress tracking — strictly file-upload + parse + import.

## Business rules

### CSV format expected
The merchant exports products from WooCommerce admin → All Products → Export. WooCommerce's CSV format includes columns for: ID, SKU, Name, Categories, Tags, Regular price, Sale price, Stock, Description, Short description, Images, Attributes, etc. CloudCart's importer parses these into its product model.

### Single upload per session
Standard CSV import — large catalogs may need batching across multiple uploads.

### Import-only
Like other competitor migrations, WooCommerce → CloudCart is one-way.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### Standard WooCommerce export format only — fixed column indexes

The importer reads cells by hardcoded column position — column 0 = ID, 1 = type (`variable` / simple), 3 = Name, 4 = Active, 8 = Description, 25 = Categories, 28 = images, 38-47 = up to three variant attribute name/value pairs. These positions match WordPress's built-in WooCommerce → All Products → Export. CSVs from third-party plugins (WP All Export, Import/Export Products) usually emit different column orders and **will not import correctly** with this app — the merchant must use the standard WooCommerce export.

### Variable products → CloudCart variants automatically

Rows with type `variable` are detected and their child variation rows (grouped via the `id:{parent_id}` reference in column 31) are collected as variants. Up to **three** variant attributes are supported (e.g., Color + Size + Material). Each variation row contributes one CloudCart variant with its own SKU, barcode, price, quantity, weight, and images. Simple products (no variations) become single-variant CloudCart products.

### Category nesting preserved — `>` delimiter converted

WooCommerce's `Cat1 > Cat2 > Cat3` notation in the Categories column is split on `>` and re-joined with CloudCart's internal category delimiter. Deep hierarchies are kept.

### Images downloaded into CloudCart's media library

Image URLs from the CSV column are fetched and uploaded into CloudCart's storage (using the same ERP-importer image pipeline). The original WooCommerce server can be retired after import without breaking CloudCart product images.

### Custom attributes — variant attributes consumed, "category property" hint stored

The first variant attribute name/value pair (cols 38/39) is duplicated into a product-level `category_properties` hint that maps to a CloudCart property option for the category. WooCommerce's freely-defined attributes beyond the three slots are not imported.

### No order or customer import path

Per the formatter's restriction to `'import_type' => 'product'` records: only products are imported. The CSV format itself contains no order or customer data, and the importer has no separate path for them. Order history and customer accounts stay on the WordPress / WooCommerce side.

### Single upload — process runs in 50-row chunks

The uploaded CSV is parsed, formatted products are inserted into the staging `erp_import` table in batches of 50, and the integration's `complete` counter increments per batch. A large catalog uploaded in one file is handled in batches — the merchant cannot pause / resume mid-file.

### When to choose WooCommerce vs the generic CSV import

The WooCommerce app handles WooCommerce's specific CSV layout (column positions, `variable` product type, `id:{parent}` variant grouping, `>`-delimited categories) automatically. The generic [[apps-csv-import]] expects the merchant to map columns manually and supports any column order, but requires more setup. Merchants exporting straight from WooCommerce should pick this app; merchants with a custom column layout should use [[apps-csv-import]].

### Modern Vue screen is a placeholder — Smarty templates drive the actual flow

The modern Vue route is empty — the install / upload / progress screens are rendered by legacy Smarty templates. Vue migration is pending.

### CSV is validated by column count BEFORE upload begins — requires column 38+

The first sanity check parses the first CSV row and ensures column index 37 exists (so the file has at least 38 columns). If not, the upload fails with `error.invalid.file`. This catches obviously wrong / truncated exports before bytes are pushed to S3. The check uses CloudCart's CSV file analyser to auto-detect the delimiter (comma / semicolon / tab) before splitting the first row.

### S3 storage for the uploaded CSV — per-site, timestamp-keyed

The uploaded CSV is stored at `{site_id}/imports/woocommerce/{timestamp}.csv` on S3. The `woocommerce_products` queue task reads it back via the `s3` disk and deletes it after processing. Like Shopify importer, this works across multiple worker servers and avoids local disk pressure.

### Pre-upload progress reset wipes prior state

Each new upload clears completed / complete / total / msg / info settings AND deletes existing import records (records / failed_records on the app). The merchant cannot resume a partial import — restarting begins from scratch.

### Uninstall stops in-progress imports

Uninstalling the app calls `setWorking(0)`, which removes the queued `woocommerce_products` job. So uninstalling during an import stops the worker; surviving items remain in the staging table but no further imports happen.

## Related

- [[apps]] — App Store hub.
- [[apps-csv-import]] — generic CSV import (overlap — verify when to use WooCommerce vs generic).
- [[apps-magento]] — sister API-based competitor migration.
- [[apps-shopify]] — sister competitor migration.
- [[products-products]] — destination of imported products.

## Open questions

