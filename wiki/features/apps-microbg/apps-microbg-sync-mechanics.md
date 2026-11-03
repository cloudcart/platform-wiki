---
type: feature
nav_path: "Apps → MicroBG → Sync mechanics"
route_name: apps.microbg.overview
route_path: /admin/apps/microbg/overview
aliases: ["MicroBG sync", "MicroBG 3-min push", "MicroBG order webhooks", "MicroBG product matching", "Поръчка vs Продажба", "MicroBG transformation rule", "MicroBG webhook activation"]
tags: [apps, erp, bulgaria, sync, inventory-sync, order-sync, webhooks, json-api]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-microbg]]. See the hub for the other aspects (architecture split, registration, prerequisites, partner matching, troubleshooting).

# MicroBG — sync mechanics (3-min push, order webhooks, transformation rule)

## Purpose

This aspect documents the runtime sync — the every-3-minute Micro.bg → CloudCart quantity + price push, the real-time CloudCart → Micro.bg order webhooks, the product-code matching that joins the two catalogues, and the Поръчка → Продажба transformation rule that decides when stock is written off on the accounting side.

## Where to find it

Every sync action is triggered from Micro.bg's side, even though the data lands in CloudCart:

- **Micro.bg admin** → **Номенклатури → Стоки → Списък стоки → CloudCart контролен панел**.
- Inside the Control Panel: **Проверка съответствие на стоките**, **Синхронизация (импорт) на ВСИЧКИ стоки от ЕЛМ към складовия софтуер**, **Активиране на известията (WebHooks) в ЕЛМ**, auto-sync checkbox, transformation-status picker.

The CloudCart side is the receiver: the [[json-api-v2|JSON-API v2]] surface accepts the quantity / price PATCHes, and the [[settings-hooks|webhooks]] surface delivers the order events Micro.bg subscribed to.

## What the merchant can do here

- Run **Проверка съответствие на стоките** to detect missing / duplicate / mismatched product codes.
- Run the one-time bulk import of CloudCart products into Micro.bg.
- Click **Активиране на известията** to subscribe Micro.bg to CloudCart's order webhooks.
- Tick the auto-sync checkbox so the 3-min quantity + price push runs.
- Pick the transformation status (when an order becomes a Продажба).

### What the merchant CANNOT do here

- Change the 3-minute cadence. It is owned by Micro.bg's scheduler and is not configurable from CloudCart.
- Trigger a manual quantity push from CloudCart's side. The push is unidirectional Micro.bg → CloudCart and runs only on Micro.bg's scheduler.
- Bypass code matching. A product without a matched code in Micro.bg won't have its stock updated.

## Settings & fields

### Inside Micro.bg's CloudCart Control Panel

- **Auto-sync checkbox** — when ticked, the 3-minute scheduler runs.
- **Кога поръчката се трансформира в продажба** — picks the CloudCart-side status (e.g. *Платена*, *Изпратена*) at which Micro.bg writes off stock and creates the accounting record.
- **Винаги да се създава Продажба** — alternative mode where every CloudCart order becomes a Продажба immediately on arrival.
- **Обект** — see [[apps-microbg-prerequisites]] for the price-group + warehouse-source mapping.

### On the CloudCart side

There are no sync-tuning fields on the CloudCart side. The platform exposes its data via [[json-api-v2|JSON-API v2]] and the webhook surface — Micro.bg drives the actual cadence.

## Business rules

### Order transformation: Поръчка vs Продажба

By default Micro.bg creates a **Поръчка** (order) row for every CloudCart order. It only transforms into a **Продажба** (sale) — which writes off stock and creates the accounting record — when the order reaches the configured status (the *"Кога поръчката се трансформира в продажба"* field in the Micro.bg CloudCart Control Panel).

Alternatively the merchant can set *"винаги да се създава Продажба"* — every CloudCart order becomes a Продажба immediately on arrival. This is unusual; most stores want the Поръчка-then-Продажба two-step so they can review before stock-writing.

**Alignment requirement**: the chosen transformation status on the Micro.bg side must match the **"Намали количество ако статусът на поръчката е"** setting on [[settings-cart]] (see [[apps-microbg-prerequisites]] + [[inventory-decrement-timing]]). Misaligned settings produce stock-drift between the two systems.

