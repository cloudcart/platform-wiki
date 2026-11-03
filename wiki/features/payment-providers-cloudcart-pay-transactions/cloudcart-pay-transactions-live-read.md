---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Transactions → Live read & environment"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay transactions live read", "Transactions test vs live", "CloudCart Pay test payments not shown", "Transactions Load More", "Transactions status filter", "Transactions refresh"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, payments, pagination]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-transactions]]. See the hub for the other aspects (list and filters, totals, status and amounts).

# Transactions — where the list comes from & environment

## Purpose

Where the Transactions list comes from and why it shows what it shows. CloudCart keeps a **copy of every charge** per account, and the tab reads it once the account's whole history is in; until then it reads CloudCart Pay live. It covers only **this store's payments**, even when the account serves several stores, and only the environment (test or live) the store charges in. This page also explains **Load More**, **Refresh** and how the **Status** filter finds refunds. It is the page for "why can't I see my test payment?" and "why does a refund show late?".

## Where to find it

Settings → Payment methods → CloudCart Pay → **Transactions** tab. The only controls involved are **Refresh** at the top and **Load More** under the table; the environment is shown read-only in the page header.

## What the merchant can do here

- **Refresh** — reads the list and the totals again.
- **Load More** — adds the next 25 payments under the list.
- The merchant **cannot** switch between test and live payments: the environment is set by CloudCart for the whole platform.

## Settings & fields

No settings. What the tab sends with each read:

| What | Comes from | Effect |
|---|---|---|
| Environment | The platform's test/live setting | Only payments of that environment are listed. |
| Store | The store's connected account | Only this store's payments are listed, also on a shared account. |
| Status | The **Status** filter | **Succeeded**, **Pending**, **Failed** match the payment's state; **Refunded** matches any payment with a refund. |
| Dates | **From** / **To** | Start of the From day to end of the To day. |
| Page | **Load More** | 25 payments per page. |

## Business rules

### Where the payments are read from

CloudCart's copy is refreshed every 10 minutes for the last 2 hours, once after each completed payment, and daily for a rolling 35-day window, as refunds can land on old payments. Once the account's whole history is in the copy, the tab and the totals read it, and the first page re-reads the last 2 hours. Until then they read CloudCart Pay live. A refund or dispute made outside CloudCart can therefore show with up to a day's delay, unless it falls within those 2 hours.

### Per environment, account and store

- **Environment.** A payment made in the test environment never appears while the store charges in the live environment, and the other way round. A merchant who "can't find" a payment should check the environment badge in the page header first.
- **Account.** After the store disconnects and links another account, the tab shows the new account's payments; there is nothing to clear.
- **Store.** On an account shared by several stores, the tab shows a notice naming the others and lists only this store's payments ([[cloudcart-pay-account-model]]).

### How the Status filter finds refunds

A refund does not change a payment's own state, which stays succeeded. So **Refunded** searches for payments that have a refund operation, which returns both fully and partially refunded payments. The label in the row then says which one it is — see [[cloudcart-pay-transactions-status-amount]].

### Load More

The list loads 25 payments at a time, newest first. **Load More** fetches the next 25 and disappears when there are no more. The totals cards are not recalculated by **Load More**; they already cover every matching payment ([[cloudcart-pay-transactions-totals]]).

### Refresh, Apply Filters, Clear

Each of them reads the first page again and recalculates the totals.

### No account

Without a connected account nothing is read and the tab shows *"Please complete the onboarding process first."*

### Staff access

The tab and its reads are available only to staff whose role allows the store's payment methods settings ([[settings-staff]]).

## Related

- [[payment-providers-cloudcart-pay-transactions]] — hub.
- [[cloudcart-pay-transactions-list-filters]] — the filter bar.
- [[cloudcart-pay-transactions-totals]] — the totals.
- [[cloudcart-pay-account-model]] — the account and the test/live environment.
- [[payment-providers-cloudcart-pay-onboarding]] — needed before anything is listed.
- [[payment-providers-cloudcart-pay-payouts]] — read live in the same way.

## Open questions

- How far back the date filter can reach (CloudCart sets no limit).
