---
type: feature
nav_path: "Apps → Nekorekten → Blocked customers"
route_name: apps.nekorekten.blocklist
route_path: /admin/apps/nekorekten/blocklist
aliases: ["Blocked customers", "blocked list", "blocklist", "block a customer from cash on delivery", "automatically block customers", "unclaimed order status", "Check existing orders", "report customer to nekorekten.com", "Блокирани клиенти", "черен списък", "Блокирай", "Докладвай", "Провери съществуващите поръчки", "непотърсена поръчка", "блокиране на клиент"]
tags: [apps, nekorekten, blocklist, cod, order-status, reporting]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 8
---

# Nekorekten — Blocked customers

> Part of [[apps-nekorekten]]. See the hub for the other aspects (settings, checkout, order check, whitelist, plan limits).

## Purpose

The store's own list of phones and e-mails that are refused cash on delivery. The screen's own words: *"These customers never get "Cash on delivery". Phone numbers are matched in any format — 0888…, +359… or with spaces all count as the same customer."* The list is filled by hand, from an order, or automatically when an order reaches a chosen status, and it works without a nekorekten.com account.

## Where to find it

**Apps → Nekorekten → Blocked customers** (Блокирани клиенти) (`/admin/apps/nekorekten/blocklist`). The automatic rule and **Check existing orders** are on **Settings → Orders** ([[apps-nekorekten-settings]]). Single buyers can also be blocked from the order card ([[apps-nekorekten-order-check]]).

## What the merchant can do here

- **Block** a phone, an e-mail or both, with a note.
- **Remove** an entry.
- **Report** an entry to nekorekten.com, once reporting is allowed.
- Search and filter the list by **Type** and **Source** (verify that the filters take effect).

## Settings & fields

### Add form

| Field | Notes |
|---|---|
| **Phone** (Телефон) | A phone field with a country picker. Up to 64 characters. |
| **Email** (Имейл) | Up to 191 characters. Only the format is checked. |
| **Note** (Бележка) | Placeholder *"e.g. did not collect the parcel"*. Up to 255 characters. |
| **Block** (Блокирай) | Adds the entry. Phone and/or e-mail are required: *"Enter a phone and/or an email"*. |

### List columns

| Column | Shows |
|---|---|
| **Type** (Тип) | **phone** or **email**. |
| **Value** (Стойност) | The contact, phones in international form (`+359…`), e-mails in lower case. |
| **Source** (Източник) | **manual** (ръчно), **by order status** (по статус на поръчка) or **nekorekten.com**. |
| **Note** (Бележка) | The note. |
| **Status** (Статус) | What nekorekten.com said last time this contact was looked up: **unchecked** (непроверен), **clean** (чист) or **reported × N** (докладван × N). |
| **Date** (Дата) | When it was added. |
| **Report** (Докладвай) | Button, only when reporting is allowed and the entry has not been reported yet. |
| Remove | Asks *"Remove this customer from the blocked list?"* |

## Business rules

### One entry per contact

A phone and an e-mail added together become **two** entries, and each blocks on its own: an order matching either the phone or the e-mail is a blocked buyer. Adding a contact that is already listed updates its note and marks it **manual**. There is no edit button — to change an entry, remove it and add it again.

A phone that cannot be read as a valid number is dropped. If an e-mail was given too, only the e-mail is added, without a warning. Local numbers are read as numbers of the store's country.

### What a blocked buyer loses

Under the default checkout option, a blocked buyer never sees cash on delivery. Under **Always show it** they keep it and are only flagged **High risk** on every new order. See [[apps-nekorekten-checkout]]. A contact on the whitelist is never treated as blocked, even if it is on this list ([[apps-nekorekten-whitelist]]).

### The Status column is mostly "unchecked"

Status comes from the app's stored lookups, so opening the list costs nothing from the plan. A blocked contact is never looked up automatically — the blocked list is checked before nekorekten.com. So an entry shows **clean** or **reported** only if the contact was looked up before it was blocked, or through **Check again** on an order.

### Automatic blocking by order status

With **Automatically block customers of orders with status** set ([[apps-nekorekten-settings]]), every time an order **changes into** that status, its phone and e-mail are added with source **by order status** and the note *"Automatically blocked from order #N"*. This applies to orders with **any** payment method, not only cash on delivery. Whitelisted contacts are skipped, and contacts already listed are left as they are. It needs an enabled app, but no API key.

Orders that were already in the status when it was chosen are not caught, because nothing changed. That is what **Check existing orders** is for.

### Check existing orders

The button blocks the buyers of every order currently in the selected status, with the same rules: whitelisted contacts skipped, nothing blocked twice, safe to run again. Its hint asks the merchant to save the status first. Answers:

| Message | When |
|---|---|
| *"Checked {scanned} order(s), blocked {blocked} new contact(s)."* | Up to 200 orders, done on the spot. |
| *"Started — you will get a notification when it finishes."* | More than 200 orders. The system queues a background task, and the result arrives in [[notifications]]: *"Checked N existing order(s) and blocked N new contact(s)."* If that task fails, no notification arrives. |
| *"No orders in this status."* | Nothing to do. |
| *"Choose the order status to block by first, then save."* | No valid status selected. |
| *"The app is not installed on this store."* | Also shown when the app is installed but **Disabled**. |

### Reporting to nekorekten.com

With **Allow reporting customers to nekorekten.com** on, each unreported entry gets a **Report** button. A report is sent under the merchant's own nekorekten.com account, spends a request from their plan, and makes the contact visible to other merchants. It carries:

- that one entry's phone **or** e-mail — a buyer listed with both needs two reports;
- the entry's **Note** as the report text, or *"Customer did not collect a cash-on-delivery order."* (Клиентът не потърси поръчка с наложен платеж.) when the note is empty. Automatically blocked entries carry the note *"Automatically blocked from order #N"*, and that is the text sent;
- the store's web address.

After a successful report the button disappears. Failures: *"Reporting to nekorekten.com is turned off in the app settings."*, *"The report could not be sent to nekorekten.com."*, or nekorekten.com's reason, such as a spent plan ([[apps-nekorekten-quota]]). A report cannot be withdrawn from CloudCart; removing the entry leaves it on nekorekten.com.

## Related

- [[apps-nekorekten]] — hub.
- [[apps-nekorekten-settings]] — the automatic-blocking status and the reporting switch.
- [[apps-nekorekten-order-check]] — blocking and unblocking from an order.
- [[settings-statuses]] — the store's order statuses.
- [[notifications]] — where the result of a large **Check existing orders** arrives.

## Open questions

- No part of the app was found adding entries with source **nekorekten.com**, although the column and filter offer it (verify).
- The list's filter bar appears to send its choices under different names from the ones the list reads, so **Type**, **Source** and search may not narrow the list (verify on a live store).
