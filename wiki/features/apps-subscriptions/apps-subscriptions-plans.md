---
type: feature
nav_path: "Apps → Subscriptions → Plans"
route_name: apps.subscriptions.plans
route_path: /admin/apps/subscriptions/plans
aliases: ["Subscription plans", "subscription options", "plan group", "subscribe and save discount", "which products can be subscribed", "delivery frequency", "Абонаментни планове", "честота на доставка", "отстъпка за абонамент"]
tags: [apps, subscriptions, plans, pricing, targeting]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-08-28
source_count: 5
---

> Part of [[apps-subscriptions]]. See the hub for the other aspects (setup, billing cycle, failed payments, customer controls, managing).

# Subscriptions — plans, what they apply to, and pricing

## Purpose

A **plan** is one subscription option a customer can choose — *"every month"*, *"every 3 months, 10% off"*. Plans are organised into **groups**, and it is the group that decides **which products** the options are offered on. This aspect covers that structure, the two intervals a plan carries, and how the price changes over the life of a subscription.

## Where to find it

**Apps → Subscriptions → Plans**.

## What the merchant can do here

- Create a **plan group** and attach it to what it should cover.
- Add the individual **plans** inside it — the options the customer picks between.
- Set **how often the customer pays** and **how often they receive**.
- Set a **discount**, optionally one that changes after a number of payments.
- Bound the commitment with a **minimum** and **maximum** number of payments.
- Deactivate a plan so it stops being offered without disturbing contracts already on it.

## Settings & fields

### Plan group — what the options apply to

A group is attached to one or more targets. Four kinds, offered narrowest first:

| Target | Covers |
|---|---|
| **Product** | One product, optionally one specific variant. |
| **Category** | Everything in a category ([[products-categories]]). |
| **Selection** | A curated collection. |
| **Vendor** | Everything from one brand ([[products-vendors]]). |

A product is offered the options of **every group that matches it** — directly, or through its category, collection or brand. A product with no matching group has no subscription option at all, which is the second thing to check when the storefront shows none (the first is on [[apps-subscriptions-setup]]).

### Plan — the option itself

| Field | What it does |
|---|---|
| **Name** | What the customer sees as the choice. |
| **Billing interval** + count | How often the customer is charged — `day` / `week` / `month` / `year`, times a number. |
| **Delivery interval** + count | How often they receive something, on the same units. |
| **Minimum payments** (`min_cycles`) | How many payments the customer commits to before they may cancel. |
| **Maximum payments** (`max_cycles`) | After how many payments the subscription ends by itself (`expired`). Leave unset for open-ended. |
| **Stock policy** (`inventory_policy`) | Whether stock is taken when the money is taken, or when the parcel goes out — see [[apps-subscriptions-billing-cycle]]. |
| **Active** | Whether the option is currently offered. |
| **Position** | The order the options appear in on the product page. |

Validation: the maximum cannot be lower than the minimum — *"The maximum number of payments cannot be lower than the minimum."*

### Pricing — a discount that can change over time

A plan carries one or more price rules, each applying **after a given number of payments**. Three kinds:

| Type | Meaning |
|---|---|
| **Percentage** | A percentage off the line price. Capped at 100% — *"A discount cannot be more than 100%."* |
| **Fixed amount** | A flat amount off the line price. |
| **Price** | An absolute price for the line, replacing it rather than reducing it. |

Because each rule names the cycle it starts from, a plan can open at one price and settle at another — an introductory discount that reduces after the first few payments, or a loyalty discount that improves later.

## Business rules

### 🔴 Billing and delivery are two different questions

The pair of intervals is the heart of the plan, and the most common thing to get wrong. **How often the customer pays** and **how often they receive** are set separately:

- **Equal** (pay monthly, receive monthly) — pay-as-you-go. Each payment covers one delivery.
- **Billing less frequent than delivery** (pay every 3 months, receive monthly) — **prepaid**. One payment covers several deliveries, and the ones it covers go out without any further charge.

How many deliveries a payment covers is **worked out from the two intervals**, never stored separately, so the two can never drift apart. The consequences for scheduling and stock are on [[apps-subscriptions-billing-cycle]].

Note that months are not equal in length, which is why the count is derived from calendar intervals rather than day arithmetic — *3 months / 1 month* is 3 deliveries, not the 2 that a day-count would floor to.

### Deactivating a plan does not end its subscriptions

Setting a plan inactive removes it from the product page. Customers already on it keep their terms and keep renewing. A plan is a **template for new contracts**; the contract copies its terms at purchase and no longer depends on it.

This is also why terms cannot be edited retroactively: changing a plan changes what future customers get, not what existing ones agreed to.

### The customer's choice can be preselected

The **Preselect the subscription instead of the one-time purchase** setting (`preselect_plan`) decides which option the product page opens on. It changes only the default — the one-time purchase remains available either way.

### Saving a group with no plans is refused

*"Add at least one subscription option."* A group exists to hold options; an empty one would attach itself to products and offer nothing.

## Related

- [[apps-subscriptions]] — hub.
- [[apps-subscriptions-setup]] — the payment-method requirement that hides plans regardless of targeting.
- [[apps-subscriptions-billing-cycle]] — what the two intervals produce in practice.
- [[products-categories]] — category targeting.
- [[products-vendors]] — vendor targeting.
- [[product-detail]] — the storefront page where the options are shown.

## Open questions

- What happens when two groups match the same product and both offer an option with identical terms — whether the duplicate is suppressed or shown twice.
