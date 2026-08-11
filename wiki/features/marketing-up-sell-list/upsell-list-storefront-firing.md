---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → UpSell List → Storefront firing"
route_name: admin.up_sell.list
route_path: /admin/marketing-new/up-sell
aliases: ["UpSell popup firing", "UpSell in-stock gate", "UpSell already-in-cart filter", "UpSell view counter", "UpSell counters", "Кога се показва UpSell popup"]
tags: [marketing, upsell, storefront, counters, popup]
plan_gates: ["upsells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-up-sell-list]]. See the hub for the other aspects (table, actions, validation, plan budget).

# UpSell List — storefront firing & counters

## Purpose

This aspect explains **when an UpSell popup actually shows to a customer** and how the three lifetime counters (`views`, `added_to_cart`, `total_cancel`) are maintained. A merchant who has saved an active, in-window offer but never sees it firing usually trips one of the two storefront gates documented here.

## Where to find it

These behaviours run on the **storefront**, not the admin. The merchant observes the results in the metric columns of the UpSell List (`/admin/marketing-new/up-sell`) — Views, Added to cart, Total cancel, In stock — see [[upsell-list-table]].

## What the merchant can do here

The merchant cannot directly control firing beyond keeping the offer active and the offer variant in stock — the gates below are automatic. The counters are read-only from the admin; the merchant cannot manually reset them.

## Settings & fields

There are no merchant-editable settings on the firing path. The relevant inputs are the offer's Active state and date window (see [[upsell-list-validation]]) and the offer variant's stock + `continue_selling` flag.

## Business rules

### The popup only fires when the offer variant is in stock OR the product is in continue-selling mode

The storefront's UpSell proposal query chains an `inStockOfferCheck` — the popup fires only if the offer variant has remaining inventory OR the product is configured to keep selling at 0 stock. So an UpSell with an exhausted offer variant is **invisible** to customers until restocked, but still counts towards the merchant's plan budget (see [[upsell-list-plan-budget]]). The list's **In stock** column reflects this same check at view time (see [[upsell-list-table]]).

### The popup is also blocked when the offer variant is already in the cart

The storefront filters out UpSell offers whose `offer_variant_id` is already present in the customer's current cart (`whereNotIn('offer_variant_id', $cartInstance->items->pluck('variant_id'))`). There is no point offering "upgrade to X" if X is already in the cart.

### The view counter increments on EVERY render, including same-customer repeats

The view counter has **no cookie dedupe** — every time the popup is shown to anyone (including the same customer hitting the trigger product twice), `views` goes up by 1. Compare with Cross-Sell, where `max_user_views` enforces a per-browser cap via cookies (see [[marketing-cross-sell]]); UpSell has **no** equivalent cap field, so the same customer keeps seeing the popup on every qualifying add-to-cart action until they dismiss it. Dismissing still increments `total_cancel` but does not block future popups on later visits.

### Lifetime counters update outside the admin

The three counters are updated by the storefront, so the merchant cannot manually reset them:

- The `site.upSell.proposal` route increments **`views`** when the popup is served.
- A cart-add of the offered variant increments **`added_to_cart`**.
- The `site.up_sell.discard` route increments **`total_cancel`** when the popup is dismissed.

The **success rate** shown in the list is derived from `total_orders` (the paid-order attribution count) divided by `added_to_cart` — see [[upsell-list-table]].

## Related

- [[marketing-up-sell-list]] — hub.
- [[upsell-list-table]] — the columns these counters and the in-stock gate feed.
- [[upsell-list-validation]] — the Active state and date window that also gate firing.
- [[upsell-list-plan-budget]] — out-of-stock offers still count against the plan cap.
- [[marketing-cross-sell]] — Cross-Sell, which has a per-browser view cap UpSell lacks.
- [[apps-up-cross-sell]] — the storefront flow that serves the popup.

## Open questions

No outstanding questions.