### Product matching rules

For sync to work, CloudCart products and Micro.bg stock items must share a **code**:

- **CloudCart SKU / Barcode** ↔ **Micro.bg "основен код" / Barcode**.
- For [[variant|Variants]]: **every variant must have its own unique SKU / barcode**. Micro.bg treats each variant as a separate stock item.
- Mismatches are listed by the **Проверка съответствие на стоките** action in Micro.bg's Control Panel.

**Recommended source of truth**: CloudCart (the merchant creates products in CloudCart first, then the bulk import copies them into Micro.bg). For products that already exist in Micro.bg before CloudCart is connected, the merchant must manually align codes — the platform won't guess.

### Quantity + price sync interval

Micro.bg → CloudCart sync runs **automatically every 3 minutes** (when the auto-sync checkbox is ticked in the Control Panel). Each cycle pushes the per-SKU quantities + prices from the chosen Обект into the matched CloudCart variants. So a warehouse stock edit in Micro.bg shows up on the storefront within roughly 3 minutes.

Stock writes arrive via [[json-api-v2|JSON-API v2]] and update the `quantity` field documented on [[inventory-variant-model]]. The writes ripple through the standard side-effects: the search index re-index, storefront cache invalidation, and the `product.updated` webhook firing (see [[inventory-tracking]]).

### Real-time order push

Orders flow in the opposite direction in real time:

- New order in CloudCart → CloudCart fires the `order.created` webhook → Micro.bg's webhook endpoint receives it → Micro.bg creates the corresponding Поръчка / Продажба.
- Order edited → `order.updated` webhook → Micro.bg updates the row.
- Order deleted → `order.deleted` webhook → Micro.bg removes the row.

The merchant must run the **Активиране на известията (WebHooks) в ЕЛМ** action once from Micro.bg's Control Panel to register Micro.bg as a webhook subscriber. After that, every order event auto-delivers to Micro.bg until the merchant deactivates the integration. See [[settings-hooks]] for the webhook delivery details + [[platform-rate-limits]] for the per-receiver delivery cap.

## Related

- [[apps-microbg]] — hub.
- [[json-api-v2]] — the API surface the 3-min quantity + price push writes to.
- [[settings-hooks]] — the webhook surface the order push delivers through.
- [[inventory-tracking]] — the per-Variant stock model the 3-min push updates.
- [[inventory-variant-model]] — the `quantity` integer the push writes.
- [[inventory-decrement-timing]] — the CloudCart-side decrement timing that must align with the Micro.bg transformation rule.
- [[variant]] / [[product]] — entities Micro.bg matches against by SKU / barcode.
- [[order-processing-pipeline]] — the order-status transitions that fire the webhooks.
- [[platform-rate-limits]] — webhook delivery cap that constrains the order push.
- [[products-change-log]] — the audit trail where the 3-min push entries appear.

## How it works (verified against backend)

The 3-min cadence is owned by Micro.bg's scheduler, not CloudCart's. Micro.bg's scheduler periodically calls CloudCart's JSON-API v2 to PATCH variant quantities + prices. This means: turning off the merchant's Micro.bg login does NOT stop the sync — only deactivating the integration in Micro.bg's CloudCart Control Panel does.

### Webhook activation — what the "Активиране на известията" button does

The button in Micro.bg's CloudCart Control Panel calls CloudCart's webhook API (POST `/api/v2/webhooks`) with Micro.bg's listener URL, subscribing to `order.created`, `order.updated`, `order.deleted`, and product events. After activation, every relevant CloudCart event auto-delivers to Micro.bg until the merchant either deletes the webhook from [[settings-hooks]] or revokes the API key.

### Stock writes show up in the Change log

Because the 3-min push updates Variants via the standard JSON-API v2, each stock change appears in the parent product's Change log with the API-key Initiator — see [[inventory-debugging-playbook]].

## Open questions

- Whether the 3-min cadence can be tightened on the Micro.bg side for stores with high stock-turn velocity. `(verify)` — Micro.bg-side configuration, not visible from CloudCart.
