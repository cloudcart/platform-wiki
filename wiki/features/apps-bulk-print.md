---
type: feature
nav_path: "Apps → Bulk print"
route_name: apps.bulk_print.overview
route_path: /admin/apps/bulk_print
aliases: ["Bulk print", "Bulk Print app", "bulk printing", "batch printing", "print many orders at once", "bulk waybills", "generate waybills in bulk", "print order slips in bulk", "print labels in bulk", "Enable Bulk print", "Групов печат", "Масов печат", "Включи Масов печат", "Поръчки — групов печат", "групов печат на поръчки", "масов печат на товарителници", "товарителници за много поръчки наведнъж", "разписки на партиди", "стокови разписки наведнъж"]
tags: [apps, administration, orders, printing, waybills, labels, pdf, shipping, background-jobs]
plan_gates: ["bulk_print_daily_orders"]
created: 2026-10-05
updated: 2026-10-05
source_count: 34
---

# Bulk print

> **The app is a mode inside Orders, not a screen in Apps.** After installing it, the merchant works in **Orders → Enable Bulk print** (Включи Масов печат), at `/admin/orders/bulk-print`. Opening the installed app from the Apps list goes to the same place.

## Purpose

Printing order slips and courier waybills one order at a time is slow for a busy store. **Bulk print** lets the merchant filter the orders, tick a page of them, and get back:

1. **Order slips** for all of them as PDF files ([[apps-bulk-print-order-slips]]).
2. **Courier waybills** issued for all of them in one run, with every installed courier using its own settings ([[apps-bulk-print-waybills]]).
3. **Waybill labels** as PDF files, in **A6 thermo** or **A4** ([[apps-bulk-print-labels]]).

Every run is prepared in the background. A progress panel shows it, it can be stopped, and its files stay in a **Documents** tab ([[apps-bulk-print-runs]]).

The app is **free to install**. What is paid for is the number of orders a day that can be bulk printed: **3 a day free**, then packs of 10, 25, 50 or 51+ orders a day from **€24.99 a month** ([[apps-bulk-print-quota]]).

## Where to find it

- **Apps → Bulk print** (`/admin/apps/bulk_print`): the app page with the install button, the description, the prices and the **Daily printing plan** panel.
- **Orders → Enable Bulk print** (`/admin/orders/bulk-print`): the working screen, titled **Orders - Bulk print** (Поръчки — групов печат). The button appears on the Orders list only while the app is installed ([[apps-bulk-print-mode]]).

| Tab | Address | Aspect |
|---|---|---|
| **Orders print** (Печат на поръчки) | `/admin/orders/bulk-print` | [[apps-bulk-print-order-slips]] |
| **Waybills print** (Печат на товарителници) | `/admin/orders/bulk-print?tab=waybills` | [[apps-bulk-print-waybills]], [[apps-bulk-print-labels]] |
| **Documents** (Документи) | `/admin/orders/bulk-print?tab=documents` | [[apps-bulk-print-runs]] |

## Sub-pages (in this cluster)

- [[apps-bulk-print-mode]] — the Bulk print screen in Orders: how to get in and out, the header card, the banners, the three tabs, who may use it.
- [[apps-bulk-print-order-slips]] — the **Orders print** tab: filters, columns, **Print selected**, what a slip contains, the **Printed** stamp.
- [[apps-bulk-print-waybills]] — the **Waybills print** tab: which orders are listed, filters, **Generate waybills**, **Cancel waybill**, and every reason a waybill is not issued.
- [[apps-bulk-print-labels]] — **Print waybills**: the A6 / A4 dialog, how each courier's label is fetched, printing the labels of a finished generation, printing again in another size.
- [[apps-bulk-print-runs]] — background runs: the progress panel, **Stop**, files of 50 orders, the **Documents** tab, downloads, failures, and how long files are kept.
- [[apps-bulk-print-quota]] — the daily allowance: the free 3, the packs and prices, what counts and what is free, reset at 00:00, and the refusal messages.

## What the merchant can do here

