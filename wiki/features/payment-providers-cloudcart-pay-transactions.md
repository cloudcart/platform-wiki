---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Transactions"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay transactions", "CloudCart Pay payments list", "Card payments list", "Транзакции CloudCart Pay", "Плащания с карта"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, payments]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---
# Transactions

## Purpose

A **live transactions list** showing every card payment that has run through this merchant's CloudCart Pay account — read directly from the Paypercut payments ledger on every page load (nothing is mirrored to CloudCart's database). Each row shows the date, formatted amount, currency, status, payment method (card brand + last 4), and the Paypercut payment reference. Clicking a row expands an inline details panel with the cardholder name, captured / refunded / fee breakdown, network outcome, and a link back to the underlying CloudCart order. The merchant uses this page to audit individual charges, troubleshoot a customer dispute ("did the card actually charge?"), reconcile against payouts, or find a specific payment by order reference / customer / payment ID.

This hub is split into three aspect pages so the Assistant can drill into just the slice a question touches.

## Sub-pages (in this cluster)

- [[cloudcart-pay-transactions-list-filters]] — the list UI: filter bar, table columns, expanded detail panel, the order click-through, and the two distinct empty states.
- [[cloudcart-pay-transactions-live-read]] — the live read from Paypercut: test/live mode + account scoping, no-caching/idempotency, cursor pagination, status-filter mapping, and the permission gate.
- [[cloudcart-pay-transactions-status-amount]] — the two pieces of derived display logic: client-side refund detection (status pills) and minor-unit + scale amount formatting.

## Where to find it

Payment Providers → CloudCart Pay → **Transactions** tab.

The route is `/admin/payment-providers/cloudcart_pay/transactions`.

## What the merchant can do here

- **See the list of card payments** with date, amount, currency, status badge, payment method label, and Paypercut reference ID — see [[cloudcart-pay-transactions-list-filters]].
- **Refresh** the list at any time (e.g., after a fresh order or refund).
- **Filter** by order reference, payment ID, customer ID, status, and date range, then **Apply Filters** / **Clear** — see [[cloudcart-pay-transactions-list-filters]].
- **Expand a row** to see cardholder name, full card label, captured / refunded amounts, fees, network outcome, customer ID, timestamps, and a link to the order — see [[cloudcart-pay-transactions-list-filters]].
- **Click the order-reference link** to jump to the corresponding [[orders-details|order details page]] in another tab.
- **Load more** results via cursor pagination (25 rows per page by default) — see [[cloudcart-pay-transactions-live-read]].

## Settings & fields

The page has two field groups — a **filter bar** and the **transactions table** (plus a 12-field expanded detail panel per row). Every field is documented on [[cloudcart-pay-transactions-list-filters]], which is the page the Assistant should cite for any "what does this column / filter show?" question.

- **Filter bar**: Order Reference, Payment ID, Customer ID, Status (Succeeded / Pending / Failed / Refunded / All), From / To dates, Apply Filters, Clear.
- **Transactions table**: chevron toggle, Date, Amount, Currency, Status pill, Payment Method, Reference.
- **Expanded row** (12 fields): Card, Cardholder, Description, Captured, Refunded, Fee, Outcome, Order Reference, Customer, Created, Updated, Payment ID.

Two display fields carry non-obvious logic: the **Status** pill is derived client-side (refunds never change Paypercut's `status`), and the **Amount** is formatted from a minor-unit integer plus a currency `scale`. Both are documented on [[cloudcart-pay-transactions-status-amount]].

## Business rules

- **Live read, scoped by mode + account.** The list is fetched live from Paypercut on every load; the platform forces `livemode=true|false` and a `Paypercut-Account` header so only this merchant's test-or-live payments appear. There is no UI mode toggle. See [[cloudcart-pay-transactions-live-read]].
- **Cursor pagination.** Paypercut v2 paginates with an opaque `last_key` cursor; 25 rows default, capped at 100. See [[cloudcart-pay-transactions-live-read]].
- **Refund status is derived client-side.** A refund never changes Paypercut's `status` enum (`failed | pending | succeeded`); the page surfaces `refunded` / `partially_refunded` from the refund amount. See [[cloudcart-pay-transactions-status-amount]].
- **Amounts read minor-unit + scale.** Paypercut returns amounts as integers in the currency's smallest unit (`1995 = €19.95`). See [[cloudcart-pay-transactions-status-amount]].
- **Two empty states.** "No transactions yet" vs "No transactions match the filters." — distinguished by whether any filter is active, so a tightly filtered query doesn't look like a broken integration. See [[cloudcart-pay-transactions-list-filters]].
- **"No account" fallback.** With no connected account, the page short-circuits and shows *"Please complete the onboarding process first."* — the same fallback the Payouts page uses; both depend on a completed [[payment-providers-cloudcart-pay-onboarding|onboarding]].
- **What this page does NOT do.** No per-row refund actions (refunds run from [[orders-payment-refund]]), no CSV export (known gap), no cross-provider list (CloudCart Pay payments only), no test/live toggle (platform-managed).
- **Permission.** The page is under `hasApiPermission:settings,store.payment_providers`. A staff member without that grant cannot reach the page or its API endpoint.

## Related

- [[payment-providers-cloudcart-pay]] — parent overview with the checkout flow.
- [[payment-providers-cloudcart-pay-onboarding]] — prerequisite for the upstream `Paypercut-Account` header to resolve.
- [[payment-providers-cloudcart-pay-settings]] — the *Save Customer Card* switch produces the `Customer ID` column entries.
- [[payment-providers-cloudcart-pay-payouts]] — payouts list these transactions settle into.
- [[orders-details]] — the page each row's order-reference link goes to.
- [[orders-payment-refund]] — refund flow that produces the `refunded` / `partially_refunded` status here.
- [[orders-payment-capture]] — automatic-capture context for the `amount_captured` field.
- [[payment-status]] — platform-level payment status mapping.
- [[payment-provider]] — entity definition.

## Open questions

- ⏸️ Maximum date-range window — CloudCart does not enforce one; Paypercut may apply its own server-side cap. The actual cap value is not encoded in CloudCart's integration.
