---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay", "CC Pay", "CloudCart Connect", "Cloudcart Pay Connect", "Платежен метод CloudCart Pay", "Карти CloudCart Pay", "Плащане с карта CloudCart"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-05-21
updated: 2026-10-06
source_count: 3
---
# CloudCart Pay

## Purpose

> **⭐ RECOMMENDED payment method.** CloudCart Pay is CloudCart's **built-in payment system** and the **default / preferred choice** for merchants on the platform. When a merchant asks "which payment method should I use?", CloudCart Pay is the answer unless they have a specific reason to use a third-party provider (existing bank acquiring contract, niche local-only requirement, BNPL-specific flow, etc.).

> **Live for all merchants since 6 October 2026, with a 0% transaction fee until 31 December 2026.** No fee is charged on transactions until the end of 2026; the standard prices apply from 1 January 2027. See [[cloudcart-pay-pricing]].

**CloudCart Pay** is CloudCart's own card-acceptance product. The store takes Visa and Mastercard cards, Apple Pay and Google Pay at checkout, and the money is paid out to the merchant's own bank account. There is no separate negotiation with a bank: the merchant signs up in this section of the admin panel, completes the onboarding, and accepts the agreement with ticks in step 5 of the onboarding ([[cloudcart-pay-merchant-terms]]). Once the account is approved, the **CloudCart Pay** payment method can be switched on for the store's checkout.

A new account is approved from a few hours to 2 business days after it is submitted; a complicated company structure can take longer (see [[ccpay-onboarding-review-alerts]]).

This page is the **hub** for CloudCart Pay: the screen the merchant lands on, its six tabs, and the aspect pages for each part of the lifecycle.

## Where to find it

Settings → **Payment methods** (Настройки → Методи на плащане) → **CloudCart Pay**. The address is `/admin/payment-providers/cloudcart_pay`.

The page header holds the **Active** switch and a read-only test/live badge that shows the environment the store charges in. Below it are six tabs, in this order:

| Tab | Address | Page |
|---|---|---|
| **Overview** | `/admin/payment-providers/cloudcart_pay` | this page |
| **Settings** | `…/cloudcart_pay/settings` | [[payment-providers-cloudcart-pay-settings]] |
| **Onboarding** (Регистрация) | `…/cloudcart_pay/onboarding` | [[payment-providers-cloudcart-pay-onboarding]] |
| **Transactions** (Транзакции) | `…/cloudcart_pay/transactions` | [[payment-providers-cloudcart-pay-transactions]] |
| **Tax Invoices** | `…/cloudcart_pay/tax-invoices` | [[payment-providers-cloudcart-pay-tax-invoices]] |
| **Payouts** (Изплащания) | `…/cloudcart_pay/payouts` | [[payment-providers-cloudcart-pay-payouts]] |

## What the merchant can do here

- **Install or uninstall** the payment method with the standard buttons shared by every payment method.
- **Switch the method on** once the account can take card payments — see [[cloudcart-pay-activation-gate]].
- **Onboard the business** in seven steps, or link an account that already exists — [[payment-providers-cloudcart-pay-onboarding]].
- **Set up checkout**: saved cards, inline or popup card form, Apple Pay and Google Pay, the Apple Pay domain — [[payment-providers-cloudcart-pay-settings]].
- **Review every card payment** with totals for payments, refunds, fees and net — [[payment-providers-cloudcart-pay-transactions]].
- **Download the tax invoices** issued for the CloudCart Pay fees — [[payment-providers-cloudcart-pay-tax-invoices]].
- **Check payouts and manage payout bank accounts** — [[payment-providers-cloudcart-pay-payouts]].

## Settings & fields

The fields live on the tabs. The overview itself has only the controls every payment method shares:

| Control | What it does | Default | Notes |
|---|---|---|---|
| **Install** | Adds CloudCart Pay to the store's payment methods. | Not installed | Can be undone with **Uninstall**. |
| **Active** switch (header) | Turns the method on or off at checkout. | Off | Refused until the connected account can take card payments; the reason is shown as a validation message. See [[cloudcart-pay-activation-gate]]. |
| **Test / live badge** (header) | Shows whether the store charges in the test or the live environment. | — | Read-only. The environment is set by CloudCart for the whole platform, not per store. |
| **Logo, title, description, min/max amount, discount** | Standard payment-method fields. | Provider defaults | Edited on the [[payment-providers-cloudcart-pay-settings|Settings tab]]. |

