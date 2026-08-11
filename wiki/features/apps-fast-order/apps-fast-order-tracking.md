---
type: feature
nav_path: "Apps → Fast Order → Tracking, meta flag & countdown"
route_name: apps.fast_order.overview
route_path: /admin/apps/fast_order
aliases: ["Fast Order Pixel events", "Fast Order meta flag", "Fast Order filter", "Fast Order countdown discount"]
tags: [apps, others, conversion, checkout, conversion-rate]
plan_gates: ["checkout"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[apps-fast-order]]. See the hub for the other aspects (popup form + cart lifecycle, COD payment + customer + address).

# Fast Order — tracking, meta flag & countdown

## Purpose

This aspect covers how a Fast Order is **tracked and tagged** after creation: which Facebook Pixel events fire (configurable), the `fast_order` meta flag that powers the orders-list filter, and the deliberate exclusion of countdown discounts from Fast Order carts. The popup form is on [[apps-fast-order-popup-flow]]; the COD payment path is on [[apps-fast-order-payment-cod]].

## Where to find it

The Facebook Pixel event selectors are on [[apps-fast-order-settings]]. The resulting **Fast order** filter lives on the [[orders]] list.

## What the merchant can do here

- Choose which Facebook Pixel start / complete events fire for Fast Order.
- Filter the orders list to Fast Order vs regular-checkout orders.

## Settings & fields

Facebook Pixel event selectors (on [[apps-fast-order-settings]]):
- **Start event** — `InitiateCheckout` (default) or `InitiateFastCheckout`.
- **Complete event** — `Purchase` (default) or `FastPurchase`.

## Business rules

### Facebook Pixel event configuration

The merchant can configure WHICH Facebook Pixel event names fire when Fast Order is used (start = `InitiateCheckout` / `InitiateFastCheckout`; complete = `Purchase` / `FastPurchase`). This lets the merchant separate Fast Order conversions from regular checkout in their Pixel analytics if they wish — for example, keeping `Purchase` for full-checkout conversions and switching Fast Order to `FastPurchase` so the two funnels can be reported separately.

### Order flagged in meta for filtering

Every Fast Order gets `fast_order = true` set in its order meta. This is what powers the **Fast order** filter on the orders list (see [[orders]]). Merchants can filter Yes / No to isolate orders that came through this flow versus the full checkout. Combined with the Pixel split above, this gives the merchant both an analytics-side and an admin-side way to measure how much volume Fast Order drives.

### Countdown discounts are explicitly DISABLED for Fast Order

Fast Order carts disable countdown discounts before creating the order — countdown-timer discounts (the [[marketing-discounts-countdown]] type) do NOT apply to Fast Order purchases. The countdown popup does not fire, the timer is not started, and the per-cart countdown meta is not written. This is intentional: countdown discounts incentivize fast purchases, but Fast Order itself is the "fast" path, so doubling up was deemed redundant.

The practical consequence: a customer who'd get a countdown discount in regular checkout LOSES that discount when using Fast Order. The merchant should be aware — a Countdown urgency promotion cannot be combined with the Fast Order one-click buy flow.

## Related

- [[apps-fast-order]] — hub.
- [[apps-fast-order-settings]] — where the Pixel event selectors are configured.
- [[orders]] — the **Fast order** Yes / No filter driven by the `fast_order` meta flag.
- [[marketing-discounts-countdown]] — the countdown discount type that Fast Order disables.

## Open questions

None.
