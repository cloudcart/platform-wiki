---
type: feature
nav_path: "Plan → Feature → Pack list (Vue)"
route_name: plan-feature-packs
route_path: /admin/plan/feature/:id
aliases: ["Plan feature pack list", "Feature pack table (Vue)", "Buy feature pack table", "+100 products pack row", "Dynamic-pricing pack step", "Списък пакети за функция"]
tags: [plans, plan-feature, feature-pack, pack-list, vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-feature]]. See the hub for the other aspects (buy → checkout flow, plan restrictions, pack lifecycle).

# Plan feature — pack list (Vue)

## Purpose

The **pack list** is the table that fills the body of the modern Vue *Plan feature* screen. It lists every pack the merchant can buy to extend the **one** feature they landed on (e.g. *+100 products*, *+500 products*, *+1000 products*, or dynamic-priced steps like *1000 products / 2000 products / ...*). Each row is a self-contained offer: a pack name, a per-cycle price, and a **Buy** button. There is no quantity spinner — quantities are baked into each row.

## Where to find it

- Rendered inside the **plan-feature-packs** Vue screen at `/admin/plan/feature/{id}`, where `{id}` is the feature mapping (e.g. `products`, `customers`, `storage`, `discount-code-pro`, `support_meetings`).
- The screen renders either as a full Vue page (URL reached directly) or as a `b-modal` side panel when opened from a card in [[plan-features]] — the body content is identical, only the chrome differs.
- The pack table is shown only when packs exist AND the feature isn't blocked by a plan restriction (see [[plan-feature-detail-restrictions]] for the banner / empty states that replace it).

## What the merchant can do here

### See the screen header

The screen opens with a fixed header — a calendar-star icon (`fa-light fa-calendar-star`) and the static title *Plan feature* (NOT the per-feature name). The screen does **not** render a per-feature usage bar or *used / total* counter of its own — that context lives on the calling card in [[plan-features]]. Internally the feature's current value is computed (numeric value + suffix, *Disabled* for boolean/storage, percent for fee casts) but it is only used to label suffixes, not shown as a progress bar here.

### Browse the pack list

A table below the header lists every pack available for this feature:

| Column | What it shows |
|--------|---------------|
| **Name** | Pack name (e.g. *+100 products*; for dynamic-pricing features includes the quantity, e.g. *2000 products*) |
| **Price** | Per-cycle price without VAT (e.g. *10.00 EUR / month*, *50.00 EUR / year*) |
| **Buy** | Action button — opens the checkout side panel with the selected pack (see [[plan-feature-detail-buy-flow]]) |

Below the table: *"The quoted prices are exclusive of VAT"*.

### Pick one pack and buy it

The merchant clicks **Buy** on a single row to start checkout for that pack. See [[plan-feature-detail-buy-flow]] for what the button triggers.

## Settings & fields

This is a browse / buy screen — no editable fields. The merchant sees per pack row:

| Field shown | What it represents |
|-------------|--------------------|
| **Pack name** | Localised pack name (`pack.name_translated` or `pack.name`) |
| **Pack price** | Per-cycle price excluding VAT (`pack.price_without_vat_formatted`) |
| **Buy button** | Triggers the checkout panel with the chosen pack pre-loaded |

### Fixed-price pack examples

- *+100 products*
- *+500 products*
- *+1000 products*

### Dynamic-pricing pack examples

For features with `dynamic_pricing = 1`, the pack name on each row includes the quantity:

- *500 products*
- *1000 products*
- *2000 products*

The merchant sees discrete steps along a server-generated ladder — **not** a free-form slider. The price for each step is computed server-side with the volume-discount curve documented in [[plan-feature-detail-restrictions]].

## Business rules

### Pack list filtered by `dynamic_pricing` match

The backend returns only the packs whose `dynamic_pricing` flag matches the feature's `dynamic_pricing` flag. A fixed-price feature shows only fixed packs; a dynamic-pricing feature shows only dynamic-pricing packs. **The two pack types never mix on the same screen.**

### One pack at a time

Quantities are baked into each row, and the cart is reset on each *Buy* click. The merchant cannot combine multiple packs in one checkout, nor set a custom quantity outside the dynamic-pricing ladder — they pick ONE step. To get *2× +100 products* they would buy *+200 products* (if such a pack exists) or repeat the flow.

### Mapping is the route key

The URL pattern `/admin/plan/feature/{id}` accepts the feature mapping verbatim — `products`, `customers`, `storage`, `discount-code-pro`, `support_meetings`, `custom_hostname`, etc. If the feature isn't found by mapping, the backend returns 404 and the Vue screen routes the merchant to the `error404` page. Some mappings are aliased internally before the post-purchase app-activation step — see [[plan-feature-detail-pack-lifecycle]].

### Boolean features render *Active* / *Disabled*

For boolean features (e.g. `discount-code-pro`, `support_meetings`, `authorize_payment`), the state reads *Disabled* until an active pack subscription exists, then flips to *Active*. There's no separate enable switch — the state is computed live from active-subscription presence.

## Related

- [[plan-feature]] — hub.
- [[plan-feature-detail-buy-flow]] — what the *Buy* button does (checkout side panel + post-purchase quota refresh).
- [[plan-feature-detail-restrictions]] — the banner / empty-packs states that replace the table; the `max_value` cap + dynamic-pricing formula.
- [[plan-features]] — the cards screen (one card per feature) that opens this panel.
- [[plans-purchase]] — the checkout flow the *Buy* button hands off to.

## Open questions

None.
