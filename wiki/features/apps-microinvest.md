---
type: feature
nav_path: "Apps → Microinvest"
route_name: apps.microinvest.overview
route_path: /admin/apps/microinvest
aliases: ["Microinvest", "Микроинвест", "Microinvest Warehouse Pro", "Microinvest ERP", "Microinvest integration", "enable disable button", "app active toggle"]
tags: [apps, erp, accounting, bulgaria, retail]
plan_gates: ["microinvest_total_products"]
created: 2026-05-22
updated: 2026-08-06
source_count: 6
---
# Microinvest (ERP / retail accounting)

## Purpose

**Microinvest** integration — Bulgaria's leading retail / accounting software, used widely by physical stores, restaurants, and SMEs. The CloudCart integration syncs orders, customers, products, and stock between the online store and the merchant's Microinvest installation.

Used by merchants who run **physical AND online stores** — Microinvest is the source of truth for inventory and accounting; CloudCart's online store reflects what's in Microinvest.

This page is the **hub** for the Microinvest cluster — a definition + the sub-page map. Drill into the aspect that matches the question rather than reading all of them.

> **Has an on/off control.** This ERP counts as configured from the moment it is installed, so the app screen carries the **Enable / Disable** button straight away — it can be switched off without uninstalling it. A disabled integration stops syncing while keeping its settings.

## Where to find it

Sidebar → Apps → install → **Microinvest**. The app's tabs (Overview / Status / Settings / Processed products / Tasks / Import history) and every config field are catalogued on [[apps-microinvest-settings]].

## What the merchant can do here

- Sync orders from CloudCart → Microinvest (for accounting / invoicing).
- Sync stock from Microinvest → CloudCart (real-time inventory updates).
- Sync the product catalogue (one direction or bi-directional), matching products by Barcode / SKU.
- Configure event-driven sync and new-product defaults.

### What the merchant CANNOT do here
- Use Microinvest without a paid Microinvest license + the network module enabled.
- Run multiple Microinvest companies on one CloudCart store (verify).

## Sub-pages (in this cluster)

- [[apps-microinvest-settings]] — the Settings-tab config fields (credentials, Action, Compare by, Price field, Updates, defaults, `disable_missings`, `units`, `debug_mode`) + the tab layout.
- [[apps-microinvest-sync-model]] — sync direction & conflict resolution, on-demand (not polled), one-feed-per-store, local deployment, and the "product/stock only — not invoicing" boundary.
- [[apps-microinvest-product-matching]] — how an incoming record updates vs creates a product: the `compare_by` match, the internal `ExternalMetaData` mapping, the `sync-ids` id push, and deletion detection.
- [[apps-microinvest-reset-import]] — the Reset-import (unlink) button: what it does, when to use it, and what to do after.
- [[apps-microinvest-debug]] — **internal** sync-debugging: the Tasks tab + the `erpTasks` / `erpTaskXml` GraphQL queries that read what Microinvest actually sent.

## Settings & fields

The full field reference is on [[apps-microinvest-settings]]. In brief: credentials (`identifier` / `password`), sync `Action` (import / export), `compare_by` (match field), `price_field`, the `updates` overwrite-allowlist, new-product defaults, `disable_missings`, `discount_id`, `units` (Grocery Store only), and the staff-only `debug_mode`.

## Business rules

Each rule lives on its aspect page:

- **Sync direction / authority** — Microinvest is master for stock + price (the chosen `Updates` fields); CloudCart for orders + customers. Syncs are on-demand, one feed per store. See [[apps-microinvest-sync-model]].
- **Matching & dedup** — two layers (the `compare_by` field, then the persistent `ExternalMetaData` id↔id mapping populated via `sync-ids`); mismatches create duplicates. See [[apps-microinvest-product-matching]].
- **Reset import** — unlinks the store from Microinvest (drops the mapping + `app_import` tag) without deleting products. See [[apps-microinvest-reset-import]].
- **Debugging** — read the exact received payload with the internal `erpTasks` / `erpTaskXml` queries. See [[apps-microinvest-debug]].

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `microinvest_total_products` | Numeric (global cap) | App-specific cross-task cap on imported products from Microinvest. When the cap is hit, additional products are skipped on subsequent imports. |

No install-level access gate — the app can be installed on any plan, but the total-product cap applies during catalogue import. See [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[erp-integrations]] — ERP & accounting integrations hub.
- [[external-record-mapping]] — the shared `ExternalMetaData` mapping the matches write to + the internal read queries.
- [[apps]] — App Store.
- [[apps-posmaster]] — alternative Bulgarian retail/POS.
- [[apps-szamlazz]] / [[apps-fgo]] / [[apps-smart-bill]] — pure-invoicing apps (different model).
- [[apps-selmatic]] — another BG ERP.
- [[settings-hooks]] — Microinvest sync may dispatch / consume webhook events.

## Open questions

(none — questions about merchant-facing behaviour have been resolved against backend)
