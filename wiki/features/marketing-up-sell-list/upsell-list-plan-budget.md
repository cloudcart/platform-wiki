---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → UpSell List → Plan budget & permissions"
route_name: admin.common.remaining
route_path: /admin/common/remaining/{feature}
aliases: ["UpSell plan budget", "UpSell remaining slots", "UpSell plan cap", "upsells feature", "UpSell app gate", "Лимит на UpSell оферти"]
tags: [marketing, upsell, plan-gates, permissions, limits]
plan_gates: ["upsells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-up-sell-list]]. See the hub for the other aspects (table, actions, validation, storefront firing).

# UpSell List — plan budget & permissions

## Purpose

This aspect documents the two access gates on the UpSell feature: the **`upsells` plan-feature counter** (how many offers the merchant's plan allows) and the **`cc_apps_purchase:up_cross_sell` app middleware** (the Up/Cross-Sell app must be installed at all). Together they decide whether the merchant can reach the screen and whether the **Add UpSell** button can create another record.

## Where to find it

The remaining-slots counter is shown on the **Add UpSell** button in the UpSell List header (`/admin/marketing-new/up-sell`), fed by an AJAX call to `admin.common.remaining/upsell`. The app gate runs as middleware on every UpSell admin route.

## What the merchant can do here

The merchant reads the **(N remaining)** counter to know how many more offers the current plan allows, and — if at the cap — upgrades the plan or buys a feature pack via [[plan-features]] / [[plan-vs-feature-pack]] to raise it.

## Settings & fields

There are no editable fields here — the slot budget is a function of the merchant's [[plans|plan tier]] and any feature packs applied. The counter is read-only.

## Business rules

### "Remaining slots" counter — plan-based budget

The Add button's *"(N remaining)"* label is fed by `admin.common.remaining/upsell`. The platform tracks total UpSell records against the merchant's plan-tier limit. When the merchant hits the cap, the counter is 0; the Add button still works, but creating a new record **fails server-side**.

### Each offer counts once

Each UpSell offer counts against the cap. (Legacy multi-step chains counted every descendant record too, so a deep chain consumed the budget faster than its single list row suggested — this only affects offers built under the retired chain builder.) Out-of-stock offers still count (see [[upsell-list-storefront-firing]]).

### `upsells` is a separate counter from `cross_sells`

The numeric `upsells` plan-feature is independent of Cross-Sell's `cross_sells` counter — UpSell and Cross-Sell offers draw from separate budgets (see [[marketing-cross-sell]]). The `upsells` mapping is also listed in `restrict.creating`; when over the cap the merchant is redirected to the per-feature upsell at [[plan-features]]. The numeric cap extends via packs ([[plan-vs-feature-pack]]).

### Permission — the Up/Cross-Sell app gate

All routes in the UpSell list / create / edit / delete flow are gated by the middleware `cc_apps_purchase:up_cross_sell`. This is a **separate, non-plan gate** from the `upsells` counter: without the Up/Cross-Sell app installed, the merchant is bounced to the install gateway at `apps.up_cross_sell` (see [[apps-up-cross-sell]]) before the plan cap is ever evaluated.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `upsells` | Numeric | Per-plan cap on the number of UpSell offers (counted against the platform code). Also listed in `restrict.creating` — when the cap is hit, the **+ Add UpSell** button's "(N remaining)" counter reaches 0 and create attempts fail server-side. Each offer counts against the cap (legacy chains also counted descendants). Extendable via feature pack. Cross-Sell offers count against the **separate** `cross_sells` counter (see [[marketing-cross-sell]]). |

The whole [[apps-up-cross-sell]] gateway app must also be installed — the middleware `cc_apps_purchase:up_cross_sell` is a separate non-plan gate that bounces uninstalled merchants to the install gateway.

## Related

- [[marketing-up-sell-list]] — hub.
- [[plans]] — plan tier that sets the slot budget.
- [[plan-gates]] — how plan-feature gating works platform-wide.
- [[plan-features]] — per-feature upsell shown when over the cap.
- [[plan-vs-feature-pack]] — extending the numeric cap via packs.
- [[apps-up-cross-sell]] — the gateway app whose middleware gates all UpSell routes.
- [[marketing-cross-sell]] — Cross-Sell, which uses the separate `cross_sells` counter.

## Open questions

No outstanding questions.
