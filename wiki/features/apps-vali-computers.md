---
type: feature
nav_path: "Apps → Vali Computers"
route_name: apps.vali_computers.overview
route_path: /admin/apps/vali_computers
aliases: ["Vali Computers", "Vali Computers ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 20 20 12 61 79 80 81 98 101 33 100 204 250 395 398 399 400 333 701(2+1))
---
# Vali Computers (ERP)

## Purpose

**Vali Computers** integration — ERP / accounting system connector. Syncs orders and customers between CloudCart and Vali Computers's system.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **Vali Computers**.

## What the merchant can do here
- Configure Vali Computers credentials.
- Sync orders / customers / inventory based on configured events.

### What the merchant CANNOT do here
- Use without an active Vali Computers subscription / license.

## Settings & fields
Backend manager handles credential validation and event-driven sync. App key: **vali_computers**.

## Business rules
Standard event-driven ERP integration pattern. Status-change triggers sync actions.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### Coverage country / vertical
Vali Computers is a Bulgarian computer hardware distributor. The integration is targeted at IT hardware resellers who want to import the Vali catalogue and sell it through their CloudCart store.

### Credentials
A single field — **API Key** — provided by Vali Computers. The platform validates it on save; success message: *"Successfully connecting to Vali Computers."* Failure: *"Failed to connect to Vali Computers. Please check that you have entered the correct API key."*

### Action mode
- **Import and Synchronize** — pull the catalogue and keep stock + prices in sync.
- **Synchronize Only** — keep the existing CloudCart catalogue and only refresh stock + prices.

### Product matching identifier
The merchant selects how to match products between Vali and CloudCart: **SKU**, **Model**, or **Barcode**, both for the CloudCart side and for the matching Vali identifier.

### Category mapping
The merchant chooses which Vali categories to import from, and maps each to a CloudCart category. If the merchant connects a Vali category to a CloudCart category, the imported products are placed in that store category. Otherwise products go to a chosen default category.

### Pricing
The merchant picks which Vali price to use:
- **Wholesale Price**.
- **End Customer Price**.

A **markup percentage** can be applied per category.

### Status mapping
Vali exposes five availability statuses; the merchant decides which to import and which default quantity to assign per status when CloudCart has no exact quantity from Vali:
- Out of Stock
- In Stock
- Limited Quantity
- On the Way
- Order Only

### Plan limit on imported products
The merchant has a product import limit defined by the plan. When approached, the storefront shows *"Your product import limit is {count} products"* with a link to purchase an **Additional product package**.

### Import status filter
The merchant chooses with which **statuses** products should be created on import — for example "Active" only.

### Identifier ON THE VALI SIDE: Model or Barcode (not SKU)
The product-matching uses TWO independent identifiers:
- **Identifier in Vali Computers** (`identifier_erp`) — either `model` (default) or `barcode`. This is what Vali sends.
- **Compare by** (`compare_by`) — either `sku` or `barcode`. This is what CloudCart uses on its side to look up the product.

**Nothing** is NOT supported as a compare-by option (`supportCompareNothing = false`), unlike most other ERP integrations. Vali Computers products MUST match an existing CloudCart SKU or barcode.

### Price source has 4 combinations
- **The price is taken from** — `price_partner` (wholesale) or `price_client` (end-customer).
- **The promo price is taken from** — `no_promo_price`, `price_promo` (partner promo), or `price_client_promo` (client promo).

When a promo source is selected, an additional **Discount** field becomes required — a CloudCart discount entity that groups all promo-priced products together.

### VAT add-on
A separate **VAT % to be added** field (`default_vat`) applies an additional VAT percentage on top of the imported price before it lands on the storefront. Default is 0%.

### Custom stock quantities per Vali availability status
Vali exposes 5 availability statuses (Out of Stock, In Stock, Limited Quantity, On the Way, Order Only). The merchant configures a **default integer quantity** per status (`status_qty_0` through `status_qty_4`) — so when Vali reports "Limited Quantity" without a specific number, CloudCart uses the merchant-configured fallback.

Defaults: 0 / 5 / 0 / 0 / 0 (so "In Stock" defaults to 5 units; everything else defaults to zero).

### Category mapping is REQUIRED
`requiredCategoryMapping = true` — the merchant CANNOT save settings without mapping at least one Vali category to a CloudCart category. The `import_category` toggle decides:
- ON (default) — imported products land in their mapped Vali-to-CloudCart category.
- OFF — all imported products land in a single **default_category** (required when the toggle is off).

### "Only visible for clients" filter
The toggle `only_visible` (default ON) restricts the import to products Vali has marked as client-visible. Hidden / staff-only Vali products are skipped.

### Plan limit measured by IMPORTED product count
The plan feature `vali_computers_import` reads the platform code from the integration's own product table — the merchant's plan caps how many Vali products can be imported (not how many they can have visible). Once the cap is reached, the platform shows the upgrade CTA with the merchant's current count vs limit.

### Reset-import supported
The integration supports a full reset (per `supportResetImport`) — clears the import history so the next run pulls Vali's whole catalogue fresh.

## Vue tab structure (admin UI)

Per `vuejs-sitecp/.../ErpSystems/ValiComputers/router/index.js`:

| Tab | Route name | Component | What's there |
|---|---|---|---|
| **Overview** | `apps.vali_computers.overview` | `ErpOverview` | Install / activation. |
| **Settings** | `apps.vali_computers.settings` | `ValiComputers/components/Settings.vue` | Credentials + Box settings. |
| **Categories mapping** | `apps.vali_computers.categoriesMapping` | `ValiComputers/components/CategoriesMapping.vue` | REQUIRED — Vali categories ↔ CloudCart categories (`requiredCategoryMapping = true`). |
| **Status** | `apps.vali_computers.status` | `ValiComputers/components/Status.vue` | Start / Stop task + product-import-limit upsell. |
| **Products** | `apps.vali_computers.products` | `ValiComputers/components/Products.vue` | Vali-imported products. |
| **Import history** | `apps.vali_computers.importLog` | `ErpImportLog` | Per-run log. |

(Two routes are COMMENTED OUT in the router source: `apps.vali_computers.notifications` and an older legacy variant. Merchants don't see those tabs.)

### Settings tab — Credentials helper

Single field:

| Field | Input | Required | Placeholder | Error |
|---|---|---|---|---|
| **API KEY** (`api_key`) | text | yes | `020cTPmGcQkVlSR2N2hzk42gDwa9r0pv6ep9FXnXnRl62uYHjjbBTp60JW` | "Invalid credentials" |

Save messages: success — *"Successfully connecting to Vali Computers."* / failure — *"Failed to connect to Vali Computers. Please check that you have entered the correct API key."*

### Categories mapping modal (specific to Vali)

The shared `MappingModal` is used; per-mapping fields are the same Vali category + CloudCart category + Percent (0–500). Because `requiredCategoryMapping = true`, the platform marks the Settings save as incomplete until at least one mapping exists.

### Status tab — plan-upsell CTA

When the merchant approaches the `vali_computers_import` plan limit, the Status tab's `appFeatures` block renders:
> *"Your product import limit is **{current}** products. Currently imported products: **{used}**"*

with an inline "Purchase an additional bundle of products" link that opens the plan-bundle purchase modal.

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared ExternalMetaData mapping (integration = vali_computers) + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.

## Open questions

_None — all questions answered above._
