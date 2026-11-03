---
type: feature
nav_path: "Apps → MicroBG → Prerequisites"
route_name: apps.microbg.overview
route_path: /admin/apps/microbg/overview
aliases: ["MicroBG prerequisites", "MicroBG required settings", "MicroBG service products", "MicroBG Обект", "MicroBG warehouse choice", "MicroBG payment-type mapping", "MicroBG BGN VAT BG"]
tags: [apps, erp, bulgaria, prerequisites, settings-cart, currency, vat]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-microbg]]. See the hub for the other aspects (architecture split, registration, sync mechanics, partner matching, troubleshooting).

# MicroBG — prerequisites + required settings before sync

## Purpose

A merchant who installs MicroBG and runs the handshake successfully can still end up with broken sync — orders that don't post, partners that collapse together, stock that drifts — because the prerequisites on **both sides** weren't met. This aspect catalogues every setting that must be in place before the first order or stock update flows.

## Where to find it

The prerequisites split into three groups by location:

- **CloudCart admin** → [[settings-cart]] (the EIK field + the stock-decrement-status setting + cart-level fee / discount definitions).
- **CloudCart admin** → Sidebar → **Settings → Payments** — every active payment method must have a matching type on Micro.bg.
- **Micro.bg admin** → **Номенклатури → Стоки → Списък стоки** — the merchant must pre-create "service products" so cart-level adjustments have something to attach to.
- **Micro.bg admin** → **За фирмата → Типове плащания** — the matching payment-type catalogue.

## What the merchant can do here

This aspect is a configuration checklist — there's no single UI action. The merchant works through the list once at install time, then re-checks whenever they add a new payment method or change cart-level fees.

### What the merchant CANNOT do here

- Run MicroBG sync in currencies **other than BGN** or with VAT rules not set to country **Bulgaria**. Micro.bg's data model expects BGN amounts and the standard BG VAT rate. Stores configured for other countries shouldn't enable the app.
- Skip the **2-user Micro.bg license** requirement. Single-user Micro.bg plans don't enable the API connection.
- Use the integration on a CloudCart plan below STARTUP. The `microbg_subscription` feature pack isn't available on the bottom tier.

## Settings & fields

### Required CloudCart-side settings BEFORE running sync

These settings decide whether sync will be lossless:

- **[[settings-cart]] → "Bulstat/EIK or EGN" = Опционално** (NOT Required, NOT Hidden). If this is **Required**, customers who don't have a Bulgarian EIK can't checkout; if it's **Hidden**, EIK never reaches the order so Micro.bg's partner-match-by-EIK fails (see [[apps-microbg-partner-matching]]). **Опционално** is the only configuration that supports both B2B and B2C buyers cleanly.
- **[[settings-cart]] → "Намали количество ако статусът на поръчката е"** — should be set so the moment Micro.bg considers the order "transformed into a sale" (configured on Micro.bg's side) matches the same status on the CloudCart side. Options on CloudCart: `Платена/Изпратена` or `Изчакваща/Изпратена`. Picking different statuses on the two sides produces stock-drift. See [[inventory-decrement-timing]] for the CloudCart-side timing model.
- **Payment methods** — every payment method active in CloudCart's checkout **must** have a matching `Тип на плащане` in Micro.bg (**За фирмата → Типове плащания → Нов тип плащане**). When the merchant adds a new payment method later, they must add the matching type to Micro.bg too.

### Required Micro.bg-side "service products" BEFORE running sync

Cart-level adjustments in CloudCart orders need to be carried into Micro.bg as separate line items, and Micro.bg requires a real stock item to back each one. The merchant must pre-create these as **type = услуга** ("service") in **Номенклатури → Стоки → Списък стоки**:

| What CloudCart sends | Required Micro.bg service product (example name) |
|---|---|
| **Shipping line** (the courier price added at checkout) | "Доставка" or "Куриерска услуга" |
| **Cart-level discount** (e.g. "5 лв off the whole order") | "Търговска отстъпка" or "Отстъпка" |
| **Cart-level fee** (e.g. "Обслужваща такса") | "Такса" |

Without these, Micro.bg can't post the order — the line items would have nothing to attach to. The names are merchant-pickable; what matters is having one service product per category.

### Object / price-group mapping

Micro.bg has the concept of **Обекти** (locations / warehouses). The merchant picks which Обект (or *Всички*) feeds CloudCart inside Micro.bg's CloudCart Control Panel:

- **"Всички"** → Micro.bg pushes prices from the **"Цени на дребно"** price group.
- **Specific Обект** → Micro.bg pushes prices from that Обект's configured price group, and stock quantities from that Обект's inventory.

If the merchant has multiple warehouses and wants only one to feed the e-shop, they pick that warehouse here. Switching the chosen Обект later changes which warehouse's stock and prices flow into the storefront.

## Business rules

### Prerequisites the merchant must satisfy

These are **enforced by Micro.bg**, not by CloudCart — the merchant who clicks Save without them will see Micro.bg's error message bubble up as HTTP 503 (see [[apps-microbg-troubleshooting]] for the error decoding).

| Requirement | Why |
|---|---|
| **Micro.bg license for at least 2 users** | Single-user Micro.bg plans don't enable the API connection. |
| **CloudCart plan above STARTUP** | The bottom-tier plan doesn't include the `microbg_subscription` feature pack. |
| **Storefront currency = BGN** | Micro.bg's data model is BGN-based; mixed-currency carts won't round-trip cleanly. |
| **VAT rules set for country Bulgaria** | Micro.bg expects the standard BG VAT rate. |

### Why the EIK setting matters specifically

Hiding the EIK field in CloudCart's checkout (via [[settings-cart]] → "Bulstat/EIK or EGN" = Hidden) breaks the EIK match and forces email-based dedup, which collapses every B2B order from the same buyer into one anonymous partner without their EIK. See [[apps-microbg-partner-matching]] for the cascade and why this matters for accounting.

### Why payment-type alignment matters

Micro.bg refuses to post the order when the payment method on the CloudCart order doesn't exist on the Micro.bg side. Each time the merchant adds a new gateway, they must mirror the change on Micro.bg. Symptom: orders not appearing in Micro.bg — see [[apps-microbg-troubleshooting]].

### Why service products must be pre-created

CloudCart's order model expresses shipping, discounts, and fees as cart-level adjustments. Micro.bg's data model treats those as line items against real stock entries. Mismatches produce silent partial sync (product lines come through, shipping / discount / fee lines disappear).

## Related

- [[apps-microbg]] — hub.
- [[settings-cart]] — EIK field config, decrement-status setting, cart-level fees + discounts.
- [[settings-general]] — store currency, default VAT country.
- [[settings-invoicing]] — VAT rules.
- [[inventory-decrement-timing]] — the CloudCart-side decrement-timing model that must align with Micro.bg's transformation rule.
- [[settings-payment-providers]] — the CloudCart payment-method catalogue that must mirror Micro.bg's `Типове плащания`.

## How it works (verified against backend)

The prerequisites are merchant-configurable settings; CloudCart does not refuse to install MicroBG when they're wrong. The integration fails silently or with HTTP 503 errors from Micro.bg's side, not at install time. This means: a fresh installation in a non-BG or non-BGN store will look healthy on CloudCart's Apps screen but will fail on the first order push. Support should always confirm the checklist when the merchant reports "we installed it and nothing's happening".

## Open questions

- Whether Micro.bg has tightened its validation on `Check` to refuse non-BG VAT rules at registration time, or whether it still accepts the registration and only fails downstream. `(verify)`
