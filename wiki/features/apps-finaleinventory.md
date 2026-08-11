---
type: feature
nav_path: "Apps → Finale Inventory"
route_name: apps.finaleinventory.overview
route_path: /admin/apps/finaleinventory
aliases: ["Finale Inventory", "Finale Inventory ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: ["finaleinventory"]
created: 2026-05-22
updated: 2026-08-06
source_count: 20 20 12 61 79 80 81 98 101 33 100 204 250 395 398 399 400 333 701(2+1))
---
# Finale Inventory (ERP)

## Purpose

**Finale Inventory** integration — ERP / accounting system connector. Syncs orders and customers between CloudCart and Finale Inventory's system.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **Finale Inventory**.

## What the merchant can do here
- Configure Finale Inventory credentials.
- Sync orders / customers / inventory based on configured events.

### What the merchant CANNOT do here
- Use without an active Finale Inventory subscription / license.

## Settings & fields
Backend manager handles credential validation and event-driven sync. App key: **finaleinventory**.

## Business rules
Standard event-driven ERP integration pattern. Status-change triggers sync actions.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### Vertical
**Warehouse / inventory management.** Finale Inventory is a US-based cloud warehouse management system (WMS). The integration is geared towards merchants who fulfil from one or more physical warehouses and want a single source of truth for stock levels.

### Credentials
- **Account name** — the merchant's Finale Inventory account identifier.
- **Username** + **Password** — Finale Inventory user credentials.

The Settings tab title: *"Please follow the instructions below to properly configure your online store with Finale Inventory."*

### Warehouse selection
The merchant picks one **facility (warehouse)** from their Finale Inventory account — stock for that warehouse is what CloudCart uses.

### Client selection
If the Finale Inventory account has multiple clients, the merchant picks one (*"Select client"*).

### Action mode
- **Import products + update quantities** — pull catalog and refresh stock.
- **Update quantities only** — keep existing CloudCart catalog and only refresh stock.

### Product matching identifier
Both sides of the matching are configurable:
- **Finale Inventory side**: Product ID, UPC, or EAN.
- **CloudCart side**: SKU.

### Default category and publish status
On import, the merchant selects:
- A **default category** for newly imported products.
- A **publish status** — Published or Unpublished.

### Order commit
Optional setting *"Commit orders (lock order at finale inventory when created at the store)"* — when ON, each order is committed (locked) in Finale Inventory the moment it is placed in CloudCart. This reserves stock for that order.

### Order prefix
The merchant can set an **Order prefix** for orders sent to Finale Inventory, useful for distinguishing online-store orders in the WMS.

### Sync events in order history
Successful sync events log `send_erp_success`; failures log `send_erp_error` with the upstream error message.

### Sync frequency
The product-data sweep (`finaleinventory_product_data`, loads quantities + product info) runs every **8 hours** (28800 s). Per-order sends (`finaleinventory_send_order`) and the explicit `finaleinventory_import_products` job run on demand, with no recurring schedule.

### Bi-directional pattern
The integration imports product data + quantities **from** Finale Inventory and pushes **orders** back — typical WMS pattern. The merchant decides via the `action` setting whether new Finale Inventory products auto-create in CloudCart (`import` mode) or only refresh existing matches (`quantities only`).

### Order commit reserves stock at Finale Inventory
The `order_commit` toggle: when ON, every order placed in CloudCart triggers Finale Inventory to **lock / commit** the stock for those items immediately. Useful for merchants who don't want oversells across channels — but means partial fulfillment / cancellation requires Finale Inventory-side intervention.

### Order prefix
The `order_prefix` setting prepends a string (e.g., "CC-") to order numbers sent to Finale Inventory. Lets the merchant distinguish CloudCart-originated orders from other sales channels feeding the same Finale Inventory account.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `finaleinventory` | Access gate (install URL) | The install URL `/admin/apps/finaleinventory/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Vue tab structure (admin UI)

The CategoriesMapping route is COMMENTED OUT in `router/index.js` — Finale Inventory uses a single Default category from settings, no per-category mapping tab. The merchant sees:

| Tab | Route name | Component | What's there |
|---|---|---|---|
| **Overview** | `apps.finaleinventory.overview` | `ErpOverview` | Install card. |
| **Settings** | `apps.finaleinventory.settings` | `Finaleinventory/Tabs/Settings` | Credentials + BoxOne (facility + client + action + order_commit + order_prefix). |
| **Status** | `apps.finaleinventory.status` | `ErpStatus` | Start / Stop task. |
| **Products** | `apps.finaleinventory.products` | `ErpProducts` | Finale-imported products + ProductConnectModal. |
| **Import history** | `apps.finaleinventory.importLog` | `ErpImportLog` | Per-run log. |

(A CategoriesMapping `.vue` file exists in source but its route is commented out — merchants will not see this tab in the admin sidebar.)

### Settings tab — Credentials helper

| Field | Input | Required | Error |
|---|---|---|---|
| **Account name** (`accountname`) | text | yes | "Invalid credentials" |
| **Username** (`username`) | text | yes | "Invalid credentials" |
| **Password** (`password`) | password (masked) | yes | "Invalid credentials" |

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared ExternalMetaData mapping (integration = finaleinventory) + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.

## Open questions

_None — all questions answered above._
