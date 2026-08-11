---
type: feature
nav_path: "Apps → Polycomp"
route_name: apps.polycomp.overview
route_path: /admin/apps/polycomp
aliases: ["Polycomp", "Polycomp ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: ["polycomp_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 3
---
# Polycomp (ERP)

## Purpose

**Polycomp** integration — ERP / accounting system connector. Syncs orders and customers between CloudCart and Polycomp's system.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **Polycomp**.

## What the merchant can do here
- Configure Polycomp credentials.
- Sync orders / customers / inventory based on configured events.

### What the merchant CANNOT do here
- Use without an active Polycomp subscription / license.

## Settings & fields
Backend manager handles credential validation and event-driven sync. App key: **polycomp**.

## Business rules
Standard event-driven ERP integration pattern. Status-change triggers sync actions.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### Coverage country / vertical
Polycomp is a Bulgarian distributor of computer / hardware brands. The in-app description: *"Polycomp is a leading distributor of a wide range of hardware products."* Target users are IT / hardware retailers who want to re-sell Polycomp's catalogue.

### Credentials
- **Polycomp Rest API URL** — distributor's API endpoint.
- **Username** + **Password** — Polycomp account login.
- **API Code** — Polycomp account API code.

If incorrect, the form shows *"Invalid credentials"*.

### Category mapping
The merchant runs **Sync Brands, Groups, and Subgroups** to pull Polycomp's catalogue tree, then manually links each Polycomp category to a CloudCart category. Each link must be unique — *"Polycomp category is already sync"* prevents duplicates.

### Pricing
The merchant picks one of Polycomp's price types:
- Price per Client without VAT.
- Price per Client in BGN without VAT at the rate of the day.
- Price per Client in BGN with VAT at the rate of the day.
- Dealer price without VAT.
- Dealer price with VAT.
- Dealer price with discounts without VAT.
- Price with all discounts in BGN without/with VAT at the rate of the day.

A **percentage markup** can then be applied to inflate the price.

### Availability-status-driven quantities
Polycomp returns availability statuses rather than exact stock numbers. The merchant maps each Polycomp status to a CloudCart default quantity:
- **In stock**.
- **On the road**.
- **Limited quantity**.
- **With an order**.
- **Pending**.

### Product status filter
The merchant chooses **Import products with Status** — only products in selected statuses are imported / updated.

### Missing-product handling
The integration can be configured to **delete missing products** when they vanish from Polycomp's feed (default ON), with a "Syncing missing products from Polycomp" job that handles disabling.

### Sync events in order history
Successful sync events log `send_erp_success`; failures log `send_erp_error` with the upstream error message.

### Sync frequency
Two recurring jobs:
- **Product / stock collection** (`polycomp_collect`) — every **24 hours** (86400 s).
- **Category collection per site** (`polycomp_category_collect_per_site`) — every **3 hours** (10800 s).
- On-demand jobs: `polycomp_sync` (full sync trigger), `polycomp_delete` (mass delete), `polycomp_category_collect_per_site_fetch` (one-off category fetch).

So Polycomp's catalogue refreshes once per day; categories more frequently.

### Sync direction is PULL ONLY
Polycomp is a distributor catalogue: products + categories flow Polycomp → CloudCart only. CloudCart does NOT push orders, stock, or customer data back to Polycomp.

### Default settings on install
The defaults pre-populated when the merchant installs:
- `price_type = kkprice` (one of the Polycomp price columns).
- `in_stock = 5`, `on_the_road = 1`, `limited_quantity = 1`, `with_an_order = 0`, `pending = 0` (the merchant can override each).
- `delete_missing_products = 1` (disable products that disappear from Polycomp's feed).

### Validation calls Polycomp live
On Save, the platform calls Polycomp's `getVendors` API with the supplied credentials. If the response array is non-empty, credentials are accepted; otherwise the form shows *"Invalid credentials"*.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `polycomp_total_products` | Numeric (global cap) | App-specific cross-task cap on imported products from Polycomp. When the cap is hit, additional products are skipped on subsequent imports. |

No install-level access gate — the app can be installed on any plan, but the total-product cap applies during catalogue import. See [[plan-vs-feature-pack]] for downgrade rules.

## Vue tab structure (admin UI)

The Polycomp admin UI uses the shared **ERP Core** layout with these tabs (per `vuejs-sitecp/.../ErpSystems/Polycomp/router/index.js`):

| Tab | Route name | Vue component | What's there |
|---|---|---|---|
| **Overview** | `apps.polycomp.overview` | `Core/.../ErpOverview` → `Apps/Install` | Install / uninstall card; activation toggle. |
| **Settings** | `apps.polycomp.settings` | `Polycomp/Tabs/Settings` → `Core/.../ErpSettings` | Credentials + 3 setting boxes (see below). |
| **Categories mapping** | `apps.polycomp.categoriesMapping` | `Polycomp/Tabs/CategoriesMapping` → `Core/.../ErpCategoriesMapping` | Paginated table of Polycomp → CloudCart category mappings + Add modal. |
| **Status** | `apps.polycomp.status` | `Polycomp/Tabs/Status` → `Core/.../ErpStatus` | Start / Stop task button + progress / plan-feature CTAs. |
| **Products** | `apps.polycomp.products` | `Polycomp/Tabs/Products` → `Core/.../ErpProducts` | Paginated products table (Polycomp ID, name, action, status) + ProductConnectModal. |
| **Import history** | `apps.polycomp.importLog` | `Core/.../ErpImportLog` | Per-run log with Created / Updated / Errors counts. |
| **Import list (per run)** | `apps.polycomp.importList` | `Core/.../ErpImportList` | Drill-down for one import run. |

### Settings tab — Credentials helper

Per `Polycomp/Tabs/Helpers/Credentials.vue`, three required inputs:

| Field | Input type | Required | Error label |
|---|---|---|---|
| **Username** | text | yes | "Invalid credentials" |
| **Password** | password (masked) | yes | "Invalid credentials" |
| **API Code** | text | yes | "Invalid credentials" |

On Save the form runs a single live API call (the platform code); empty array → all three fields display "Invalid credentials".

### Settings tab — 3 box accordion (`getAdditionalSettings`)

| Box | Key | Fields |
|---|---|---|
| **Box one** | `price_and_status` | `price_type` (select, required, 9 options from the platform code); `product_status` (multi-select, required — options: All / In stock / On the road / Limited quantity / With an order). |
| **Box two** | `polycomp_inventory` | 5 required number inputs — `availability_quantity.in_stock`, `on_the_road`, `limited_quantity`, `with_an_order`, `pending`. Defaults 5 / 1 / 1 / 0 / 0. |
| **Box three** | `import_settings` | 4 switches — `status` (Publish imported products), `track_inventory`, `continue_selling`, `delete_missing_products` (default ON). |

### Categories mapping modal (shared `MappingModal.vue`)

The "Add new mapping" button opens a **right-side slide modal** (size lg, no close on backdrop/esc, no footer). Three required fields:

| Field | Input | Validation |
|---|---|---|
| **Polycomp category** | searchable select | required; "Polycomp category is already mapped" if duplicate. |
| **CloudCart category** | searchable select | required; live check against current categories. |
| **Percent** | numeric, step 1, min 0, max **500** | optional; defaults 0 (no markup). |

Header has "Cancel" + "Save" buttons; spinner on Save. Success toast: "Record was created successfully" / "Record was updated successfully".

### Products tab — Product connect modal

The "Products connect" button opens a right-side modal with:
- **Product** picker (`SelectWithAjax` against `/admin/api/core/products` filtered to active, non-digital).
- **External ID** free-text input.

This lets the merchant manually link an existing CloudCart product to a Polycomp ID (overrides automatic matching by SKU/barcode). The entered External ID is written to the shared external-record mapping (`integration = polycomp`, see [[external-record-mapping]]); imported products also carry the `app_import = 'polycomp-<id>'` origin tag that the collect job and missing-product cleanup match on.

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared mapping the connect modal writes to + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.

## Open questions

_None — all questions answered above._
