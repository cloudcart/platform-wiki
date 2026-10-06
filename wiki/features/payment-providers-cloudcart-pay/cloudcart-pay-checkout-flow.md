---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Checkout flow"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay checkout flow", "CloudCart Pay inline checkout", "CloudCart Pay embedded checkout", "CloudCart Pay popup checkout", "CloudCart Pay Apple Pay Google Pay", "CloudCart Pay capture", "Плащане с карта в поръчката", "Вградено плащане", "Изскачащ прозорец за плащане"]
tags: [paymentproviders, payment-providers, cloudcart-pay, checkout]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, express checkout, Apple Pay domain, refunds, saved card) and the six tabs.

# CloudCart Pay — checkout flow

## Purpose

How a shopper pays with CloudCart Pay on the store's checkout: the two ways the card form can appear (inline, the default, or a popup), Apple Pay and Google Pay, what happens when the total changes or the session runs out, and why every payment is captured at once. It is the page for "how does the card form look?", "does CloudCart Pay take Apple Pay?" and "why did the shopper see a message about the total?".

## Where to find it

The behaviour is on the **storefront checkout**, payment step (see [[checkout-flow]]). The merchant chooses the form in Settings → Payment methods → CloudCart Pay → **Settings** → **Checkout display** (Показване при плащане), and turns the wallets on or off in **Digital wallets** (Дигитални портфейли) — see [[payment-providers-cloudcart-pay-settings]].

## What the merchant can do here

- **Show the card fields inside the checkout page** (inline, the default) or **in a popup** after the complete-order button.
- **Offer Apple Pay and Google Pay** next to the card form, each on or off separately.
- **Rely on automatic capture** — there is no separate capture step.

## Settings & fields

| Setting (Settings tab) | Options | Default | Effect at checkout |
|---|---|---|---|
| **Card form display** | **Inline card fields** / **Popup window** | Inline card fields | Where the card form appears. |
| **Apple Pay** | On / Off | On | Apple Pay button next to the card form. |
| **Google Pay** | On / Off | On | Google Pay button next to the card form. |
| **Save Customer Card** | On / Off | On | Signed-in customers can save and reuse a card — see [[cloudcart-pay-save-card]]. |

## Business rules

### Inline card fields (default)

When the shopper selects CloudCart Pay on the payment step, the card form opens right inside that payment method, for guests and signed-in customers alike. It is prepared for the cart total at that moment.

When the shopper completes the order, the order is created and the card is charged in the same click. If 3-D Secure is needed, the bank's check appears inside the form.

- **The total changed.** If the cart total changed after the form appeared, the shopper sees *"The order total changed — please confirm the payment again."* (Сумата на поръчката се промени — моля, потвърдете плащането отново.) and the form reloads for the new total.
- **The form expired.** It reloads itself.
- **The form cannot load** (for example the account is not set up): it is hidden, and the payment continues in the popup.
- **Wallets inline.** Tapping Apple Pay or Google Pay first checks the checkout form (terms, required fields) without creating an order. The order is created only once the wallet payment succeeds, so a cancelled wallet leaves no pending order.

### Popup window

With **Popup window**, the shopper completes the order first; a window then opens with the order total, the card form and the enabled wallets. On phones the window fills the whole screen. Its close button is hidden while a payment or a 3-D Secure check is in progress.

The popup is also where a payment goes when the inline form could not load.

### Look of the card form

The card form uses CloudCart Pay's own fixed styling (red buttons, rounded fields on a white card), not the store theme's colours. Card details are typed into the secure form and never reach the store.

### Automatic capture

Every payment is captured at once on success. There is no authorize-then-capture option, so [[orders-payment-capture|manual capture]] does not apply to CloudCart Pay.

### Payment window and abandoned payments

A payment session stays payable for **2 hours**. A declined card does not end it: the shopper can try another card in the same form, and the payment is marked failed only once the session can no longer be paid. A payment that is still open after **3 hours** is closed as timed out by a background check, so the order does not stay "requested" — see [[cloudcart-pay-refunds-webhooks]].

### No double charge for the same cart

If the same cart was already paid (for example the shopper went back and pressed the button again), the shopper is taken to that order's confirmation page instead of being charged a second time.

### Order reference on the payment

Each payment carries a description of the form "Order #<number> | <store domain>" and the order number, so it can be found on the [[payment-providers-cloudcart-pay-transactions|Transactions tab]] by **Order Reference**.

### Currency

The popup charges in the order's currency. The inline form is prepared in the store's main currency. Payouts are made in the settlement currencies listed on the [[payment-providers-cloudcart-pay-payouts|Payouts tab]].

### Subscriptions

When the basket holds a subscription product, the card is always saved for the renewals, even if **Save Customer Card** is off — see [[cloudcart-pay-save-card]].

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-settings]] — where the form and wallets are set.
- [[cloudcart-pay-apple-pay-domain]] — Apple Pay needs the store domain registered.
- [[cloudcart-pay-express-checkout]] — wallet buttons on product pages.
- [[cloudcart-pay-save-card]] — saved cards at checkout.
- [[cloudcart-pay-refunds-webhooks]] — how payment statuses are updated afterwards.
- [[checkout-flow]] — the storefront checkout.
- [[orders-payment-capture]] — manual capture, not used by CloudCart Pay.
- [[payment-status]] — payment statuses on orders.

## Open questions

- What a shopper sees when the inline form is prepared in the store's main currency but the order is placed in another currency on a multi-currency store.
- Which card brands beyond Visa and Mastercard are accepted (the merchant help article says "Visa, Mastercard and more").
