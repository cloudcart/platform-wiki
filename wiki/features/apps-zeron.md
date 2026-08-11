---
type: feature
nav_path: "Apps → Zeron"
route_name: apps.zeron.overview
route_path: /admin/apps/zeron
aliases: ["Zeron", "Zeron ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 5
---
# Zeron (ERP)

## Purpose

**Zeron** integration — connector to the Zeron ERP / accounting system (a Bulgarian ERP). It imports products and stock from Zeron, refreshes prices, and pushes CloudCart orders into Zeron based on configured order events. App key: **zeron**.

Zeron's settings form **independent behaviour axes** (inbound Action, the order-export trigger, and single- vs multi-warehouse via Site ID) — see [[zeron-sync-modes]] for the model and how they combine.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **Zeron**. The app opens with five tabs:

- **Overview** (`apps.zeron.overview`) — install card.
- **Settings** (`apps.zeron.settings`) — credentials + sync configuration.
- **Status** (`apps.zeron.status`) — Start / Stop the sync task.
- **Products** (`apps.zeron.products`) — Zeron-imported products, with a connect-product modal.
- **Import history** (`apps.zeron.importLog`) — per-run log.

## What the merchant can do here
- Enter Zeron connection credentials.
- Choose how products are matched (SKU vs Barcode) and whether to import the full catalog or only refresh stock + prices.
- Select which Zeron warehouses feed stock, and which warehouse fulfils outgoing orders.
- Choose when CloudCart pushes an order to Zeron.
- Start / stop the sync task and review per-run import history.

### What the merchant CANNOT do here
- Use the app without an active Zeron subscription / license.

## Settings & fields

### Credentials (Settings tab)
All credential fields are validated together: saving calls Zeron's quantity endpoint and accepts the credentials only if the response is non-empty. This also confirms Zeron is reachable **and** that at least one warehouse / quantity record exists — an account with no warehouses configured on the Zeron side fails validation with **"Invalid credentials"**.

| Field | Key | Required | Notes |
|---|---|---|---|
| **Server URL** | `sync_url` | yes | Zeron server address. |
| **Username** | `username` | yes | |
| **Password** | `password` | yes | Masked input. |
| **Database** | `database` | yes | |
| **Site ID** | `site_id` | no | The **Zeron Website ID** (Zeron's internal partition identifier) — *not* CloudCart's site id. |

### Sync configuration (Settings tab)

| Field | Key | Type | Required | Shown when | Notes |
|---|---|---|---|---|---|
| **A unique identifier** | `compare_by` | SKU / Barcode select | yes | always | How products are matched between Zeron and CloudCart. |
| **Action** | — | mode select | yes | always | *Import products + update quantities* (pulls the full catalog and creates/updates products) vs *Update quantities and prices only* (keeps the catalog as-is, refreshes stock + price). |
| **Product price percent** | `product_price_percent` | number (`%`) | yes | Action = import | Markup over the Zeron price on import. **Default 20%** — change to 0 (or another value) before the first import if you want Zeron prices as-is. |
| **Default category** | `category_id` | category search | yes | Action = import | Category for newly imported products. |
| **Publish imported products** | `product_status` | switch | no | Action = import | Off = new products stay unpublished (hidden from storefront). |
| **Zeron warehouses** | `warehouses` | multi-select | yes | `site_id = 0` | Whose stock feeds CloudCart. Loaded live from Zeron when the Settings tab opens. |
| **Warehouse for orders** | `warehouse_order` | single select | yes | `site_id = 0` | The warehouse Zeron debits for fulfilment of outgoing orders. |
| **Create warehouses as Stores** | `create_warehouses` | switch | no | [[apps-stores]] installed AND `site_id = 0` | Creates each selected Zeron warehouse as a CloudCart Store for [[apps-store-locations]] use. Hidden entirely when Stores is not installed. |
| **Warehouse → Store map** | `warehouses_map` | (auto-managed) | — | `create_warehouses` on | Internal mapping of each Zeron warehouse to the CloudCart Store created for it — populated when **Create warehouses as Stores** runs, and used to route each warehouse's stock to the right store. Not edited directly by the merchant. |
| **Send order** | `send_order` | select (3 options) | no | always | When CloudCart pushes the order to Zeron — see Business rules (labels are misleading). |
| **Use new structure** | `new_structure` | switch | no | CloudCart staff console login only | Internal staff toggle for testing a newer Zeron schema — **not shown to merchants**. |

The warehouse dropdowns share one live fetch: opening the Settings tab makes a single call to Zeron's quantity endpoint regardless of how many warehouse selects appear, cached for the rest of that request. Reloading the page fetches again. There is no merchant control over the cache duration.

## Business rules

### Order export trigger labels are MISLEADING
The **Send order** selector has three options whose UI labels do not match their actual trigger semantics:

| Selector option | Actual trigger event |
|---|---|
| **New order** | Order creation. |
| **Order complete** | Order's payment status changed (i.e., Paid or Sent). |
| **Paid or Sent** | Order's status changed to Completed. |

"Order complete" and "Paid or Sent" appear swapped. When configuring, test by changing an order's status rather than trusting the label text.

### Sync events in order history
Each push to Zeron is written to the order history. Successful pushes log `send_erp_success`; failed pushes log `send_erp_error` with the upstream error message. See [[orders-history]].

### Stores integration
**Create warehouses as Stores** only appears when [[apps-stores]] is installed and `site_id = 0`. Enabling it creates each selected Zeron warehouse as a CloudCart Store.

### Permission
Standard apps permission scope.

## Related
- [[zeron-sync-modes]] — how Action, the order-export trigger, and the Site ID single/multi-warehouse gating combine into independent behaviour modes.
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared ExternalMetaData mapping (integration = zeron) + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error`).
- [[apps-stores]] / [[apps-store-locations]] — required for the warehouses-as-Stores option.
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.

## Open questions

_None — all questions answered above._
