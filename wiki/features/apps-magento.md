---
type: feature
nav_path: "Apps → Magento Importer"
route_name: apps.magento.settings
route_path: /admin/apps/magento
aliases: ["Magento", "Magento Importer", "Migrate from Magento"]
tags: [apps, migration, magento, import, competitor-platform]
plan_gates: ["magento"]
created: 2026-05-22
updated: 2026-06-10
source_count: 1
---
# Magento Importer

## Purpose

**Magento Importer** is a one-way migration tool from a **Magento** store to CloudCart. The merchant points the app at their existing Magento store via API credentials; the app fetches and imports products, variations, categories, attributes, and customers into the merchant's CloudCart catalog.

It uses Magento's **SOAP v1 API** (`api/soap/?wsdl`), which only Magento 1.x exposes. Magento 2 stores speak REST + GraphQL and do not answer SOAP v1, so this app effectively supports **Magento 1.x only** — Magento 2 merchants cannot use it.

Used when a merchant is switching platforms: they keep Magento running during migration, run the import, verify on CloudCart, then cut over. The import runs as a background process and can take **10 minutes to a couple of hours** depending on catalog size. It can be cancelled mid-flight; already-imported products stay in CloudCart.

## Where to find it

Sidebar → Apps → install → **Magento Importer**. The breadcrumb reads "Apps → Magento"; the route is `/admin/apps/magento`.

## What the merchant can do here

### Install (Header: "Install Magento Importer")
Read the install description — *"You are about to install Magento Importer. This app will be able to import data from your Magento store to your CloudCart store."* — then proceed to configuration.

### Configure credentials (Header: "Get started with the Magento Importer")
Supply three fields, obtained from the Magento admin under API access permissions:
- **Magento store URL** (`label.store_url`) — required, valid URL (`error.base_url.invalid` / `error.base_url.required`).
- **Magento API username** (`label.api_username`) — required (`error.api_user.required`).
- **Magento API key** (`label.api_key`) — required (`error.api_key.required`).

### Import setup (Header: "Setup the Magento Importer")
- **Import type** — **Everything** (`label.everything`), **Products only** (`label.products`), or **Customers only** (`label.customers`). Required (`error.magento_import.required`); must be one of the three (`error.magento_import.in_all_products_customers`).
- **Product weight unit** — **Kilograms** (`label.kilograms`) or **Pounds** (`label.pounds`). Required (`error.product_weight.required`); must be one of the two (`error.product_weight.in_kilogram_pound`).

### Monitor progress (Header: "Importing in Progress")
The progress page walks the import through its stages: collecting migration data → fetching attributes, categories, customers, products, and other required data → "Downloaded" confirmation → "Migrate customers" / "Migrate products" → final "Total customers created" / "Total products created" counts. Each stage shows its own message; a failure surfaces the specific error returned by the Magento API.

### Cancel
- **Cancel Import Process** button (`button.cancel_import`), confirmation *"Are you sure want to cancel this process"*.
- *"This import can be canceled if needed and all imported products will remain on your CloudCart store."*
- The Magento store is untouched: *"Your Magento store's content will remain the same during and after the import."*

### What the merchant CANNOT do here
- **No two-way sync** — import-only. After migration, CloudCart is the master; edits happen there.
- **No editing of existing CloudCart data** — the importer only adds / creates.
- **No order import** — only Everything / Products / Customers. Magento order history is not carried over; critical orders must be re-created manually.
- **No attribute remapping** — there is no merchant-facing mapping screen. Magento attribute sets are read as-is and CloudCart properties / custom fields are created automatically.

## Settings & fields

### Credentials

| Field (lang key) | Required | Validation |
|---|---|---|
| Magento store URL (`label.store_url`) | Yes | Valid URL format |
| Magento API username (`label.api_username`) | Yes | Non-empty |
| Magento API key (`label.api_key`) | Yes | Non-empty |

### Import options

| Field | Allowed values |
|---|---|
| Import type | Everything / Products / Customers |
| Product weight unit | Kilograms / Pounds |

When `send_forgotten_password` is enabled, CloudCart emails each migrated customer a forgotten-password link so they can set a new password (see Business rules).

## Business rules

### One-way only, cancellable, Magento read-only
The flow is Magento → CloudCart with no back-sync. The Magento store is only ever read, never modified. Cancelling preserves already-created CloudCart products and customers, but the importer does not resume from where it stopped — a restart re-fetches everything from Magento and creates-or-updates from scratch. A **reset** wipes all migration state and staged data, returning the merchant to a clean baseline as if newly installed.

### Configurable products become CloudCart variants
Each child simple product of a Magento configurable product becomes a CloudCart variant; the Magento `configurable_attributes` label/value pairs map to CloudCart variant attributes. A simple Magento product with no variations becomes a single-variant CloudCart product. Magento's hierarchical category tree is re-created in CloudCart with the same parent / child nesting, however deep.

### Images are copied into CloudCart media
Every product image is downloaded from Magento and uploaded into CloudCart's own media library — not hot-linked. After migration, products display correctly even if the source Magento store goes offline.

### Customers: randomized passwords, marketing OFF, email confirmed
Each migrated customer gets a new random password generated on CloudCart; the original Magento password hash is discarded, so customers cannot log in with their old password. Migrated customers are saved with `marketing = 0` (not opted in), `banned = 0`, `imported = 1`, and `email_confirmed = 1` — they can log in after a password reset but receive no marketing email until they opt in. With `send_forgotten_password` on, CloudCart sends each one a reset email automatically.

### Weight unit conversion
Magento stores weights in kg or lbs; the merchant declares which, and CloudCart converts during migration.

### Plan gate
Gated by the `magento` plan-feature (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]): the install URL `/admin/apps/magento/install` is blocked and the app hidden from the Apps catalog on plans lacking the feature. Existing installs keep working after a downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules. Otherwise standard apps permission scope.

## Related

- [[apps]] — App Store hub.
- [[apps-shopify]] — sister competitor migration.
- [[apps-woocommerce]] — sister competitor migration.
- [[apps-etsy]] — sister Etsy integration (different model — two-way sync).
- [[apps-csv-import]] — alternative if Magento export to CSV is preferred.
- [[apps-xml-import]] — alternative if Magento exports XML feed.
- [[products-products]] — destination of imported products.

## Open questions
