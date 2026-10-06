---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Transactions → Status & amount"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay transactions status", "Partially Refunded CloudCart Pay", "Refunded still succeeded", "Transactions amount formatting", "Status label colours", "Частично възстановено"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, payments, refunds]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-transactions]]. See the hub for the other aspects (list and filters, totals, live read).

# Transactions — status & amount

## Purpose

Two things on the Transactions list are worked out by the tab rather than shown as stored: the **Status** label and the **amounts**. The status label shows **Refunded** or **Partially Refunded** even though the payment itself stays succeeded after a refund; the amounts are shown in each payment's own currency. It is the page for "why does it say Succeeded after I refunded?" and "what does Partially Refunded mean?".

## Where to find it

Settings → Payment methods → CloudCart Pay → **Transactions** tab — the **Status** and **Amount** columns, and **Captured**, **Refunded** and **Fee** in an opened row.

## What the merchant can do here

- **Read the status label** and its colour.
- **Read the amounts** in the payment's currency.

Nothing here can be edited.

## Settings & fields

| Field | What it shows | How it is worked out |
|---|---|---|
| **Status** | **Succeeded**, **Pending**, **Failed**, **Refunded**, **Partially Refunded**, and less often **Processing**, **Requires Action**, **Canceled**, **Expired**, **Disputed**. | From the payment's state and its refunded amount — see below. |
| **Amount** | The payment total. | The amount as formatted by CloudCart Pay when available; otherwise the stored amount in the currency's smallest unit, converted. |
| **Captured / Refunded / Fee** | Amount captured, refunded so far, and CloudCart Pay's fee. | Same conversion as **Amount**. |

## Business rules

### How the refund labels are worked out

A refund never changes the payment's own state at CloudCart Pay; it stays succeeded and the refund is recorded next to it. The tab therefore decides the label like this:

| Refunded amount | Label |
|---|---|
| Equal to or more than the payment amount (or the payment is marked refunded) | **Refunded** |
| More than zero but less than the payment amount | **Partially Refunded** |
| Zero | The payment's own state, e.g. **Succeeded** |

So a fully refunded payment is still "succeeded" at the payment level; **Refunded** is the tab's reading of the refund on top of it. On the order, the payment status is set separately — a full refund turns it to **Refunded**, a partial one leaves it **Completed** ([[cloudcart-pay-refunds-webhooks]]).

### Colours

| Labels | Colour |
|---|---|
| Succeeded, Completed, Captured, Paid | Green |
| Processing, Requires Action, Pending | Amber |
| Failed | Red |
| Canceled, Expired | Grey |
| Refunded, Partially Refunded, Disputed | Blue |
| Anything else | Neutral |

### Amounts in the payment's own currency

Amounts are stored in the currency's smallest unit (1995 = €19.95) together with the number of decimals, and shown as a normal money amount in that currency in the browser's number format. If the browser cannot format a currency, the amount is shown as number and code, e.g. "19.95 EUR".

### Fees during the promotion

**Fee** is what CloudCart Pay took on the payment. Until 31 December 2026 the transaction fee is 0% ([[cloudcart-pay-pricing]]).

## Related

- [[payment-providers-cloudcart-pay-transactions]] — hub.
- [[cloudcart-pay-transactions-list-filters]] — the table and opened row.
- [[cloudcart-pay-transactions-totals]] — totals built from the same amounts.
- [[cloudcart-pay-refunds-webhooks]] — full and partial refunds and the order's payment status.
- [[payment-status]] — payment statuses on orders.

## Open questions

- Whether the **Fee** field reads 0 or is empty for payments taken during the 0% promotion.