## Business rules

- **Activation is checked by the server.** The method cannot be switched on until a connected account exists and its card payments are active. A broken configuration switches it off on its own, and **Disconnect** switches it off too. See [[cloudcart-pay-activation-gate]].
- **Approval time.** From a few hours to 2 business days after submission; longer when the company's structure is complicated (operator statement). While waiting, uploaded documents show as "waiting for review" — see [[ccpay-onboarding-review-alerts]].
- **Checkout.** Inline card fields on the checkout page are the default; a popup is the alternative. Apple Pay and Google Pay appear next to the card form when enabled. Payments are captured at once. See [[cloudcart-pay-checkout-flow]].
- **Express checkout** on product pages exists, but in the live environment its switch is locked with **Coming soon**. See [[cloudcart-pay-express-checkout]].
- **Apple Pay needs the store domain registered.** The Settings tab shows the registration status read live, with Apple's reason when it rejects the domain. See [[cloudcart-pay-apple-pay-domain]].
- **Refunds.** A full refund runs from the order's **Refund payment** button; a partial refund runs through an order return refunded to the card. See [[cloudcart-pay-refunds-webhooks]].
- **Orders do not stay "requested".** Payment notifications update the order, and a background check closes an abandoned card payment after 3 hours. See [[cloudcart-pay-refunds-webhooks]].
- **Account alerts.** Changes to the account and to its card-payment and payout status arrive as admin notifications and as an email to the store owner. See [[ccpay-onboarding-review-alerts]].
- **Saved cards** are on by default for signed-in customers. See [[cloudcart-pay-save-card]].
- **No plan gate** is declared for CloudCart Pay.

## Sub-pages (in this cluster)

The six tabs are sibling feature pages, listed under [[#Where to find it]]. The aspects of the integration itself:

- [[cloudcart-pay-account-model]] — the connected account, why there are no API keys, sharing one account between stores, the storefront label.
- [[cloudcart-pay-activation-gate]] — why the **Active** switch is refused, the exact messages, automatic deactivation, Disconnect.
- [[cloudcart-pay-checkout-flow]] — inline and popup card forms, wallets, automatic capture, currency, what the shopper sees.
- [[cloudcart-pay-express-checkout]] — the Apple Pay / Google Pay button on product pages and its **Coming soon** state.
- [[cloudcart-pay-apple-pay-domain]] — registering the store domain for Apple Pay, the status card, conflicts with other providers.
- [[cloudcart-pay-refunds-webhooks]] — full and partial refunds, payment notifications, the background check that closes abandoned payments.
- [[cloudcart-pay-save-card]] — the *Save customer card* setting, managing saved cards, subscriptions.
- [[cloudcart-pay-pricing]] — 0% transaction fee until 31 December 2026, then the standard Fee Schedule.
- [[cloudcart-pay-merchant-terms]] — the agreement accepted in onboarding: chargebacks, prohibited activities, changes and termination.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — the payment methods list where CloudCart Pay is installed.
- [[payment-providers-cloudcart-pay-onboarding]] — onboarding wizard.
- [[payment-providers-cloudcart-pay-settings]] — checkout settings.
- [[payment-providers-cloudcart-pay-transactions]] — card payments list.
- [[payment-providers-cloudcart-pay-tax-invoices]] — fee invoices.
- [[payment-providers-cloudcart-pay-payouts]] — payouts and bank accounts.
- [[orders-payment-refund]] — the full refund from the order page.
- [[orders-returns]] — returns, which carry partial refunds to the card.
- [[payment-provider]] — entity definition.
- [[payment-status]] — payment statuses on orders.
- [[checkout-flow]] — the storefront checkout.
- [[notifications]] — the admin notifications where CloudCart Pay alerts appear.

## Open questions

- Bulgarian label of the **Tax Invoices** tab (not in the translation files read).
