---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings → Checkout display → CloudCart Pay payment page"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay payment page", "CloudCart Pay hosted page", "CloudCart Pay redirect", "Hosted checkout CloudCart Pay", "Secure payment page", "Back to the store", "Платежна страница CloudCart Pay", "Сигурно плащане", "Пренасочване към страница за плащане"]
tags: [paymentproviders, payment-providers, cloudcart-pay, checkout, hosted]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects; the other two display modes are on [[cloudcart-pay-checkout-flow]].

# CloudCart Pay — payment page

## Purpose

**CloudCart Pay payment page** is the third option of **Card form display**, next to inline card fields and the popup window. The shopper completes the order on the store, pays on a CloudCart Pay page, and returns to the store's order page. The page needs no Apple Pay verification of the store's domain. It is the page for "can the customer pay on a separate page?" and "what is this payment page my customer saw?".

## Where to find it

Settings → Payment methods → CloudCart Pay → **Settings** tab → **Checkout display** box (Показване при плащане) → **Card form display** → **CloudCart Pay payment page**. The box's help text: *"Choose whether the card fields render directly in the checkout page, in a popup after clicking the complete order button, or on a CloudCart Pay payment page the customer is sent to. The payment page needs no Apple Pay verification of your store domain."*

## What the merchant can do here

- **Send shoppers to the payment page** instead of showing the card form on the checkout.
- **Keep the switches of the Settings tab**: **Apple Pay**, **Google Pay** and **Save Customer Card** apply here as well.

## Settings & fields

| Setting | Key | Values | Default |
|---|---|---|---|
| **Card form display** | `display_mode` | **Inline card fields** (`inline`), **Popup window** (`popup`), **CloudCart Pay payment page** (`hosted`) | Inline card fields |

## Business rules

### What the shopper sees

The page shows the store's name and logo, the order number and the amount, the card form with the enabled wallets, and a link back to the store. Its language follows the order.

| Text | Bulgarian |
|---|---|
| *"Secure payment"* | Сигурно плащане |
| *"Order #:id"* | Поръчка №:id |
| *"Loading the payment form…"* | Зареждане на формата за плащане… |
| *"Back to the store"* | Обратно към магазина |
| *"Secure payment by CloudCart Pay"* | Сигурно плащане с CloudCart Pay |
| *"The payment form could not be loaded. Please refresh the page."* | Формата за плащане не можа да се зареди. Моля, презаредете страницата. |

### How long the link works

The shopper's link is valid for **3 hours**: the 2-hour payment session plus 1. A reload after the session expired opens a new session. A payment no longer open goes through the return step and back to the store.

### A second visit does not charge twice

An attempt already paid, or still being paid, is settled first; one still open is reopened. See [[cloudcart-pay-checkout-flow]].

### Apple Pay on this page

The page runs on CloudCart's own payments address, so Apple Pay here does not depend on the store's domain. The Apple Pay sheet shows a CloudCart icon as the merchant icon, because Apple takes it from the page the shopper is on.

The rule on the **Apple Pay** switch still applies whichever display is chosen: while the store's domain is not verified, a switch that is off cannot be turned on ([[cloudcart-pay-apple-pay-domain]]).

### Express buttons

Display mode does not affect the express buttons on product pages, the cart and the checkout. They follow their own switches ([[cloudcart-pay-express-button-settings]]) and still need the store's domain for Apple Pay.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-settings]] — the Settings tab.
- [[cloudcart-pay-checkout-flow]] — inline and popup, payment window, resumed checkouts.
- [[cloudcart-pay-apple-pay-domain]] — Apple Pay on the store's domain.

## Open questions

(none)