- **Install** the app and open the Bulk print screen with **Open**.
- **Choose or change a daily pack** (**Choose a plan** / **Change plan**).
- **Print order slips** for up to 1000 selected orders at a time.
- **Generate waybills** for many orders at once, and **cancel** them in bulk.
- **Print waybill labels** for orders that already have a waybill, in A6 or A4.
- **Follow, stop and re-open** runs, and download their files later.

### What the merchant CANNOT do here

- **Change how many orders go into one file or the preselected label size.** The app has no settings screen: files hold **50** orders and the size dialog opens on **A6 thermo**.
- **Print automatically.** Nothing runs on a schedule or for new orders. Every run starts from a button.
- **Choose parcels, weight or service per order** when generating in bulk. Bulk generation sends one parcel per order with the courier's own defaults ([[apps-bulk-print-waybills]]). Shipments that need more go through the order screen ([[waybill-generate-flow]]).
- **Print invoices or credit notes.** Only order slips and waybill labels.

## Business rules

### What is automatic and what is not

| Happens by itself | Needs the merchant |
|---|---|
| The run continues in the background after it is started, even if the page is closed | Starting every run |
| The progress panel picks a running run back up after a reload | Choosing the label size for every label run |
| An order is stamped **Printed** when its slip made it into a file | Opening or downloading the files |
| When a waybill generation run finishes, the size dialog opens for the orders that got a waybill | Pressing **Print** in that dialog |
| Orders that failed, and orders of a stopped run, get their daily allowance back | Fixing the order and running it again |

### One order, one allowance a day

Only two actions spend the daily allowance: **Print selected** (order slips) and **Generate waybills**. An order counts **once per day**, whatever it was used for. Printing labels, printing again in another size, cancelling waybills and the single **Print order** on the order screen ([[orders-details-header]]) are free ([[apps-bulk-print-quota]]).

### Who can use it

Every action of the app needs the staff member's **Orders** permission. Without it the screen answers *"Forbidden! You do not have permission to access this page."* ([[merchant-roles]]).

### Two Bulgarian names

The Orders list button reads **Включи Масов печат**, and the app's own name in the Bulgarian admin is **Масов печат**. The screen itself says **Групов печат** (Bulk print). All three mean this app.

### Not the courier apps' own bulk print

A courier app's own **Shipments** tab, for example [[econt-shipments]], prints existing labels of **that courier** only. Bulk print works across couriers, also issues waybills and prints order slips, and its generation counts against the daily allowance.

### Uninstalling

Uninstalling deletes the stored PDFs, the history of runs and the **Printed** stamps. A reinstall starts with every order **Not printed**. Today's usage is **kept**, so uninstalling and reinstalling does not give a new free allowance ([[apps-bulk-print-quota]]).

## Settings & fields

The app page (**Apps → Bulk print**):

| Element | Shows |
|---|---|
| **App** card | **Installed** (Инсталирано) / **Not installed** (Не е инсталирано). |
| **Active** card | **Running** (Работи) / **Inactive** (Неактивно). |
| **Bulk print** card | **Orders section** (Раздел „Поръчки“) and **Open** (Отвори). |
| **Daily printing plan** | Pack, usage, **Choose a plan** / **Change plan** ([[apps-bulk-print-quota]]). |
| Description | **What you get** and **What it costs**. |

## Related

- [[apps]] — the Apps hub.
- [[orders]] — the Orders list that carries the **Enable Bulk print** button.
- [[orders-shipping-waybill]] — the one-order waybill flow that bulk generation drives for each order.
- [[waybill-print-pdf]] — printing one order's waybill.
- [[settings-invoicing-html-templates]] — the **Packing slip / Order print** template the slips use.
- [[econt-shipments]] — a courier's own Shipments tab with label printing for that courier only.
- [[plan-vs-feature-pack]] — how the daily packs are bought.

## Open questions

- The app record (App Store listing, visibility, any price on the app itself) is not in the code. The code treats the app as free and charges only the daily packs (verify the App Store card).
- Which name the Bulgarian App Store card shows, **Масов печат** or **Групов печат** (verify).
