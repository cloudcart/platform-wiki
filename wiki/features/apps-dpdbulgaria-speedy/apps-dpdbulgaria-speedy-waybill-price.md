---
type: feature
nav_path: "Orders → Order details → Shipping → DPD Bulgaria waybill → price sync"
route_name: admin.internal.waybill
route_path: /admin/orders/action/shipping/:order_id/waybill
aliases: ["DPD waybill price", "DPD price sync", "Do you want to sync the prices", "Courier price differs from the charged shipping", "DPD COD differs from order total", "DPD international parcel size", "Искаш ли да синхронизираш цените", "Цената на куриера се различава от начислената доставка", "Товарителница DPD цена", "Спиди цена товарителница"]
tags: [apps, shipping, courier, bulgaria, waybill, cod, order-history]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

> Part of [[apps-dpdbulgaria-speedy]]. See the hub for credentials, channels and pricing.

# DPD Bulgaria — waybill price, COD and the order history

## Purpose

What happens when DPD's price on the waybill differs from the shipping the customer was charged, and how the order, the cash-on-delivery amount and the order history respond.

## Where to find it

Order page → **Shipping** → the DPD Bulgaria waybill form ([[orders-shipping-waybill]]). The history entry is on the order's history panel ([[orders-history-action-codes]]).

## What the merchant can do here

- Answer the sync question when generating a waybill on an unpaid order.
- Read the courier's price and the charged shipping side by side in the order history.

## Settings & fields

The waybill form asks:

> *"Do you want to sync the prices?"* / *"If you agree, the shipping price will be synced with the provider`s price"*
> *"Искаш ли да синхронизираш цените?"* / *"Ако се съгласиш, цената за доставка на поръчката ще се синхронизира с тази на доставчика"*

**Money transfer** (`money_transfer`), shown when the DPD contract allows it, also decides the cash-on-delivery payment type in the [[apps-n18-audit]] file.

## Business rules

### Agreeing to the sync

| Waybill | What happens |
|---|---|
| **With a COD** | The order keeps its amounts, because the courier collects what was already sent. The courier's price is stored as the provider cost, converted to store currency, with the order's VAT split scaled to it: 9.25 becomes 7.71 + 1.54. Fields `provider_amount`, `provider_amount_with_vat`, `provider_amount_vat`, `provider_amount_without_vat`. |
| **Without a COD** | The order moves to the courier's price. |

### The history entry

When the merchant agrees on a waybill with a COD and the courier's price differs from the charged shipping, the order history gets entry 65: *"Courier price differs from the charged shipping"* / *"Цената на куриера се различава от начислената доставка"*, showing *"Shipping charged to the customer"* / *"Доставка, платена от клиента"*, *"Courier price (waybill)"* / *"Цена на куриера (товарителница)"* and the waybill number.

### Re-quotes from the admin

On couriers that add shipping to the COD themselves (Econt, Sameday, Pigeon Express, DPD Bulgaria, DPD Romania), shipping is counted once in the COD base, so re-saving the same office does not raise the price ([[shipping-provider-mech-cod]]).

### The street on the waybill

A waybill sends DPD's own street id when DPD confirms it. This avoids a fee DPD adds when it has to normalise a free-text address, which a checkout quote cannot show.

### International destinations

DPD requires a parcel size for an international quote, so **Submit product sizes** (`item_sizes`) is forced on for it. When no box or size applies, one parcel is built from the product sizes ([[shipping-provider-mech-locker-fit]]), then the default sizes, then 10 cm. Bulgarian quotes keep the merchant's setting.

## Related

- [[apps-dpdbulgaria-speedy]] — hub.
- [[orders-shipping-waybill]] — the waybill flow.
- [[orders-history-action-codes]] — action code 65.
- [[api-order-shipping]] — `provider_amount` on the API.

## Open questions

None.
