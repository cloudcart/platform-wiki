---
type: feature
nav_path: "Orders → open an order → Virtual Wallet amount"
route_name: ""
route_path: ""
aliases: ["Wallet reserved", "Wallet refund on cancel", "Money refunded to wallet", "Wallet returned after cancel", "Reverse wallet top-up", "Възстановена сума в портфейл", "Връщане в портфейла при отказ", "Анулиране на зареждане на портфейл"]
tags: [wallet, store-credit, orders, order-status, refunds]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — reserved, spent, returned

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

What an order does to the wallet after checkout: when the amount leaves the balance, what brings it back, and what happens when a top-up order is cancelled or refunded.

## Where to find it

There is no screen of its own. The effects show on the order page ([[orders-details]]), in its history, on [[virtual-wallet-transactions]] and on the customer's [[customer-wallet]] page.

## What the merchant can do here

- Change the order's status. A negative status returns the wallet money.
- Edit the order. A total below the wallet amount returns the excess.
- Read the movement in the order history, under `Money refunded to wallet` / `Възстановена сума в портфейл`.

To refund a return into the wallet as a new credit, see [[orders-returns-refunds]].

## Settings & fields

No settings. Effects by event:

| Event on the order | Effect on the wallet |
|---|---|
| Order placed | The amount is reserved and leaves the balance at once |
| Order paid or completed, or a shipment created | The reservation becomes final |
| Shipment removed and the order back to pending | Back to reserved. The balance does not change |
| Order edit raises the total | The amount due absorbs it. The wallet is never increased automatically |
| Order edit drops the total below the wallet amount | Only the excess returns to the balance, with one history entry and the email `wallet_adjusted` |
| Order enters a negative status (voided, timed out, cancelled, failed, refunded, and so on) | The whole wallet amount returns to the original credits, with one history entry and no email |

## Business rules

### Returned money goes back to the same credits

Returning wallet money does not create a new credit. If one of those credits expired in the meantime, its part does not revive and stays out of the balance. See [[virtual-wallet-expiry]].

This differs from **refunding a return to the wallet**, which always creates a new credit with its own expiry ([[orders-returns-refunds]]). On an order in a negative status the two are kept apart: the return credits only the value not already paid by wallet.

### Newest part released first on an edit

When an edit returns part of the wallet amount, the most recently allocated part goes back first, so the soonest-to-expire credit stays on the order.

### Reversing a top-up order

When a top-up order enters a negative status, the credit it created is reversed by what is still free:

| State of the credit | Result |
|---|---|
| Untouched | Status becomes Rejected |
| Partly spent | Only the free part is removed. The spent part stays spent |
| Fully spent | Nothing changes |

The balance never goes negative from this. One history entry on the order records the total removed. The money back to the buyer is a separate refund on the order; see [[orders-payment-refund]].

Gift cards follow the same logic through their own order; see [[apps-gift-card-reversal]].

### Top-up lines are not goods

A top-up line cannot go on a return, a withdrawal or a credit note. Reversal only comes from the order's status. See [[wallet-gift-instrument-checkout]].

### Payment on a fully wallet-paid order

The internal `wallet` provider completes the payment at once, so such an order is already paid when placed. See [[virtual-wallet-checkout]].

## Related

- [[virtual-wallet]] — hub.
- [[order-status-workflow]] — the statuses, including the negative ones.
- [[orders-returns-refunds]] — refunding a return to the wallet.
- [[virtual-wallet-emails]] — the `wallet_adjusted` email.
- [[apps-gift-card-reversal]] — the gift card equivalent.

## Open questions

None.
