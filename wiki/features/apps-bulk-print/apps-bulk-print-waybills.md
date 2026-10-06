---
type: feature
nav_path: "Orders → Enable Bulk print → Waybills print"
route_name: orders.bulk-print.list
route_path: /admin/orders/bulk-print?tab=waybills
aliases: ["Waybills print", "Generate waybills", "bulk waybill generation", "issue waybills for many orders", "Cancel waybill in bulk", "Execution", "Without waybill", "waybill not generated", "courier does not support automatic waybills", "Печат на товарителници", "Генерирай товарителници", "Анулирай товарителница", "Изпълнение", "Изпълнена", "С товарителница", "Без товарителница", "Генериране на товарителница"]
tags: [apps, bulk-print, orders, waybills, shipping, couriers]
plan_gates: ["bulk_print_daily_orders"]
created: 2026-10-05
updated: 2026-10-05
source_count: 11
---

# Bulk print — Waybills print (generating and cancelling waybills)

> Part of [[apps-bulk-print]]. See the hub for the other aspects (the screen, order slips, labels, runs, daily allowance).

## Purpose

The **Waybills print** tab issues courier waybills for many orders in one run, cancels them in bulk, and prints their labels. Each order goes through its own courier app with that app's settings, the same way as **Generate waybill** on the order page ([[waybill-generate-flow]]). This page covers the list, **Generate waybills** and **Cancel waybill**. Printing labels is in [[apps-bulk-print-labels]].

## Where to find it

**Orders → Enable Bulk print → Waybills print** (Печат на товарителници), at `/admin/orders/bulk-print?tab=waybills` ([[apps-bulk-print-mode]]).

## What the merchant can do here

- Filter and tick orders, then press:
  - **Generate waybills** (Генерирай товарителници) — for orders with no waybill yet.
  - **Cancel waybill** (Анулирай товарителница) — for orders that have one.
  - **Print waybills** (Отпечатай товарителници) and **Print the last generated (N)** — see [[apps-bulk-print-labels]].
- Hover the red warning icon under **Waybill** to see why the last attempt failed.

## Settings & fields

### Which orders are listed

Only orders that a courier could ship: not drafts, with **at least one physical product**, and with a **courier** chosen at checkout. Orders whose delivery method has no courier integration (for example the store's own delivery) and digital-only orders are not here.

### Filters

| Filter | Options |
|---|---|
| **Courier** (Куриер) | The store's installed couriers that can issue waybills. |
| **Waybill** (Товарителница) | **No waybill** (Без товарителница) / **With waybill** (С товарителница). |
| **Execution** (Изпълнение) | **Executed** (Изпълнена) — the order is fulfilled — or **Pending** (Чакаща). |
| **Number from** / **Number to** | An order number range. |
| **Status** | **Exclude declined**, **Pending**, **Paid**, **Completed**, **Declined** ([[apps-bulk-print-order-slips]]). |
| **Search term** | Order number, customer name, shipping city. |

There is no date filter on this tab.

### Columns

**Order #**, **City**, **Date**, **Courier**, **Amount**, **Status**, **Execution** (**Yes** when fulfilled) and **Waybill**. The **Waybill** cell shows:

| Cell | Meaning |
|---|---|
| A number | The waybill. |
| **Without waybill** (Без товарителница) | Fulfilled, but with no waybill number. |
| **No** | Not shipped yet. |
| Red warning icon | The last generation attempt failed; the reason is in the tooltip. A later success removes it. |

### When the buttons are active

All selected rows must qualify, or the button stays grey:

- **Generate waybills** — none has a waybill or a shipment yet.
- **Cancel waybill** — each has a waybill, or a shipment without a number.
- **Print waybills** — each has a waybill number.

## Business rules

### Generate waybills runs in the background

1. Today's allowance is taken for the selection first ([[apps-bulk-print-quota]]). An order whose slip was already printed today costs nothing more.
2. The system queues a background run: *"Waybill generation started for {count} order(s)"*.
3. Orders go to their couriers **one at a time**, one request each, so large selections take minutes. Numbers appear as they arrive.
4. A failed order is recorded and the run moves on. Its allowance is given back at the end.
5. At the end: *"{count} waybill(s) generated successfully"* (Успешно генерирани {count} товарителници), or *"Finished with {failed} error(s): {succeeded} of {total} completed."* Then the label size dialog opens for the orders that got a waybill ([[apps-bulk-print-labels]]).

Up to **1000** orders per run. **Stop** halts it between two orders ([[apps-bulk-print-runs]]). Waybills already issued stay issued.

### What is sent to the courier

Bulk generation fills in what the order page's waybill form would have, without asking:

- **One parcel**: the products' total weight (the courier's default weight where a product has none), the courier's default dimensions, contents *"#order number"*.
- **Send date**: today.
- **Who pays** the courier: as for the order.
- **Cash on delivery**: none for **Paid** or **Completed** orders. Otherwise a manually set amount on the order wins, else the courier's own calculation from the order total.
- **Insurance**: if the order has it.
- **Service**: the one the customer chose at checkout. If the courier app no longer allows it, the first allowed service.
- **Options switched on in the courier app's settings** (SMS, return documents, pay after inspection or test, and similar), as the order page pre-ticks them. For delivery to a **parcel machine**, the open-or-test-before-paying options are not sent.

