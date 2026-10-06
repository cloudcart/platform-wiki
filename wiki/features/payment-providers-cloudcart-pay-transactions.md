---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Transactions"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay transactions", "CloudCart Pay payments list", "Card payments list", "CloudCart Pay totals", "CloudCart Pay net amount", "Транзакции CloudCart Pay", "Плащания с карта"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, payments]
plan_gates: []
created: 2026-05-21
updated: 2026-10-06
source_count: 2
---
# CloudCart Pay — Transactions

## Purpose

The **Transactions** tab (Транзакции) lists every card payment taken through the store's CloudCart Pay account, read live each time the tab opens. Above the list, **totals cards** sum the payments, refunds, fees and net amount for the current filters. Each row shows the date, amount, currency, status, payment method and reference; opening a row shows the card, cardholder, captured / refunded / fee amounts, the bank's outcome and a link to the order. The merchant uses it to check a single payment, answer "did the card really get charged?", see the fees, and reconcile with payouts.

## Sub-pages (in this cluster)

- [[cloudcart-pay-transactions-list-filters]] — the filter bar, the table columns, the expanded row, the order link, the empty states.
- [[cloudcart-pay-transactions-totals]] — the Total Payments, Total Refunds, Total Fees and Net cards.
- [[cloudcart-pay-transactions-live-read]] — live reading, test vs live environment, **Load More**, how the status filter works.
- [[cloudcart-pay-transactions-status-amount]] — how the status label (including **Partially Refunded**) and the amounts are worked out.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Transactions** tab. Address: `/admin/payment-providers/cloudcart_pay/transactions`.

## What the merchant can do here

- **See the card payments**, newest first, 25 at a time — [[cloudcart-pay-transactions-list-filters]].
- **Filter** by order reference, payment ID, customer ID, status and date range; **Apply Filters** / **Clear**.
- **Read the totals** for the filtered payments, per currency — [[cloudcart-pay-transactions-totals]].
- **Open a row** for the card, cardholder, captured, refunded, fee, outcome and order link.
- **Open the order** from the row.
- **Load More** and **Refresh** — [[cloudcart-pay-transactions-live-read]].

## Settings & fields

- **Filter bar**: Order Reference, Payment ID, Customer ID, Status (Succeeded / Pending / Failed / Refunded, or all), From, To, **Apply Filters**, **Clear**.
- **Totals cards**: Total Payments, Total Refunds, Total Fees, Net.
- **Table**: Date, Amount, Currency, Status, Payment Method, Reference.
- **Opened row**: Card, Cardholder, Description, Captured, Refunded, Fee, Outcome, Order Reference, Customer, Created, Updated, Payment ID.

Field-by-field detail is on [[cloudcart-pay-transactions-list-filters]].

## Business rules

- **Live, per environment and per account.** The list shows only this store's account and only the environment the store charges in (test or live). Nothing is copied into the store. See [[cloudcart-pay-transactions-live-read]].
- **Totals cover the whole filter, not just the page.** Up to 5,000 matching payments are summed; beyond that a note says the figures are partial. See [[cloudcart-pay-transactions-totals]].
- **Refunds change the label, not the payment.** A refunded payment stays succeeded at CloudCart Pay; the tab shows **Refunded** or **Partially Refunded** from the refunded amount. See [[cloudcart-pay-transactions-status-amount]].
- **Fees.** The **Fee** of each payment and **Total Fees** show what CloudCart Pay charged; until 31 December 2026 the transaction fee is 0% ([[cloudcart-pay-pricing]]). The invoices for the fees are on the [[payment-providers-cloudcart-pay-tax-invoices|Tax Invoices tab]].
- **No account yet.** Without a connected account the tab shows *"Please complete the onboarding process first."*
- **Read-only.** No refunds from this list (they are made on the order — [[cloudcart-pay-refunds-webhooks]]), no export, and only CloudCart Pay payments.
- **Staff access** needs the permission for the store's payment methods settings ([[settings-staff]]).

## Related

- [[payment-providers-cloudcart-pay]] — CloudCart Pay hub.
- [[payment-providers-cloudcart-pay-onboarding]] — needed before the tab shows anything.
- [[payment-providers-cloudcart-pay-tax-invoices]] — fee invoices.
- [[payment-providers-cloudcart-pay-payouts]] — where the money is paid out.
- [[cloudcart-pay-refunds-webhooks]] — full and partial refunds.
- [[orders-details]] — the order each row links to.
- [[payment-status]] — payment statuses on orders.

## Open questions

- How far back the date filter can reach (CloudCart sets no limit).
