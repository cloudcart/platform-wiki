---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Transactions → List & filters"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay transactions list", "Transactions filter bar", "Transactions table columns", "Transaction details", "No transactions yet", "No transactions match the filters", "Филтри транзакции CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, payments, filters]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay-transactions]]. See the hub for the other aspects (totals, live read, status and amounts).

# Transactions — list & filters

## Purpose

The visible part of the Transactions tab: the **filter bar**, the **table** and the **opened row**. It lets the merchant find a payment by order, payment ID, customer, status or date, scan the list, and open one payment to see the card, the cardholder, the captured / refunded / fee amounts, the bank's outcome and the order.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Transactions** tab. The filters and the totals sit in the card at the top; the table is below. Clicking a row (or its arrow) opens it.

## What the merchant can do here

- **Filter** and press **Apply Filters** (Прилагане на филтри), or Enter in a text filter.
- **Clear** (Изчистване) all filters at once.
- **Open a row** and click its **Order Reference** to open the order.
- **Refresh** (Обнови) and **Load More** (Зареди още).

## Settings & fields

### Filter bar

| Filter | What it matches | Notes |
|---|---|---|
| **Order Reference** (Референция на поръчката) | The order number stamped on the payment. | Placeholder "Order ID". Up to 100 characters. |
| **Payment ID** (ID на плащането) | The payment's own ID (the **Reference** column). | Up to 100 characters. |
| **Customer ID** | The CloudCart Pay customer record of a signed-in customer who saved a card ([[cloudcart-pay-save-card]]). | Up to 100 characters. |
| **Status** | **Succeeded**, **Pending**, **Failed** or **Refunded**; empty = all. | **Refunded** finds every payment with a refund, full or partial — see [[cloudcart-pay-transactions-live-read]]. |
| **From** / **To** | Payment date. | From the start of the From day to the end of the To day. |
| **Apply Filters** | Runs the search and recalculates the totals. | |
| **Clear** | Empties every filter and reloads. | Shown only while a filter has a value. |

### Table

| Column | What it shows |
|---|---|
| **Date** | When the payment was created, in the store's date format. |
| **Amount** | The payment amount in its currency — see [[cloudcart-pay-transactions-status-amount]]. |
| **Currency** | Currency code, e.g. EUR. |
| **Status** | Coloured label: **Succeeded**, **Pending**, **Failed**, **Refunded**, **Partially Refunded** … |
| **Payment Method** (Метод на плащане) | Usually the card brand; "-" when unknown. |
| **Reference** (Референция) | The payment ID. |

### Opened row

| Field | What it shows |
|---|---|
| **Card** | Brand, last four digits and expiry, e.g. "Visa •••• 4242 · 09/2028". |
| **Cardholder** (Картодържател) | Name on the card. |
| **Description** | E.g. "Order #1234 \| mystore.bg". |
| **Captured** (Прихванато) | Amount captured. |
| **Refunded** | Amount refunded so far. |
| **Fee** | CloudCart Pay's fee on this payment. |
| **Outcome** (Резултат) | The bank's or network's message on the payment. |
| **Order Reference** | The order number, as a link to the order. |
| **Customer** | The customer record ID, or "-". |
| **Created** / **Updated** | Timestamps. |
| **Payment ID** | Full payment ID. |

## Business rules

### From payment to order

The **Order Reference** in an opened row links to the order's page ([[orders-details]]). Clicking it does not close the row.

### Two empty states

- With a filter set: *"No transactions match the filters."* (Няма транзакции, които да отговарят на филтрите.)
- Without filters: *"No transactions yet."* (Все още няма транзакции.)

When a merchant says "I see no transactions", the first thing to check is a forgotten filter, often an old date range.

### No account

Without a connected account the tab shows only *"Please complete the onboarding process first."* (Моля, първо завършете процеса на регистрация.) — see [[payment-providers-cloudcart-pay-onboarding]].

### No refund button here

The list does not move money. Refunds are made on the order — the full refund with **Refund payment**, a partial one through a return ([[cloudcart-pay-refunds-webhooks]]). The result then shows here as **Refunded** or **Partially Refunded**.

### Status labels are in English

The status labels and the status filter options are shown as written above, also in the Bulgarian admin.

## Related

- [[payment-providers-cloudcart-pay-transactions]] — hub.
- [[cloudcart-pay-transactions-totals]] — the totals cards in the same card.
- [[cloudcart-pay-transactions-status-amount]] — how labels and amounts are worked out.
- [[orders-details]] — the page the order link opens.
- [[cloudcart-pay-refunds-webhooks]] — refunds.
- [[cloudcart-pay-save-card]] — where customer records come from.

## Open questions

(none)
