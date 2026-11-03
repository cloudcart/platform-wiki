---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings → Express checkout → Placements"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["Express checkout placements", "Express checkout in the cart", "Express checkout in the checkout", "Express checkout gift card", "Express checkout wallet top-up", "Apple Pay on gift card", "Express buttons dimmed", "Express buttons missing on product", "Експресно плащане в количката", "Експресно плащане при поръчка", "Бутоните Apple Pay и Google Pay липсват", "Бутоните са сиви"]
tags: [paymentproviders, payment-providers, cloudcart-pay, express-checkout, apple-pay, google-pay, storefront]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects; the general rules of the buttons are on [[cloudcart-pay-express-checkout]].

# CloudCart Pay — express checkout placements

## Purpose

Where the Apple Pay and Google Pay express buttons show on the storefront, what each placement pays for, and when a placement hides or blocks them. It is the page for "why are the buttons not on this product?" and "what does the button in the cart buy?".

## Where to find it

The placements are on the storefront. Their switches are in Settings → Payment methods → CloudCart Pay → **Settings** tab → **Express checkout** box: see [[cloudcart-pay-express-button-settings]].

## What the merchant can do here

- **Turn the product, cart and checkout placements on or off.** The two forms below follow the first switch.
- **See what each placement pays for** and when it stands aside, to answer a shopper or set up the store.

## Settings & fields

| Placement | Switch | Pays for |
|---|---|---|
| **Product page**, also in quick view | **Express checkout on product pages** | The variant, quantity and options selected in the form, bundles included. |
| **Cart page** and **cart side panel** | **Express checkout in the cart** | The shopper's whole cart. |
| **Checkout page** | **Express checkout in the checkout** | The whole cart. |
| **Gift card form** ([[storefront-gift-card]]) | **Express checkout on product pages** | The gift card chosen in the form. |
| **Wallet top-up form** in the customer account ([[customer-wallet]]) | **Express checkout on product pages** | The amount chosen in the form. |

## Business rules

### Product page

The buttons sit under the add-to-cart block, after Fast Order. A product with variants shows them once a variant is chosen, and hides them while a choice the add-to-cart needs is missing from the form, such as an option combination that sold out. A product with no variants works from the first tap, also while the page is still loading. A bundle's buttons wait until every component is filled in. The shopper's own cart is not touched: the form becomes a single-use cart, through the same checks as the add-to-cart button (stock, cart limits, options, plan).

They are not offered for a product with a file option, as a wallet sheet cannot carry a file, or for a bundle without components. Cross-sell and up-sell popups have no buttons, because an offer joins the cart the shopper is building.

### Cart page and side panel

The buttons pay for the whole cart, read at the moment of the tap, so changes to quantities and discount codes carry over. The cart is emptied once its order is paid.

### Checkout page

The box sits right after the customer info step, above the delivery type and address choice. It disappears:

- once an address is on the cart, including an office or locker picked before signing in;
- once a payment method is picked or saved.

The store's default payment provider does not count as a choice until the cart reaches the payment step. Any other saved provider, such as a credit plan picked on the product page, hides the buttons.

### Whole-cart refusals

The cart and checkout placements are not offered when the cart is empty, holds a subscription, or is below the store's minimum order (`checkout_min_price`).

### Gift card and wallet top-up

The buttons in these two forms are for signed-in customers only. On tap the form becomes a fresh single-use cart, built by the same code as the page's own Buy or Top up button, and the wallet sheet asks for no address.

- A wallet top-up goes straight to its own checkout, so it never has buttons on a cart page.
- A gift card has its own cart page and gets the buttons there while **Express checkout in the cart** is on.
- Both isolated checkouts show the buttons on the checkout page while **Express checkout in the checkout** is on.

See also [[wallet-gift-instrument-checkout]].

### Blocked buttons

While the form cannot be paid (a refused amount, a missing required option), the buttons are dimmed and cannot be tapped. They are inert for a moment while the price loads. A tap on them says why: a refused amount or recipient e-mail shows under its field, as with the page's own Buy or Top up button; a missing option shows a message such as the "please choose" text. The total in the sheet follows the chosen variant, option, quantity or amount.

## Related

- [[cloudcart-pay-express-checkout]] — when the buttons appear, the wallet sheet, the order.
- [[payment-providers-cloudcart-pay]] — hub.
- [[cloudcart-pay-express-button-settings]] — the switches.
- [[product-detail]] — the product page.
- [[wallet-gift-instrument-checkout]] — gift card and top-up checkouts.

## Open questions

(none)
