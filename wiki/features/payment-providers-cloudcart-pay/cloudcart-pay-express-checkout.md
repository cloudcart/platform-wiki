---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings → Express checkout"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay express checkout", "Express checkout on product pages", "Apple Pay button on product page", "Google Pay button on product page", "Buy now with Apple Pay", "Експресно плащане", "Експресно плащане в продуктовите страници", "Coming soon express checkout"]
tags: [paymentproviders, payment-providers, cloudcart-pay, express-checkout, apple-pay, google-pay]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, checkout flow, Apple Pay domain, refunds, saved card) and the six tabs.

# CloudCart Pay — express checkout

## Purpose

Express checkout puts **Apple Pay and Google Pay buttons on the product page**, so a shopper can buy a single product straight from the wallet sheet without the cart or the checkout. This page covers the switch, its **Coming soon** state in the live environment, when the buttons appear, and how the order, shipping and payment are put together.

## Where to find it

- The switch: Settings → Payment methods → CloudCart Pay → **Settings** tab → **Express checkout** box (Експресно плащане) → **Express checkout on product pages** (Експресно плащане в продуктовите страници).
- The buttons: the storefront [[product-detail|product page]], under the variant and quantity selection.

## What the merchant can do here

- **Switch express checkout on or off** — while the store charges in the test environment.
- **See "Coming soon"** under the switch in the live environment, where it cannot be changed.
- **Choose which wallets appear** with the **Apple Pay** and **Google Pay** switches in **Digital wallets** — they apply to express checkout too.

## Settings & fields

| Field | What it does | Default | Notes |
|---|---|---|---|
| **Express checkout on product pages** | Shows the Apple Pay / Google Pay express button on product pages. | Off | In the live environment the switch is disabled and shows **Coming soon**. |
| **Apple Pay** / **Google Pay** (Digital wallets box) | Which wallet buttons appear. | On / On | With both off, no express button appears. |

Help text of the box: *"Show an Apple Pay / Google Pay express checkout button on product pages so shoppers can buy a single product without going through the cart and checkout."*

## Business rules

### Not yet available in the live environment

When CloudCart Pay runs in the **live** environment (the badge in the page header), the switch is locked off with **Coming soon**. Merchants on the live environment therefore cannot turn express checkout on yet. The merchant help article lists express checkout as a feature; the screen is what applies.

### When the buttons appear

All of these must hold:

- the CloudCart Pay method is **Active** and a connected account is linked;
- **Express checkout on product pages** is on;
- at least one of **Apple Pay** / **Google Pay** is on.

On the page, the buttons hide themselves when the shopper's device or browser offers neither wallet. Apple Pay also needs the store domain registered — see [[cloudcart-pay-apple-pay-domain]].

### What is bought

The express button buys **one piece of the product's default variant**. The price shown in the wallet starts from the product's (discounted) price; the final amount is always worked out by the store, never taken from the shopper's device. The shopper's own cart is not touched.

### Shipping in the wallet sheet

The wallet sheet asks for an **email**, a **phone number** and a **shipping address**. Addresses are limited to the store's country.

- For the address entered, the store quotes every active courier that **delivers to an address**, live, and lists them cheapest first. Delivery to a courier office or locker is not offered in express checkout.
- The sheet shows two lines: **Subtotal** (Междинна сума) and **Shipping** (Доставка), and the total updates when the shopper picks another courier option.
- If no courier can deliver to the address, the wallet treats the address as not deliverable.

### The order and the payment

When the shopper confirms in the wallet:

1. The order is created from that one product with the chosen courier option. A signed-in customer is used as is; for a guest, a customer is created from the wallet's email and name, and the address is saved.
2. The payment is taken on the merchant's connected account. If the card issuer asks for 3-D Secure, the check is completed in the wallet.
3. The shopper is sent to the order's confirmation page.

If something fails, the wallet shows the payment as failed and the shopper sees the store's general checkout error. The order's payment status is then updated like any other CloudCart Pay payment — see [[cloudcart-pay-refunds-webhooks]].

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-settings]] — the Settings tab with the switches.
- [[cloudcart-pay-checkout-flow]] — the regular checkout with CloudCart Pay.
- [[cloudcart-pay-apple-pay-domain]] — Apple Pay domain registration.
- [[product-detail]] — the storefront product page.
- [[checkout-flow]] — the regular checkout the express flow skips.

## Open questions

- When express checkout will be available in the live environment.
- Whether the express button is meant to follow the variant the shopper selected; it currently buys the default variant.
- Whether express checkout has been tested on real Apple and Android devices (the code marks the wallet flow as not yet run on real devices).
