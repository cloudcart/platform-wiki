---
type: feature
nav_path: "Orders → Enable Bulk print → Documents"
route_name: orders.bulk-print.list
route_path: /admin/orders/bulk-print?tab=documents
aliases: ["Documents tab", "bulk print progress", "bulk print history", "Stop bulk print", "download bulk print PDF", "bulk print files", "Done with errors", "The task failed. No documents were produced.", "no documents", "Документи", "Спри", "Обнови", "Готово с грешки", "Задачата е неуспешна", "няма документи", "В опашка", "Спряна"]
tags: [apps, bulk-print, background-jobs, pdf, downloads, troubleshooting]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 10
---

# Bulk print — runs, progress, Stop and the Documents tab

> Part of [[apps-bulk-print]]. See the hub for the other aspects (the screen, order slips, waybills, labels, daily allowance).

## Purpose

Every Bulk print action except **Cancel waybill** is a **run** the system prepares in the background: an order slip run, a waybill generation run, or a label run. This page covers how a run is followed and stopped, how its files are split and opened, how it can fail, and the **Documents** tab that keeps every run and its files after the page is closed.

## Where to find it

- The **Bulk print** progress panel, above the tabs on **Orders → Enable Bulk print** ([[apps-bulk-print-mode]]).
- **Orders → Enable Bulk print → Documents** (Документи), at `/admin/orders/bulk-print?tab=documents`.

## What the merchant can do here

- Watch a run's progress and **Stop** (Спри) it.
- Open each file of a run as soon as it is ready.
- Read which orders failed and why.
- Come back later and open the files of any past run in **Documents**, with **Refresh** (Обнови) and page-by-page browsing.
- Print a label run again in another size, or print the labels of a generation run ([[apps-bulk-print-labels]]).

## Settings & fields

### The progress panel

| Element | Shows |
|---|---|
| Counter | *"{processed} of {total} processed"* ({processed} от {total} обработени) and a percentage bar. |
| **Stop** | While the run is queued or running. |
| Verdict | **Done**, **Done with {count} error(s)**, **Failed** or **Stopped**. |
| File buttons | One per file, added as each file is written. |
| Failures | *"{count} order(s) failed"* and one line per order: *#N — reason*. |

### A run in Documents

| Element | Values |
|---|---|
| Type | **Order slips** (Разписки за поръчки), **Waybill labels** (Етикети на товарителници) or **Waybill generation** (Генериране на товарителница). |
| Size badge | **A6 thermo** or **A4**, on label runs. |
| Line | Date and time, *"{processed} of {total} processed"*, *"{count} order(s) failed"*. |
| Status | **Queued** (В опашка), **Running** (Работи), **Done** (Готово), **Done with {count} error(s)** (Готово с {count} грешка(и)), **Failed** (Неуспешна), **Stopped** (Спряна). |
| Files | A button per file, or *"— no documents"* (няма документи) on a print run that produced none. |
| Buttons | **Print in another size** (finished label run), **Print waybill labels** (finished generation run). |
| Errors | The per-order reasons. |

Runs are listed newest first, 25 per page. The tab text reads *"The documents produced by the last runs. They stay available here after you leave the page."* With no runs: *"Nothing has been printed yet."*

## Business rules

### Background processing

Starting a run only queues it, and the screen answers at once. The run then goes through a background queue reserved for this kind of work. There is no promised finishing time. Slip and label runs write a file of **50 orders** at a time. Generation makes one courier request per order, so a few hundred orders take minutes. The panel checks the run every **3 seconds**.

The run carries on if the page is closed. The browser remembers the run, so the panel picks it up after a reload. Every past run is also in **Documents**.

### Files of 50 orders

Slip and label runs are split into files of **50 orders**, named like `orders-<run>-<part>.pdf` and `waybills-<run>-<part>.pdf`. A file opens in a new browser tab, from where it is printed or saved. A generation run produces no file; it writes waybill numbers onto the orders.

### When a run ends

| Outcome | Toast |
|---|---|
| Everything worked, slips or labels | *"{count} document(s) are ready for print"* ({count} документа са готови за печат). |
| Everything worked, generation | *"{count} waybill(s) generated successfully"* |
| Some orders failed | *"Finished with {failed} error(s): {succeeded} of {total} completed."* |
| Nothing worked | The first reason from the run, or *"The task failed. No documents were produced."* |

For slips and labels with at least one success, a run with **one** file opens it in a new tab by itself. A run with several says *"The run was split into {count} files — open them from the Bulk print panel above."* If the browser blocks the new tab, the file button in the panel opens it. CloudCart's own error texts are written in the store's admin language; a courier's message comes as the courier sent it.

### Failed

A run is **Failed** when every order failed, when a slip or label run produced no file at all, or when a slip or label run broke off. A run with some failures is **Done with N error(s)**, and its files hold the orders that worked.

### Stop is not undo

**Stop** takes effect at the next safe point: after the current file of 50 for slips and labels, after the current order for generation. Files already written stay downloadable and waybills already issued stay issued. The allowance of orders that were not delivered is given back ([[apps-bulk-print-quota]]).

### How long files are kept

Nothing is deleted on a schedule: runs and their files stay in **Documents** until the app is **uninstalled**, which deletes them all. Files are stored privately on CloudCart's file storage. They are not in the store's File manager and do not count toward the plan's storage.

### Download errors

- *"This batch no longer exists."* — the run is gone, for example after an uninstall.
- *"This batch is still being generated."* — the file is not available.

## Related

- [[apps-bulk-print]] — hub.
- [[apps-bulk-print-labels]] — **Print in another size** and **Print waybill labels**.
- [[apps-bulk-print-quota]] — what a failed or stopped run gives back.

## Open questions

- A run queued while the store's subscription has expired is skipped by the background worker. It looks like it would stay **Queued**, holding its allowance for the day (verify).
- A stored file that has gone missing also answers *"This batch is still being generated."* That reads as "wait", although waiting will not help (verify; possible bug).
- After **Stop**, the browser keeps the stopped run in the panel on later visits until another run starts (verify).
- A run stopped while still **Queued** ends before it starts and appears not to give its reserved orders back ([[apps-bulk-print-quota]]; verify, possible bug).
