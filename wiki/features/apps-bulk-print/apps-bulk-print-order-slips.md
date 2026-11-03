---
type: feature
nav_path: "Orders → Enable Bulk print → Orders print"
route_name: orders.bulk-print.list
route_path: /admin/orders/bulk-print
aliases: ["Orders print", "Print selected", "bulk print order slips", "order slips in batches", "packing slips in bulk", "Printed column", "Not printed filter", "Print status", "Exclude declined", "Печат на поръчки", "Отпечатай избраните", "Статус на печат", "Отпечатани", "Неотпечатани", "Без отказаните", "Разписки за поръчки", "стокови разписки"]
tags: [apps, bulk-print, orders, order-slips, packing-slip, pdf]
plan_gates: ["bulk_print_daily_orders"]
created: 2026-10-05
updated: 2026-10-05
source_count: 10
---

# Bulk print — Orders print (order slips)

> Part of [[apps-bulk-print]]. See the hub for the other aspects (the screen, waybills, labels, runs, daily allowance).

## Purpose

The **Orders print** tab turns a selection of orders into **order slips** — the same document as **Print order** on an order's page — collected in PDF files of 50 orders each. Each order printed this way is stamped **Printed**, so the **Not printed** filter shows what is still waiting, across days and across computers.

## Where to find it

**Orders → Enable Bulk print → Orders print** (Печат на поръчки), the first tab, at `/admin/orders/bulk-print` ([[apps-bulk-print-mode]]).

## What the merchant can do here

- Filter the list, tick orders (a whole page at once), and press **Print selected** (Отпечатай избраните).
- See next to the button how the selection will be split: *"{count} selected ({batches} batch of {size})"*.
- Sort by **Order #**, **Date** or **Amount**. The list opens newest first.

## Settings & fields

### Filters

| Filter | Options / behaviour |
|---|---|
| **Print status** (Статус на печат) | **Not printed** (Неотпечатани) / **Printed** (Отпечатани). |
| **Number from** / **Number to** (Номер от / Номер до) | An order number range. Empty or 0 is ignored. |
| **Date from** / **Date to** (Дата от / Дата до) | The date the order was placed. Either end can be left open. |
| **Status** (Статус) | **Exclude declined** (Без отказаните) — everything except declined and cancelled — or exactly **Pending**, **Paid**, **Completed**, **Declined**. |
| **Search term** (Търсене) | *"Name/city/number..."* — order number, customer first or last name, shipping city. |

### Columns

| Column | Shows |
|---|---|
| **Order #** | Order number and **From** customer (their order count). |
| **City** | Shipping city. |
| **Date** | Date and time placed. |
| **Delivery** (Доставка) | The shipping method. |
| **Payment method** (Начин на плащане) | The payment method. |
| **Amount** (Сума) | Order total. |
| **Status** | Order status badge. |
| **Waybill** (Товарителница) | The waybill number, or **No**. |
| **Printed** | **Yes** / **No**. |

## Business rules

### What happens on Print selected

1. The selection is checked against today's allowance and the allowance is taken **before** anything is printed. If the selection does not fit, nothing is queued and the pack picker opens ([[apps-bulk-print-quota]]).
2. The system queues a background run. The toast reads *"Print started for {count} order(s)"* and the progress panel appears ([[apps-bulk-print-runs]]).
3. The orders are split into files of **50 orders**. Each file appears as soon as it is written, so printing can start before the run ends.
4. An order is stamped **Printed** only once its slip is in a file. An order that failed stays **Not printed** and gets its allowance back.

At most **1000** orders per run: *"You cannot process more than 1000 orders at once."* (Не можете да обработите повече от 1000 поръчки наведнъж.)

### What a slip contains

The slip depends on the store's **Packing slip / Order print** template ([[settings-invoicing-html-templates]]):

- **The store saved its own template** → every slip uses it, the same template as **Print order** on the order page ([[orders-details-header]]) and the Pick & Pack terminal ([[apps-pick-and-pack]]).
- **The store never saved one** → the slip is the order page as it prints from the browser: products with SKU, barcode, variant and option lines, totals with shipping and weight, payment and shipping method, the order history, the customer, and both addresses. A discounted product shows its new and old price, but the discount lines under the product name are left out.

Slips are A4, one order starting on a new page. They are made as PDF on CloudCart's side rather than by the browser. The app adapts side-by-side columns and a logo wider than the page so that a slip comes out as it does from the browser, but it is a separate rendering.

### The internal note prints too

On the default slip (no template of the store's own), the comment box holds the order's **internal note** as on the order page, and the customer's note above it. A merchant who puts slips into parcels should know the internal note goes with them.

### Printing again

**Printed** does not block anything. A printed order can be selected and printed again. The stamp is moved to the latest print. Printing the same order again **on the same day** costs no extra allowance.

### Only slips stamp "Printed"

Printing waybill labels does not set **Printed**. The header's **Not printed** number and the **Print status** filter follow order slips only.

### Why a slip run can fail

- An order deleted since it was selected: *"Order #N no longer exists."* (Поръчка №N вече не съществува.)
- No slip came out for any order: the run ends **Failed** and the first reason is shown ([[apps-bulk-print-runs]]).

## Related

- [[apps-bulk-print]] — hub.
- [[settings-invoicing-html-templates]] — the slip template.
- [[orders-details-header]] — **Print order** for one order, free of the allowance.
- [[apps-pick-and-pack]] — the warehouse terminal that prints from the same template.

## Open questions

- **Number from / Number to** filter on the internal order number. A store that shows a different order number ([[settings-cart-limits-and-decrement]]) may get a range that does not match what it sees (verify).
- Whether a slip from the store's own template spans pages the same way as in the browser for very long orders (verify).
- The order of slips inside a file: the selection is re-read from the store's orders before printing, which suggests order-number order rather than the order of ticking (verify).
