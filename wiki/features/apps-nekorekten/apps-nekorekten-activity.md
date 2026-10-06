---
type: feature
nav_path: "Apps → Nekorekten → Activity"
route_name: apps.nekorekten.activity
route_path: /admin/apps/nekorekten/activity
aliases: ["Checkout activity", "Nekorekten activity", "how many customers were blocked", "Nekorekten statistics", "Активност", "Активност на касата", "Проверки", "Блокирани"]
tags: [apps, nekorekten, activity, checkout, statistics]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 4
---

# Nekorekten — Checkout activity

> Part of [[apps-nekorekten]]. See the hub for the other aspects (settings, checkout, order check, lists).

## Purpose

How many buyers the app checked at checkout and how many of them had cash on delivery withheld. The screen's own words: *"Customers checked at checkout, and how many of them had "Cash on delivery" withheld. Each customer is counted once per cart, not once per page view."*

## Where to find it

**Apps → Nekorekten → Activity** (Активност) (`/admin/apps/nekorekten/activity`). The panel is titled **Checkout activity** (Активност на касата).

## What the merchant can do here

- Read the totals for today, the last 7 days and all time.
- Pick a date range to see that period's totals and its day-by-day figures.
- **Clear** (Изчисти) the range.

## Settings & fields

| Element | Shows |
|---|---|
| **Today** (Днес) | Checks and blocked for the current day. |
| **Last 7 days** (Последните 7 дни) | Today plus the six days before it. |
| **All time** (За цялото време) | Everything since the app was installed. |
| **Selected period** (Избран период) | Appears only once a range is picked. |
| Date range picker + **Clear** | Sets or removes the range. |
| Day table: **Date**, **Checks** (Проверки), **Blocked** (Блокирани) | One row per day with activity, newest first, up to 90 rows. |

Each card reads *"N checks"* and *"N blocked"*.

## Business rules

### What counts as a check

A **check** is one buyer evaluated at the checkout payment step: cash on delivery was on offer, the app was enabled, and the shopper had entered a phone or e-mail. Buyers answered from the whitelist, the blocked list or a stored lookup count too, so this is the number of buyers screened, not the number of nekorekten.com lookups spent. **Blocked** means cash on delivery was hidden from that buyer.

The same cart is counted once within an hour, however many times the payment step is redrawn.

### What does not count

- The background check on new cash-on-delivery orders and **Check again** on an order ([[apps-nekorekten-order-check]]).
- Checkouts where cash on delivery was not offered anyway.
- Everything while **Cash on delivery at checkout** is set to **Always show it**, since checkout makes no checks then ([[apps-nekorekten-checkout]]).

So a store using **Always show it** sees zeros here even though its orders are being checked.

### Days with no activity

Only days on which something was counted have a row. Empty days are simply absent from the table.

### Reset on uninstall

The figures are deleted with the app. A reinstall starts from zero.

## Related

- [[apps-nekorekten]] — hub.
- [[apps-nekorekten-checkout]] — the checkout behaviour these figures count.
- [[apps-nekorekten-quota]] — lookups actually spent, as shown by the plan counters.

## Open questions

None.
