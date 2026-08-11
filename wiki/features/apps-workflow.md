---
type: feature
nav_path: "Apps → Workflow"
route_name: apps.workflow.overview
route_path: /admin/apps/workflow
aliases: ["Workflow", "Workflow ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: ["workflow_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 20 20 12 61 79 80 81 98 101 33 100 204 250 395 398 399 400 333 701(2+1))
---
# Workflow (ERP)

## Purpose

**Workflow** integration — ERP / accounting system connector. Syncs orders and customers between CloudCart and Workflow's system.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **Workflow**.

## What the merchant can do here
- Configure Workflow credentials.
- Sync orders / customers / inventory based on configured events.

### What the merchant CANNOT do here
- Use without an active Workflow subscription / license.

## Settings & fields
Backend manager handles credential validation and event-driven sync. App key: **workflow**.

## Business rules
Standard event-driven ERP integration pattern. Status-change triggers sync actions.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### What the integration does
The merchant can:
- import products from Workflow into the online shop;
- export orders from CloudCart to Workflow.

### Connection method (FTP, not direct API)
Workflow connects over **FTP** (not a REST API). The merchant supplies:
- **Host** (the FTP server address).
- **Username** + **Password**.
- **Port** (FTP port).
- **Has SSL** switch — turns on FTPS when Workflow requires encrypted FTP.

### File paths the merchant configures
- **The path of the file from which the products will be imported** (`products_file_path`) — for example `D:/CloudCart/products.xml`. Products + quantities are read from this XML on the Workflow side.
- **The path of the file where the orders will be imported from CloudCart** (`orders_export_file_path`) — for example `D:/CloudCart/orders.csv`. CloudCart writes orders here for Workflow to consume.

### Product matching identifier
Products are matched between Workflow and CloudCart by **Barcode** by default.

### Product publishing flags
On import, the merchant can set defaults: publish as **active**, mark as **featured**, mark as **new**, and enable **quantity tracking** + **continue selling when out of stock**.

### Compare-by is limited to barcode or nothing (no SKU option)
The Workflow Settings form exposes only **Barcode** or **Nothing** as the product matcher — unlike most other ERPs in CloudCart that also offer SKU. Workflow products are matched exclusively by their barcode value. The default is `barcode`; selecting `nothing` disables product matching entirely (new products are always inserted, never updated).

### FTP connect validation runs on save with 5-second timeout
When the merchant saves credentials, the platform attempts a live FTP/FTPS connection to the configured host:port with a 5-second timeout. The credential validation method `connectFTP` returns null on any connection or authentication error and the save fails. The merchant gets immediate feedback at save time — no separate "test connection" button.

### Empty username rejected without a connection attempt
`validateCredentials` checks for non-empty `username` first; if the field is empty it returns false immediately without attempting a TCP connection. This prevents accidental anonymous FTP connections.

### Orders push fires only at order CREATION (not on status change)
Workflow's the platform code listens to **`OrderCreated`** only. Once-created orders that later change status (e.g., to "Paid" or "Cancelled") do NOT re-trigger an FTP push. The merchant cannot reconfigure this — there is no "send on paid / sent" selector on the form.

The platform writes/appends to the configured **orders export CSV** on the FTP server; downstream Workflow is responsible for picking up the file.

### Three job mappings: products import + order export + (commented) quantity import
The platform registers two active queue mappings:
- `workflow_products` — periodic re-import of the catalogue from the configured XML file path.
- `workflow_order_export` — push each new order to the FTP CSV.

A third mapping (`workflow_import_quantities` — stock-only updates from a separate CSV) is **commented out** in the code; the wiki's stock-import description reflects a future / merchant-DIY workflow rather than a built-in periodic job at this time.

### Active toggle resets all records
Switching the app's active state (`setWorking`) clears all completion/progress flags AND **deletes every import record + failed-import record** for the integration. So re-activating after a pause restarts the import from scratch — there is no resume behaviour.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `workflow_total_products` | Numeric (global cap) | App-specific cross-task cap on imported products from Workflow's FTP feed. When the cap is hit, additional products are skipped on subsequent imports. |

No install-level access gate — the app can be installed on any plan, but the total-product cap applies during catalogue import. See [[plan-vs-feature-pack]] for downgrade rules.

## Vue tab structure (admin UI)

Workflow does NOT have a Categories mapping tab — there's no route for it (the merchant matches products by barcode only, with no per-category mapping). Per `router/index.js`:

| Tab | Route name | Component | What's there |
|---|---|---|---|
| **Overview** | `apps.workflow.overview` | `ErpOverview` | Activation card. |
| **Settings** | `apps.workflow.settings` | `Workflow/Tabs/Settings` → `ErpSettings` + `Credentials` + `DatabaseStructure` | FTP credentials + path modal + BoxOne. |
| **Status** | `apps.workflow.status` | `ErpStatus` | Start / stop task. |
| **Products** | `apps.workflow.products` | `ErpProducts` | Workflow-imported products + ProductConnectModal. |
| **Import history** | `apps.workflow.importLog` | `ErpImportLog` | Per-run log. |

### Settings tab — Credentials helper

| Field | Input | Required | Error |
|---|---|---|---|
| **FTP address** (`host`) | text | yes | "Invalid credentials" |
| **FTP port** (`port`) | number | yes | "Invalid credentials" |
| **FTP username** (`username`) | text | yes | "Invalid credentials" |
| **FTP password** (`password`) | password (masked) | yes | "Invalid credentials" |
| **Has SSL** (`has_ssl`) | switch | no — default 0 | Toggles FTPS. |

The `validateCredentials` method rejects an empty username before any TCP attempt — preventing anonymous FTP. Then opens a connection with 5-second timeout.

### Settings tab — Database Structure modal

A `SettingModalRow` exposes 3 FTP path fields:
- **Path of the file from which products will be imported** — e.g. `D:/CloudCart/products.xml`.
- **Path of the file from which inventory will be imported** — e.g. `D:\CloudCart\product_quantities.csv`.
- **Path of the file where orders will be exported** — e.g. `D:/CloudCart/orders.csv`.

### Settings tab — BoxOne

The shared box exposes `compare_by` restricted to Barcode / Nothing (no SKU option for Workflow), plus publish-status switches: `active`, `featured`, `new`, `track_inventory`, `continue_selling`.

## Related
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.

## Open questions

_None — all questions answered above._
