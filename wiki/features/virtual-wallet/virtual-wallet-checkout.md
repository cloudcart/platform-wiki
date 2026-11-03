---
type: feature
nav_path: "Storefront → Checkout → Payment step → Pay with wallet"
route_name: ""
route_path: ""
aliases: ["Pay with wallet", "Wallet at checkout", "Partial wallet payment", "Pay order from wallet", "Amount due", "Плащане с портфейл", "Плати цялата поръчка от портфейла", "За плащане", "Частично плащане с портфейл"]
tags: [wallet, store-credit, checkout, payment]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — paying at checkout

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

How a signed-in customer pays an order from the wallet: the box in the payment step, partial and full payment, and what the order shows afterwards. The merchant has no setting for this behaviour beyond the name of the method ([[virtual-wallet-settings]]).

## Where to find it

On the storefront, in the [[checkout-step-payment|payment step]] of the checkout. In the admin, the result shows on the order ([[orders-details]]).

## What the merchant can do here

- Rename the method with **Payment method name** on [[virtual-wallet-settings]].
- See the wallet line and **Amount due** on the order.

## Settings & fields

### The box

`Pay with wallet` / `Плащане с портфейл` is a checkbox section in the payment step. It shows when all of these hold:

- the customer is signed in, with a balance above 0;
- the cart is not a top-up or gift card cart ([[wallet-gift-instrument-checkout]]);
- the cart has no subscription line, because a subscription needs a card that can recur ([[apps-subscriptions]]).

| Control | Behaviour |
|---|---|
| Checkbox | Ticking it applies the most that can be spent |
| Balance line | `Available in wallet: %s` / `Налично в портфейла: %s` |
| Amount field and `Apply` / `Приложи` | Set a smaller amount. Typing 0 turns the wallet off |
| `Pay the whole order from the wallet` / `Плати цялата поръчка от портфейла` | Shown when the balance exceeds the total, shipping is settled, and only part is applied |

Error messages:

- `The amount exceeds your wallet balance (%s).` / `Сумата надвишава наличността в портфейла (%s).`
- `The amount exceeds the order total (%s).` / `Сумата надвишава стойността на поръчката (%s).`

## Business rules

### Partial payment

The rest goes through any method otherwise available, including cash on delivery. The gateway is charged only the amount due, and its breakdown carries a negative line `Payment from virtual wallet` / `Плащане от виртуален портфейл`. With cash on delivery, the courier collects only the amount due; see [[virtual-wallet-shipping-cod]].

### Full payment

When the wallet covers everything, all methods hide. The internal `wallet` payment provider is selected automatically and the payment completes at once with no gateway. This provider never appears in the list as a choice. If the customer lowers the amount, the normal methods come back.

### A tender, not a discount

The grand total, the VAT base and the invoice totals stay full. The summary adds a wallet line and shows `Amount due` / `За плащане` as the main figure. The wallet line uses the custom **Payment method name** if there is one, otherwise `Virtual wallet` / `Виртуален портфейл`. The admin order page moves its emphasis to the amount due in the same way.

### Which credit is spent first

The soonest-to-expire credit goes first, and never-expiring credit goes last. Among equal dates, the oldest goes first. See [[virtual-wallet-expiry]].

### What happens after the order is placed

The amount leaves the balance when the order is placed. Cancelling or editing the order can bring it back; see [[virtual-wallet-order-lifecycle]].

### Headless storefronts

The wallet box, balance and gift cards belong to the theme storefront. The headless storefront API has no operations for them. There, "wallet" refers to Apple Pay and Google Pay.

## Related

- [[virtual-wallet]] — hub.
- [[checkout-step-payment]] — the payment step.
- [[virtual-wallet-order-lifecycle]] — reserved, spent, returned.
- [[virtual-wallet-shipping-cod]] — COD and shipping when a wallet is used.
- [[virtual-wallet-vat-documents]] — how the payment appears on documents.
- [[apps-subscriptions]] — subscription carts pay by card.

## Open questions

None.
