---
type: feature
nav_path: "Storefront → Gift cards page → Buy"
route_name: ""
route_path: ""
aliases: ["Buy a gift card", "Gift card purchase", "Gift card code issued", "Several gift cards one order", "Покупка на подаръчен ваучер", "Издаване на код за подаръчен ваучер"]
tags: [apps, gift-card, checkout, orders]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card — purchase and issuing codes

> Part of [[apps-gift-card]]. See the hub for the other aspects.

## Purpose

How a customer buys a gift card, what the order looks like, and when the codes appear.

## Where to find it

The purchase starts on [[storefront-gift-card]] at `/gift-card`. In the admin, the result shows as an order ([[orders-details]]) and as rows on [[apps-gift-card-cards]].

## What the merchant can do here

- Set what is on sale on [[apps-gift-card-settings]].
- Keep at least one online payment method active, since the card can be paid in no other way ([[wallet-gift-instrument-checkout]]).
- Follow the order and its cards in the admin.

An admin cannot add a gift card to an order by hand. See [[wallet-gift-instrument-checkout]].

## Settings & fields

No settings of its own. The buy form's fields are on [[storefront-gift-card]]. What the buyer enters becomes options on the order line:

| Line option | Comes from |
|---|---|
| `Recipient email` | **Recipient email (optional)** |
| `Recipient name` | **Recipient name (optional)** |
| `Message` | **Message (optional)** |
| `Send on` | **Send on (optional)** |

## Business rules

### The gift cart

**Buy** adds the card to a separate gift-only cart. It never touches the shopper's main cart and cannot hold products. It can hold several gifts:

- Different recipients or amounts are separate lines.
- Identical gifts merge and raise the quantity.

The shopper goes to checkout from that cart. The express buttons on the page ([[cloudcart-pay-express-checkout]]) are for signed-in customers and buy just the gift chosen in the form, leaving the gift cart alone.

### Checkout rules

A gift card purchase follows [[wallet-gift-instrument-checkout]]: a registered customer is needed at checkout, online payment methods only, no discounts, no billing address, no shipping.

### When codes are issued

Codes are issued when the payment completes, or when the order's status becomes paid or completed. Retried payment notifications never issue twice: the platform only issues what a line is still owed.

**One card, with its own code, per unit.** Buying 3 at 25 gives three codes of 25, not one of 75. All cards on a line share its recipient details.

Until the payment completes, no code exists. If the customer cancels the payment, they return to the same gift checkout ([[wallet-gift-instrument-checkout]]).

### The code

Each code has 16 characters, shown as `XXXX-XXXX-XXXX-XXXX`. It uses letters and digits, leaving out characters that are easy to confuse, so a code read aloud or from paper is entered correctly. See [[apps-gift-card-redeem]].

### Value and currency

The card's value is the line's unit price, in the order's currency. A top-up or gift card line has no VAT and no invoice ([[virtual-wallet-vat-documents]]).

### What happens next

The emails go out in the background once the cards exist ([[apps-gift-card-delivery]]). The buyer also finds the cards under My account → [[customer-gift-cards|Gift cards]].

### Errors on the buy form

- `Gift cards are not available at the moment.`
- `Please choose a valid gift-card amount.`

## Related

- [[apps-gift-card]] — hub.
- [[storefront-gift-card]] — the buy form.
- [[wallet-gift-instrument-checkout]] — the checkout rules.
- [[apps-gift-card-delivery]] — who gets the code.
- [[apps-gift-card-cards]] — the issued cards in the admin.

## Open questions

None.
