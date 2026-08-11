---
type: feature
nav_path: "Apps → IT4Profit"
route_name: apps.it4profit.overview
route_path: /admin/apps/it4profit
aliases: ["IT4Profit", "IT4Profit ERP", "enable disable button", "app active toggle", "missing enable button"]
tags: [apps, erp]
plan_gates: ["it4profit", "it4profit_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 20 20 12 61 79 80 81 98 101 33 100 204 250 395 398 399 400 333 701(2+1))
---
# IT4Profit (ERP)

## Purpose

**IT4Profit** integration — connects CloudCart to **ASBIS Bulgaria's B2B IT4Profit** distributor platform. ASBIS is one of Bulgaria's leading distributors of IT products (computers, components, software). The integration lets the merchant import the ASBIS catalogue into the storefront and keep it in sync.

> **On/off control appears only when the integration is configured.** Every ERP that uses this shared screen supports being switched on and off, but the **Enable / Disable** button (and the enabled / disabled indicator next to the app name) stays hidden until the connection credentials are filled in and saved — so a missing button on a fresh install is not a fault. Fill in the credentials on the **Settings** tab, save, and the button appears.

## Where to find it
Sidebar → Apps → install → **IT4Profit**.

## What the merchant can do here
- Configure IT4Profit credentials.
- Sync orders / customers / inventory based on configured events.

### What the merchant CANNOT do here
- Use without an active IT4Profit subscription / license.

## Settings & fields
Backend manager handles credential validation and event-driven sync. App key: **it4profit**.

## Business rules
Standard event-driven ERP integration pattern. Status-change triggers sync actions.

### Permission
Standard apps permission scope.

## How it works (verified against backend)

### Coverage country / vertical
**Bulgaria — IT distribution.** The integration backs ASBIS Bulgaria's B2B IT4Profit platform. From the in-app description: *"ASBIS is among Bulgaria's leading IT distributors — computers, computer components, software."*

### Credentials
The merchant supplies their **ASBIS IT4Profit account username and password** (from the ASBIS portal). No API key — standard ASBIS account credentials.

### Category mapping
The merchant maps ASBIS catalogue categories to CloudCart categories before import begins. *"Map your categories from ASBIS IT4Profit."*

### Pricing markup
A **markup percentage** can be applied so the merchant's storefront price is higher than the ASBIS dealer price. (Field label: *"Increase the prices of items by %"*.)

### Sync events in order history
Successful sync events log `send_erp_success`; failures log `send_erp_error` with the upstream error message.

### Sync frequency
The catalogue import (`it4profit_parse`) runs every **24 hours** (86400 s). The category tree refresh (`it4profit_categories`) runs every **3 hours** (10800 s). A one-off fetch (`it4profit_categories_fetch`) runs on demand when the merchant requests a categories refresh.

### Sync direction is PULL ONLY
Like Also, IT4Profit is a distributor-catalogue integration. Products flow from ASBIS IT4Profit → CloudCart only. CloudCart does NOT push orders or stock back to IT4Profit.

### Sole configurable behaviour
Beyond credentials and category mapping, the only behavioural toggle is the **percentage markup**. There are no per-status sync triggers, no test environment — it's a one-way catalogue pull with a markup. Plan-feature gates apply at install time and on the total-products cap (see **Plan gates** section below).

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `it4profit` | Access gate (install URL) | The install URL `/admin/apps/it4profit/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |
| `it4profit_total_products` | Numeric (global cap) | App-specific cross-task cap on imported products from the ASBIS IT4Profit catalogue. When the cap is hit, additional products are skipped. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## UI structure — tabs + sub-flows

IT4Profit shares the **Asbis** Vue tree internally (`vuejs-sitecp/src/CcModules/Erp/ErpSystems/Asbis/`) — the app key is `it4profit` but the components are named "Asbis" because the integration backs ASBIS Bulgaria's distributor portal. Visible tabs: **Overview**, **Status**, **Settings**, **Categories mapping**, **Processed products**, **Import history** (+ drilldown).

### Settings tab — Asbis credentials

The `Credentials.vue` exposes two required fields:
- **Access username** (`username`, string, required) — the ASBIS portal username.
- **Access password** (`password`, `PasswordInputComponent`, required).

Field-level errors come straight from `responseErrors.username` / `responseErrors.password` (translated). The save flow calls ASBIS's auth endpoint; on rejection the merchant sees the upstream error message attached to whichever field is offending.

Below credentials: the standard fetch-data-after-validate-credentials queue progress panel (shared with all ERPs).

After validation: the configuration panel exposes the **markup percentage** field (label: *"Increase the prices of items by %"*), plus the optional CloudCart **discount** picker (to group all IT4Profit-flagged products under a discount).

### Categories mapping modal

Standard ERP CategoryMap table + side-sheet MappingModal — three fields:
- **IT4Profit category** select (searchable, required) — server-fed from ASBIS category list.
- **CloudCart category** select (searchable, required).
- **Percent** (number, 0–500, optional category-level markup that stacks on the global one).

## Related
- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the import-origin tagging (app_import = 'it4profit-<id>') the integration uses to track and re-find its imported products + the internal read queries.
- [[apps]] — App Store.
- [[orders-history]] — ERP sync events appear here (`send_erp_success` / `send_erp_error` action strings).
- [[apps-microinvest]] / [[apps-posmaster]] — alternative ERP integrations.

## Open questions

_None — all questions answered above._
