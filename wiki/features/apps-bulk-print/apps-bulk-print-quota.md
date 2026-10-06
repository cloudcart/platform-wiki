---
type: feature
nav_path: "Apps → Bulk print → Daily printing plan"
route_name: apps.bulk_print.overview
route_path: /admin/apps/bulk_print
aliases: ["Bulk print daily limit", "Bulk print price", "Bulk print packs", "Daily printing plan", "Free allowance", "Printed today", "Left for today", "Choose a plan", "Change plan", "Bulk printed orders per day", "daily limit reached", "bulk_print_daily_orders", "Масово отпечатани поръчки на ден", "До 10 поръчки на ден", "51+ поръчки на ден", "дневен лимит за печат", "Достигнахте дневния си лимит"]
tags: [apps, bulk-print, plans, feature-packs, limits, pricing]
plan_gates: ["bulk_print_daily_orders"]
created: 2026-10-05
updated: 2026-10-05
source_count: 12
---

# Bulk print — daily allowance, packs and prices

> Part of [[apps-bulk-print]]. See the hub for the other aspects (the screen, order slips, waybills, labels, runs).

## Purpose

Installing Bulk print costs nothing. What is sold is **how many orders a day** can go through the two metered actions: printing order slips and generating waybills. A store with no pack gets **3 orders a day**. This page covers the packs, what counts and what is free, when the count resets, and what the merchant sees when a run does not fit.

## Where to find it

- **Apps → Bulk print** → the **Daily printing plan** panel, once the app is installed.
- **Orders → Enable Bulk print**: **Printed today** in the header card, the orange banner when nothing is left, and **Choose a plan** / **Change plan** at the top right ([[apps-bulk-print-mode]]).
- The app's **What it costs** description lists the packs.

## What the merchant can do here

- See today's usage and what is left.
- Buy a pack, or change it, from **Choose a plan** / **Change plan**. The purchase panel opens over the current screen ([[plan-vs-feature-pack]]).

## Settings & fields

### The packs

Plan feature `bulk_print_daily_orders`, named **Bulk printed orders per day** (Масово отпечатани поръчки на ден):

| Pack | Monthly | Yearly |
|---|---|---|
| **Up to 10 orders per day** (До 10 поръчки на ден) | €24.99 | €249.90 |
| **11 – 25 orders per day** (11 – 25 поръчки на ден) | €49.99 | €499.90 |
| **26 – 50 orders per day** (26 – 50 поръчки на ден) | €99.99 | €999.90 |
| **51+ orders per day** (51+ поръчки на ден) | €199.99 | €1,999.90 |

Each pack is sold **monthly** (месечно) or **yearly (2 months free)** (годишно (2 месеца безплатно)): a year costs ten months. The pack sets the day's limit at **10**, **25**, **50**, or no practical limit for **51+**. Without a pack the limit is **3**.

### The Daily printing plan panel

| Row | Shows |
|---|---|
| Heading | **Daily printing plan**, *"Resets every night at 00:00"*. |
| **Plan** | The pack's name, or **Free allowance**, and *"{limit} orders per day"* or *"51+ orders per day"*. |
| **Billing** | **Monthly** or **Yearly**, when a pack is bought. |
| **Printed today** | Orders counted today. |
| **Left for today** | Hidden on the 51+ pack. |
| Note on the free allowance | *"You are on the free allowance of {limit} orders a day. Choose a pack to print more — monthly, or yearly for the price of 10 months."* |
| Button | **Choose a plan**, or **Change plan** once a pack is bought. |

Before installing: *"Install the app to see your daily printing allowance."*

## Business rules

### What counts and what is free

| Counts | Free |
|---|---|
| **Print selected** on **Orders print** ([[apps-bulk-print-order-slips]]) | **Print waybills**, and the labels printed after a generation ([[apps-bulk-print-labels]]) |
| **Generate waybills** ([[apps-bulk-print-waybills]]) | **Print in another size** / **Print waybill labels** in Documents |
| | **Cancel waybill** |
| | **Print order** for one order on the order page ([[orders-details-header]]) |

An order counts **once per day**, whatever it was used for. Printing its slip in the morning and generating its waybill in the afternoon is one order. So is printing the same slip twice, or two staff members selecting the same order.

### The day

The count follows the store's own calendar day and time zone. It starts again at **00:00** store time, and nothing has to run for that.

### Taken when the run starts, all or nothing

The orders a run would count are reserved **when it is queued**, before anything is printed. That keeps the limit exact while runs wait in the queue. A run that does not fit is refused **as a whole**, and nothing is queued:

- Some room left: *"Only {left} more order(s) can be printed today. Narrow your selection, wait for the limit to reset at 00:00, or choose a bigger pack."* (Днес можете да отпечатате още {left} поръчк(и). Намалете селекцията, изчакайте нулирането в 00:00 или изберете по-голям пакет.)
- None left: *"You have reached your daily limit of {limit} orders. It resets at 00:00 — or choose a bigger pack to print more today."* (Достигнахте дневния си лимит от {limit} поръчки. Лимитът се нулира в 00:00 — или изберете по-голям пакет, за да печатате още днес.)

The pack panel opens over the selection, so the merchant can buy and press the button again. The selection is kept.

### Given back

An order that was reserved but not delivered returns to the day's allowance at the end of its run:

- an order whose slip did not render;
- an order whose waybill was not issued;
- the orders a **Stop** or a broken run never reached ([[apps-bulk-print-runs]]).

An order marked as shipped without a waybill number (no courier API) counts as delivered.

### Buying and changing packs

There is only ever **one** pack. Buying another, whether bigger, smaller, or the other billing period, **replaces** it instead of adding to it. The new limit applies at once. The free 3 are not added on top of a pack.

A store still paying for the earlier all-in-one Bulk print subscription is treated as having no daily limit until it cancels.

### Uninstalling does not reset the day

Today's count survives an uninstall, so removing and reinstalling the app gives no new free allowance ([[apps-bulk-print]]).

## Related

- [[apps-bulk-print]] — hub.
- [[plan-vs-feature-pack]] — how feature packs are bought and billed.
- [[plan-features]] — the store's plan features.

## Open questions

- A run stopped while still **Queued** appears to end without giving its reserved orders back (verify; possible bug).
- Whether prices on the purchase panel include VAT (verify against billing).
