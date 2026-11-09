---
type: feature
nav_path: "Orders → Order details → Shipping → DPD Bulgaria waybill → price sync"
route_name: admin.internal.waybill
route_path: /admin/orders/action/shipping/:order_id/waybill
aliases: ["DPD waybill price", "DPD price sync", "Do you want to sync the prices", "Courier price differs from the charged shipping", "DPD COD differs from order total", "DPD international parcel size", "Искаш ли да синхронизираш цените", "Цената на куриера се различава от начислената доставка", "Товарителница DPD цена", "Спиди цена товарителница", "Промени сумата за наложен платеж", "Сума за наложен платеж", "Издаване на касова бележка", "Add a Fiscal Receipt", "Money transfer", "Опции преди плащане", "Разнос в събота", "Saturday delivery", "Чуплива пратка"]
tags: [apps, shipping, courier, bulgaria, waybill, cod, order-history]
plan_gates: []
created: 2026-11-03
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-dpdbulgaria-speedy]]. See the hub for credentials, channels and pricing.

# DPD Bulgaria — waybill price, COD and the order history

## Purpose

What happens when DPD's price on the waybill differs from the shipping the customer was charged, and how the order, the cash-on-delivery amount and the order history respond. Also the cash-on-delivery, fiscal-receipt and delivery options of the waybill form.

## Where to find it

Order page → **Shipping** → the DPD Bulgaria waybill form ([[orders-shipping-waybill]]). The history entry is on the order's history panel ([[orders-history-action-codes]]).

## What the merchant can do here

- Answer the sync question when generating a waybill on an unpaid order.
- Read the courier's price and the charged shipping side by side in the order history.

## Settings & fields

The waybill form asks:

> *"Do you want to sync the prices?"* / *"If you agree, the shipping price will be synced with the provider`s price"*
> *"Искаш ли да синхронизираш цените?"* / *"Ако се съгласиш, цената за доставка на поръчката ще се синхронизира с тази на доставчика"*

**Money transfer** (`money_transfer`), shown when the DPD contract allows it, also decides the cash-on-delivery payment type in the [[apps-n18-audit]] file: on, the payment method's own type; off, code 5. The switch's value is copied onto the order whenever its shipping is priced (at checkout, or when an edit to the order re-prices it), not read when the file is built. Until 26 October 2026 DPD orders were always copied as off, so earlier DPD cash-on-delivery sales carry code 5.

### Cash on delivery on the waybill form

Shown only when the order is paid by cash on delivery. The form is sent with **Generate Waybill** / *"Генериране на товарителница"*.

- **Edit the amount for cash on delivery** / *"Промени сумата за наложен платеж"* — a switch revealing **Total** / *"Сума за наложен платеж"*, the amount DPD collects. Left off, the amount is the computed one: with or without shipping by pricing type and payer side, less returned items and wallet ([[shipping-provider-mech-cod]]). When shipping is left out, only the shipping line is removed; every other line of the order total stays in. Turning it on is refused for a paid or completed order.
- The form has no option to add DPD's own price to the cash on delivery: the platform always sends DPD's "include shipping price" flag off and puts any shipping into the amount itself.
- **Add a Fiscal Receipt** / *"Издаване на касова бележка"* — shown when **Money transfer** is off, checked by default from the setting of the same name. The receipt lists the order's lines with their VAT groups, adjusted so it adds up to the amount collected; above 20 lines it becomes one line *"Order No. N"* / *"Поръчка №N"*.
- With **Money transfer** on, the cash on delivery is sent as a postal money transfer and no fiscal receipt is sent: the two exclude each other. The settings show **Money transfer** only when the contract allows a money transfer, and **Add a Fiscal Receipt** only when it allows a fiscal receipt and the store has VAT set up. What each pays out, and from when DPD stops allowing one of them for a sender, is DPD's contract; **Renew client information** re-reads the contract ([[apps-dpdbulgaria-speedy-credentials]]).

### Options before payment, Saturday delivery and Fragile

- **Options before payment** / *"Опции преди плащане"*: **No options** / *"Без опции"*, **Test before payment** / *"Тест преди плащане"*, **Open before payment** / *"Отваряне преди плащане"*. The default is the setting in the app's last box; the waybill can change it. It is sent only with a cash-on-delivery amount and never to a locker, where the form keeps **No options**. With an option chosen, **If the order is canceled the returning cost is paid by the merchant** / *"При отказ на пратка след преглед: връщането да е за моя сметка"* and a return service can be set.
- **Saturday delivery** / *"Разнос в събота"* — a switch on each waybill, sent to DPD as a Saturday-delivery request. It is not one of the **Services**, has no setting in the app, so it starts off on every waybill, and is not part of the checkout price.
- **Fragile** / *"Чуплива пратка"* — starts from the order's own flag. The order copies it from **The package contains fragile** when it is placed or its shipping is priced again, so changing the setting later does not change orders already placed.

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

DPD requires a parcel size for an international quote, so **Submit product sizes** (`item_sizes`) is forced on for it. When no box or size applies, one parcel is built from the product sizes ([[shipping-provider-mech-locker-fit]]), then the default sizes, then 10 cm. Bulgarian quotes keep the merchant's setting. How parcels are built in general: [[apps-dpdbulgaria-speedy-parcels]].

## Related

- [[apps-dpdbulgaria-speedy]] — hub.
- [[orders-shipping-waybill]] — the waybill flow.
- [[orders-history-action-codes]] — action code 65.
- [[api-order-shipping]] — `provider_amount` on the API.

## Open questions

None.
