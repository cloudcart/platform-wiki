---
type: feature
nav_path: "Orders → open an order → Shipping (order paid in part from the wallet)"
route_name: ""
route_path: ""
aliases: ["Wallet and cash on delivery", "Wallet COD amount", "Wallet sender pays shipping", "Наложен платеж с портфейл", "Портфейл и наложен платеж", "Подател плаща доставката при портфейл"]
tags: [wallet, store-credit, shipping, cod, couriers]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — shipping and cash on delivery

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

How a wallet payment changes what the courier collects, how the shipping price is worked out, and who pays for shipping.

## Where to find it

There is no setting. The effects show at checkout, on the waybill form of the order ([[orders-details]]), and on the courier's document.

## What the merchant can do here

- Read the reduced cash-on-delivery amount on the waybill.
- For Econt, choose whether the wallet appears as its own line on the receipt, through the department agreement. See below.

## Settings & fields

No settings of its own. Two courier settings affect the result:

| Setting | Where | Effect here |
|---|---|---|
| Who pays shipping (receiver-pays option) | The courier's settings, for example [[apps-econt]] | Overridden when any wallet amount is used |
| Department agreement | [[apps-econt]] | Decides whether the wallet appears as a negative line |

## Business rules

### The COD amount is what is left to pay

The cash-on-delivery amount on the waybill equals the amount due after the wallet. All couriers use one shared calculation, so this holds across them, including Wolt's cash to collect and the prefilled Sameday waybill.

### The COD fee follows the reduced amount

The checkout re-quotes shipping when the wallet changes. A courier's COD fee is calculated on the reduced amount, so a wallet can lower the shipping price and, with it, the order total.

### Any wallet use means the sender pays shipping

Any wallet amount, even a partial one, makes the shipping **sender pays**, overriding a store setting of receiver pays. The waybill drops the receiver option.

### A fully wallet-paid order has no COD

It is treated as prepaid, the same as an order paid online. See [[virtual-wallet-checkout]].

### After the order is placed

If the order is edited and wallet funds return to the balance ([[virtual-wallet-order-lifecycle]]), the waybill reads the current wallet amount when it is created.

Creating a shipment makes the wallet amount final. Removing the shipment and returning the order to pending puts it back to reserved.

### On the courier's receipt

- **Econt:** with a department agreement, the wallet appears as a negative line `Payment from virtual wallet` / `Плащане от виртуален портфейл`. Without one, or on an agreement with two tax groups when the order has 9% goods, it is spread across the line prices.
- **DPD and other couriers:** the wallet is spread across the line prices, so the parcel contents match what the courier collects.

See [[virtual-wallet-vat-documents]] for the store's own documents.

### Sameday quotes

Sameday's checkout quote and its waybill cost come from Sameday's own service and can differ. (verify)

## Related

- [[virtual-wallet]] — hub.
- [[virtual-wallet-checkout]] — partial and full payment.
- [[apps-econt]] — the department agreement.
- [[shipping]] — the courier hub.
- [[online-sales-without-cash-register]] — the courier's fiscal receipt on COD orders.

## Open questions

- Whether Sameday's quote and waybill cost still differ after a wallet payment. (verify)
