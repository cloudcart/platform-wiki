---
type: feature
nav_path: "Orders → Order details → Shipping → Fulfill products (Econt)"
route_name: apps.econt.waybill
route_path: /admin/orders/details/:order_id (Econt waybill modal)
aliases: ["Econt waybill form", "Econt waybill fields", "Генериране на товарителница", "Опис на пратката", "Econt inventory rows", "Econt опис fields", "Econt department per product", "Econt 9% VAT опис"]
tags: [apps, shipping, courier, bulgaria, econt, waybill, inventory, opis]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[apps-econt]]. See the hub for the other aspects (settings, addresses, waybill save, recipient mapping, pallet, COD / insurance).

# Econt — the waybill form

## Purpose

The form Econt opens when the merchant clicks **Fulfill products** (**Подготви за изпращане**) on an order whose shipping method is Econt. Its fields are pre-filled from the order and the Econt settings; the merchant reviews them and clicks **Generate Waybill** (**Генериране на товарителница**). What happens on that click is on [[econt-waybill-save]].

## Where to find it

[[orders-details]] → Shipping row → **Fulfill products**. The button and its conditions are on [[orders-details-shipping]].

## What the merchant can do here

- Review and change the pre-filled fields below, then generate the waybill.
- See, read-only, the inventory (опис) rows built for Econt.

## Settings & fields

Labels as the admin shows them (English / Bulgarian):

| Field | Pre-filled from | Notes |
|---|---|---|
| The package is sent from / Пратката се изпраща от | Default Econt address | Shown only with more than one sender address ([[econt-addresses-tab]]). |
| Description of the shipment / Съдържание на пратката | "Order: <number>" plus the order's content | Free text, sent up to 200 characters. |
| Packages / Пакети | Order products | Name and dimensions per package; **Pallet shipment / Палетна пратка** select (Colet / Pallet) when pallets are on ([[econt-pallet]]). |
| Who pay the shipping cost / Страна платец по подразбиране | Order's payer side | [[waybill-payer-side]]. |
| Enable SMS notifications / Активирай известие чрез SMS при доставка на пратката | Econt settings | |
| Deliver invoice before payment of COD / Предай фактура преди плащане на наложения платеж | Econt settings | The label warns it may raise the delivery price. |
| Acknowledgment of receipt / Активирай обратна разписка | Econt settings | Same warning. |
| Back documents request / Заявка за обратни документи | Econt settings | |
| Instructions / Инструкция за предаващия куриер | Empty | Sent only with the back-documents request. |
| Package count / Брой пакети, weight | The latest checkout quote, else the order's products | |
| Under **Допълнителни настройки от следния тип**: Payment after receiving / Разрешаване само на преглед на пратката преди заплащане, and Payment after testing / Разрешаване на преглед и тестване на пратката преди заплащане | Econt settings | Only one of the two; not for an Econtomat. |
| При отказ на пратка след преглед: доставката и връщането да са за моя сметка / …: връщането да е за моя сметка | Econt settings | Who pays when the customer refuses after inspection; only with one of the two options above. |
| Specify a sending date / Дата на изпращане | Today | |
| Delivery date / Дата на доставка | Empty | Optional; a list of days. |
| Priority hour / Фиксиран час на доставка | Order's delivery hour | Type and hour. |
| Package number / Номер на пакета | Empty | Optional. |
| Cash on delivery: switch and **Сума за наложен платеж** | A manually set COD amount, else the order's COD total | Hidden on a paid order. |
| Insurance / Обявяване на стойността на пратката и застраховане | The order's insurance flag and amount | |
| **Опис на пратката** | Order lines | Read-only table: item, unit price, quantity, total, inventory total. |

## Business rules

### Inventory (опис) rows

The опис is sent only when **Inventory Enable** is on ([[econt-settings-tab]]). Each row carries an inventory number, a description (the product name), weight, price and count, plus, in the one case below, an alternative-tax-group flag. No VAT rate, department or agreement number is sent per row. The cash-on-delivery agreement number goes once per shipment, not per row ([[econt-cod-insurance]]).

Rows besides products: tax and shipping lines, and, under a department agreement, negative discount and wallet lines. Zero-priced products and returned quantities are left out. With cash on delivery, the rows are adjusted so their total equals the cash-on-delivery amount.

### Department and VAT routing

There is no choice of department, or reserve department, per product, category, tax group or shipment. The only routing is automatic: with **Inventory Enable**, the department agreement and **I have an agreement with two tax groups** all on, every row whose product VAT rate is 9% is flagged for the alternative tax group. Without the two-tax-groups switch, nothing about VAT reaches Econt. Changing a product's VAT category therefore matters to Econt only through that 9% flag.

### Price sync question

On an order that is not paid or completed, Generate Waybill first asks **Do you want to sync the prices? / Искаш ли да синхронизираш цените?** Yes replaces the order's shipping price with the waybill's price and recomputes the totals; No keeps them. Details: [[econt-waybill-save]].

## Related

- [[apps-econt]] — hub.
- [[econt-waybill-save]] — what Generate Waybill does, errors, timeouts, duplicates.
- [[econt-waybill-recipient-mapping]] — how the recipient block is built.
- [[econt-cod-insurance]] — department agreement and discount lines in the опис.
- [[online-sales-without-cash-register]] — the regime behind the department agreement.
- [[orders-details-shipping]] — the Shipping row and its buttons.

## Open questions

None.
