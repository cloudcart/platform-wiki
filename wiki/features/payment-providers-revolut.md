---
type: feature
nav_path: "Settings → Payment methods → Revolut"
route_name: apps.revolut.settings
route_path: /admin/payment-providers/revolut, /admin/payment-providers/revolut/settings
aliases: ["Revolut", "Revolut Pay", "Revolut Merchant", "Revolut Business", "Revolut Pay by Bank", "Revolut Apple Pay", "Revolut webhook", "Плащане с Revolut", "Револют"]
tags: [paymentproviders, payment-providers, revolut, apple-pay, google-pay]
plan_gates: []
created: 2026-05-22
updated: 2026-11-03
source_count: 2
---
# Revolut

## Purpose

Revolut accepts online payments through the merchant's own **Revolut Business** merchant account. The shopper pays in a pop-up widget on the store, or on a Revolut-hosted page. Which methods the shopper sees (card, Revolut Pay, Google Pay, Apple Pay, Pay by Bank) is decided in the Revolut Business Dashboard. This page covers the settings, the webhook and Apple Pay cards, capture, refunds, and what happens when a checkout is resumed.

## Where to find it

Settings → **Payment methods** → **Revolut**. Address: `/admin/payment-providers/revolut` (overview) and `/admin/payment-providers/revolut/settings` (settings). No plan gate is declared.

## What the merchant can do here

- Enter the **Live** and **Test** keys, and switch between test and live mode.
- Choose **Checkout mode** (pop-up or hosted page) and **Capture mode** (automatic or manual).
- **Register, re-register or remove the webhook**, and see every webhook on the Revolut account.
- Turn **Apple Pay** on and **register the store domain** for it.
- Set the standard fields of a payment method: logo, title and description, minimum and maximum order amount, discount.

## Settings & fields

| Field / box | What it does | Default | Notes |
|---|---|---|---|
| **Test mode / Live mode** | Which set of keys is used. | Test | Webhook and Apple Pay status follow the selected mode. |
| **Live Secret Key**, **Test Secret Key** | API secret key from the Revolut Merchant account. | Empty | Required for the selected mode. Checked with Revolut on save. Must not contain whitespace. |
| **Live Public Key**, **Test Public Key** | Key the pop-up widget uses. | Empty | Pop-up mode refuses to save without it: *"Pop-up checkout requires the Revolut public key (pk_…)."* |
| **Live Webhook Secret**, **Test Webhook Secret** | Signing secret of the webhook. | Empty | Filled in when the webhook is registered from this page. |
| **Checkout behaviour** box → **Checkout mode** | **Pop-up (embedded checkout widget)** keeps the shopper on the store; **Hosted Checkout (redirect)** sends them to a Revolut page. | Pop-up | The shopper sees a notice about the window or the redirect at checkout. |
| **Checkout behaviour** box → **Capture mode** | **Automatic** captures at once; **Manual** only authorises, and the merchant captures from the order. | Automatic | See [[orders-payment-capture]]. |
| **Checkout behaviour** box → **Apple Pay** | Turns Apple Pay on for this method and registers the domain. | Off | See below. |

## Business rules

### Webhook card

The card shows the **Webhook endpoint**, **Registered** or **Not registered**, and the buttons **Register webhook** / **Re-register** and **Remove**. Messages:

- *"Save your secret key first, then register the webhook."*
- *"Order status updates will not reach your store until the webhook is registered."*
- *"The webhook is registered but no signing secret is stored. Re-register to obtain a new one."*
- *"The webhook is missing some events. Re-register to subscribe to all of them."*

Below that, **All webhooks on this Revolut account** lists every webhook on the account, also those of another store or added in the Revolut Dashboard, marking this store's as **This store**. **Remove** asks for confirmation. Removing another store's webhook stops order updates reaching it, and cannot be undone from this page.

### Apple Pay domain card

The card shows the store's primary domain, **Registered** or **Not registered**, and **Register domain** / **Re-register** and **Remove**. Turning the **Apple Pay** switch on or off and saving registers or removes the domain too. The page's notes:

- Apple Pay must be enabled on the Revolut account first; until then registering returns *"Registration for merchantId not found"*.
- The store domain must be reachable from the internet so Apple can read the verification file CloudCart serves. Test stores are not.
- *"A domain can verify Apple Pay for only one payment provider. Registering here takes Apple Pay away from PayPal and CloudCart Pay on this store."* See [[cloudcart-pay-apple-pay-domain]].

### How the payment status updates

The webhook, the shopper's return and a background check all update the payment. The check starts 10 minutes after the order is sent to Revolut and repeats every 5 minutes. A payment still open after 3 hours is timed out, and its order at Revolut is closed so it can no longer be paid. A declined attempt marks the payment `failed`; the order status then follows the rules on [[order-status-auto-transitions]].

### Resumed checkout: no second order at Revolut

A resumed checkout, or a second press of the finish button after closing the pop-up, reuses the Revolut order the payment already holds:

| The earlier Revolut order is | What happens |
|---|---|
| Paid or authorised | The payment is settled and the shopper goes to the order. |
| Still payable at the same amount | The same order is reopened. |
| Still payable, amount changed | It is cancelled and a new one is created, or the payment is settled if it was paid meanwhile. |
| Being processed, amount changed | The shopper is asked to try again in a minute. |
| Cancelled or expired | A new order is created. |
| Cannot be checked (Revolut unreachable) | The shopper sees an error. No second order is created. |

An unpaid Revolut order expires after **1 hour**. A notification about an older paid order of the same payment settles the payment; if the payment was already settled, the second charge is flagged for a refund.

### Refunds

A full refund runs from the order's **Refund payment** button ([[orders-payment-refund]]). A partial refund runs through an order return ([[orders-payment-refund-partial-refunds]]). Revolut finishes refunds asynchronously, so the payment shows as refunded once Revolut reports the money moved.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — the payment methods list.
- [[cloudcart-pay-apple-pay-domain]] — one Apple Pay provider per domain.
- [[orders-payment-capture]] — capturing a manual authorisation.
- [[orders-payment-refund]] — full refunds.
- [[orders-payment-refund-partial-refunds]] — partial refunds.
- [[order-status-auto-transitions]] — how the order follows its payments.
- [[payment-status]] — payment statuses.

## Open questions

- The Bulgarian admin labels (production translation table).
