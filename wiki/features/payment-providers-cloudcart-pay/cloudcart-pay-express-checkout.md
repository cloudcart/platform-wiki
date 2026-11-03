---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings → Express checkout"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay express checkout", "Express checkout", "Express checkout on product pages", "Apple Pay button on product page", "Google Pay button on product page", "Apple Pay button in the cart", "Google Pay button in the cart", "Buy now with Apple Pay", "One tap checkout", "Експресно плащане", "Експресно плащане в продуктовите страници", "Експресно плащане в количката", "Плащане с един клик", "Бутон Apple Pay в продукта", "Бутон Google Pay в количката"]
tags: [paymentproviders, payment-providers, cloudcart-pay, express-checkout, apple-pay, google-pay]
plan_gates: []
created: 2026-10-06
updated: 2026-11-03
source_count: 3
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, checkout flow, Apple Pay domain, refunds, saved card) and the six tabs.

# CloudCart Pay — express checkout

## Purpose

Express checkout puts **Apple Pay and Google Pay buttons** on the product page, in the cart, on the checkout page, and in the gift card and wallet top-up forms, so a shopper pays in one tap from the wallet sheet without filling in the checkout. This page covers when the buttons appear, who can buy, what the wallet sheet asks, and how the order and the payment are made. What each placement pays for is on [[cloudcart-pay-express-placements]]; the switches and the look of the buttons are on [[cloudcart-pay-express-button-settings]].

## Where to find it

- The settings: Settings → Payment methods → CloudCart Pay → **Settings** tab → **Express checkout** box (Експресно плащане). Address: `/admin/payment-providers/cloudcart_pay/settings`.
- The buttons: the storefront pages listed on [[cloudcart-pay-express-placements]].

## What the merchant can do here

- **Turn express checkout on or off** for product pages, the cart and the checkout.
- **Set the look of the buttons**: wallet order, layout, height, corner radius, theme.
- **Choose which wallets appear** with the **Apple Pay** and **Google Pay** switches in **Digital wallets**.

## Settings & fields

| Switch | Default | Placement |
|---|---|---|
| **Express checkout on product pages** (Експресно плащане в продуктовите страници) | On | Product page, quick view, gift card form, wallet top-up form. Also the master switch for the two below. |
| **Express checkout in the cart** | On | Cart page and cart side panel. |
| **Express checkout in the checkout** | Off | Checkout page. |

The full box, with its look settings, is on [[cloudcart-pay-express-button-settings]].

## Business rules

### When the buttons appear

All of these must hold:

- the CloudCart Pay method is **Active** and a connected account is linked;
- the placement's switch is on;
- at least one wallet is usable: **Google Pay** switched on, or **Apple Pay** switched on and usable on the store's domain ([[cloudcart-pay-apple-pay-domain]]).

On the page, the buttons hide themselves when the shopper's device or browser offers no wallet.

### Who can buy

- **Guests** do not see the buttons when the product or cart is digital, or when the store sells to registered customers only ([[settings-cart]]).
- **A buyer who is not signed in, whose wallet e-mail belongs to an account:** the order is placed on that account. With a new e-mail it is a guest order, with the name from the wallet.
- **Selling plans:** the buttons show for a signed-in customer with a plan selected, and stay hidden from guests. Renewals are charged to the card that paid ([[cloudcart-pay-save-card]]).

### What the wallet sheet asks

The sheet always asks for an **e-mail** and a **phone number**.

- **Something ships:** it asks for a **shipping address**, and a billing address as well, because Google Pay hands over the phone number only with it. The sheet sets no country limit: any address gets the couriers that quote it.
- **Nothing ships (digital):** no shipping address and no rates. The wallet's billing address becomes the order's only address, unless the store hides the billing address for digital carts (`checkout_hide_billing_address`). `checkout_digital_shipping` makes digital products shippable.
- **Gift card and wallet top-up:** no address at all. See [[wallet-gift-instrument-checkout]].

### Couriers and the total

For the address entered, the store quotes every active courier that **delivers to an address**, live, and lists them cheapest first, labelled "Courier (Service)". Delivery to a courier office or locker is not offered in express checkout. The sheet shows **Subtotal** (Междинна сума) and **Shipping** (Доставка), and the total updates when the shopper picks another option. The final amount is always worked out by the store, never taken from the shopper's device.

### Refused addresses

A wallet address with no courier is treated as not deliverable. A wallet address with no city, or no postcode unless `post_code_not_required` is on, is refused in the sheet and again at the order step, before anything is saved or charged. The shopper sees: *"The address in your wallet has no city or postcode. Please complete it or choose another address."* (В адреса във вашия портфейл липсва град или пощенски код. Моля, допълнете го или изберете друг адрес.)

### The order and the payment

When the shopper confirms in the wallet:

1. The order is created with the chosen courier option, and the address is saved on the customer.
2. The payment is taken on the merchant's connected account. If the card issuer asks for 3-D Secure, the check is completed there.
3. The shopper is sent to the order's confirmation page.

An express session stays payable for 2 hours, like other CloudCart Pay payments. If something fails, the wallet shows the payment as failed and the shopper sees the error. The payment status then updates like any other CloudCart Pay payment ([[cloudcart-pay-refunds-webhooks]]).

### Headless storefronts

Headless storefronts show the same buttons through the Storefront API, with some rules of their own: see [[headless-cloudcart-pay]].

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[cloudcart-pay-express-placements]] — where the buttons show and what each pays for.
- [[cloudcart-pay-express-button-settings]] — the switches and the look of the buttons.
- [[payment-providers-cloudcart-pay-settings]] — the Settings tab.
- [[cloudcart-pay-checkout-flow]] — the regular checkout with CloudCart Pay.
- [[cloudcart-pay-apple-pay-domain]] — Apple Pay domain registration.
- [[cloudcart-pay-save-card]] — selling plans and the card that paid.
- [[headless-cloudcart-pay]] — express and wallets on headless storefronts.

## Open questions

- Bulgarian labels of the newer switches and look settings (production translation table).
