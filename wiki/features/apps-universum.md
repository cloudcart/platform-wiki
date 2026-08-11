---
type: feature
nav_path: "Apps → Universum"
route_name: apps.universum.overview
route_path: /admin/apps/universum
aliases: ["Universum", "Universum ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp, accounting]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 3
---
# Universum (ERP)

## Purpose

**Universum** integration — accounting / ERP system synchronisation. Pushes orders + customer data from CloudCart to Universum; may sync product / stock data in return.

The integration has its own dedicated Orders controller (the backend manager) — likely for handling Universum-specific order export / status sync logic.

> **On/off control appears only once the saved credentials validate against Universum.** Unlike the other ERP integrations, this one is treated as configured only after the stored credentials are accepted by the Universum service; until then the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden — so a missing button is not a fault. Correct the credentials on the **Settings** tab and save until they are accepted.

## Where to find it

Sidebar → Apps → install → **Universum**.

## What the merchant can do here
- Configure Universum credentials.
- Sync orders / customers / products bi-directionally.
- See sync history + errors per order in [[orders-history]] (entries `send_erp_success` / `send_erp_error`).

### What the merchant CANNOT do here
- Use without Universum license.

## Settings & fields

Manager (the backend manager) — standard event-driven ERP integration.

## Business rules

### Order push fires on creation

Order export fires **on order creation** (`OrderCreated`), not on later status changes — the trigger is hardwired because the selector is commented out in the UI (see "Order export trigger" below). Failed pushes surface in [[orders-history]] and can be retried via the manual Send-order action.

### Send ERP error history

Failed sync attempts appear in [[orders-history]] with the `send_erp_error` action_string. Successful syncs use `send_erp_success`.

### Permission
Standard apps scope.

## How it works (verified against backend)

### Vertical
**Integrated business ERP.** From the in-app description: *"Universum is an integrated ERP system that allows you to get the information you need in real time and optimize your business processes."* Targeted at multi-website / multi-store businesses (the integration has a "Website ID" concept).

### Credentials
- **Sync address** — Universum server URL.
- **Username** + **Password** — Universum account credentials.
- **Website ID** — the merchant's website ID inside Universum (required, lets Universum partition data between multiple online stores).

### Product matching identifier
The merchant picks how products are matched between Universum and CloudCart (`compare_by`):
- **SKU code**.
- **Barcode**.
- **Nothing** (no field match).

Once linked, the platform stores it in the shared external-record mapping (`ExternalMetaData`, `integration = universum`) plus the `app_import = 'universum-<id>'` origin tag — see [[external-record-mapping]]. On later syncs the variant is found by the stored id; **Reset import** (below) does not touch this mapping — it only clears the `last_sync` watermark.

### Order export trigger — fixed, NOT selectable
Orders are pushed to Universum **automatically on creation** (`OrderCreated`). The backend keeps three trigger keys (`new_order` / `complete` / `payorship`), but the selector is **commented out in the UI** — so the merchant cannot choose a different trigger; every order pushes on creation. (A manual re-send is still available — see below.)

### Manual send-order
On any order, the merchant can use **Send order** to manually trigger the push to Universum. Success: *"Order sent successfully."* Failure: *"Universum: Error while sending the order."*

### Discount mapping
A CloudCart **discount** can be selected to group all Universum-discounted products.

### Category property mapping
The merchant can map Universum category properties to CloudCart product properties (`category_properties_mapping`) so attributes carry over.

### Product import status
The merchant can choose **with which status** newly imported products are created (active / inactive).

### Sync events in order history
The order in Universum receives a **Universum Order ID** (`keyid`). Successful sync events log `send_erp_success`; failures log `send_erp_error` with the upstream error message.

### Order export trigger is NOT selectable
The wiki previously suggested the merchant could pick "New order / Order completed / Paid or Sent" — that selector is **commented out** in the current Settings form. The integration runs only the **`new_order`** trigger (the default in `default_settings`): orders are pushed at order-creation time.

To re-export an order later, the merchant uses the per-order **Send order** action manually.

### Reset import supported
The integration supports a **Reset import** action (`supportResetImport = true`) — it clears the `last_sync` timestamp, forcing the next sync to pull the full Universum catalogue again rather than only changes since the last run.

### Manual ERP actions not supported
The Universum integration sets `supportActions = false`, so per-order ERP actions in the order details (e.g., a manual "Re-send to ERP" with action arguments) are not exposed. The single trigger is the order-created event plus the **Send order** quick button.

### Credential validation hits Universum API on every isConfigured check
The `isConfigured` method calls `validateCredentials` which makes a live API request against the Universum sync URL with the saved username/password. If Universum's server is down, the integration is reported as "not configured" even when settings are fully populated.

### Settings persisted
The exact persisted keys are: `sync_url`, `username`, `password`, `send_order`, `compare_by`, `discount_id`, `product_status`, `category_properties_mapping`. The `compare_by` field accepts `sku` / `barcode` / `nothing` (the universal ERP-core comparison values).

## Vue tab structure (admin UI)

Universum is the only ERP with an EXTRA tab — **Category Properties Mapping** — for mapping Universum's attribute schema. Per `router/index.js`:

| Tab | Route name | Component | What's there |
|---|---|---|---|
| **Overview** | `apps.universum.overview` | `ErpOverview` | Install card. |
| **Settings** | `apps.universum.settings` | `Universum/Tabs/Settings` | Credentials + BoxOne. |
| **Category mapping** | `apps.universum.categoryMapping` | `Universum/Tabs/CategoriesMapping` | Universum categories ↔ CloudCart categories (route is `categoryMapping`, singular — unique among ERPs). |
| **Category properties mapping** | (sub-route) | `Universum/Tabs/CategoryPropertiesMapping.vue` | Maps Universum attribute properties to CloudCart product properties. |
| **Status** | `apps.universum.status` | `ErpStatus` | Start/stop task. |
| **Products** | `apps.universum.products` | `ErpProducts` | Universum-imported products + ProductConnectModal. |
| **Import history** | `apps.universum.importLog` | `ErpImportLog` | Per-run log. |

### Settings tab — Credentials helper (`Credentials.vue`)

| Field | Input | Required | Error |
|---|---|---|---|
| **Sync address** (`sync_url`) | text | yes | "Invalid credentials" |
| **Username** (`username`) | text | yes | "Invalid credentials" |
| **Password** (`password`) | password (masked) | yes | "Invalid credentials" |

(NOTE: the `Website ID` field mentioned earlier in this page does NOT appear in `Credentials.vue` — it's part of older docs. Current required credentials are just 3 fields.) The save handler calls the platform code against Universum.

### Settings tab — Box one fields (the platform code)

| Field | Type | Required | Notes |
|---|---|---|---|
| `compare_by` | SKU / Barcode / Nothing select | yes | inherits shared `compareBy`. |
| `discount_id` | discount picker | no | groups discounted products. |
| `product_status` | switch | no | "Publish imported products". |
| `send_order` | select | commented out | The trigger selector is HIDDEN in current code — Universum runs only the `new_order` default. |

### `supportActions = false`, `getCompareDepends = null`, `supportResetImport = true`

These three flags mean: no per-order ERP action menu; the `compare_by` field has no dependent visibility logic; the merchant CAN trigger a full reset via the Status tab's Reset action.

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared `ExternalMetaData` mapping (`integration = universum`) + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — sync events visible here.
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP apps.

## Open questions

_None — all questions answered above._
