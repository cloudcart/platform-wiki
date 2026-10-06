---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Transactions → Totals"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay totals", "Total Payments", "Total Refunds", "Total Fees", "Net CloudCart Pay", "How much did I earn with CloudCart Pay", "Общо плащания CloudCart Pay", "Такси общо CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, totals, fees]
plan_gates: []
created: 2026-10-06
updated: 2026-10-06
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-transactions]]. See the hub for the other aspects (list and filters, live read, status and amounts).

# Transactions — totals

## Purpose

The **totals cards** at the top of the Transactions tab add up every payment that matches the current filters: what was captured, what was refunded, what CloudCart Pay charged in fees, and what is left (**Net**). They answer "how much did I take with CloudCart Pay this month?" and "how much went on fees?" without adding up rows by hand.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Transactions** tab, in the filter card, under the filters. The cards appear once there is something to total.

## What the merchant can do here

- **Read the four totals** for the current filters.
- **Change the filters** (for example **From** / **To** for a month) and press **Apply Filters** to total a different set.
- **Read the totals per currency** when the account took payments in more than one currency.

## Settings & fields

Four cards per currency:

| Card | Amount | Second line |
|---|---|---|
| **Total Payments** | Sum of the amounts captured. | "<n> payments" — every matching payment counted, including failed and pending ones. |
| **Total Refunds** | Sum of the amounts refunded. | "<n> refunded" — payments with any refund, full or partial. Shown in amber when above zero. |
| **Total Fees** | Sum of CloudCart Pay's fees. | — |
| **Net** | Total Payments − Total Refunds − Total Fees. | — |

When the account has payments in several currencies, each currency gets its own row of cards, headed by the currency code. Currencies are never added together.

When the limit is reached, a note reads: *"Totals cover only the first 5000 matching payments. Narrow the filters for an exact figure."*

## Business rules

### The whole filter, not the visible page

The totals cover **every payment matching the filters**, not only the 25 rows loaded in the table. **Load More** therefore does not change them; **Apply Filters**, **Clear** and **Refresh** recalculate them.

### Only captured money counts

Failed, pending and not-captured payments add nothing to **Total Payments** (their captured amount is zero), but they are included in the "<n> payments" count. A status filter changes both accordingly.

### Up to 5,000 payments

Totals are added up over at most 5,000 matching payments. Beyond that the figures are partial and the note above appears; a shorter date range gives an exact figure.

### Fees and the promotion

**Total Fees** adds up the fee of each payment. Until 31 December 2026 CloudCart Pay charges a 0% transaction fee ([[cloudcart-pay-pricing]]). The invoices for fees are on the [[payment-providers-cloudcart-pay-tax-invoices|Tax Invoices tab]].

### Net is not a payout

**Net** is captured minus refunded minus fees for the filtered payments. It is not a statement of what was paid out or when; payouts are on the [[payment-providers-cloudcart-pay-payouts|Payouts tab]].

### Same environment and account as the list

Like the list, the totals cover only this store's account in the environment the store charges in ([[cloudcart-pay-transactions-live-read]]).

## Related

- [[payment-providers-cloudcart-pay-transactions]] — hub.
- [[cloudcart-pay-transactions-list-filters]] — the filters the totals follow.
- [[cloudcart-pay-transactions-status-amount]] — how amounts are shown.
- [[payment-providers-cloudcart-pay-tax-invoices]] — fee invoices.
- [[payment-providers-cloudcart-pay-payouts]] — payouts.
- [[cloudcart-pay-pricing]] — fees.

## Open questions

- Bulgarian labels of the four cards (not in the translation files read).
