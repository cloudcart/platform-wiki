---
type: feature
nav_path: "Apps → Colibri ERP"
route_name: apps.colibri.overview
route_path: /admin/apps/colibri
aliases: ["Colibri ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: ["colibri", "colibri_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 3
---
# Colibri ERP

## Purpose

**Colibri ERP** integration — connector to Colibri, a Bulgarian internet-based business information system for company management. It pulls products, categories and stock from Colibri ERP into CloudCart (a one-way catalogue / stock sync). It does **not** push orders back to Colibri — fulfilment / invoicing stays on the Colibri side. In-app description: *"Colibri ERP is an Internet-based business information system designed to successfully support company management in Bulgaria."* Coverage country: **Bulgaria**.

> **On/off control appears only when the integration is configured.** Colibri is treated as configured when every credential field for the **selected protocol** (SOAP or REST — each has its own field set) is filled in and saved; until then the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden, so a missing button is not a fault. Pick the protocol on the **Settings** tab, complete that protocol's fields, and save.

## Where to find it

Sidebar → Apps → install → **Colibri ERP**. The app opens on a shared ERP shell with these tabs (in order): **Overview**, **Status**, **Settings**, **Categories mapping**, **Processed products**, **Import history** (with per-import drilldown).

## What the merchant can do here

- Choose the connection protocol (**SOAP** or **REST**) and enter Colibri credentials.
- Limit imports to specific Colibri store IDs (optional).
- Map each Colibri category to a CloudCart category.
- Choose a Colibri price list / price level and add a markup percentage.
- (REST only) configure how products are matched between Colibri and CloudCart.
- Trigger an on-demand "refresh categories now" sync after editing categories in Colibri.
- View processed products and import history.

### What the merchant CANNOT do here

- Use the app without an active Colibri ERP subscription / license.
- See per-order ERP buttons in the order detail view — the integration has no per-order actions. Orders flow through CloudCart's standard checkout; fulfilment / invoicing is handled on the Colibri side.
- (SOAP only) configure product matching — that sub-form is hidden for SOAP deployments (REST only).

## Settings & fields

App key: **colibri**. The merchant first picks the **Protocol** from a required dropdown (not searchable, not clearable). The visible credential fields depend on the protocol; switching protocol shows/hides the corresponding field set, and the other protocol's values are kept in the form but not submitted.

**When Protocol = SOAP** (also the default fallback) — five required fields:
- **Url** — Colibri SOAP endpoint.
- **Username**.
- **Password**.
- **DBName** — Colibri database name.
- **CNUM** — Colibri client number / client code.

**When Protocol = REST** — two required fields plus one optional:
- **Client ID**.
- **Client Secret**.
- **Stores** (optional) — comma-separated Colibri store IDs, placeholder `e.g. 1000, 2000, 3000`. A yellow warning box notes that listing stores explicitly limits orders / stock to only those Colibri store IDs. The IDs aren't validated; invalid IDs simply return no data. Leave blank to import from all Colibri stores. Accepts values like `001,05,004`.

**Price list / level** (both protocols):
- Toggle **Use a different price list** — when off, the base list is used.
- **Price level** (numeric) — applies only when "Use a different price list" is on. If the entered level doesn't exist in Colibri, the price is silently taken from the main list (no hard error).
- **Markup percentage** — added on top of the selected list price.

**Categories mapping** (Categories mapping tab) — a mapping table plus an add/edit side-sheet with: Colibri category select, CloudCart category select, and a **Percent** value (0–500). Each Colibri category maps to a CloudCart category.

**Product matching — REST only** (hidden for SOAP). Two identifiers form the join key:
- **`compare_colibri`** — the Colibri-side identifier, one of: **`idMat`** (default — Colibri's internal product ID), **`MNum`** (Colibri SKU / Manufacturer Number), **`Barcode`**.
- **`compare_by`** — the CloudCart-side identifier, one of: **`external_id`** (default — CloudCart's external_id field), **`sku`**, **`barcode`**.

`external_id` is the default and is unusual for ERP integrations — REST mode is designed for merchants who already track Colibri's `idMat` on their CloudCart products' external_id field.

## Business rules

- **Credentials are validated live on save.** For SOAP, the platform logs in to the Colibri SOAP server using the URL, username, password, CNUM and database. For REST, it requests an OAuth access token using the Client ID and Client Secret (the token is then managed by the platform). An invalid combination blocks the save with an "Invalid credentials" error against the relevant fields.
- **Configuration is considered complete only when all fields of the selected protocol are filled** — SOAP needs Url, Username, Password, DBName and CNUM; REST needs Client ID and Client Secret. The **Stores** field is never required.
- **Category mapping may gate other tabs.** Until at least one category mapping exists, the Status and Processed-products tabs stay hidden when category mapping is required.
- **Product matching is REST-only.** SOAP is import-only without bidirectional product lookups. On Colibri's side products are matched by **idMat**, **MNum** or **Barcode**; on CloudCart's side by external_id, SKU or barcode.
- **Recurring syncs.** The integration runs a recurring product import and a recurring category-tree sync in the background. A separate on-demand "refresh categories now" sync can be triggered from the admin UI after categories are edited in Colibri.
- **Sync events appear in order history.** A successful sync logs the `send_erp_success` action; a failure logs `send_erp_error` with the upstream error message — see [[orders-history]].

### Permission

Standard apps permission scope.

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `colibri` | Access gate (install URL) | The install URL `/admin/apps/colibri/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |
| `colibri_total_products` | Numeric (global cap) | App-specific cross-task cap on imported products from Colibri ERP. When the cap is hit, additional products are skipped. |

Lower plans cannot install the app. Existing installs keep working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared ExternalMetaData mapping (integration = colibri) the Products connect modal writes to + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.

## Open questions

_None — all questions answered above._
