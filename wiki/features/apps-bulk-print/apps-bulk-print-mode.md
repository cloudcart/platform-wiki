---
type: feature
nav_path: "Orders → Enable Bulk print"
route_name: orders.bulk-print.list
route_path: /admin/orders/bulk-print
aliases: ["Bulk print mode", "Orders - Bulk print", "Enable Bulk print", "Exit Bulk print", "bulk print screen", "Not printed count", "Last sync", "Printed today", "Групов печат", "Поръчки — групов печат", "Включи Масов печат", "Излез от групов печат", "Неотпечатани", "Последна синхронизация"]
tags: [apps, bulk-print, orders, printing]
plan_gates: ["bulk_print_daily_orders"]
created: 2026-10-05
updated: 2026-10-05
source_count: 9
---

# Bulk print — the Bulk print screen in Orders

> Part of [[apps-bulk-print]]. See the hub for the other aspects (order slips, waybills, labels, runs, daily allowance).

## Purpose

Bulk print does not add a page under Apps that the merchant works in. It adds a **mode** to the Orders section: a separate screen with its own order lists, built for selecting many orders and turning them into PDFs or waybills. This page covers the frame of that screen: how to enter and leave it, the cards and banners at the top, the three tabs, and who may use it.

## Where to find it

- **Orders** → the **Enable Bulk print** (Включи Масов печат) button at the top of the Orders list, next to **+ Add order** ([[orders-list-columns]]). The button is shown only while the app is installed.
- **Apps → Bulk print → Open**, or opening the installed app from the Apps list.
- Directly: `/admin/orders/bulk-print`. Tabs have their own address: `?tab=waybills` for **Waybills print** and `?tab=documents` for **Documents**. A link to a tab can be bookmarked or sent to a colleague, and the browser's Back button walks the tabs.

The breadcrumb reads **Orders → Bulk print** and the title **Orders - Bulk print** (Поръчки — групов печат).

## What the merchant can do here

- Switch between **Orders print**, **Waybills print** and **Documents**.
- **Choose a plan** / **Change plan** at the top right, at any time ([[apps-bulk-print-quota]]).
- **Exit Bulk print** (Излез от групов печат) — back to the normal Orders list.
- Watch the run that is in progress in the **Bulk print** panel above the tabs ([[apps-bulk-print-runs]]).

## Settings & fields

### Header card

| Figure | Meaning |
|---|---|
| **Total** (Общо) | Every order in the store. |
| **Not printed** (Неотпечатани) | Orders with no slip printed through Bulk print yet ([[apps-bulk-print-order-slips]]). Label runs do not change it. |
| **Last sync** (Последна синхронизация) | When the most recent run last changed. Hidden until the first run. |
| **Printed today** | `used / limit (resets at 00:00)`. On the top pack only the used number is shown ([[apps-bulk-print-quota]]). |

### Banners

- Blue, always: *"You are now in Bulk print mode. You can bulk print orders and waybills here. Click Exit Bulk print to return to the main Orders list."* (В режим „Групов печат“ си. Тук можеш да печаташ групово поръчки и товарителници. Натисни „Излез от групов печат“, за да се върнеш към списъка с поръчки.)
- Orange, when nothing is left for today: *"You have printed {used} of {limit} orders allowed today. The limit resets at 00:00."* with **Choose a plan** / **Change plan**.

### Tabs

| Tab | What it lists | Aspect |
|---|---|---|
| **Orders print** (Печат на поръчки) | All orders except drafts | [[apps-bulk-print-order-slips]] |
| **Waybills print** (Печат на товарителници) | Orders with physical products and a courier | [[apps-bulk-print-waybills]] |
| **Documents** (Документи) | Past runs and their files | [[apps-bulk-print-runs]] |

The screen opens on **Orders print**. Neither list has a filter set when it opens. Changing tab clears the page number and filters of the tab being left.

### The filter bar

Both order tabs have the same bar above the list, always open: labelled boxes, **Filter** (Филтър), and **Clear filters** (Изчисти филтрите) once something is set. The bar fills back in from the address after a reload. It is separate from the Orders list's filters, and unlike the Orders list it does not hide cancelled orders until a filter is set ([[orders-list-default-visibility]]).

## Business rules

### Getting in when the app is not installed

Opening `/admin/orders/bulk-print` without the app installed sends the merchant to **Apps → Bulk print**, where the install button is. The screen never shows the "expired subscription" page for this reason.

### Who can use it

Every list and action on the screen needs the staff member's **Orders** permission ([[merchant-roles]]). Without it the request is refused with *"Forbidden! You do not have permission to access this page."*

### One run panel for all tabs

The **Bulk print** progress panel sits above the tabs and stays while the merchant changes tab. The browser remembers the run in progress, so a reload or coming back later picks it up again. While a run advances, the open tab reloads its rows, so waybill numbers and the **Printed** flag appear as they are written ([[apps-bulk-print-runs]]).

### The order cell links out

Each row starts with **Order #N** and **From** *customer name (number of orders)*. The order link opens the normal order page ([[orders-details]]) in the same tab, which leaves Bulk print. The customer name opens the customer.

### Status badges

The **Status** column colours the order status: green for paid, completed and fulfilled; yellow for pending, authorized and processing; red for declined, cancelled and refunded.

## Related

- [[apps-bulk-print]] — hub.
- [[orders]] — the Orders list this mode sits beside.
- [[orders-list-columns]] — the Orders list header where **Enable Bulk print** appears.
- [[merchant-roles]] — the Orders permission.

## Open questions

- A moderator restricted to certain orders on the Orders list ([[settings-staff]]): the Bulk print lists apply no such restriction in the code read (verify whether such a moderator sees all orders here).
- Whether archived orders appear in the two lists. The code excludes only drafts (verify).
- **Total** counts every order, drafts included, so it can be higher than the **Orders print** list (verify).
