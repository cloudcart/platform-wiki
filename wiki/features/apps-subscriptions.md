---
type: feature
nav_path: "Apps → Subscriptions"
route_name: apps.subscriptions.overview
route_path: /admin/apps/subscriptions
aliases: ["Subscriptions app", "Subscription products", "Recurring orders", "Repeat delivery", "Subscribe and save", "Sell subscriptions", "Абонаменти", "Абонаментни продукти", "Повтарящи се поръчки", "Абонирай се и спести"]
tags: [apps, subscriptions, recurring, billing, retention]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-08-28
source_count: 6
---

# Subscriptions (recurring orders)

> **No on/off control — this app has no "active / inactive" state.** Its own screens carry no Enable / Disable button and no activation toggle; it is either installed or not. Uninstalling stops **new** subscriptions being sold, but does not cancel contracts already running (see *Business rules*). An agent looking for a switch to explain why subscriptions are not being offered should check the payment method instead ([[apps-subscriptions-setup]]).

## Purpose

Lets the store sell a product on a **repeating schedule** instead of as a one-off: the customer picks a subscription option on the product page, and from then on the platform charges their saved card and raises a new order each time the schedule comes round — without the customer returning to the shop.

The merchant defines **what may be subscribed to** and **on what terms**; everything after the first purchase runs on its own.

## Where to find it

Sidebar → **Apps → Subscriptions** (`/admin/apps/subscriptions`). The screen carries two tabs:

| Tab | What it holds |
|---|---|
| **Plans** | The subscription options offered to customers — see [[apps-subscriptions-plans]]. |
| **Subscriptions** | Every live contract, with its schedule and history — see [[apps-subscriptions-managing]]. |

**Settings** sits alongside them at `/admin/apps/subscriptions/settings`.

## Sub-pages (in this cluster)

- [[apps-subscriptions-setup]] — installing it, and the payment-method requirement that decides whether it can run at all.
- [[apps-subscriptions-plans]] — plan groups, what a plan can be attached to, the billing and delivery intervals, and per-cycle pricing.
- [[apps-subscriptions-billing-cycle]] — how a renewal happens, prepaid versus pay-as-you-go, and when stock is taken.
- [[apps-subscriptions-failed-payments]] — what happens when a card is declined: the retry schedule, `past_due`, and when a contract is given up on.
- [[apps-subscriptions-customer-controls]] — what the customer may do with their own subscription, and which of those the merchant can switch off.
- [[apps-subscriptions-managing]] — the merchant's list and detail view, the actions available on a contract, and the four e-mails.

## What the merchant can do here

- **Create subscription options** and attach them to a product, a category, a collection or a brand ([[apps-subscriptions-plans]]).
- **Choose which payment methods** may carry a subscription ([[apps-subscriptions-setup]]).
- **Decide what the customer may do alone** — skip a delivery, pause, cancel, change the address ([[apps-subscriptions-customer-controls]]).
- **Act on an individual contract** — pause, skip, charge now, resume, cancel ([[apps-subscriptions-managing]]).
- **Set the failure policy** — how many declined attempts before a subscription is given up on ([[apps-subscriptions-failed-payments]]).

### What the merchant CANNOT do here

- **Sell a subscription without a card-storing payment method.** No capable method means no plan is offered at all — this is the first thing to check when plans do not appear on the storefront. See [[apps-subscriptions-setup]].
- **Change an existing contract's plan.** Terms are fixed at purchase; a different schedule means a new subscription.
- **Bill a subscription manually outside its schedule**, other than the one-off **Charge now** action on a contract.

## Business rules

### The customer buys a contract, not just an order

The first purchase creates a **subscription** that outlives the order it came from. It carries its own status, its own schedule of upcoming deliveries, and its own history. Every renewal raises a **new, ordinary order** in [[orders]] — so fulfilment, invoicing, stock and reporting all behave exactly as they do for any other order.

A subscription is therefore never "an order that repeats". It is the agreement that keeps producing orders.

### A subscription has five states

| Status | What it means |
|---|---|
| **`active`** | Running normally; the next date is scheduled. |
| **`paused`** | Temporarily stopped. No charge, no delivery, no schedule advance, until it is resumed. |
| **`past_due`** | A charge failed and further attempts are pending. The customer keeps the subscription in the meantime — see [[apps-subscriptions-failed-payments]]. |
| **`cancelled`** | Ended — by the customer, by the merchant, or by exhausting the failed-payment attempts. |
| **`expired`** | Ran to the end of a plan that had a maximum number of payments. |

Only **`active`** and **`past_due`** contracts are ever charged.

### Billing and delivery are separate schedules

A plan states how often the customer is **charged** and how often they are **sent** something, and the two need not match. Paying monthly and receiving monthly is one arrangement; paying every three months and receiving monthly is another, and the platform treats the second as **prepaid** — the money is taken once and the deliveries that it covers follow without further charges. See [[apps-subscriptions-billing-cycle]].

### It runs on its own, hourly

Contracts due today are picked up **within the hour** rather than on a nightly pass, and a separate check runs every two hours to settle charges whose outcome is not yet known. Neither is something the merchant triggers; both matter when watching a first renewal go through. See [[apps-subscriptions-billing-cycle]].

### Turning the app off does not cancel what is already sold

Uninstalling stops **new** subscriptions being sold. Existing contracts are a commitment to a customer, and the platform is deliberate about not stranding them — the same principle applies when a payment method is un-ticked or a plan feature lapses. See [[apps-subscriptions-setup]].

## Settings & fields

Grouped on the Settings screen; the full reference is on the aspect pages:

| Group | Covers |
|---|---|
| **Payment methods** | Which methods may carry a subscription — [[apps-subscriptions-setup]] |
| **Product page** | Whether the subscription option is preselected over the one-time purchase — [[apps-subscriptions-plans]] |
| **Customer notifications** | Start, renewal, and upcoming-renewal reminders — [[apps-subscriptions-managing]] |
| **Failed payments** | Attempts before giving up, and merchant alerts — [[apps-subscriptions-failed-payments]] |
| **What the customer may do** | Skip, pause, cancel, change address — [[apps-subscriptions-customer-controls]] |

## Related

- [[apps]] — the Apps hub.
- [[orders]] — where every renewal order lands.
- [[settings-payment-providers]] — where the card-storing payment methods are configured.
- [[customers]] — the customer whose card and address the contract holds.
- [[inventory-tracking]] — stock taken by renewal orders.
- [[plan-gates]] — the `subscriptions` plan feature behind the paid payment methods.

## Open questions

- Whether a merchant can migrate customers from one plan to another in bulk, or whether each customer must re-subscribe.
