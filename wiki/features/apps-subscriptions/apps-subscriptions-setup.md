---
type: feature
nav_path: "Apps → Subscriptions → Settings → Payment methods"
route_name: apps.subscriptions.settings
route_path: /admin/apps/subscriptions/settings
aliases: ["Subscriptions setup", "subscription payment methods", "no subscription option on product page", "subscription plans not showing", "recurring payment method", "card saving subscriptions", "Абонаменти настройка", "не се показва абонамент"]
tags: [apps, subscriptions, payment-providers, plan-gate, setup]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-08-28
source_count: 5
---

> Part of [[apps-subscriptions]]. See the hub for the other aspects (plans, billing cycle, failed payments, customer controls, managing).

# Subscriptions — setup and the payment-method requirement

## Purpose

Installing the app is the easy half. The half that decides whether anything works is the **payment method**: a subscription is a promise to charge a card the customer is not present for, so the store must have a method that can do exactly that. This aspect covers that requirement, and why it is the first thing to check when subscription options do not appear.

## Where to find it

**Apps → Subscriptions → Settings** → the **Payment methods** section.

## What the merchant can do here

- Tick which of the store's payment methods may carry a subscription.
- See which methods are **Included** on the current plan and which are a **Paid service**.
- Jump to **Set up payment methods** when none is configured yet.

## Settings & fields

| Field | What it does |
|---|---|
| **Payment methods** (`payment_providers`) | The methods a new subscription may be sold through. A method the merchant has not ticked is never offered, even when it is technically capable. |

## Business rules

### 🔴 A method must clear three separate bars

A payment method is only offered for subscriptions when **all three** hold. Missing any one of them is enough to hide every plan on the storefront:

1. **Capable** — the gateway can charge a stored card **while the customer is away**, *and* the store actually keeps the card. A gateway that can charge a token is useless if checkout never stores one, because every renewal would have nothing to charge.
2. **Selected** — the merchant ticked it here. A store may hold several capable methods and still want subscriptions on only one.
3. **Paid for** — every capable method except the free ones needs the `subscriptions` plan feature.

The same three checks govern three different screens, which is why they agree: the settings here (what may be ticked), the product page (never offer a plan that cannot renew), and the checkout payment step (never let a subscription reach a method that cannot renew it).

### Two methods are free, the rest are a paid feature

**CloudCart Pay** and **Stripe** may be used for subscriptions on any plan at no extra cost — CloudCart Pay because the platform already earns on the processing itself. Every other capable method requires the `subscriptions` plan feature ([[plan-gates]]); the settings screen marks these **Paid service** and refuses a save that selects one without the feature.

### The messages tell you which bar failed

The Settings screen distinguishes the cases, and so should any diagnosis:

- *"No payment method on this store can charge a saved card yet."* — nothing installed is **capable**. The fix is on [[settings-payment-providers]], not here.
- *"Not set up on this store yet."* — the method is capable but not configured on this store.
- **Paid service** — capable and configured, but the plan feature is missing.

Saving with nothing selected is refused outright: *"Choose at least one payment method for subscriptions."*

### 🔴 When no method qualifies, the storefront shows nothing at all

The product page asks the platform which subscription options apply, and gets an **empty answer** when the app is disabled **or** when no recurring-capable method is available. There is no error, no notice and no greyed-out control — the subscription choice simply is not rendered.

This is the explanation for *"I created the plans and customers still cannot subscribe"*. Check, in this order: is the app installed, is a capable method ticked here, and does a plan actually target the product ([[apps-subscriptions-plans]]).

### Existing contracts are protected from the merchant's later changes

Un-ticking a payment method, or losing the plan feature, controls only what may be **sold from now on**. Subscriptions already running keep renewing on the method they were sold with. The platform treats stranding a paying customer as the worse outcome than continuing to bill through a method the merchant has since deselected.

The practical consequence for support: a store whose plan no longer includes the feature can still have live subscriptions renewing, and that is not a billing fault.

## Related

- [[apps-subscriptions]] — hub.
- [[settings-payment-providers]] — where the methods themselves are installed and configured.
- [[plan-gates]] — the `subscriptions` plan feature.
- [[apps-subscriptions-plans]] — the second reason a plan may not appear on a product.
- [[checkout-step-payment]] — the checkout step that refuses a subscription cart on an unsuitable method.

## Open questions

- Whether a merchant is warned at the point of un-ticking a method that live contracts will keep using it, or whether that is only discoverable afterwards.
