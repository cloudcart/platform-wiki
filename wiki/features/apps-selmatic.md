---
type: feature
nav_path: "Apps → Selmatic"
route_name: apps.selmatic.overview
route_path: /admin/apps/selmatic
aliases: ["Selmatic", "Selmatic ERP", "Selmatic Bulgaria", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp, accounting, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 4
---
# Selmatic (Bulgarian ERP)

## Purpose

**Selmatic** integration — Bulgarian retail / accounting ERP. Used by Bulgarian merchants who run their accounting in Selmatic and want CloudCart orders / customers synced for unified bookkeeping.

The Manager exposes an `orderDetails($order)` method referenced in [[orders-details]] (commented out in current code) — suggesting Selmatic may add a sidebar module showing Selmatic-specific order metadata.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it

Sidebar → Apps → install → **Selmatic**.

## What the merchant can do here
- Configure Selmatic credentials.
- Sync customers to Selmatic, and **manually** push individual orders. (Automatic order push is currently **disabled** in code — see Business rules.)
- (Possibly) see per-order Selmatic module on the order details page.

### What the merchant CANNOT do here
- Use without Selmatic license + network module.

## Settings & fields

Manager (the backend manager) — standard ERP integration pattern.

## Business rules

Standard event-driven sync model. Bulgarian local deployment typical.

### Permission
Standard apps scope.

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[apps]] — App Store.
- [[apps-microinvest]] / [[apps-posmaster]] — alternative BG ERPs.
- [[orders-details]] — Selmatic order module may appear in the sidebar.

## How it works (verified against backend)

### 4 credentials: host + port + username + password

Required credentials are `host`, `port`, `username`, `password`. The merchant configures Selmatic's local server endpoint (host + port) + auth. Confirms **Selmatic is a LOCAL / SELF-HOSTED ERP** (not a cloud service), with the merchant exposing a specific host:port to CloudCart.

### Two background queue jobs

Selmatic sync has TWO distinct background pipelines (`selmatic_load_quantities_and_prices`, `selmatic_categories`):
1. **Quantities + prices** — frequent sync of stock + price changes.
2. **Categories** — periodic sync of category structure.

These run on different cadences (verify intervals).

### Order-details module IS active

The integration renders a per-order sidebar module on [[orders-details]]. **Answers the order-details module question**: YES, the module is active. It shows Selmatic-specific data (e.g., the order's status in Selmatic's system).

### resetImport via `resetViews`

The reset-import action instructs Selmatic to drop / reset its database views used for sync. Simpler than Microinvest's full meta cleanup; relies on Selmatic-side cleanup.

### supportActions + supportCompareNothing

Per the support flags: `supportActions = true` (per-action UI) and `supportCompareNothing = true` (allows comparison-less sync mode where Selmatic data fully overrides CloudCart without checking differences).

### Bi-directional sync confirmed

The integration has both directions:
- **Selmatic → CloudCart**: `selmatic_load_quantities_and_prices`, `selmatic_load_products`, `selmatic_load_images`, `selmatic_load_external_data`, `selmatic_import_products`, `selmatic_remove_missing_products`.
- **CloudCart → Selmatic**: `selmatic_send_order` (orders pushed to Selmatic).
- Stock-write back: `selmatic_set_quantities_and_prices` (rare reverse direction for setting prices back).

Products + stock + prices flow from Selmatic to CloudCart. Order push in the other direction (CloudCart → Selmatic) exists but its **automatic listener is currently disabled** (see "Order push is currently DISABLED in the listener" below) — orders reach Selmatic only via the manual send-order action.

### Database-view based integration

Selmatic exposes 15 named database VIEWS that the integration reads (`ITEMS_VIEW_ID`, `PRICES_VIEW_ID`, `QUANTITIES_VIEW_ID`, `VENDORS_VIEW_ID`, `DYNAMIC_ATTRIBUTES_VIEW_ID`, `DYNAMIC_ATTRIBUTES_VALUES_VIEW_ID`, `CUSTOM_ATTRIBUTES_VALUES_VIEW_ID`, `CATEGORIES_VIEW_ID`, `ITEM_TO_CATEGORY_VIEW_ID`, `CUSTOMER_VIEW_ID`, `ADDRESS_VIEW_ID`, `MASTER_ORDER_VIEW_ID`, `DETAILS_ORDER_VIEW_ID`, `COMMIT_ORDER_VIEW_ID`, `LOGRESET`).

The merchant's Selmatic admin / consultant creates these database views in Selmatic; the merchant then enters each view's ID into the Settings tab. This means Selmatic must expose a network-accessible database (typically MS SQL) that CloudCart reads from. **The merchant should restrict network access via firewall / IP whitelist** to CloudCart's egress IPs.

### Settings persisted (per `keySettings`)

