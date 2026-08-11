---
type: feature
nav_path: "Orders → Order details → Receipt → Numbering"
route_name: admin.orders.receipt
route_path: /admin/orders/receipt/:order_id
aliases: ["Receipt numbering", "Receipt number series", "Receipt auto-generation", "order_receipt_sent", "Receipt history row", "Receipt number permanence"]
tags: [orders, receipt, numbering, invoicing, history]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-receipt]]. See the hub for the other aspects (surfaces, eligibility, rendering).

# Receipt — numbering (per order)

## Purpose

Explains **how the receipt number is assigned**: its own sequential series (separate from invoice / credit-note numbering), the `max + 1` generation rule with concurrency retry, number permanence, and the fact that assignment happens automatically on order events — never via a merchant click. This is the aspect to read for any *"why does the receipt number look like that / when was it assigned / why is there a history entry"* ticket.

## Where to find it

The merchant does not assign receipt numbers manually and there is no receipt-numbering screen in [[settings-invoicing]] (contrast invoice numbering, which is configurable). The assigned number surfaces only as the *"Order receipt #&lt;number&gt;"* link in the **Order history** section of [[orders-details]] — see [[orders-receipt-surfaces]].

## What the merchant can do here

Nothing directly — receipt numbering is fully automatic. The merchant only sees the resulting number on the history link. To make a receipt number appear, the merchant moves the order into a payable / fulfilled state (see [[orders-receipt-eligibility]]); the platform does the rest.

## Settings & fields

No merchant-facing settings. Receipts are NOT exposed as a configurable numbering sequence the way invoices are. The number is stored on the order once assigned and rendered verbatim into the history link and the PDF.

## Business rules

### Separate sequential series, per store

When a receipt is issued, the platform consumes a number from a **separate sequential counter**, distinct from the invoice and credit-note series. The next receipt number is `max(receipt_number across all orders) + 1`. Each receipt-issuance attempt uses a retry-5 pattern with 2-second backoff to handle concurrency between simultaneous order finalisations.

### Number permanence

Once a number is assigned to an order it is **permanent** — the same audit-trail rule as invoices. It is never reused, even if the order is later voided / cancelled / refunded.

### One receipt per order — summarises all payments

The platform generates ONE receipt per order regardless of how many payment records the order has. The receipt summarises the order's total payment(s); it does NOT produce a separate receipt per payment record. For complex multi-payment orders, the receipt acts as the unified proof-of-payment for the order's full total.

### Auto-generation triggered by order events, not by a click

The receipt number is assigned automatically by the platform's order event subscriber whenever the order transitions into a state that satisfies `isReadyForReceipt` (which delegates to `isReadyForInvoice` — fulfilled OR paid/completed OR digital-only; see [[orders-receipt-eligibility]]). The merchant never clicks "Generate receipt" — it happens as a side-effect of status-change / fulfillment / payment events. The merchant only OPENS the resulting PDF via the history link.

### First generation writes the `order_receipt_sent` history row

The first generation also writes the `order_receipt_sent` history row (action code 48) with the customer email, names, and the assigned receipt number + date. This row is what renders the clickable *"Order receipt #&lt;number&gt;"* link on the order history (see [[orders-receipt-surfaces]]). Subsequent opens of the PDF do not write further history rows.

## Related

- [[orders-receipt]] — hub.
- [[orders-receipt-eligibility]] — the `isReadyForReceipt` predicate that triggers number assignment.
- [[orders-history]] — where the `order_receipt_sent` (action 48) row renders.
- [[orders-invoice-single-numbering]] — the invoice numbering series this is deliberately kept separate from.
- [[order]] — entity carrying the stored receipt number.

## Open questions

None.