A shipment that needs several parcels or other choices has to be issued from the order page ([[waybill-generate-flow]]).

### What issuing a waybill changes

It is the courier app's own waybill step, so the order becomes **fulfilled** and the usual effects follow ([[waybill-generate-flow]]).

If the order's delivery method has **no courier API** for waybills, the order is marked as shipped without a number. The cell then reads **Without waybill**, and the allowance is kept.

### Why a waybill is not issued

| Message | Cause |
|---|---|
| *"Order #N has no shipping provider."* (Поръчка №N няма избран куриер.) | No courier on the order. |
| *"Order #N already has a waybill."* (Поръчка №N вече има товарителница.) | Issued already. |
| *"Order #N is in a status that does not allow a waybill."* (Поръчка №N е в статус, който не позволява издаване на товарителница.) | Only **Pending**, **Paid** and **Authorized** orders can get one. |
| *"Orders in BGN cannot be shipped after 01.01.2026. Please convert the order to EUR."* | The order is in BGN. |
| *"Order #N has no unshipped physical products."* (Поръчка №N няма неизпратени физически продукти.) | The delivery method has no courier API and every physical product is already shipped. |
| *"Order #N no longer exists."* | Deleted since selection. |
| The courier's own message | Refused by the courier, for example an invalid address or service. |

Errors list the order's internal number, which differs from the displayed one when the store shows a hashed order number ([[settings-cart-limits-and-decrement]]).

### Cancel waybill is immediate

**Cancel waybill** does not queue. For each selected order it removes the shipment from the order, returns it to not fulfilled, and asks the courier to cancel the waybill. A return waybill on the order is cancelled too. The toast reads *"{count} waybill(s) cancelled"*. Cancelling is free. It is the bulk form of removing a waybill on the order page ([[waybill-remove-void]]).

## Related

- [[apps-bulk-print]] — hub.
- [[waybill-generate-flow]] — the one-order flow bulk generation repeats.
- [[waybill-remove-void]] — removing one order's waybill.
- [[orders-shipping-waybill]] — waybills on the order page.
- [[shipping]] — the courier apps whose settings are used.

## Open questions

- The selected rows are protected from a second **Generate waybills** only until the run first reports progress. After that, rows not yet processed can be selected and sent again (verify; possible double courier request).
- When some orders fail to cancel, the toast shows only the number cancelled and not which orders failed (verify whether this is intended).
- The full list of courier apps that can issue waybills in bulk is per store: the **Courier** filter lists the installed ones that can (verify a fixed list before quoting one to a merchant).
