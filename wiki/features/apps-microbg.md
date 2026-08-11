---
type: feature
nav_path: "Apps → MicroBG"
route_name: apps.microbg.overview
route_path: /admin/apps/microbg/overview
aliases: ["MicroBG", "Micro.bg", "micro.bg", "MicroBG ERP", "Микро БГ", "no enable disable button", "app has no active toggle"]
tags: [apps, erp, bulgaria, accounting, inventory-sync, order-sync]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 4
---
# MicroBG (Micro.bg cloud accounting + warehouse)

## Purpose

**MicroBG** is the integration between CloudCart and **[micro.bg](https://micro.bg)** — a Bulgarian cloud-based accounting + warehouse software. After setup, the two platforms exchange:

- **Products** — CloudCart's catalogue is mirrored into Micro.bg's stock list (one-time import + ongoing updates via webhooks).
- **Orders** — every new / edited / deleted order in CloudCart is pushed to Micro.bg in **real time** as a *Поръчка* (or directly as a *Продажба*, depending on the merchant's chosen transformation rule).
- **Customers / partners** — every new buyer is checked against Micro.bg's partner list (by EIK if a billing address is set, otherwise by email) and auto-created when not found.
- **Quantities + prices** — Micro.bg pushes per-SKU stock and pricing back to CloudCart **every 3 minutes**, so the storefront mirrors warehouse reality.

**Architectural split (important):** the CloudCart-side app is **only a registration handshake**. The real sync runs **inside Micro.bg's CloudCart Control Panel** against the store's API key + [[json-api-v2|JSON-API v2]] + [[settings-hooks|webhooks]]. When a support ticket about "products not syncing" comes in, the answer is usually *"open Micro.bg's CloudCart Control Panel and run the matching check"* — not *"edit something in the CloudCart app"*. See [[apps-microbg-architecture-split]] for the full divide.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> Whether data actually flows is governed on the **Micro.bg side** — the registration in Micro.bg's CloudCart Control Panel plus a live subscription — not by anything switchable on the CloudCart screen, see [[apps-microbg-architecture-split]].

## Where to find it

- **CloudCart admin** → Sidebar → **Apps** → **MicroBG** (search) → Install → Settings tab.
- **Micro.bg admin** → **Администриране → Връзка с ел.магазини** (where the merchant registers CloudCart as an external e-shop) → then **Номенклатури → Стоки → Списък стоки → CloudCart контролен панел** (where the actual sync happens).

The CloudCart-side route is `/admin/apps/microbg/overview`; the registration form is at `/admin/apps/microbg/settings`. The integration's app key is **`microbg`**.

## What the merchant can do here

### In the CloudCart admin (Apps → MicroBG)

- Subscribe to Micro.bg through CloudCart's checkout (the `microbg_subscription` feature pack is a paid add-on).
- Pick between *Existing user* and *New registration* in the Settings tab.
- See the current Micro.bg subscription status — expiration date, order ID, subdomain, and the **API key** Micro.bg uses to connect back.

### In the Micro.bg admin (CloudCart Control Panel)

This is where the actual sync runs:

- **Проверка съответствие на стоките** — code-based match check between CloudCart products and Micro.bg stock items.
- **Синхронизация (импорт) на ВСИЧКИ стоки от ЕЛМ към складовия софтуер** — one-time bulk import of CloudCart products into Micro.bg.
- **Активиране на известията (WebHooks) в ЕЛМ** — Micro.bg self-subscribes to CloudCart's webhook API.

### What the merchant CANNOT do here

- Use Micro.bg without an active license for at least 2 users.
- Use Micro.bg on a CloudCart plan lower than STARTUP.
- Run sync in currencies other than BGN or with VAT not set to Bulgaria.
- Edit historical Micro.bg records from CloudCart.
- Bypass the API key mechanism (see [[settings-api-keys]]).

## Sub-pages (in this cluster)

This integration is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the support question, not read every page.

- [[apps-microbg-architecture-split]] — the CloudCart-side handshake vs the Micro.bg-side sync engine; what each side owns; why most "sync" tickets resolve in Micro.bg's UI.
- [[apps-microbg-registration]] — the Settings tab form (Existing-user vs New-registration), the two install paths, the `microbg_subscription` plan-feature gate, the handshake API flow, error responses.
- [[apps-microbg-prerequisites]] — CloudCart-side settings the merchant must adjust before sync (EIK field, decrement-status alignment, payment-type mapping, Micro.bg service products, Обект / warehouse choice).
- [[apps-microbg-sync-mechanics]] — the 3-minute quantity + price push, the real-time order webhook chain, the *Поръчка vs Продажба* transformation rule, product code matching (SKU / barcode).
- [[apps-microbg-partner-matching]] — partner-lookup cascade (EIK first, email second); B2B vs B2C consequences; why hiding the EIK field corrupts dedup.
- [[apps-microbg-troubleshooting]] — common support questions + answers, Micro.bg error-message decoding, the test environment that is in code but unused, [[orders-history]] ERP-sync entries.

## Settings & fields

The Settings tab calls **GET `/admin/api/microbg/info`** to load the merchant's existing store info (used to pre-fill the registration form) and **GET `/admin/api/microbg/settings`** to load the current subscription state. On save, **POST `/admin/api/microbg/settings`** sends to Micro.bg. The complete field-by-field breakdown — both *Existing user* and *New registration* variants — is on [[apps-microbg-registration]].

The integration depends on the `microbg_subscription` plan feature (a paid add-on bought through CloudCart's checkout). Without it, the registration flow always redirects to checkout, never to the live form. Full plan-gate flow on [[apps-microbg-registration]].

## Business rules

The full business-rules catalogue is distributed across the aspect pages:

- **Prerequisites** (≥ 2-user Micro.bg license, plan above STARTUP, BGN currency, BG VAT, mandatory settings on both sides, Обект choice) → [[apps-microbg-prerequisites]].
- **Install paths** (new vs existing Micro.bg customer) → [[apps-microbg-registration]].
- **Product matching, sync cadence, order push, Поръчка → Продажба rule** → [[apps-microbg-sync-mechanics]].
- **Partner matching cascade** (EIK → email) → [[apps-microbg-partner-matching]].
- **Permission** — standard apps scope on the CloudCart side; administrator-only on the Micro.bg side.

## Related

- [[erp-integrations]] — ERP & accounting integrations hub.
- [[apps]] — App Store catalogue.
- [[apps-microinvest]] — **different product** (Microinvest Delta, on-premise ERP, not micro.bg). Don't confuse the two when triaging tickets.
- [[apps-fgo]] / [[apps-szamlazz]] / [[apps-smart-bill]] / [[apps-flix-facts]] — alternative invoicing / ERP integrations.
- [[settings-api-keys]] — the API key Micro.bg uses to authenticate against CloudCart.
- [[json-api-v2]] — the API surface Micro.bg pulls products and pushes quantity / price updates through.
- [[settings-hooks]] — the webhook subscriptions Micro.bg self-registers.
- [[settings-cart]] — the EIK-field config + the stock-decrement-status setting + the cart-level fee / discount definitions.
- [[settings-statuses]] — order status taxonomy that Micro.bg's transformation rule references.
- [[inventory-tracking]] — the per-Variant stock model that the 3-min push updates.
- [[inventory-decrement-timing]] — the decrement-status setting that must align with Micro.bg's transformation rule.
- [[order-processing-pipeline]] — the order-status transitions that fire the webhooks Micro.bg listens to.
- [[variant]] / [[product]] — entities Micro.bg matches against by SKU / barcode.
- [[customer]] — the partner-matching cascade reads customer + billing address data.
- [[orders-history]] — ERP-sync events appear here when Micro.bg posts back status updates.
- [[platform-rate-limits]] — the per-receiver webhook delivery cap that constrains the order push.

## How it works (verified against backend)

Sync runs on Micro.bg's side using the CloudCart store's API key against the [[json-api-v2|JSON-API v2]] and [[settings-hooks|webhook]] surfaces. The CloudCart-side app does the registration handshake only. The detailed mechanics — handshake API flow, webhook activation chain, 3-minute scheduler, error response shape, non-standard 2-tab UI, the unused test endpoint — are all on the aspect pages: [[apps-microbg-architecture-split]] for the high-level divide, [[apps-microbg-registration]] for the handshake APIs, [[apps-microbg-sync-mechanics]] for the runtime sync, [[apps-microbg-troubleshooting]] for the error decoding.

## Open questions

- The Micro.bg side maintains the actual sync logic; CloudCart's view is what flows through the API + webhooks. Diagnostics for "Micro.bg said X but didn't show Y" need access to Micro.bg's own logs.
- The aspect pages reflect the platform integration as documented by Micro.bg's merchant-facing instructions; any updates to Micro.bg's side (new auto-sync settings, new entity types) need to be cross-checked there first.
