---
type: feature
nav_path: "Apps → Versus ERP"
route_name: apps.versus_erp.overview
route_path: /admin/apps/versus-erp
aliases: ["Versus ERP", "Versus ERP ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: ["versus_erp_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 20 20 12 61 79 80 81 98 101 33 100 204 250 395 398 399 400 333 701(2+1))
---
# Versus ERP (ERP)

## Purpose

**Versus ERP** integration — ERP / accounting system connector. Syncs orders and customers between CloudCart and Versus ERP's system.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **Versus ERP**.

## What the merchant can do here
- Configure Versus ERP credentials.
- Sync orders / customers / inventory based on configured events.

### What the merchant CANNOT do here
- Use without an active Versus ERP subscription / license.

## Settings & fields
Backend manager handles credential validation and event-driven sync. App key: **versus_erp**.

## Business rules
Standard event-driven ERP integration pattern. Status-change triggers sync actions.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### Coverage country / vertical
Versus ERP is a Bulgarian distributor. The in-app description: *"Versus ERP is a leading distributor of a wide range of hardware products and represents more than 5 leading international brands for: ecommerce systems and components."* Aimed at IT / hardware retailers re-selling Versus's catalogue.

### Credentials
A single field — **Versus Rest API URL** — provides the connection endpoint. Optionally the merchant can also supply a **Versus Images API URL** for product photos. Validation: the platform calls Versus's `product` endpoint and confirms a valid array response.

### Product matching identifier
Products are matched between Versus and CloudCart using either **SKU code** or **Barcode** (corresponds to `art_nomer` in Versus).

### Action mode
- **Import and Update** — pull the catalog into CloudCart and keep prices / quantities in sync.
- **Update only** — keep the CloudCart catalog as-is and only refresh prices and stock.

### Discount mapping
The merchant can pick a CloudCart **discount** in which all Versus-discounted products will be grouped.

### Sync events in order history
Successful sync events log `send_erp_success`; failures log `send_erp_error` with the upstream error message.

### Sync frequency
The catalogue collection runs every **12 hours** (43200 s, `versus_erp_collect` mapping). The follow-on `versus_erp_import` and the per-order `versus_send_order` jobs fire on demand.

### Sync direction is BI-DIRECTIONAL
- Versus → CloudCart: products + categories + images (via the recurring `versus_erp_collect`).
- CloudCart → Versus: orders (via `versus_send_order`, fired by the order event listener).

So Versus is both a catalogue source AND an order destination, unlike pure-catalogue distributors (Also, IT4Profit, Polycomp).

### Images via separate URL
The merchant supplies a separate **Versus Images API URL** — product images are fetched from a different endpoint than the catalogue data. Per the README, this URL "may not have the same name" as their public folder — a quirk of Versus's setup where pictures live on a different host (`/pictures/`).

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `versus_erp_total_products` | Numeric (global cap) | App-specific cross-task cap on imported products from Versus ERP. When the cap is hit, additional products are skipped on subsequent imports. |

No install-level access gate — the app can be installed on any plan, but the total-product cap applies during catalogue import. See [[plan-vs-feature-pack]] for downgrade rules.

## Vue tab structure (admin UI)

Per `vuejs-sitecp/.../ErpSystems/VersusERP/router/index.js`:

| Tab | Route name | Component | What's there |
|---|---|---|---|
| **Overview** | `apps.versus_erp.overview` | `ErpOverview` | Install / activation card. |
| **Settings** | `apps.versus_erp.settings` | `VersusERP/Tabs/Settings` → `ErpSettings` + `Credentials` + `DatabaseStructure` | URL credential + image-URL modal + BoxOne. |
| **Categories mapping** | `apps.versus_erp.categoriesMapping` | `VersusERP/Tabs/CategoriesMapping` → shared `ErpCategoriesMapping` | Versus categories ↔ CloudCart categories with per-row percent markup. |
| **Status** | `apps.versus_erp.status` | `ErpStatus` | Start/stop task. |
| **Products** | `apps.versus_erp.products` | `ErpProducts` | Versus-imported products + ProductConnectModal. |
| **Import history** | `apps.versus_erp.importLog` | `ErpImportLog` | Per-run Created / Updated / Errors. |

### Settings tab — Credentials helper

| Field | Input | Required | Help | Error |
|---|---|---|---|---|
| **Versus Rest API URL** (`url`) | text, column-style | yes | "This is URL to your Versus ERP Rest API" | "Invalid credentials" |

### Settings tab — Database Structure modal

The `DatabaseStructure.vue` modal exposes the optional **Versus Images API URL** field (`pictures`). The merchant supplies it when Versus serves product photos from a separate host (per the README, this is a quirk of Versus's setup where `/pictures/` lives on a different domain).

### Categories mapping modal

Standard shared MappingModal: Versus category + CloudCart category + Percent (0–500, default 0). Sortable, searchable table on the tab itself.

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the import-origin tagging (app_import = 'versus-erp-<id>') the integration uses to track and re-find its imported products + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.

## Open questions

_None — all questions answered above._
