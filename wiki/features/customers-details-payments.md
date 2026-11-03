---
type: feature
nav_path: "Customers → Customer details → Payments"
route_name: customers-payments
route_path: /admin/customers/details/:id/payments
aliases: ["Customer payments", "Customer transactions", "Payment history", "Плащания на клиента", "Транзакции"]
tags: [customers, payments, transactions]
plan_gates: []
created: 2026-05-21
updated: 2026-11-03
source_count: 8
---
# Customer payments

## Purpose

The list of **every payment transaction** for one customer — successful payments, failed attempts, refunds, voids, chargebacks. The merchant uses it to investigate payment disputes ("the customer says they paid but the order isn't marked paid"), audit refund flows, or check payment-method preferences. Unlike [[customers-details-orders]] (order-centric), this view is transaction-centric — one order can have several payment transactions (initial charge + refund, split payment, failed attempt + retry, authorisation + capture), all appearing here as separate rows.

This is a **read-only audit view**. No transaction can be initiated, edited, or reversed here — refunds, captures, voids, and re-attempts all happen on the related order's edit page in the orders feature, where the payment-provider API call originates.

## Where to find it

From [[customers-details]] → **Payments** tab. The route is `/admin/customers/details/:id/payments`.

## What the merchant can do here

- See every payment transaction for this customer in a paginated table.
- Filter by status, amount, provider, credit note, or date.
- Click any row's **Payment #** to open the Payment Details popup.

Sorting is fixed at ID descending (newest first) — see Business rules.

The merchant **cannot** issue a refund, re-attempt a failed payment, edit a transaction record, or mark a payment paid here — every one of those happens on the order's edit page.

## Settings & fields

### Six columns

| Column | Notes |
|--------|-------|
| **Payment #** | Renders as "Payment #<id>", the payment record's internal id. Click → opens the Payment Details popup. |
| **Date** (`date_added`) | Date and time the transaction was recorded. No link. |
| **Status** | Coloured transaction-state badge (Completed / Pending / Failed / Refunded / Voided / Cancelled / Timeouted / Initiated / Requested). Same colour mapping as the Orders-tab Status column; see [[customer-details-orders-list]]. |
| **Provider** | Renders the provider's configured **name** (`payment_provider.name`), falling back to the provider slug key (`payment_provider.provider`, e.g. `stripe` / `easypay`) if no name is set. The backend appends a provider-icon attribute, but this column's renderer does not display it. |
| **Order #** (`order_id`) | The order this payment relates to, as the text "Order #<id>". |
| **Amount** (`amount_formatted`) | Server-formatted transaction amount with currency. |

### Filters

| Filter | Operators | Options |
|--------|-----------|---------|
| **Payment status** | Is / Is not (single-select) | Initiated / Pending / Requested / Completed / Failed / Refunded / Cancelled / Timeouted |
| **Amount** | More than / Less than / More than or equal / Less than or equal | Numeric input |
| **Credit Note** | Yes / No | See Business rules |
| **Provider** | Is / Is not (single select) | Configured payment providers |
| **Date** | Exactly / More than / Less than / Not Between / Between / More than or equal / Less than or equal | Date picker |

### Pagination & sort

Default page size is **25**, max **100** (enforced by backend validation). Sorting is restricted to `id` or `date_added` only, defaulting to `id DESC`; the UI exposes neither as a sortable column header, so the merchant cannot change the order.

## Business rules

### Permission — orders, not customers

The backend endpoint requires the **orders** permission (`hasApiPermission:orders` middleware), NOT the customers permission. A merchant role with customers access but no orders access sees the Payments tab in the UI, but the list will not load.

### Customer scope traverses through the order

The list is auto-filtered to this customer via `filters[customer_id]=<id>`, applied by joining through each payment's parent **order**: it returns payment rows whose order's `customer_id` matches. A payment whose parent order has no `customer_id` (guest checkout) will NOT appear here, even if the gateway reference data carries the same customer.

### Reference number is a random internal hash — NOT the gateway transaction id

The `hash` field shown in the Payment Details popup as "Reference number" is a random 16-character code generated when the payment record is created. It is a stable identifier (used internally for return-page URLs), unique inside CloudCart, but is **NOT** the value the payment gateway recognises. The real gateway transaction id is `provider_reference_id`, stored separately and surfaced only on the order detail page — that is the value the merchant gives to the gateway's support team when investigating a chargeback, missing payout, or refund delay.

### 13 statuses in the model, 8 in the filter

The platform defines 13 payment transaction statuses: **authorized, initiated, requested, pending, held, completed, failed, refunded, voided, cancelled, timeouted, chargebacked, disputed**. The filter dropdown exposes only 8 (Initiated, Pending, Requested, Completed, Failed, Refunded, Cancelled, Timeouted). The other 5 (Authorized, Held, Voided, Chargebacked, Disputed) can still be assigned to transactions and will appear in the row Status badge — the merchant just cannot filter for them on this tab.

### This tab's statuses vs the Orders tab's

The Payments tab filters the **payment-transaction** state model (8 options). The [[customers-details-orders]] tab's payment-status filter exposes **12** options — the same data plus order-level rollups (Held, Voided, Chargebacked, Disputed) that interpret the underlying transactions at the order level.

### Credit Note filter

The **Credit Note** filter shows in the bar with Yes / No, but choosing either leaves the list unchanged.

## Related

- [[customers-details]] — parent details page.
- [[customers-details-orders]] — sister tab; payment-status filter is broader there (12 options vs 8 here).
- [[settings-payment-providers]] — payment providers used in the provider filter.
- [[order]] — entity page (refunds and all transaction actions are processed from the order page).
- [[customer]] — entity page.

## Modals & sub-flows (full surface)

### Payment Details popup

**Trigger:** clicking the **Payment # cell** on any row (rendered as `Payment #<id>` with dotted-underline tooltip styling; the whole link is the click target).

**Title:** `#<id> Details`, with the payment record's internal id. Escape and clicking outside do not close it.

**Body fields:**

| Label | Source | Notes |
|-------|--------|-------|
| ID: | `payment_id` | The payment's `payment_id`. |
| Reference number: | `hash` | 16-char random internal hash (see Business rules). NOT the gateway transaction id. |

**Footer:** a single **OK** button that closes the popup. The popup is intentionally minimal — no Edit / Refund / Re-attempt control. Full transaction detail (gateway response codes, full timestamps, card last-4, the real `provider_reference_id` gateway reference) lives on the related order page.

### No other modals or actions

The tab is read-only: no Create / Add modal, no row-level Edit / Refund / Void / Retry, no bulk actions (no checkboxes), no row-action overflow menu, and no link away from the tab. To open the order, use the [[customers-details-orders|Orders]] tab.

## Open questions

None.
