---
type: feature
nav_path: "Apps → Nekorekten"
route_name: apps.nekorekten.overview
route_path: /admin/apps/nekorekten
aliases: ["Nekorekten", "Nekorekten — COD protection", "nekorekten.com", "COD protection", "cash on delivery fraud check", "COD fraud screening", "unclaimed parcels", "refused parcels", "bad-faith buyers", "risky customers", "hide cash on delivery for a customer", "Некоректен", "Некоректен — защита при наложен платеж", "защита при наложен платеж", "непотърсени пратки", "некоректни клиенти", "недобросъвестни купувачи", "рискови клиенти", "скрий наложен платеж"]
tags: [apps, administration, cod, cash-on-delivery, fraud, risk, checkout, orders]
plan_gates: []
created: 2026-10-05
updated: 2026-10-05
source_count: 24
---

# Nekorekten (cash-on-delivery protection)

> **Installed is not switched on.** A freshly installed Nekorekten app is **Disabled**: nothing is checked or hidden and no card appears on orders until the merchant clicks **Enable** in the app header. Without a working nekorekten.com API key, only the store's own blocked list works ([[apps-nekorekten-settings]]).

## Purpose

Unclaimed cash-on-delivery parcels cost the merchant the courier both ways. **Nekorekten** looks up each cash-on-delivery buyer's phone and email in **nekorekten.com**, a Bulgarian database of reports that merchants file about buyers who did not collect their parcels. It then does up to three things, each controlled separately:

1. **Shows a verdict on the order** — **High risk** (Висок риск), **Low risk** (Нисък риск) or **Not checked** (Непроверен), with the reports themselves, in a card on the order details page.
2. **Withholds "Cash on delivery" at checkout** from flagged buyers — or not, as the merchant chooses.
3. **Keeps the store's own lists** — a blocked list (buyers who never get cash on delivery) and a whitelist (contacts that are never blocked) — and can report bad-faith buyers back to nekorekten.com.

**One report is enough for High risk.** There is no threshold to tune.

The app needs the merchant's **own nekorekten.com account and API key**. The app record is created at **€4.99 per month** with no trial (verify the current App Store price).

## Where to find it

Sidebar → **Apps → Nekorekten** (`/admin/apps/nekorekten`). The page header carries the app's **Enabled / Disabled** status and its **Enable / Disable** button. Tabs:

| Tab | Address | Aspect |
|---|---|---|
| **Overview** | `/admin/apps/nekorekten` | The app's description. |
| **Settings** | `/admin/apps/nekorekten/settings` | [[apps-nekorekten-settings]] |
| **Blocked customers** (Блокирани клиенти) | `/admin/apps/nekorekten/blocklist` | [[apps-nekorekten-blocklist]] |
| **Whitelist** (Бял списък) | `/admin/apps/nekorekten/whitelist` | [[apps-nekorekten-whitelist]] |
| **Activity** (Активност) | `/admin/apps/nekorekten/activity` | [[apps-nekorekten-activity]] |

Outside the app, the verdict appears as a **Nekorekten** (Некоректен) card in the right sidebar of a cash-on-delivery order ([[apps-nekorekten-order-check]]).

## Sub-pages (in this cluster)

- [[apps-nekorekten-settings]] — the Settings tab field by field: API key, Test connection, the IP to allow, plan counters, the three Orders settings, reporting.
- [[apps-nekorekten-checkout]] — **Cash on delivery at checkout**: the three policies, who loses cash on delivery, what the shopper sees, why it never fails a checkout.
- [[apps-nekorekten-order-check]] — the background check on new cash-on-delivery orders and the order card: verdicts, reports, **Check again**, **Block customer**.
- [[apps-nekorekten-blocklist]] — the Blocked customers list, automatic blocking by order status, **Check existing orders**, reporting to nekorekten.com.
- [[apps-nekorekten-whitelist]] — contacts that are never blocked, and why the merchant's own office phone belongs there.
- [[apps-nekorekten-activity]] — checkout activity: how many buyers were checked and how many lost cash on delivery.
- [[apps-nekorekten-quota]] — nekorekten.com plan limits, how the app rations lookups, the warning banner, and every reason an order says **Not checked**.

