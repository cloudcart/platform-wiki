---
type: feature
nav_path: "Apps → MicroBG → Architecture split"
route_name: apps.microbg.overview
route_path: /admin/apps/microbg/overview
aliases: ["MicroBG architecture", "MicroBG handshake vs sync", "Micro.bg Control Panel", "CloudCart Control Panel in Micro.bg", "Where the sync runs"]
tags: [apps, erp, bulgaria, architecture, inventory-sync, order-sync]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-microbg]]. See the hub for the other aspects (registration, prerequisites, sync mechanics, partner matching, troubleshooting).

# MicroBG — architecture split (handshake vs sync)

## Purpose

The single most important thing to understand about MicroBG when triaging a support ticket: **the CloudCart-side app is only a registration handshake. The real sync runs on Micro.bg's side.** Getting this wrong is the most common cause of wasted ticket time — agents go hunting in CloudCart's admin for a setting that lives in Micro.bg's CloudCart Control Panel.

## Where to find it

The split is invisible to the merchant in the UI; it only becomes apparent when something doesn't work. The two halves live at:

- **CloudCart side** → Sidebar → **Apps** → **MicroBG** → Settings tab (`/admin/apps/microbg/settings`). Two tabs only: Overview + Settings.
- **Micro.bg side** → **Номенклатури → Стоки → Списък стоки → CloudCart контролен панел**. This is where the merchant runs every recurring sync action.

## What the merchant can do here

This aspect documents which actions are owned by which side. The merchant interacts with both UIs, but they do different jobs.

### CloudCart side owns

- Subscribing to the `microbg_subscription` paid add-on via CloudCart's checkout.
- The one-time registration handshake — sending personal + company data to Micro.bg's `Check` and `Create` endpoints.
- Holding the API key Micro.bg authenticates against (visible in [[settings-api-keys]]).
- Displaying the current Micro.bg subscription state (expiration date, Micro.bg order ID, Micro.bg subdomain).

### Micro.bg side owns

- **Проверка съответствие на стоките** — the product-code matching report.
- **Синхронизация (импорт) на ВСИЧКИ стоки от ЕЛМ към складовия софтуер** — bulk import of CloudCart products into Micro.bg.
- **Активиране на известията (WebHooks) в ЕЛМ** — webhook self-subscription against CloudCart's API.
- The every-3-minute scheduled quantity + price push back into CloudCart.
- The partner-matching cascade (EIK first, email second — see [[apps-microbg-partner-matching]]).
- The transformation rule that decides when a Поръчка becomes a Продажба (stock-writing decision — see [[apps-microbg-sync-mechanics]]).
- The choice of **Обект** / warehouse + the price-group mapping that feeds the storefront (see [[apps-microbg-prerequisites]]).

### What the merchant CANNOT do on the CloudCart side

- Force a manual quantity push from CloudCart to Micro.bg or back. There is no Sync Now button on the CloudCart side because no sync code runs here.
- Trigger product matching, rerun the bulk catalogue import, or activate webhooks. All of these live in Micro.bg's Control Panel.
- View per-SKU sync logs. CloudCart's audit trail records only inbound API + webhook activity; Micro.bg holds the source-of-truth event log.

## Settings & fields

The CloudCart-side app stores only what's needed for the handshake — there are no per-SKU mappings, no sync-cadence settings, no transformation rules on this side. The persistent settings on the CloudCart side are:

- `is_registered` — whether the registration handshake completed.
- `PaymentToDate` — Micro.bg subscription expiration date.
- `OrderId` — Micro.bg-side subscription order ID.
- `domain` — the merchant's Micro.bg subdomain.

Everything else — the transformation status, the Обект / warehouse choice, the sync-cadence checkbox, the payment-type mapping — lives on Micro.bg's side and isn't visible from CloudCart.

## Business rules

### Why the split exists

Micro.bg is the source of truth for stock + accounting. Once a CloudCart order becomes a Продажба on Micro.bg's side, Micro.bg owns the stock decrement and the accounting entry. Sync direction is "Micro.bg pulls products + pushes quantities into CloudCart" and "CloudCart pushes orders into Micro.bg". CloudCart's app surface is intentionally minimal because building a parallel sync engine on CloudCart's side would duplicate Micro.bg's logic and create race conditions.

### Practical consequence for support

A "sync isn't working" ticket should be triaged in this order:

1. Is the registration handshake intact? Check Apps → MicroBG → Settings shows a non-empty expiration date + API key. If not, the merchant never completed registration — send them to [[apps-microbg-registration]].
2. Is the merchant logged into Micro.bg's CloudCart Control Panel? If not, the per-3-min push isn't running on Micro.bg's side. (Deactivating CloudCart's API key would also break it — see [[apps-microbg-troubleshooting]].)
3. Did the merchant run the **Активиране на известията** action? If not, the order webhooks were never subscribed and Micro.bg is missing every new order — see [[apps-microbg-sync-mechanics]].
4. Was the **Проверка съответствие на стоките** action run after the last catalogue change? Stale matching is the most common cause of "stock count differs" complaints.

### The API key is the bridge

The single dependency between the two sides is the CloudCart API key Micro.bg uses to authenticate. If the merchant rotates / deletes the API key from [[settings-api-keys]], every Micro.bg-side action stops working until the new key is pasted into Micro.bg's CloudCart Control Panel. The CloudCart-side app has no key-rotation flow specific to Micro.bg — the merchant must re-paste manually. `(verify)` the exact behaviour on key rotation.

## Related

- [[apps-microbg]] — hub.
- [[settings-api-keys]] — the API key Micro.bg uses to authenticate.
- [[json-api-v2]] — the API surface Micro.bg reaches CloudCart through.
- [[settings-hooks]] — the webhook surface Micro.bg subscribes against.

## How it works (verified against backend)

The CloudCart-side app surface is small on purpose:

- The integration's app key is **`microbg`**; the registration controller is mounted at `/admin/api/microbg/{info,settings}`.
- There are no queue mappings, no scheduled jobs, and no event subscribers on CloudCart's side — the app does not push anything to Micro.bg outside the handshake.
- The Guzzle wrapper around Micro.bg's `Check` + `Create` endpoints uses base URL `https://micro.bg/ExtApps/CloudCart/Company/` with `X-CloudCart-Key` + `X-CloudCart-Action: Check|Create` headers.

So the CloudCart-side app does ONE thing well: handshake. Everything sync-related happens on the Micro.bg side, reaching CloudCart via the standard [[json-api-v2|JSON-API v2]] + [[settings-hooks|webhook]] surfaces. The handshake API mechanics + error-response shape are documented on [[apps-microbg-registration]] and [[apps-microbg-troubleshooting]].

### UI structure — non-standard for an ERP integration

MicroBG is **NOT** built on the shared ErpMain wrapper used by the other Bulgarian / Hungarian / Romanian ERP integrations. The MicroBG screen has only **two tabs**:

1. **Overview** (`apps.microbg.overview`) — install card.
2. **Settings** (`apps.microbg.settings`) — the registration form documented on [[apps-microbg-registration]].

There is **no Status tab** (no recurring sync to monitor from CloudCart), **no Category mapping tab** (Micro.bg ingests CloudCart-side data verbatim), and **no Processed Products tab**. The absence of these tabs is itself a clue: any setting that would normally live there is owned by Micro.bg's CloudCart Control Panel instead.

## Open questions

- The exact behaviour when the API key is rotated mid-flight — does Micro.bg surface a clear error or silently fail until the next manual reconnect? `(verify)`
