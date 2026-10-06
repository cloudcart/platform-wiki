---
type: concept
nav_path: "Concept → CloudCart Admin mobile app → Orders"
aliases: ["Orders in the app", "Order details in the app", "Change order status from the phone", "Create a waybill from the phone", "Issue an invoice from the phone", "Refund from the app", "Поръчки в приложението", "Смяна на статус", "Създай товарителница и изпрати", "Издай фактура", "Отбележи като платена", "Синхронизирай плащането", "Възстанови сумата", "Запазени филтри"]
tags: [mobile-app, orders, fulfillment, waybill, invoice, payment, concepts]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 2
---

# CloudCart Admin app — working with orders

> Part of [[mobile-admin-app]]. See the hub for what the app is and how to get it.

## Definition

The **Orders** (Поръчки) tab of the CloudCart Admin app lists the store's orders and opens each one with most of what the web order page offers: status, payment, fulfilment and waybill, products, discounts, addresses, notes, invoice and printing. It works on the same orders as [[orders]] in the web admin, so a change made in the app is there at once, and the other way round. Creating new orders is on its own page: [[mobile-admin-app-new-order]].

## Scope

### The list

- **Search** — "Search orders, customers…".
- **Filter** by **Order status**, **Order total** (Exactly / Less than / More than / Not equal to), **Payment provider**, **Shipping provider** and **Date added**. The statuses offered include Pending, Authorized, Paid, Completed, Cancelled and Refunded.
- **Saved filters** (Запазени филтри) — "Set up the filters you use often, then save them under a name to apply them with one tap." They can be renamed and deleted.
- **Sort** — Newest first, Oldest first, Order number high to low or low to high.
- **Draft orders** (Чернови поръчки) — a list of their own ([[mobile-admin-app-new-order]]).

### Inside an order

| Area | What can be done in the app |
|---|---|
| **Status** | **Change Status** (Смяна на статус). **Archive Order** (Архивиране на поръчка) / **Unarchive Order** — see [[orders-archive]]. **History** shows what changed. |
| **Payment** | **Change payment method**. **Mark as paid** (Отбележи като платена) for an offline method, with an optional provider reference. **Sync payment** (Синхронизирай плащането) asks the payment provider for the current status. **Refund** (Възстанови сумата) — "The full amount goes back to the customer." See [[orders-details-payment]] and [[orders-payment-refund]]. |
| **Fulfilment** | **Fulfill Order** (Изпълнение на поръчка) / **Mark as Fulfilled** with a tracking number and tracking URL, or **Mark as unfulfilled**. **Notify customer** decides whether the customer is told. |
| **Waybill** | **Create waybill & ship** (Създай товарителница и изпрати) with the store's courier: delivery type (home / address, courier office, locker), office or locker, packages, and the courier's own options such as **Inspection before payment**. See [[orders-details-shipping]]. |
| **Products and discounts** | Add, edit or remove products and variants; change quantity and price; **Add product discount**; **Add order discount** (fixed amount or percentage). |
| **Customer and addresses** | **Edit customer**; edit the shipping and billing address, including company details (company ID, VAT number, accountable person). |
| **Notes** | The **Admin note**, kept for the staff, and the **Customer note** written at checkout. |
| **Invoice** | **Issue an invoice** (Издай фактура) — "This issues an invoice number for the order and emails the invoice to the customer. It cannot be undone." Then **Print invoice** / **Share invoice**. See [[orders-invoice]]. |
| **Printing** | **Print order**, **Print label** (Печат на етикет), and the **Packing Slip** (Стокова разписка); **Print** or **Share** from the phone. |
| **Shipping price** | Allow or disallow recalculation of the shipping price, as in the web admin ([[orders-details-actions]]). |
| **Euro** | **Convert prices to EUR** for an order still priced in BGN — "This action cannot be undone." See [[apps-bgn2eur]]. |

## Contrasts

- **App vs. web order page.** The app covers the everyday actions. When a courier's waybill form cannot be loaded, the app says "Could not load the carrier's waybill form. Fulfil this order from the admin panel instead." — the web admin ([[orders-details]]) is then the place to do it.
- **Mark as paid vs. Sync payment.** *Mark as paid* is the merchant's own statement that an offline payment arrived. *Sync payment* only asks the online payment provider what it knows.
- **Refund in the app** is always the full amount.

## Where it applies

Messages the merchant may meet, with their meaning:

| Message | Meaning |
|---|---|
| "Orders in BGN cannot be shipped. Convert the order to EUR first." (Поръчки в BGN не могат да се изпращат. Първо конвертирайте поръчката в EUR.) | A waybill cannot be made for an order priced in leva. Convert it first. |
| "The current courier has no integration, so offices cannot be listed." | The order's delivery method is not tied to a courier integration, so offices and lockers cannot be picked in the app. |
| "Before this order can be shipped, add a delivery address or check that the existing one is complete." | The address is missing or incomplete. |
| "The order was made through the "Quick Order" application. Therefore, you as the administrator need to enter a delivery address to send the order." | A Fast Order order arrives without a delivery address ([[apps-fast-order]]). |
| "This order cannot be invoiced yet." | The order is not yet in a state that can be invoiced ([[orders-invoice]]). |
| "Not included in your current plan" (Не е включено в текущия ви план) | The feature needs a higher plan ([[plan-gates]]). On iPhone the app gives no upgrade link. |

What a person can do here follows their access rights in the store ([[mobile-admin-app-sign-in]]).

## Related

- [[mobile-admin-app]] — hub.
- [[mobile-admin-app-new-order]] — creating orders, and abandoned carts.
- [[orders]] — the orders list in the web admin.
- [[orders-details]] — the web order page.
- [[orders-details-payment]] — payments on an order.
- [[orders-details-shipping]] — delivery and waybills on an order.
- [[orders-invoice]] — invoices.
- [[orders-archive]] — archived orders.
- [[mobile-admin-app-notifications]] — notifications about orders.

## Open Questions

- Whether the app's **Refund** works for every online payment provider or only some.
- Which couriers' waybill forms the app can show; the others fall back to "Fulfil this order from the admin panel instead".
