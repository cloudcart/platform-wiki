---
type: feature
nav_path: "Apps → PosMaster"
route_name: apps.posmaster.overview
route_path: /admin/apps/posmaster
aliases: ["PosMaster", "Pos Master", "PosMaster ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp, pos, retail]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 3
---
# PosMaster (POS / retail ERP)

## Purpose

**PosMaster** integration — POS system + retail ERP. Used by physical-store merchants whose checkout terminals run PosMaster and who want online + physical orders unified in one inventory + accounting system. Unlike [[apps-microinvest]] / [[apps-selmatic]] (direct API), PosMaster exchanges data over **FTP files**: PosMaster writes export files to an FTP server, CloudCart reads them; CloudCart writes new-order files back, PosMaster reads them. This is the legacy ERP integration model for older retail software with no modern API.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it

Sidebar → Apps → install → **PosMaster**.

## What the merchant can do here

The integration shows these tabs:

- **Overview** (`apps.posmaster.overview`) — install / activation.
- **Settings** (`apps.posmaster.settings`) — FTP credentials, FTP paths, and sync options.
- **Status** (`apps.posmaster.status`) — Start / stop the sync task.
- **Products** (`apps.posmaster.products`) — paginated list of PosMaster-imported products, each connectable to a CloudCart product.
- **Import history** (`apps.posmaster.importLog`) — per-run Created / Updated / Errors counts, with a drill-down for one import run (`apps.posmaster.importList`).

So the merchant can: sync orders, customers, products and stock between CloudCart and PosMaster; choose which order status triggers order export; map multiple physical warehouses to FTP directories; and review import results per run.

### What the merchant CANNOT do here

- Use PosMaster without a PosMaster subscription / license.
- Map categories — PosMaster treats the catalogue as flat (no merchant-mapped category tree).
- Use SFTP / FTPS — only plain FTP is supported. Host the exchange files on a server reachable by plain FTP, protected by firewall whitelist or VPN.

## Settings & fields

### FTP credentials (all required)

| Field | Setting key | Input | Error |
|---|---|---|---|
| FTP address | `ftp.host` | text | "Invalid credentials" |
| FTP port | `ftp.port` | number | "Invalid credentials" |
| FTP username | `ftp.username` | text | "Invalid credentials" |
| FTP password | `ftp.password` | password (masked) | "Invalid credentials" |

Changing any credential reveals a **Validate credentials and connect** button. Saving runs a live FTP connection test with a 5-second timeout.

### FTP paths (Database Structure)

A preview row + edit modal showing the saved paths:

| Field | Setting key | Required | Validation message |
|---|---|---|---|
| Image URL | `images_url` | no | "Image URL is not valid url link" |
| Product XML File Directory | `ftp.product` | yes | "Directory for products files is required" |
| Directories for your warehouses | `ftp.warehouses` (comma-separated list) | yes | "Directories for your warehouses is required" |
| Directory for order files | `ftp.orders` | yes | "Directory for order files is required" |

`ftp.warehouses` is an **array of directory paths** — chain stores point one CloudCart store at several PosMaster warehouses, each its own FTP directory; all are read on every sync cycle.

### Sync options

- `action` — **fixed to `import`**; there is no import/export selector in the settings form (the catalogue side is always an inbound import + stock/price sync). The only configurable direction choice is the outbound `send_order` trigger below.
- `compare_by` (select) — match products by SKU / EAN / etc. The link is stored in the shared external-record mapping (`ExternalMetaData`, `integration = posmaster`, key = the PosMaster article code) plus the `app_import = 'posmaster-<code>'` origin tag — see [[external-record-mapping]]. The import also runs a "look-alike" near-duplicate matching step (below).
- `send_order` (select, required) — which order status exports the order. Three options: **New Order** (`new_order`), **Paid or Sent** (`change_status_payment`), **Order complete** (`change_status_completed`). If left unset, orders are not pushed — only stock + products sync.
- `product_status` (switch) — publish imported products.
- `shipping_code` (text) — PosMaster's article code for courier services. Help text: "If the delivery of the order is at the expense of the sender and its value is greater than 0, the courier service will be added to the export file of the order. If you leave the field blank it will not be added to the export order file."
- `discount_id` — discount applied to imported data.

## Business rules

- **Catalogue / stock sync runs once per day** (every 24 h / 86400 s) — the background task reads from and writes to FTP on that cycle.
- **Order export fires in near-real-time** on the chosen status event, with no recurring schedule. The system queues a send when an order is created (`new_order`), when its status changes to completed (`change_status_completed`) or paid (`change_status_payment`), and when a fulfillment is added (treated as the paid/sent case). The `send_order` setting decides which of these are actually exported.
- **Shipping as a line item.** When `shipping_code` is set and the order's courier fee is greater than 0 and shipping is at the sender's expense, that fee is appended to the export file as an extra "product" with this code, so PosMaster sees the shipping fee as a line item. Blank `shipping_code` omits shipping from the export entirely.
- **No de-duplication guard on order push.** A send is queued for every matching status event, so multiple status changes can spawn multiple FTP writes — the merchant's PosMaster ingestion should be **idempotent on order number**.
- **Imported duplicates.** Import includes a "look-alike" matching step to catch near-duplicate products that often appear in FTP-exported data.
- Typical use is consolidating physical-shop sales with online sales in one inventory pool.

### Permission

Standard apps permission scope.

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared `ExternalMetaData` mapping (`integration = posmaster`) + the internal read queries.
- [[apps]] — App Store.
- [[apps-microinvest]] — alternative BG POS / ERP (direct API).
- [[apps-selmatic]] — alternative BG ERP (direct API).

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
