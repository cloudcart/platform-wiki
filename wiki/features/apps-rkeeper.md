---
type: feature
nav_path: "Apps → R-Keeper"
route_name: apps.rkeeper.overview
route_path: /admin/apps/rkeeper
aliases: ["R-Keeper", "R-Keeper ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 20 20 12 61 79 80 81 98 101 33 100 204 250 395 398 399 400 333 701(2+1))
---
# R-Keeper (ERP)

## Purpose

**R-Keeper** integration — ERP / accounting system connector. Syncs orders and customers between CloudCart and R-Keeper's system.

R-Keeper's settings form **independent behaviour axes** (inbound Action mode, the order-export trigger, delivery method, location) — see [[rkeeper-sync-modes]] for the model and how they combine.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **R-Keeper**.

## What the merchant can do here
- Configure R-Keeper credentials.
- Sync orders / customers / inventory based on configured events.

### What the merchant CANNOT do here
- Use without an active R-Keeper subscription / license.

## Settings & fields
Backend manager handles credential validation and event-driven sync. App key: **rkeeper**.

## Business rules
Standard event-driven ERP integration pattern. Status-change triggers sync actions.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### Vertical
R-Keeper is a **restaurant / hospitality POS system**, not a generic accounting ERP. The integration targets merchants who sell food / hospitality items and need their CloudCart store to mirror the POS catalogue and push orders into R-Keeper.

### Credentials
The merchant supplies:
- **Basic URL Server** — the R-Keeper server endpoint.
- **SID** — R-Keeper session / authentication identifier.
- **Company ID** (Corp ID) — R-Keeper company / corporate identifier.

If credentials are invalid, the form shows *"Invalid R-Keeper login details."*

### Prerequisite: Store Locations app
R-Keeper requires the **Store Locations** app to be installed first. The UI shows: *"You need to have the app installed Store Locations so you can use the R-Keeper app."* Each R-Keeper "object" (physical restaurant location) is linked to a CloudCart store location.

### Action mode
- **Import and Sync** — pull the R-Keeper catalogue into CloudCart and keep it synced.
- **Sync only** — keep the existing CloudCart catalogue and only refresh.

### Product matching identifiers
The merchant picks both a CloudCart identifier (**ID**, **SKU code**, **Barcode**) and an R-Keeper identifier (**ID**, **Code**) for matching.

### Delivery method
The merchant picks a delivery mode:
- **Personal delivery** — the merchant / restaurant delivers themselves.
- **Delivery with Glovo** — orders are forwarded to Glovo for last-mile delivery. (Requires the Glovo app to be configured with locations.)

### Object / location linking
The merchant selects an **R-Keeper object** (location) from which products are imported / synced, then links it to a CloudCart store location. *"You have no locations added to R-Keeper"* shows when R-Keeper exposes no objects.

### Order export trigger
Choose when CloudCart pushes an order to R-Keeper:
- **New Order** — immediately on creation.
- **Order complete** — when the order reaches the "Complete" status.
- **Paid or Sent** — when the order is paid or marked as sent.

### Default category
The merchant selects a default category in which newly imported R-Keeper products are placed.

### Sync events in order history
Successful sync events log `send_erp_success`; failures log `send_erp_error` with the upstream error message.

### Sync frequency
Catalogue / stock pulls run every **8 hours** (28800 s, `rkpeer_products` mapping — note typo "rkpeer" in queue name). Order-side `rkpeer_order` fires on demand from the event listener, with a separate `rkpeer_order_payment` job (10-second delay) that runs when a paid/completed order needs payment details pushed to R-Keeper.

### Order-event dispatch
The R-Keeper the platform code listens for `OrderCreated`, `OrderStatusChange`, and `FulfillmentAdd`. The dispatch matrix:
- `send_order = new_order` → fires on `OrderCreated`.
- `send_order = complete` → fires when status becomes `completed`.
- `send_order = paid` → fires when status becomes `paid`.
- `send_order = sent` → fires on `FulfillmentAdd`.

For orders that ALREADY have an `rkeeper_order_id` meta AND reach `paid` or `completed`, the listener fires `rkpeer_order_payment` — pushes the payment information separately. So R-Keeper learns of both the order AND the payment in two stages.

### Order is sent at most once per status path
Per the listener guard, the platform tracks `rkeeper_order_id` meta — if already set when a new event would trigger a send, the duplicate is suppressed (similar pattern to Barsy). Each order pushes to R-Keeper exactly once for the initial sync.

## Vue tab structure (admin UI)

Per `vuejs-sitecp/.../ErpSystems/RKeeper/router/index.js`:

| Tab | Route name | Component | What's there |
|---|---|---|---|
| **Overview** | `apps.rkeeper.overview` | `ErpOverview` | Activation card. |
| **Settings** | `apps.rkeeper.settings` | `RKeeper/Tabs/Settings` | Credentials + 3 boxes (Locations, BoxOne, Payments). |
| **Status** | `apps.rkeeper.status` | `ErpStatus` | Start/Stop task. |
| **Products** | `apps.rkeeper.products` | `ErpProducts` | Paginated R-Keeper products + ProductConnectModal. |
| **Import history** | `apps.rkeeper.importLog` | `ErpImportLog` | Per-run log. |

(NOTE: a Tab file `CategoriesMapping.vue` exists in source but is NOT registered as a route — the merchant does not see a Categories tab. R-Keeper uses a single Default category from settings, not per-category mapping.)

### Settings tab — Credentials helper (`Credentials.vue`)

Three required fields:

| Field | Input | Required | Error |
|---|---|---|---|
| **Server URL** (`basic_url`) | text | yes | "Invalid credentials" |
| **SID** (`sid`) | text | yes | "Invalid credentials" |
| **Company ID** (`corp_id`) | text | yes | "Invalid credentials" |

Save fires a live Guzzle GET `{basic_url}/rests?corpid={corp_id}` with `SID` header — valid response (status != "Err" + at least one rest entry) → credentials accepted.

### Settings tab — 3 boxes

Per the platform code:

| Box | Key | Fields | Notes |
|---|---|---|---|
| **boxLocations** | `operations` | One select per R-Keeper depot (location) → maps to a CloudCart Store Location. | Only renders when [[apps-store-locations]] is installed; the UI shows "You need to have the app installed Store Locations…" otherwise. |
| **boxOne** | main | `compare_by` (SKU/Barcode/ID); `compare_rkeeper` (ID/Code); `default_category` (search; required; dependent on `action = import`); `send_order` (4 options: New Order / Sent / Paid / Order complete; required); `qty_default` (number; help: "Regardless of the Track Product Quantity option…") | Defaults: `compare_by=sku`, `compare_rkeeper=code`, `send_order=complete`, `qty_default=1`. |
| **boxPayments** | `payments` | One select per R-Keeper payment method → multi-select of CloudCart [[settings-payment-providers]] providers. | Lets the merchant map R-Keeper's payment codes back to CloudCart's payment providers when orders sync. |

### Products tab — Product connect modal

Same shared `ProductConnectModal` as other ERPs — links one CloudCart product to one R-Keeper external ID.

## Related
- [[rkeeper-sync-modes]] — how Action mode, the order-export trigger, delivery and location combine into independent behaviour modes.
- [[food-restaurant-grocery]] — food / restaurant / grocery concept hub.
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared ExternalMetaData mapping (integration = rkeeper) + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.
- [[apps-store-locations]] — required prerequisite for the Locations mapping box.

## Open questions

_None — all questions answered above._
