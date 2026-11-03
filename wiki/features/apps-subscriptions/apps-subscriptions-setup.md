---
type: feature
nav_path: "Apps → Subscriptions → Settings → Payment methods"
route_name: apps.subscriptions.settings
route_path: /admin/apps/subscriptions/settings
aliases: ["Subscriptions setup", "subscription payment methods", "no subscription option on product page", "subscription plans not showing", "recurring payment method", "card saving subscriptions", "Абонаменти настройка", "не се показва абонамент"]
tags: [apps, subscriptions, payment-providers, plan-gate, setup]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-11-03
source_count: 5
---

> Part of [[apps-subscriptions]]. See the hub for the other aspects (plans, billing cycle, failed payments, customer controls, managing).

# Subscriptions — setup and the payment-method requirement

## Purpose

Installing the app is the easy half. The half that decides whether anything works is the **payment method**: a renewal either charges the card the customer paid with the first time, or goes out as a cash-on-delivery order, so the store must have a method that can do one of the two. This aspect covers that requirement, and why it is the first thing to check when subscription options do not appear.

## Where to find it

**Apps → Subscriptions → Settings** → the **Payment methods** section.

## What the merchant can do here

- Tick which of the store's payment methods may carry a subscription.
- See **CloudCart Pay** badged **Included** and, on a store that has the `subscriptions` plan feature, the other capable methods badged **Paid service**.
- Jump to **Set up payment methods** when none is configured yet.
- With cash on delivery selected, set how many refused parcels in a row end a subscription.

## Settings & fields

| Field | What it does |
|---|---|
| **Payment methods** (`payment_providers`) | The methods a new subscription may be sold through. A method the merchant has not ticked is never offered, even when it is technically capable. |
| **Refused cash-on-delivery parcels in a row before the subscription is cancelled** (`max_refused_deliveries`) | In the **Failed payments** box, shown with cash on delivery selected. 1 to 5, default 2. See [[apps-subscriptions-failed-payments]]. |

## Business rules

### 🔴 A method must clear three separate bars

A payment method is only offered for subscriptions when **all three** hold. Missing any one of them is enough to hide every plan on the storefront:

1. **Capable** — the gateway can charge a stored card **while the customer is away**, *and* the store actually keeps the card, because otherwise every renewal would have nothing to charge. Cash on delivery is capable without a card: *"Each renewal is sent as a cash-on-delivery order and is paid to the courier. No card is needed."*
2. **Selected** — the merchant ticked it here. A store may hold several capable methods and still want subscriptions on only one.
3. **Paid for** — every capable method except CloudCart Pay, cash on delivery included, needs the `subscriptions` plan feature.

The same three checks govern three different screens, which is why they agree: the settings here (what may be ticked), the product page (never offer a plan that cannot renew), and the checkout payment step (never let a subscription reach a method that cannot renew it).

### CloudCart Pay is free, the rest need the plan feature

**CloudCart Pay** may be used for subscriptions on any plan at no extra cost, because the platform already earns on the processing itself. It is the only free method: every other capable method, Stripe included, requires the `subscriptions` plan feature ([[plan-gates]]).

### The paid methods are currently off sale

The other methods are not on sale at the moment. What a store sees depends on whether it already has the feature:

| Store | Payment methods section |
|---|---|
| Without the `subscriptions` feature | CloudCart Pay only, with no purchase offer for the others. |
| With the feature, bought earlier or added by CloudCart | Every capable method, as before. |

A method ticked earlier and now hidden is dropped on the next save, so it cannot block the form. Running contracts keep renewing on it (see below).

### The messages tell you which bar failed

The Settings screen distinguishes the cases, and so should any diagnosis:

- *"No payment method on this store can charge a saved card yet."* — nothing installed is **capable**. The fix is on [[settings-payment-providers]], not here.
- *"Not set up on this store yet."* — the method is capable but not configured on this store.
- *"Set up, but switched off — customers cannot pick it at checkout."* — configured, but off in [[settings-payment-providers]].
- *"Saving cards is switched off in this method, so there would be no card to renew with."* — the method's own card-saving setting is off.

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
