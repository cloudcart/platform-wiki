---
type: feature
nav_path: "Apps → Subscriptions"
route_name: apps.subscriptions.overview
route_path: /admin/apps/subscriptions
aliases: ["Subscriptions app", "Subscription products", "Recurring orders", "Repeat delivery", "Subscribe and save", "Sell subscriptions", "Абонаменти", "Абонаментни продукти", "Повтарящи се поръчки", "Абонирай се и спести"]
tags: [apps, subscriptions, recurring, billing, retention]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-11-03
source_count: 6
---

# Subscriptions (recurring orders)

> **No on/off control — this app has no "active / inactive" state.** Its own screens carry no Enable / Disable button and no activation toggle; it is either installed or not. Uninstalling stops **new** subscriptions being sold, but does not cancel contracts already running (see *Business rules*). An agent looking for a switch to explain why subscriptions are not being offered should check the payment method instead ([[apps-subscriptions-setup]]).

## Purpose

Lets the store sell a product on a **repeating schedule** instead of as a one-off: the customer picks a subscription option on the product page, and from then on the platform raises a new order each time the schedule comes round, charging their saved card or sending the order cash on delivery — without the customer returning to the shop.

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
- [[apps-subscriptions-plans]] — the plan editor, what a plan can be attached to, the single delivery-and-charge period, and the discount.
- [[apps-subscriptions-billing-cycle]] — how a renewal happens, cash on delivery, older prepaid contracts, and when stock is taken.
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

- **Sell a subscription without a capable payment method** (one that charges a saved card, or cash on delivery). No capable method means no plan is offered at all — this is the first thing to check when plans do not appear on the storefront. See [[apps-subscriptions-setup]].
- **Pay a subscription cart from the [[virtual-wallet-checkout|Virtual Wallet]].** A subscription needs a card that can recur, so the wallet box is not offered on a cart with a subscription line.
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

### One payment, one delivery

An option has a single period, **Deliver and charge every**, so each delivery is paid by its own charge. Plans where one payment covers several deliveries are not available: a request with two different periods is refused. See [[apps-subscriptions-plans]].

### It runs on its own, hourly

Contracts due today are picked up **within the hour** rather than on a nightly pass, and a separate check runs every two hours to settle charges whose outcome is not yet known. Neither is something the merchant triggers; both matter when watching a first renewal go through. See [[apps-subscriptions-billing-cycle]].

### Turning the app off does not cancel what is already sold

Uninstalling stops **new** subscriptions being sold. Existing contracts are a commitment to a customer, and the platform is deliberate about not stranding them — the same principle applies when a payment method is un-ticked or a plan feature lapses. See [[apps-subscriptions-setup]].

## Settings & fields

Five boxes on the Settings screen, saved through the unsaved-changes bar; the full reference is on the aspect pages:

| Box | Covers |
|---|---|
| **Payment methods** | Which methods may carry a subscription — [[apps-subscriptions-setup]] |
| **Product page** | Whether the options show, and whether the subscription is preselected over the one-time purchase — [[apps-subscriptions-plans]] |
| **What customers can do themselves** | Skip, move a delivery, pause, cancel, change address — [[apps-subscriptions-customer-controls]] |
| **Failed payments** | Attempts before giving up, refused parcels, and merchant alerts — [[apps-subscriptions-failed-payments]] |
| **Customer notifications** | Which e-mails go out, and **Days before the renewal** (0 to 30) for the reminder — [[apps-subscriptions-managing]] |

## Related

- [[apps]] — the Apps hub.
- [[orders]] — where every renewal order lands.
- [[settings-payment-providers]] — where the card-storing payment methods are configured.
- [[customers]] — the customer whose card and address the contract holds.
- [[inventory-tracking]] — stock taken by renewal orders.
- [[plan-gates]] — the `subscriptions` plan feature behind the paid payment methods.

## Open questions

- Whether a merchant can migrate customers from one plan to another in bulk, or whether each customer must re-subscribe.
