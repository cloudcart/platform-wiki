---
type: feature
nav_path: "Apps → Subscriptions → Plans"
route_name: apps.subscriptions.plans
route_path: /admin/apps/subscriptions/plans
aliases: ["Subscription plans", "subscription options", "plan group", "subscribe and save discount", "which products can be subscribed", "delivery frequency", "Абонаментни планове", "честота на доставка", "отстъпка за абонамент"]
tags: [apps, subscriptions, plans, pricing, targeting]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-11-03
source_count: 5
---

> Part of [[apps-subscriptions]]. See the hub for the other aspects (setup, billing cycle, failed payments, customer controls, managing).

# Subscriptions — plans, what they apply to, and pricing

## Purpose

A **plan** holds the subscription **options** a customer can choose — *"every month"*, *"every 3 months, 10% off"* — and decides **which products** they are offered on. In the API a plan is a plan group and an option is a plan. This aspect covers the plan editor and what an option holds.

## Where to find it

**Apps → Subscriptions → Plans** (`/admin/apps/subscriptions/plans`). **New plan** opens the editor in a right-side panel; the pencil on a table row opens **Edit plan**.

## What the merchant can do here

- Create a plan and pick what it applies to.
- Add the **options** inside it, the choices the customer picks between.
- Set **how often an option delivers and charges**, as one period.
- Set a **discount** and a number of payments after which the subscription stops.
- Deactivate a plan or a single option so it stops being offered without disturbing contracts already on it.

## Settings & fields

### General settings

| Field | What it does |
|---|---|
| **Name shown to customers** | The plan's name. |
| **Active** | *"Inactive plans are no longer offered on the product page. Customers already subscribed keep being charged and receiving deliveries."* |

### Options

| Field | What it does |
|---|---|
| **Option name** | What the customer sees as the choice. |
| **Offer this option** | Withdraws one option without touching the rest of the plan. |
| **Deliver and charge every** + **Period** | A number and days, weeks, months or years. One control for both: each delivery has its own charge. |
| **Discount (%)** | 0 to 100, off the line price. Above that: *"A discount cannot be more than 100%."* |
| **Stop after N payments** (`max_cycles`) | After how many payments the subscription ends by itself (`expired`). *"(0 = no limit)"* |
| **Combine with other discounts** (`combines_with_discounts`) | See below. |
| **Remove option** / **Add option** | Remove is unavailable on the only option. An option removed while customers are on it comes back switched off. |

A new option saves with no minimum number of payments (`min_cycles` 0), stock taken on sale (`inventory_policy` `on_sale`, see [[apps-subscriptions-billing-cycle]]) and one percentage price rule. An option saved earlier with further price rules keeps them; the editor shows the first.

### Products — what the options apply to

One target type per plan, with as many records of it as needed:

| Target | Covers |
|---|---|
| **Specific products** | The chosen products. |
| **Category** | Everything in a category ([[products-categories]]). |
| **Collection** | Everything in a collection. |
| **Manufacturer** | Everything from one brand ([[products-vendors]]). |

A product is offered the options of **every plan that matches it** — directly, or through its category, collection or brand. A product with no matching plan has no subscription option at all, which is the second thing to check when the storefront shows none (the first is on [[apps-subscriptions-setup]]). Saving with nothing picked is refused: *"Choose at least one product, category, collection or manufacturer for this plan."*

## Business rules

### 🔴 One period: each delivery has its own charge

Delivery and payment periods must be identical, so one payment covers one delivery. A request where they differ is refused:

> *"The delivery period must match the payment period. Plans where one payment covers several deliveries are not available yet."*
> BG: *"Периодът на доставка трябва да съвпада с периода на плащане. Планове, при които едно плащане покрива няколко доставки, все още не са налични."*

An older plan with two different periods opens in the editor with the delivery period set to the billing one, and saving stores that. Contracts already running keep the schedule agreed at purchase ([[apps-subscriptions-billing-cycle]]).

### Deactivating a plan does not end its subscriptions

Setting a plan inactive removes it from the product page. Customers already on it keep their terms and keep renewing. A plan is a **template for new contracts**; the contract keeps the schedule and payment limits agreed at purchase, so changing a plan does not alter them.

The option's discount and its **Combine with other discounts** switch are read from the live plan at each renewal.

### Combine with other discounts

Each option has a **Combine with other discounts** switch (`combines_with_discounts`), on by default, so existing plans keep pricing as before. Help text: *"When off, the subscription gets only this option's discount. Product discounts, discount codes and cart rules do not apply to it. One-time purchases in the same cart keep their discounts."*

With the switch off:

- A line bought on the option takes only the option's adjustment: no automatic product discount, no discount code, no cart-rule line discount. Cross-sell subtotals are worked out the same way.
- One-time lines in the same cart keep their discounts.
- An order-level code (target "order over", or a shipping code) still applies. The switch reaches line discounts only.
- A saved order keeps the setting it was priced with.
- When a line-level code is withheld, the checkout summary tells the customer why ([[checkout-step-sidebar]]).

### The customer's choice can be preselected

The **Preselect the subscription instead of the one-time purchase** setting (`preselect_plan`) decides which option the product page opens on. It changes only the default — the one-time purchase remains available either way.

### Saving a plan with no options is refused

*"Add at least one subscription option."* A plan exists to hold options; an empty one would attach itself to products and offer nothing.

## Related

- [[apps-subscriptions]] — hub.
- [[apps-subscriptions-setup]] — the payment-method requirement that hides plans regardless of targeting.
- [[apps-subscriptions-billing-cycle]] — what the period produces in practice.
- [[products-categories]] — category targeting.
- [[products-vendors]] — vendor targeting.
- [[product-detail]] — the storefront page where the options are shown.

## Open questions

- What happens when two plans match the same product and both offer an option with identical terms — whether the duplicate is suppressed or shown twice.
