---
type: feature
nav_path: "Orders → open the gift card's order → change status"
route_name: ""
route_path: ""
aliases: ["Cancel gift card", "Refund gift card", "Void gift card", "Gift card refund", "Disable gift card", "Анулиране на подаръчен ваучер", "Възстановяване на подаръчен ваучер", "Отказ от подаръчен ваучер"]
tags: [apps, gift-card, refunds, orders, wallet]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card — cancelling and refunding

> Part of [[apps-gift-card]]. See the hub for the other aspects.

## Purpose

How a gift card is cancelled. A card has no cancel button of its own: it is reversed when its order enters a negative status, and this page covers what that does to each card and to a wallet that already holds its value.

## Where to find it

On the order ([[orders-details]]). Open it from the **Order** column on [[apps-gift-card-cards]].

## What the merchant can do here

- Move the order to a negative status, such as cancelled or refunded, which reverses all of its cards.
- Refund the money separately through the order's payment ([[orders-payment-refund]]).
- Read the result on [[apps-gift-card-cards]], in the status badges on the order line, and in the order history.

## Settings & fields

No settings. Effect per card when the order enters a negative status:

| Card | Result |
|---|---|
| Active, not redeemed | Status becomes Disabled. The code stops working: `This gift card is no longer valid.` |
| Redeemed, credit untouched | The wallet credit becomes Rejected and leaves the balance |
| Redeemed, credit partly spent | Only the unspent part is removed. The spent part stays spent |
| Redeemed, credit fully spent | Nothing changes |

## Business rules

### Only through the whole order

There is no partial, per-card refund. A gift card line cannot go on a return, a withdrawal or a credit note ([[wallet-gift-instrument-checkout]]), so an order with three cards is reversed for all three together.

### The money back is a separate step

The status change handles the cards and the wallet. Returning the money to the buyer is a refund on the order; see [[orders-payment-refund]].

### The recipient's wallet can shrink

If the recipient has redeemed the card, a later reversal removes the unspent part from their wallet, even though it was the buyer who was refunded. The wallet balance never goes negative from this, and goods already bought with that money stay paid.

### One history entry

The order history gets one entry with the total removed from wallets, under `Money refunded to wallet` / `Възстановена сума в портфейл`. Cards that were never redeemed add nothing to this total.

### Reversal does not email

No email goes to the buyer or the recipient about the reversal. A recipient who then tries the code sees the message above. A scheduled **Send on** email for a disabled card is not sent ([[apps-gift-card-delivery]]).

### The PDF follows the status

An old PDF link now carries the `Invalid` / `Невалиден` or `Redeemed` / `Активиран` watermark ([[apps-gift-card-pdf-template]]).

### Compared with a top-up

A wallet top-up order is reversed the same way, by what is still free in its credit. See [[virtual-wallet-order-lifecycle]].

### Spending a gift card, then returning goods

That is a different flow. If goods were bought with the wallet and their order is cancelled, the wallet money returns to the same credit ([[virtual-wallet-order-lifecycle]]).

## Related

- [[apps-gift-card]] — hub.
- [[apps-gift-card-cards]] — card statuses.
- [[order-status-workflow]] — the negative statuses.
- [[orders-payment-refund]] — refunding the money.
- [[virtual-wallet-order-lifecycle]] — the wallet side.

## Open questions

None.
