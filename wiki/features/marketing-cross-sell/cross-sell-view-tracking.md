---
type: feature
nav_path: "Marketing → Cross-Sell & UpSell → View tracking & randomisation"
route_name: admin.cross_sell.list
route_path: /admin/marketing-new/cross-sell
aliases: ["Cross-Sell view cap", "Cross-Sell view cookie", "cross_sell_view cookie", "cross_sell_cancel cookie", "Cross-Sell randomisation", "Cross-Sell view counter", "Cross-Sell on delete cleanup"]
tags: [marketing, cross-sell, cookies, view-cap, randomisation, metrics]
plan_gates: ["cross_sells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-cross-sell]]. See the hub for the other aspects (offer form, trigger events, display modes & discounts, filters & limits, engine comparison).

# Cross-Sell — view tracking & randomisation

## Purpose

This page documents the **runtime mechanics** of how offers are surfaced to a customer over repeat visits: how the per-customer view cap is actually enforced, how dismissals are remembered, how products and competing offers are ordered, when the list-row view counter increments, and what happens to live carts when an offer is deleted. These are the behaviours a merchant needs when an offer "shows too often", "shows different products each time", or "the numbers look off".

## Where to find it

These behaviours are not a screen — they run on the storefront when an offer fires, and surface back on the offer's list row (the metrics) at Sidebar → Marketing → **Cross-Sell & UpSell**. See [[marketing-cross-sell-list]] for the metrics columns.

## What the merchant can do here

The merchant configures the inputs (the `max_user_views` cap on [[cross-sell-filters-limits]], the `products_limit`), then **reads the resulting metrics** on the list row: Sales generated / Total sales / Added to cart / Total cancel / Success rate / Views. The runtime rules below explain how those numbers are produced.

## Settings & fields

| Mechanism | Storage | Lifetime |
|---|---|---|
| Per-offer view count | `cross_sell_view` cookie (offer UUID + count pairs) | session lifetime — currently **7 days** / 10 080 min |
| Per-offer dismissal | `cross_sell_cancel` cookie | session lifetime |
| List-row Views metric | `views` counter on the offer record | persistent |

## Business rules

### The view cap is enforced by COOKIE, not customer login

The "Max user views" cap is enforced via a **browser cookie**, NOT against the customer's account or order history. The platform writes a `cross_sell_view` cookie containing each offer's UUID + view-count pairs. On every popup-eligible action, the storefront reads that cookie and filters out offers whose recorded view-count has already reached `max_user_views`. Implications:

- The cap is **per browser**, not per customer — the same customer on phone + laptop counts as two separate visitors.
- Clearing cookies or switching browsers resets the count.
- The cookie lifetime equals the session lifetime (currently **7 days** / 10 080 minutes). After that the count resets.
- A `max_user_views = 0` (unlimited — see [[cross-sell-filters-limits]]) means the cookie never filters the offer out.

### Dismissals are remembered separately

A second cookie (`cross_sell_cancel`) tracks dismissals — once a customer clicks "Close" on an offer, that exact offer is filtered out for them for the cookie's lifetime **regardless** of the view cap.

### Products inside the popup are randomised on every render

Each time the offer fires, the products surfaced inside the popup are pulled in **random order** (`orderBy('products.id', mt_rand(0, 1) ? 'asc' : 'desc')`), capped at `products_limit`. A customer who sees the popup twice may see a different selection (within the offer's action conditions) — there is **no stable "most relevant first" ranking** on the public popup.

### Competing offers are also picked at random

When multiple offers match the same event for the same customer, the platform picks which one to show in **random order** (`inRandomOrder`), not by priority or recency. The merchant has **no priority field** to influence which offer wins when several apply.

### The view counter increments per popup-render, not per impression

The `views` counter on the list row increments inside the storefront controller every time the popup is **actually rendered** (offer matched, products loaded, modal returned). If the offer matches but the product filter returns **0 products** (e.g. everything filtered out by hide-cart-products / hide-out-of-stock), the `views` counter does **NOT** increment. So a low Views number can mean "matched but filtered to empty", not "never triggered".

### On delete, live carts are cleaned up

When a Cross-Sell offer is deleted, the platform NULLs out the `cross_sell_id` column on any active cart items tied to that offer — so historical attribution stays consistent but the deleted offer doesn't keep affecting carts. This runs in a `deleting` hook on the offer record.

## Related

- [[marketing-cross-sell]] — hub.
- [[cross-sell-filters-limits]] — the `max_user_views` cap + `products_limit` this page enforces; `0` = unlimited.
- [[cross-sell-offer-form]] — where the cap and limit are configured.
- [[marketing-cross-sell-list]] — the list-row metrics produced by these mechanics.
- [[cart-vs-order-lifecycle]] — cart-item lifecycle the on-delete cleanup touches.

## Open questions

No outstanding questions.
