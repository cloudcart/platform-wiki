---
type: feature
nav_path: "Marketing → Cross-Sell & UpSell → Engine comparison & gates"
route_name: admin.cross_sell.list
route_path: /admin/marketing-new/cross-sell
aliases: ["Cross-Sell vs Cart Rules", "Cross-Sell engine model", "Cross-Sell plan gate", "cross_sells plan gate", "Cross-Sell gateway app", "up_cross_sell middleware"]
tags: [marketing, cross-sell, cart-rules, plan-gates, engine]
plan_gates: ["cross_sells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-cross-sell]]. See the hub for the other aspects (offer form, trigger events, display modes & discounts, filters & limits, view tracking).

# Cross-Sell — engine comparison & gates

## Purpose

Cross-Sell is structurally close to [[apps-cart-rules]] but serves a different purpose, and it is fenced behind a multi-part gate (plan-feature + gateway app + middleware). This page explains **how the engine compares** to the cart-rule engine and **what must be in place** for the merchant to use it — the conceptual framing the Assistant needs when a merchant asks "why can't I create more offers?" or "what's the difference from Cart Rules?".

## Where to find it

The gating surfaces in two places: the [[apps-up-cross-sell]] gateway app (must be installed) and the plan-limit error on the list at Sidebar → Marketing → **Cross-Sell & UpSell** when the offer cap is hit. The install gateway at `/admin/apps/up_cross_sell` opens the Vue manager at `/admin/marketing-new/cross-sell`.

## What the merchant can do here

Understand the constraints before building offers:
- Confirm the **gateway app is installed** (the `cc_apps_purchase:up_cross_sell` middleware blocks the page otherwise).
- Confirm the **plan allows enough offers** (the `cross_sells` numeric cap).
- Understand that Cross-Sell and [[apps-cart-rules]] are **separate engines** with different jobs — don't expect one to do the other's work.

## Settings & fields

| Gate | Type | Effect when not satisfied |
|---|---|---|
| `up_cross_sell` app | Gateway app (middleware `cc_apps_purchase:up_cross_sell`) | The Cross-Sell pages are blocked entirely until the app is installed. |
| `cross_sells` | Numeric plan-feature (counts the platform code) | New offer creates blocked by the standard plan-limit error (`restrict.creating`); merchant redirected to [[plan-features]]. |

## Business rules

### Same trigger-action structure as Cart Rules — different payload

The engine mirrors [[apps-cart-rules]]:
- a **Trigger** (target) condition list — when to fire (see [[cross-sell-trigger-events]]);
- an **Action** (offered products) condition list — what to surface (see [[cross-sell-display-discounts]]).

Both use the same group-of-conditions UI (AND within a group, OR across groups). But where Cart Rules fires **discounts**, Cross-Sell fires **product recommendations** (optionally carrying a discount). A merchant who wants "buy 2 get 10% off the cart" wants Cart Rules; a merchant who wants "you added a phone, here's a case" wants Cross-Sell.

### Separate counters from UpSell

Cross-Sell offers count against the `cross_sells` numeric cap; UpSell offers count against a **separate** `upsells` counter (see [[marketing-up-sell-list]]). Both extend via feature packs ([[plan-vs-feature-pack]]). The two engines use the same style of offer editor (see [[marketing-up-sell-diagram]]) but are independent — separate offers, separate budgets.

### Two-part gate

Both gates must pass: the gateway **app** (a non-plan `cc_apps_purchase` middleware gate) AND the **plan-feature** cap. Installing the app does not raise the `cross_sells` cap, and a generous plan does not bypass the app requirement.

### Admin-only, no public API

The module is a Vue admin app with **no JSON-API access** — offers are admin-only (managed in `/admin/marketing-new/cross-sell`, not via the storefront API).

## Related

- [[marketing-cross-sell]] — hub.
- [[apps-cart-rules]] — the sister conditional rule engine (discounts vs recommendations).
- [[cross-sell-trigger-events]] — the Trigger half of the structure.
- [[cross-sell-display-discounts]] — the Action half + the optional discount.
- [[apps-up-cross-sell]] — the gateway app + `cc_apps_purchase:up_cross_sell` middleware.
- [[marketing-up-sell-list]] — the separate `upsells` counter.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — the plan-feature machinery.

## Open questions

No outstanding questions.
