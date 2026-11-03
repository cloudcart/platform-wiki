---
type: concept
nav_path: "Concept → Top-up and gift card checkout rules"
route_name: (none)
route_path: (none)
aliases: ["Wallet top-up checkout", "Gift card checkout", "Isolated cart", "Top-up cannot be combined", "This product is purchased on its own", "Top-up payment methods", "Gift card payment methods", "Зареждане на портфейл при плащане", "Този продукт се купува самостоятелно", "Подаръчен ваучер плащане"]
tags: [wallet, gift-card, checkout, cart, orders, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Top-up and gift card checkout rules

## Definition

A [[virtual-wallet|wallet top-up]] and a [[apps-gift-card|gift card]] are bought as stored value, not as goods. The platform keeps them on a checkout of their own, in a cart that holds nothing else, and applies one shared set of rules. The value on such an order is spent later, on other orders.

Internally both are hidden digital products, with `type_digital` set to `wallet` or `gift_card`.

## Scope

### A cart of their own

- They are sold only in a separate cart. The customer's main cart is not touched.
- Mixing is refused: `This product is purchased on its own and cannot be combined with other items in the cart.` / `Този продукт се купува самостоятелно и не може да се комбинира с други артикули в количката.`
- A top-up goes straight from the wallet page to checkout, one amount at a time. A gift cart can hold several gifts ([[apps-gift-card-purchase]]).
- A paid order deletes only that cart. A cancelled payment returns the customer to the same separate checkout ([[checkout-return]]).

### Payment

- **Online payment methods only.** Only providers marked as online payment are offered and accepted. Which ones qualify depends on the methods active on the store ([[settings-payment-providers]]).
- CloudCart Pay's express buttons work for signed-in customers, with no address asked ([[cloudcart-pay-express-checkout]]).
- The wallet box is hidden, so a top-up or gift card cannot be paid from the wallet.

### A registered customer

A customer account is needed at checkout, since guests are not allowed on digital carts. A guest can fill a gift cart, then signs in or registers at checkout.

### What is left out of the checkout

- No discounts: discount, code and cart-rule pipelines skip these lines. The discount code box and the countdown popup are hidden.
- No billing address and no shipping step.

### After the order

- **Emails:** no generic order confirmation, status-change, shipped or file-download email. Each has its own: [[virtual-wallet-emails]] and [[apps-gift-card-emails]].
- **Documents:** no VAT, invoice or receipt at purchase ([[virtual-wallet-vat-documents]]).
- **Returns:** the lines cannot go on a return, a withdrawal or a credit note. Reversal comes from the order's status ([[virtual-wallet-order-lifecycle]], [[apps-gift-card-reversal]]).
- **Repeat order:** hidden and refused: `Repeat order is not available for wallet top-ups and gift cards.`

### Where they do not appear

- They are not offered in, and do not trigger, cross-sell, up-sell or bumper offers.
- They are not in abandoned-cart tracking or recovery.
- They are not in the catalog, search, feeds, the Google Sheets export or product pickers. Their product URLs return 404.
- An admin cannot add them to an order: `Gift cards and wallet top-ups cannot be added to an order manually — they are sold only through their own checkout.` / `Подаръчни карти и захранвания на портфейл не могат да се добавят към поръчка ръчно — те се продават само през собствения си чекаут.`

## Contrasts

- **Top-up vs gift card.** A top-up credits the buyer's own wallet when paid, and is a core feature. A gift card issues a code that anyone with an account can redeem later, and needs the app.
- **Buying value vs spending it.** These rules apply when value is bought. Spending goes through the normal checkout on a normal order ([[virtual-wallet-checkout]]), where any available method can pay the rest, including cash on delivery.
- **Internal digital products vs digital products.** Merchants choose only `file` and `page` ([[digital-products]]). `wallet` and `gift_card` are internal, and show in webhook and order payloads.
- **Voucher method.** The manual [[payment-providers-voucher|Voucher]] payment method is not online, so it cannot pay for either.

## Where it applies

- [[customer-wallet]] — buying a top-up.
- [[storefront-gift-card]] — buying a gift card.
- [[storefront-cart]] — the refusal on mixing.
- [[checkout-step-payment]] — which methods are offered.
- [[checkout-return]] — where a cancelled payment leads.
- [[customer-orders]] — no repeat order.
- [[orders-add-wizard]] — no adding by an admin.
- [[orders-returns-refunds]] — not returnable.
- [[abandoned-cart-eligibility]] — not tracked.
- [[marketing-cross-sell]] / [[marketing-up-sell-list]] — not offered.
- [[settings-invoicing]] — no document at purchase.

## Related

- [[virtual-wallet]] — the wallet.
- [[apps-gift-card]] — the gift card app.
- [[digital-products]] — ordinary digital products.
- [[virtual-wallet-vat-documents]] — VAT and documents.
- [[cloudcart-pay-express-checkout]] — the express buttons.

## Open Questions

- Which online methods each store has active decides what a customer can pay with; there is no fixed list. A store with none active cannot sell either, and the wallet page warns about it ([[virtual-wallet]]).
