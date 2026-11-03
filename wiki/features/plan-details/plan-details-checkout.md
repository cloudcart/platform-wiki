---
type: feature
nav_path: "Plan → {Plan name} → Proceed to checkout"
route_name: plan-details
route_path: /admin/plans/:id
aliases: ["Plan details checkout", "Proceed to checkout plan", "Plan purchase cart", "Buy plan add-ons", "Plan checkout panel", "Покупка на план", "Към плащане план"]
tags: [plans, plan-details, plan-purchase, checkout, subscription]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Plan details — proceed to checkout

## Purpose

> Part of [[plan-details]]. See the hub for the other aspects (billing cycle, recommendations, access & variants).

This aspect covers the **purchase action** on the [[plan-details]] screen: the *Proceed to checkout* button, how the current selection becomes a cart, the checkout side-panel where payment is confirmed, and what happens after a successful purchase. It's the step that turns the merchant's choices (billing cycle + any ticked add-ons) into a real charge and live subscriptions.

## Where to find it

The *Proceed to checkout* button is the last `b-card` on the [[plan-details]] screen, below the billing-cycle picker ([[plan-details-billing-cycle]]) and the recommendation blocks ([[plan-details-recommendations]]). It opens the standard CloudCart Checkout panel as an inline side-modal over the same screen.

## What the merchant can do here

### Proceed to checkout

The **Proceed to checkout** button posts the current selection to the bulk-cart endpoint and opens the standard checkout side panel. From there the merchant confirms payment with their saved card (see [[billing-cards]]) and reviews invoice details (see [[billing-invoicing]]). After success, the merchant is redirected to the dashboard with a short delay.

### Confirm payment in the checkout panel

Opening *Proceed to checkout* opens the standard Checkout panel as a side modal — the same one used by [[plans-purchase]] (Order overview + Invoice details + Payments + Discount + Totals + Pay-now). The records passed in are the chosen plan variant plus any ticked services and apps. Promo / discount codes (which this screen has no field for) can be entered on this checkout step.

## What the merchant cannot do here

- **Re-open checkout while it's already open** — the button is disabled while the Checkout panel is open.
- **Submit an empty plan slot** — one billing variant is always selected, so the cart always has a plan entry.
- **Create subscriptions just by submitting the form** — nothing is charged until payment is confirmed in the checkout panel (see *Subscriptions created at confirm time* below).
- **Keep other seeded cart items** — the bulk-cart endpoint clears any existing cart first, so items seeded by other flows are wiped.

## Settings & fields

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **Proceed to checkout** button | Submits the selection → builds the cart → opens the checkout panel | Disabled while the checkout panel is open | Right-aligned primary button |
| **Checkout panel** (inline) | Standard checkout: order overview, invoice details, payment, discount, totals, pay-now | — | Same panel as [[plans-purchase]]; accepts promo codes |

## Business rules

### Cart shape = one plan + N services + N apps

The submitted cart contains:

- One plan entry for the chosen billing-cycle variant.
- Zero or more recommended-service entries (one per ticked service).
- Zero or more recommended-app entries (one per ticked app).

When the merchant changes the billing-cycle radio or ticks an add-on, the local selection is updated; on *Proceed to checkout* the non-empty entries are collected and posted as a single list to the bulk-cart endpoint. The endpoint **clears any existing cart first**, then re-seeds it with this list — so items seeded by other flows are wiped and there's no risk of double-buying.

### Subscriptions created at confirm time, not here

Submitting this form does NOT create subscriptions — it only seeds the cart and opens the checkout. Subscriptions are only persisted when the merchant confirms payment on the standard checkout. If the merchant closes the panel mid-flow, the cart is left seeded but nothing is charged.

### After successful purchase, redirect to dashboard

When checkout succeeds, the panel shows a success state for about 3 seconds, then closes and routes the merchant to the dashboard (`/admin`) — not back to [[plans]] or to this screen. The new plan + add-ons are live by the time they land there. The purchased plan, services, and apps then appear in [[subscriptions]].

### Cleanup on close

When the side-panel variant of the screen is closed (X / backdrop click), the local selection state resets, so the merchant lands back on the catalog with no leaked state. The seeded cart from an abandoned checkout carries no charge.

## Related

- [[plan-details]] — hub.
- [[plan-details-billing-cycle]] — selects the plan variant that becomes the cart's plan entry.
- [[plan-details-recommendations]] — ticked services / apps that join the plan in the cart.
- [[plans-purchase]] — the legacy route whose Checkout panel this reuses.
- [[billing-cards]] — saved card used to confirm payment.
- [[billing-invoicing]] — invoice details printed on the resulting invoice.
- [[subscriptions]] — purchased plan / services / apps appear here after confirm.
- [[expired-subscription]] — funnel target when the plan-detail subscription later fails.

## Open questions

(All resolved.)