## What the merchant can do here

- **Connect** a nekorekten.com account and watch its plan.
- **Decide what a flagged buyer loses at checkout.**
- **Read the verdict** on each cash-on-delivery order; re-check, block or unblock the buyer.
- **Block buyers** by hand, or automatically when their order reaches a chosen status.
- **Protect the store's own contacts** from ever being blocked.
- **Report** a blocked buyer to nekorekten.com, once reporting is allowed.

### What the merchant CANNOT do here

- **Check prepaid orders.** Only cash-on-delivery orders are checked and only they get the card.
- **Change the risk rule.** One report is always High risk.
- **Get an alert or e-mail about a risky order.** The verdict lives only on the order. The orders list has no risk column or filter.
- **Withdraw a report** already sent to nekorekten.com. Removing the buyer from the blocked list does not take it back.

## Business rules

### Four switches, four separate tasks

| Task | Setting | Needs the API key? |
|---|---|---|
| Verdict on each new cash-on-delivery order | **Check every new cash-on-delivery order** | Yes |
| Hiding cash on delivery at checkout | **Cash on delivery at checkout** | No for the blocked list; yes for nekorekten.com reports |
| Adding buyers to the blocked list automatically | **Automatically block customers of orders with status** | No |
| Reporting buyers back | **Allow reporting customers to nekorekten.com** | Yes |

Turning one off does not turn off the others. Switching off the order check does not stop checkout hiding, and **Always show it** at checkout does not stop the order check.

### How a buyer is judged

The same order is used at checkout and on new orders:

1. **Whitelist** — a match means Low risk. Nothing is looked up.
2. **Blocked list** — a match means High risk. Nothing is looked up.
3. **Recent lookup** — if this phone or email was looked up in the last **7 days**, that answer is reused.
4. **nekorekten.com** — only now is a lookup spent from the merchant's plan.

A match on **either** the phone **or** the email is enough. Phones are compared in international form, so `0888 123 456` and `+359888123456` are the same buyer.

### What is sent to nekorekten.com

- **Lookups:** the buyer's phone (from the shipping address, or the billing address when there is none) and e-mail, sent with the merchant's API key. A lookup can happen at the payment step, before the shopper has placed the order.
- **Reports** (only when allowed, only on request): one phone or e-mail, the entry's note as the report text, and the store's web address.

### It never stands in the way of a sale on its own failure

If nekorekten.com is slow, down, refusing the key or out of plan, the buyer is **Not checked** and keeps cash on delivery. Not checked never hides anything. The admin warns about the cause instead ([[apps-nekorekten-quota]]).

### Disabled, uninstalled

- **Disabled:** no checks, no hiding, no automatic blocking, no order card. The lists stay and can still be edited.
- **Uninstalled:** the API key and settings are deleted and the blocked list, whitelist, remembered lookups and activity figures are dropped. A reinstall starts empty and Disabled. Verdicts already written on orders stay on those orders, but the card only shows while the app is installed and enabled.

## Settings & fields

All settings are on the **Settings** tab ([[apps-nekorekten-settings]]):

| Box | Holds |
|---|---|
| **Connect nekorekten.com** (Свържи nekorekten.com) | API key, Test connection, IP to allow, plan counters |
| **Orders** (Поръчки) | Order check switch, Cash on delivery at checkout, automatic blocking status, Check existing orders |
| **Reporting to nekorekten.com** (Докладване към nekorekten.com) | Allow reporting switch |

## Related

- [[apps]] — the Apps hub.
- [[payment-providers-cod]] — the Cash on delivery payment method this app protects.
- [[checkout-step-payment]] — where cash on delivery disappears for a flagged buyer.
- [[orders-details-actions]] — the order sidebar that carries the Nekorekten card.
- [[settings-banned-ip]] — the platform's other buyer-blocking tool, by IP address.
- [[apps-fast-order]] — a cash-on-delivery order form that the checkout hiding does not cover ([[apps-nekorekten-checkout]]).

## Open questions

- Whether the App Store lists the app publicly yet: the app record is created hidden and marked beta (verify current visibility and price).