The integration persists: `host`, `port`, `username`, `password` (Selmatic database credentials), `images_path_id` + `drive_owner_email` (product images are loaded from a **Google Drive shared folder** — `images_path_id` is the shared-folder ID, `drive_owner_email` the Drive owner's email for access), `show_selmatic_id` (display Selmatic IDs in product short description), `merge_additional_info`, `updates` (fields to overwrite on ERP change — 9 options: name, short_description, description, category_id, vendor_id, stock_status, category_properties, track_inventory, status), `discount_id`, `publish_as_active` / `publish_as_featured` / `publish_as_new`, `require_shipping`, `quantity_tracking`, `continue_sell`, `compare_by` (SKU/EAN/etc.), `delete_missing_products` (default ON), and the 15 view IDs above.

### Product mapping — the shared `ExternalMetaData` store

Once a Selmatic item is linked it is stored in the shared [[external-record-mapping]] store: an `ExternalMetaData` row with `integration = selmatic`, `external_record_key = <Selmatic item ID>` → the CloudCart variant, plus the `app_import = 'selmatic-<ID>'` origin tag (the quantity/price jobs find Selmatic products by this `selmatic-%` tag). The first link is made by `compare_by` (SKU default / EAN / barcode); read the rows with the `externalMetaData` query on [[external-record-mapping]]. `delete_missing_products` (default ON) removes products that the Selmatic views stop returning.

### Selmatic ID as visible reference

Toggle `show_selmatic_id` (when ON): CloudCart prepends Selmatic's product ID into the short description — useful for the merchant to cross-reference with Selmatic's records.

### supportCompareNothing override

Selmatic does NOT support the "compare nothing" sync-mode override or per-action toggling — it always uses the configured `compare_by` (default SKU). Different from Microinvest which supports compare-nothing mode.

### Sync frequency
Two recurring jobs:
- **Quantities + prices** (`selmatic_load_quantities_and_prices`) — every **4 hours** (14400 s). This is the high-frequency stock / price sync.
- **Categories** (`selmatic_categories`) — every **8 hours** (28800 s). The category-tree refresh.

On-demand jobs (no recurring interval): `selmatic_load_products`, `selmatic_load_images`, `selmatic_load_external_data`, `selmatic_import_products`, `selmatic_remove_missing_products`, `selmatic_send_order`, `selmatic_set_quantities_and_prices`.

### Sync direction — automatic catalogue pull only; automatic order push is off

In practice Selmatic syncs **one direction automatically**: Selmatic → CloudCart (products, categories, prices, quantities, images, external data). The automatic **order push (CloudCart → Selmatic) does not fire** — the order-create listener is short-circuited off (`if (0 && …)` in `onOrderCreate`). Orders reach Selmatic only via the manual `send-order/{order_id}` route, or if CC support re-enables the listener. So an order placed on the storefront is **not** sent to Selmatic automatically today.

### `compare_by` per import
The integration supports comparison by SKU (default), EAN, or barcode — chosen per integration setup. Once chosen, all imports use the same identifier. The merchant can't mix identifiers within one Selmatic configuration.

## UI structure — tabs + sub-flows

ErpMain shell. Visible tabs (in order): **Overview**, **Status**, **Settings**, **Categories mapping**, **Processed products**, **Import history** (+ drilldown).

### Settings tab — credentials + DatabaseStructure modal

The `Credentials.vue` exposes **four required fields** (Selmatic exposes a local MS-SQL-style endpoint):
- **Host** (string, required) — error "Invalid credentials" surfaces on failure.
- **Port** (string, required) — validated as integer-parseable ("Port must be an integer", "Port is required").
- **Username** (string, required).
- **Password** (`PasswordInputComponent`, required).

The Settings tab also exposes a custom **DatabaseStructure** sub-modal (`Selmatic/components/Tabs/Helpers/DatabaseStructure.vue`) — visible as a separate `SettingModalRow` with a Preview/Edit pattern:

- **Preview**: shows the saved **Images base url** and **Id of the folder containing the images in Google Drive** (label-and-value rows).
- **Edit** (clicking the row opens a side-sheet modal, size `lg`): two inputs:
  - **Images base url** (string, error surfaces if `images_base_url` field returns a validation message).
  - **Id of the folder containing the images in Google Drive** (string).

These two fields are required because Selmatic does not embed images; CloudCart fetches them from a merchant-controlled Google Drive folder. The merchant configures the base URL pattern + the Drive folder ID.

Below the database-structure block, the rest of the Settings tab renders the merchant-controlled flags (`compare_by`, `updates` multi-select of 9 fields, `publish_as_active` / `publish_as_featured` / `publish_as_new`, `require_shipping`, `quantity_tracking`, `continue_sell`, `delete_missing_products` default ON, `show_selmatic_id` toggle, etc.) plus the 15 named **database view ID** fields the Selmatic admin must supply (ITEMS_VIEW_ID, PRICES_VIEW_ID, etc.).

### Categories mapping tab + modal

Standard CategoryMap table + side-sheet MappingModal (Selmatic-category select, CloudCart-category select, Percent 0–500). Required before Status / Products / Tasks unlock when `categoryMapping` is required.

### No Tasks tab

Unlike Microinvest, Selmatic does not expose a Tasks tab — its sync runs purely via the recurring queue mappings (`selmatic_load_quantities_and_prices` every 4 hours, `selmatic_categories` every 8 hours) without per-task drill-down.

### Order-details module

Per the Manager's `orderDetails` method, Selmatic renders a per-order sidebar module on the order details page showing Selmatic-side data (typically the Selmatic order status). See [[orders-details]].

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
