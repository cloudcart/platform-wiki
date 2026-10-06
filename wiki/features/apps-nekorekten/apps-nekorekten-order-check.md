---
type: feature
nav_path: "Orders → Order details → Nekorekten card"
route_name: admin.orders.details
route_path: /admin/orders/details/:order_id
aliases: ["Nekorekten card", "order risk", "High risk order", "Low risk", "Not checked", "Check again", "Block customer", "Unblock customer", "nekorekten reports on order", "Некоректен", "Висок риск", "Нисък риск", "Непроверен", "Провери отново", "Блокирай клиента", "Отблокирай клиента", "сигнали за клиента"]
tags: [apps, nekorekten, orders, order-details, cod, risk]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 7
---

# Nekorekten — order check and the order card

> Part of [[apps-nekorekten]]. See the hub for the other aspects (settings, checkout, lists, plan limits).

## Purpose

Every new cash-on-delivery order gets a verdict from the app: **High risk**, **Low risk** or **Not checked**, together with the nekorekten.com reports behind it. The verdict is shown in a **Nekorekten** (Некоректен) card on the order, where the merchant can re-check the buyer or block them before shipping. The app raises no alert of its own; the order is the only place the verdict appears.

## Where to find it

**Orders** → open a cash-on-delivery order → the **Nekorekten** card at the bottom of the right sidebar, after **Cart time life** ([[orders-details-actions]]). The card appears only when the order is paid by **Cash on delivery** and the app is installed **and enabled**.

## What the merchant can do here

- Read the verdict, the number of reports, when the buyer was last checked, and the reports themselves.
- **Check again** (Провери отново) — ask nekorekten.com afresh.
- **Block customer** (Блокирай клиента) / **Unblock customer** (Отблокирай клиента).

## Settings & fields

| Element | What it shows |
|---|---|
| Verdict | **High risk** (Висок риск), **Low risk** (Нисък риск) or **Not checked** (Непроверен). |
| Report count | *"N report(s)"* (N сигнал(а)) when there are reports; *"No reports"* (Няма сигнали) on Low risk. |
| Last check | *"Checked on dd.mm.yyyy hh:mm"* (Проверен на …), or *"Not checked yet"* (Още не е проверен). |
| **Customer is blocked** (Клиентът е блокиран) | Extra line when the buyer's phone or email is on the store's blocked list. |
| Reports | Up to 20 reports: the report text, the author's name, city and date. The list scrolls. |
| Amber notice | *"Connect your nekorekten.com account to check customers."* with **Open settings** (Към настройките) — no API key saved. |
| Red notice | What currently stops checks, for example a spent plan, with **Open settings** ([[apps-nekorekten-quota]]). |
| Buttons | **Check again**, and **Block customer** or **Unblock customer**. Both are shown even without an API key. |

## Business rules

### When the automatic check runs

When a cash-on-delivery order is created, the system queues a background check. That applies whatever created the order — the checkout, the Fast Order form, or an order created and confirmed in the admin ([[orders-add]]). The verdict is usually there by the time the order is opened, but not instantly. The check is queued only when the app is **enabled**, an **API key is saved** and **Check every new cash-on-delivery order** is on. Background checks are skipped while the store's plan has expired or it is in maintenance.

Orders placed while any of those was missing — or before the app was installed — are never checked by themselves. They show **Not checked yet** until the merchant presses **Check again**.

### What the verdict means

- **Whitelisted** buyer → **Low risk**, nothing looked up.
- **Blocked** buyer → **High risk**, nothing looked up, so no reports are listed.
- Otherwise → **High risk** with one or more reports on nekorekten.com, **Low risk** with none.
- **Not checked** → the check got no answer. With a *"Checked on"* date it means a check ran and failed; see [[apps-nekorekten-quota]] for the reasons.

The phone is read from the shipping address (the billing address when there is none), the e-mail from the order. An order with neither cannot be checked.

### Check again

**Check again** skips the 7-day memory and the one-hour pause after a spent plan, and asks nekorekten.com directly. Unlike the automatic check, it **ignores the whitelist and the blocked list**: the verdict it writes is nekorekten.com's answer alone. Whether the buyer is blocked stays visible on its own line. Its answers:

- *"The customer was checked again."* (Клиентът беше проверен наново.) — shown even when the verdict did not change.
- *"Connect your nekorekten.com account first."* — no API key.
- The reason from nekorekten.com — refused key, IP not allowed, spent plan. The card keeps the previous verdict.

A successful **Check again** also refreshes the stored answer used at checkout, and ends a spent-plan pause for the automatic checks.

### Block customer

A confirmation comes first. Its text depends on [[apps-nekorekten-checkout]]:

- *"Block this customer? They will no longer be able to order with Cash on Delivery."*
- With **Always show it**: *"Block this customer? They will be flagged on every future order. Cash on delivery stays available to them, because the app is set to never hide it at checkout."*

The order's phone and e-mail are added to the blocked list as separate entries, with source **manual** and the note *"Automatically blocked from order #N"*. No API key is needed. Whitelisted contacts are added too, but the whitelist still wins at checkout. Answer: *"The customer was added to the blocked list."* An order with no usable phone or e-mail answers *"Enter a phone and/or an email."*

### Unblock customer

Removes every blocked-list entry matching the order's phone or e-mail, without a confirmation: *"The customer was removed from the blocked list."* If there is none: *"This customer is not on the blocked list."* A report already sent to nekorekten.com is not withdrawn.

### No reporting from the card

The card has no **Report** button. Reporting is done from the Blocked customers list ([[apps-nekorekten-blocklist]]).

### Access

The card's buttons use the app's own actions, which need **Apps** access ([[merchant-roles]]). How the card behaves for a moderator without it (verify).

## Related

- [[apps-nekorekten]] — hub.
- [[orders-details-actions]] — the order sidebar the card sits in.
- [[apps-nekorekten-blocklist]] — where blocked buyers are listed and reported.
- [[apps-nekorekten-quota]] — why a verdict is Not checked.
- [[payment-providers-cod]] — the payment method that makes an order eligible.

## Open questions

- The app's Reporting info text says reports can be sent "from an order", but the card offers no way to report (verify whether an order-level report is planned).
