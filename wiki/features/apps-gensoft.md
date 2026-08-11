---
type: feature
nav_path: "Apps → Gensoft"
route_name: apps.gensoft.overview
route_path: /admin/apps/gensoft
aliases: ["Gensoft", "Gensoft ERP", "Gensoft integration", "GenSoft", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp, diagnostics, bulgaria]
plan_gates: ["gensoft_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 4
---
# Gensoft (ERP)

## Purpose

**Gensoft** integration — a Bulgarian ERP / accounting system used by local merchants. CloudCart connects to Gensoft over a **SOAP web service** to import the product catalogue (with prices and stock), keep stock in sync, and push orders back to Gensoft for accounting.

This page is the **hub** for the Gensoft cluster — a definition + the sub-page map. Drill into the aspect that matches the question rather than reading all of them.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it

Sidebar → Apps → install → **Gensoft**. The app's tabs (Overview / Settings / Status / Diagnostics / Products / Orders / Import history) and every config field are catalogued on [[apps-gensoft-settings]].

## What the merchant can do here

- Import the Gensoft catalogue into the online store, with prices + quantities.
- Keep stock in sync (Gensoft → CloudCart, and CloudCart → Gensoft after orders).
- Push / cancel orders in Gensoft from CloudCart.
- Self-check the live connection (the Gensoft-only **Diagnostics** tab).

### What the merchant CANNOT do here
- Use Gensoft without a Gensoft license + a reachable SOAP endpoint.

## Sub-pages (in this cluster)

- [[apps-gensoft-settings]] — the Settings tab: SOAP credentials (`wsdl_url` + employee/password), catalogue scope, the "Works with" data model, `compare_by`, Action, the import-default fields, send-all-products, discount, and the tab layout.
- [[apps-gensoft-sync-model]] — the SOAP pull, the **date-based incremental import** (`last_import` watermark), sweep frequencies (4 h / 10 min paid / 6 h resend), Action modes, and order export following the order lifecycle (increment / decrement).
- [[apps-gensoft-product-matching]] — `compare_by` (SKU / Barcode / External ID), the shared `ExternalMetaData` mapping, the manual **Connect** modal, and the "missing Gensoft ID" order-push block.
- [[apps-gensoft-reset-import]] — Reset import = clear the incremental watermark for a **full re-fetch** (it does NOT unlink — the opposite of Microinvest's reset).
- [[apps-gensoft-diagnostics]] — the read-only **Diagnostics** self-check (Connection / Auth / Catalog / Categories / Products / Known products) — Gensoft's main troubleshooting tool.

## Settings & fields

The full field reference is on [[apps-gensoft-settings]]. In brief: SOAP `wsdl_url` + `identifier` / `password` (with a validate step), the `catalog_id` catalogue, the "Works with" data model, `compare_by`, `Action`, the import-default fields (`updates`, `publish_as_*`, `require_shipping`, `quantity_tracking`, `continue_sell`, `images`, `simple`), `discount_id`, `all_products` (send all order lines), and `ten_minute_update` (paid fast sweep).

## Business rules

Each rule lives on its aspect page:

- **Sync model** — SOAP pull, incremental import by `last_import` date, 4 h / 10 min / 6 h sweeps, order push with lifecycle increment/decrement. See [[apps-gensoft-sync-model]].
- **Matching & mapping** — `compare_by` + the `ExternalMetaData` (`integration = gensoft`) article-id mapping; order push needs that id. See [[apps-gensoft-product-matching]].
- **Reset import** — clears the date watermark for a full re-fetch; keeps products linked. See [[apps-gensoft-reset-import]].
- **Diagnostics** — read-only connection self-check. See [[apps-gensoft-diagnostics]].

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `gensoft_total_products` | Numeric (global cap) | App-specific cross-task cap on imported products. When the cap is hit, additional products are skipped on subsequent imports. |
| `gensoft_update` | Feature flag | When enabled, all Gensoft order-related jobs route to the faster `system8` queue (prioritised order sync); otherwise the default queue. |

No install-level access gate — the app can be installed on any plan, but the total-product cap and queue-priority feature apply during runtime. See [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared `ExternalMetaData` mapping Gensoft writes to + the internal read queries.
- [[apps-microinvest]] — sibling BG ERP (contrast: XML-push + unlink-style reset).
- [[apps]] — App Store.
- [[orders-history]] — `send_erp_success` / `send_erp_error` sync events.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
