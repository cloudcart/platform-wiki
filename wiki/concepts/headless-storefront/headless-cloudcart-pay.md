---
type: concept
nav_path: "Concept → Headless storefronts → CloudCart Pay express buttons"
aliases: ["Headless CloudCart Pay", "Headless express checkout", "cloudCartPayExpressSettings", "cloudCartPayExpressQuote", "cloudCartPayExpressSubmit", "cloudCartPayExpressCartSettle", "X-Storefront-Host", "Apple Pay on a headless storefront", "Apple Pay в Nitrogen", "Експресно плащане в Nitrogen"]
tags: [nitrogen, headless, storefront-api, cloudcart-pay, express-checkout, apple-pay, google-pay, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[headless-storefront]].

# Headless — CloudCart Pay express buttons

## Definition

A headless storefront can show CloudCart Pay's Apple Pay and Google Pay express buttons through the Storefront API: on a product or bundle page, and for the whole cart on its page and drawer. The buttons follow the merchant's settings ([[cloudcart-pay-express-button-settings]]). The field list comes from the API's own schema; this page gives the rules around it, including those that differ from a theme storefront.

## Scope

Covered: when to show the buttons, which domain Apple Pay is checked for, who the buyer is, how a cart is settled.

The embedded card form with its wallet buttons, and the repeated `form_validation` event, are on [[headless-checkout-submit]]. Request limits are on [[headless-storefront-limits]].

## Contrasts

- **Express buttons vs the embedded form** — express pays from the wallet sheet without a checkout; the embedded form sits in the storefront's own checkout and uses `cartSubmitForCompletion`.
- **API vs theme storefront: the wallet's e-mail** — on a theme storefront, a wallet e-mail that belongs to an account places the order on that account ([[cloudcart-pay-express-checkout]]). On the API it never does: the buyer is the signed-in customer, or a guest with the wallet's e-mail.
- **`domain` vs `X-Storefront-Host`** — `domain` is an argument of one query. The header goes with every call from the storefront's server, so it also covers the cart's buttons, the quote, the order and its settlement.

## Where it applies

### When to show the buttons

`cloudCartPayExpressSettings(domain:)` answers with the buttons as the merchant set them up, or `null` when they must not be shown: CloudCart Pay is off or not connected, the merchant switched the buttons off, or no wallet is enabled. Merchants change these settings in the admin, so refresh them at most once a minute.

Show the buttons only when the settings are not null **and** the product's or cart's `cloudCartPayExpress` is not null. In the cart, `onCart` must also be true. A cart's field is null when the cart is empty, holds a subscription, or is below the store's minimum order.

`guestAllowed` is false when the product or cart is digital or the store sells to registered customers only: hide the buttons from a buyer who is not signed in.

### Apple Pay and the domain

`wallets` lists Apple Pay only on a domain of the store that Apple has verified ([[cloudcart-pay-apple-pay-domain]]). The domain is taken in this order:

1. the `domain` argument;
2. the `X-Storefront-Host` header, as a bare host name, sent by the storefront's server with its private token;
3. the page the browser calls from (Origin, then Referer);
4. the API's own host.

A domain that is not one of the store's never has Apple Pay and is never registered. Without the private token the header is ignored. An unregistered domain of the store is registered on the way, as on a theme storefront.

### Pricing and placing the order

`cloudCartPayExpressQuote` prices the sheet, and is asked again on each address or courier change. Send one of `line`, `bundle` and `cartId`. For a product or bundle it does not use or change any cart the buyer has.

`cloudCartPayExpressSubmit` places and pays the order. The charge is the order's own total, never an amount the client sends. Without a selected courier or complete address the order is refused, with the reason in `userErrors`.

### A cart becomes the order

A cart (`cartId`) becomes the order and is removed once the payment is through. When `cloudCartPayExpressSubmit` returns a `clientSecret` (3-D Secure), call `confirmPayment` and then `cloudCartPayExpressCartSettle` before sending the buyer to `redirectUrl`. If the payment failed, the cart stays as it was. Never store or log `clientSecret`.

## Related

- [[headless-storefront]] — hub.
- [[cloudcart-pay-express-checkout]] — the buttons, the wallet sheet, the order.
- [[cloudcart-pay-express-button-settings]] — the merchant's settings.
- [[cloudcart-pay-apple-pay-domain]] — domain verification.
- [[headless-checkout-submit]] — the embedded form and `form_validation`.
- [[headless-storefront-limits]] — request limits.
- [[headless-storefront-api]] — tokens and headers.

## Open Questions

(none)
