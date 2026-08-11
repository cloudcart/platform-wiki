---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Transactions → List & filters"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay transactions list", "Transactions filter bar", "Transactions table columns", "Transaction detail panel", "No transactions yet", "No transactions match the filters"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, payments, filters]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-transactions]]. See the hub for the other aspects (live read + scoping, derived status / amount formatting).

# Transactions — list & filters

## Purpose

This is the visible surface of the Transactions tab — the **filter bar**, the **transactions table**, and the per-row **expanded detail panel**. It lets the merchant find a specific card payment (by order reference, payment ID, customer, status, or date range), scan the ledger at a glance, and drill into any single charge to see the cardholder, the captured / refunded / fee breakdown, the network outcome, and a click-through to the underlying order.

## Where to find it

Payment Providers → CloudCart Pay → **Transactions** tab. The filter bar sits above the table; clicking any row (or its chevron) toggles the inline detail panel.

The route is `/admin/payment-providers/cloudcart_pay/transactions`.

## What the merchant can do here

- **See the list of card payments** with date, amount, currency, status badge, payment method label, and Paypercut reference ID.
- **Filter** by Order Reference, Payment ID, Customer ID, Status, and a From / To date range.
- **Apply Filters** to re-query, or **Clear** to reset every filter at once.
- **Expand a row** to read the 12-field detail panel.
- **Click the order-reference link** to jump to the corresponding [[orders-details|order details page]] in another tab.
- **Load more** results (cursor pagination, 25 rows per page by default — the mechanics live on [[cloudcart-pay-transactions-live-read]]).

## Settings & fields

### Filter bar

| Field | What it filters by | Validation / notes |
|-------|--------------------|--------------------|
| **Order Reference** | The `client_reference_id` Paypercut field — the CloudCart order ID stamped on the payment when the checkout was created. | Max 100 chars. Pressing Enter applies filters. |
| **Payment ID** | The Paypercut payment `id`. | Max 100 chars. Pressing Enter applies filters. |
| **Customer ID** | Paypercut customer `id` (populated when *Save Customer Card* is ON — see [[payment-providers-cloudcart-pay-settings]]). | Max 100 chars. |
| **Status** | One of `succeeded`, `pending`, `failed`, `refunded`. **"All"** is selectable to clear the filter. | Mapped server-side to the Paypercut `status` enum or the `operation=refund` filter — see [[cloudcart-pay-transactions-live-read]]. |
| **From** (date) | Lower bound on `created` timestamp. | Sent as ISO 8601 at start-of-day. |
| **To** (date) | Upper bound on `created` timestamp. | Sent as ISO 8601 at end-of-day. |
| **Apply Filters** button | Triggers a fresh query with the active filters. | Always available. |
| **Clear** button | Resets every filter to its empty default. | Shown only when at least one filter has a value. |

### Transactions table

| Column | What it shows | Notes |
|--------|---------------|-------|
| (Chevron) | Toggles the inline detail panel for the row. | Clicking anywhere on the row also toggles. |
| **Date** | Payment `created` timestamp, formatted via the store's `format.dateTime` server setting. | |
| **Amount** | Paypercut's `formatted_amount` if present, otherwise computed from the minor-unit integer and the currency `scale`. | See [[cloudcart-pay-transactions-status-amount]] for the formatting rule. |
| **Currency** | ISO code, upper-cased. | Paypercut returns currency as `{ iso, scale }`; the column shows `iso`. |
| **Status** | Coloured pill with the human-readable status. | The pill is derived client-side — `refunded` / `partially_refunded` appear even though Paypercut keeps `status` as `succeeded`. See [[cloudcart-pay-transactions-status-amount]]. |
| **Payment Method** | Free-text label from `tx.payment_method` (typically the card brand) — or `"-"` if absent. | Detailed card info is in the expanded row. |
| **Reference** | The Paypercut payment ID, in `<code>` style. | |

### Expanded row detail panel

Twelve fields in a three-column grid:

| Field | Source |
|-------|--------|
| Card | `payment_method_details.card.brand` + ` •••• ` + `last4` + ` · MM/YYYY` (formatted from `exp_month`/`exp_year`). |
| Cardholder | `payment_method_details.card.cardholder_name`. |
| Description | `tx.description` (typically `Order #<id> | <hostname>` from the checkout creation). |
| Captured | `amount_captured` formatted in transaction currency. |
| Refunded | `amount_refunded` formatted in transaction currency. |
| Fee | `tx.fee` formatted in transaction currency (Paypercut platform fee). |
| Outcome | `outcome.seller_message` falling back to `outcome.network_status`. |
| Order Reference | `client_reference_id` linked to `/admin/orders/details/{id}`. |
| Customer | `tx.customer` (Paypercut customer ID, or `-`). |
| Created | `created` timestamp. |
| Updated | `updated` timestamp. |
| Payment ID | The full Paypercut payment ID. |

## Business rules

### Click-through to the underlying order

Every row that has a `client_reference_id` exposes a link in the expanded panel pointing to `/admin/orders/details/{id}`. This is the canonical bridge from "payment ledger" to "order details" — the linked page is [[orders-details]]. Clicking the order link does **not** also toggle the row's expand/collapse — that click is intercepted so the merchant doesn't accidentally collapse the panel they just opened.

### Two distinct empty states

The empty state distinguishes two cases:

- If the merchant has **at least one filter applied**, the copy is *"No transactions match the filters."*
- Otherwise, the copy is *"No transactions yet."*

This avoids the common confusion where a tightly filtered query looks like "the integration is broken". When a merchant reports "I see no transactions", the first thing to check is whether a filter (often a stale date range) is still active.

### "No account" state

If no connected account exists yet, the page short-circuits the upstream call and renders: *"Please complete the onboarding process first."* This is the same fallback the Payouts page uses — both pages depend on a completed [[payment-providers-cloudcart-pay-onboarding|onboarding]].

### No per-row refund action

The list is read-only with respect to money movement: there is **no per-row refund button**. Refunds run from the [[orders-payment-refund|order details page]] — partly to keep the refund decision next to the order context, partly because Paypercut requires the refund to be associated with the order's checkout reference. Once a refund completes there, it surfaces back here as a `refunded` / `partially_refunded` pill (derived — see [[cloudcart-pay-transactions-status-amount]]).

### Permission

The page is under `hasApiPermission:settings,store.payment_providers`. A staff member without that grant cannot reach the page or its API endpoint.

## Related

- [[payment-providers-cloudcart-pay-transactions]] — hub.
- [[orders-details]] — the page each row's order-reference link opens.
- [[orders-payment-refund]] — where refunds are actually run (no refund action on this list).
- [[payment-providers-cloudcart-pay-settings]] — the *Save Customer Card* switch that populates the Customer ID filter/column.
- [[payment-providers-cloudcart-pay-onboarding]] — onboarding the "No account" state points to.

## Open questions

_None._
