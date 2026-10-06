---
type: feature
nav_path: "Orders → Enable Bulk print → Waybills print → Print waybills"
route_name: orders.bulk-print.list
route_path: /admin/orders/bulk-print?tab=waybills
aliases: ["Print waybills", "bulk print waybill labels", "A6 thermo", "A4 labels", "label size", "thermal labels", "Print the last generated", "Print in another size", "Print waybill labels", "The courier did not return a label", "Отпечатай товарителници", "A6 термо", "Етикети на товарителници", "етикетен принтер", "термо етикети", "Куриерът не върна етикет"]
tags: [apps, bulk-print, waybills, labels, pdf, printing, couriers]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 7
---

# Bulk print — printing waybill labels (A6 / A4)

> Part of [[apps-bulk-print]]. See the hub for the other aspects (the screen, order slips, waybill generation, runs, daily allowance).

## Purpose

Once orders have waybills, **Print waybills** collects their courier labels into PDF files, in the paper size the merchant picks for that run: **A6 thermo** for a label printer or **A4** for an office printer. Label printing is **free**: it never counts against the daily allowance.

## Where to find it

- **Orders → Enable Bulk print → Waybills print** → tick orders → **Print waybills** (Отпечатай товарителници) ([[apps-bulk-print-waybills]]).
- The size dialog that opens by itself when a **Generate waybills** run finishes, and the **Print the last generated (N)** button next to **Print waybills**.
- **Documents** tab → **Print in another size** or **Print waybill labels** on a past run ([[apps-bulk-print-runs]]).

## What the merchant can do here

- Pick the size for every label run.
- Print the labels of the waybills just generated without finding the orders again.
- Print a finished label run again in the other size.

## Settings & fields

### The size dialog

Title **Print waybills**, text *"In what size should the {count} waybill(s) be printed?"* (В какъв размер да бъдат отпечатани {count} товарителници?):

| Option | Tooltip |
|---|---|
| **A6 thermo** (A6 термо) | *"One label per page, for a label printer."* (По един етикет на страница, за етикетен принтер.) |
| **A4** | *"The full-sheet waybill, for an office printer."* (Товарителницата на цял лист, за офис принтер.) |

Buttons **Print** (Печат) and **Cancel** (Отказ). The dialog opens on **A6 thermo**. It does not remember the last choice. Nothing is queued until **Print** is pressed.

**Print waybills** is active only when every selected order has a waybill number.

## Business rules

### A label run

1. The system queues a background run: *"Print started for {count} waybill(s)"*.
2. For each order, the label is fetched from **its courier**, so one file can hold labels of several couriers.
3. Labels go into files of **50 orders** ([[apps-bulk-print-runs]]). A multi-parcel shipment gives the labels of all its parcels. Each page keeps the size the courier sent, so one file can mix sizes.
4. Up to **1000** orders per run.

### How the size reaches each courier

The choice is passed to each courier in the courier's own terms. Couriers do not all offer both:

- **Econt**: A6 asks for the 10×15 label, A4 for the full sheet.
- **Berry**: always the A4 sheet, whatever is picked.
- Couriers that hand out their label as a link, other than Econt: the size choice has no effect. The label comes as the courier serves it.
- The other couriers receive the size in their own wording, the same as their print dialog on the order page.

When a file comes out in an unexpected size, try the other option, then check the courier app's own print setting ([[waybill-print-pdf]]).

### Retries before giving up

Couriers under load often refuse a burst of requests. Each label is therefore requested up to **3 times**, **2 seconds** apart, and link-based labels **5 at a time** with a **30-second** wait each. A reply that is not a PDF, such as a courier's error or login page, counts as a failure. Only after the last attempt is the order reported.

### Why a label is missing

| Message | Cause |
|---|---|
| *"Order #N has no waybill."* (Поръчка №N няма товарителница.) | Removed since selection. |
| *"Order #N has no shipping provider."* | No courier, or its app is no longer installed. |
| *"The courier of order #N does not support automatic waybills."* (Куриерът на поръчка №N не поддържа автоматични товарителници.) | A link-based courier, but no label link was stored with the waybill. |
| *"The courier did not return a label for order #N."* (Куриерът не върна етикет за поръчка №N.) | Still no PDF after the retries. |
| The courier's own message | The courier refused the request. |

The other labels still go into the file. A run that produced **no file at all** ends **Failed**.

### Right after a generation run

When **Generate waybills** finishes, the size dialog opens by itself for the orders that **got** a waybill. Pressing **Print** queues the labels: *"Printing the {count} new waybill(s) — the PDF appears below when it is ready."* If the dialog was closed, **Print the last generated (N)** opens it again for the same orders. That button lasts until the merchant leaves the tab or reloads. After that, use **Print waybill labels** on the run in **Documents**.

The dialog opens only when the generation run ends **Done**, including **Done with N error(s)**. It does not open after a run that **Failed** or was **Stopped**.

### Printing again in another size

On a finished label run in **Documents**, **Print in another size** opens the dialog on the **other** size. It queues a **new** run for the same orders: *"Printing {count} waybill(s) in {size} — the new file appears in this list when it is ready."* The original run stays with its size badge, so A6 and A4 files are told apart.

On a finished generation run, **Print waybill labels** prints only the orders that got a waybill. The dialog opens on A6.

Orders deleted since the first run are left out. A run without saved orders answers *"This run cannot be printed again. Select the orders in the Waybills print tab instead."*

### Not the same as the courier's Shipments tab

A courier app's own **Shipments** tab ([[econt-shipments]]) also prints several labels together, but only that courier's, and it follows the store's print-size preference, asking only when none is set. Bulk print asks every run and mixes couriers.

## Related

- [[apps-bulk-print]] — hub.
- [[waybill-print-pdf]] — printing one order's label.
- [[econt-shipments]] — a courier's own label list.
- [[apps-econt]] — the courier with the 10×15 / A4 switch.

## Open questions

- Which couriers serve their labels as a link, and so ignore the size choice, other than Econt (verify per courier).
